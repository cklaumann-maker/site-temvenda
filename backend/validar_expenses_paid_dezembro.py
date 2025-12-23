#!/usr/bin/env python3
"""
Script de validação para verificar se expenses_paid está sendo calculado corretamente
baseado APENAS na data de pagamento (payment_date) e não na data de vencimento (due_date).

Valida todas as datas de dezembro de 2025 (12-25).
"""

import sys
import os
from datetime import date, datetime

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from supabase import create_client
    from app.config import get_settings
    
    def get_supabase():
        settings = get_settings()
        return create_client(settings.supabase_url, settings.supabase_service_role_key)
    
    def parse_month_code(month_code: str):
        """Converte 'MM-YY' para (ano, mês)"""
        mm, yy = month_code.split("-")
        return 2000 + int(yy), int(mm)
        
except Exception as e:
    print(f"❌ Erro ao importar módulos: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    try:
        month_code = "12-25"
        year, month = parse_month_code(month_code)
        last_day = 31  # Dezembro tem 31 dias
        
        supabase = get_supabase()
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print(f"🔍 Validando cálculo de expenses_paid para dezembro 2025 ({month_code})")
    print("=" * 100)
    print()
    
    # Busca todos os expense_items do mês
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    print(f"📊 Total de expense_items encontrados: {len(items)}")
    print()
    
    # Busca finance_daily do mês
    days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    days = days_resp.data or []
    
    print(f"📅 Total de dias em finance_daily: {len(days)}")
    print()
    
    # Validação dia a dia
    problemas = []
    acertos = []
    
    for day_num in range(1, last_day + 1):
        d = date(year, month, day_num)
        d_iso = d.isoformat()
        
        # Busca o dia em finance_daily
        day_record = next((d for d in days if d.get("date") == d_iso), None)
        if not day_record:
            continue
        
        expenses_paid_banco = float(day_record.get("expenses_paid", 0))
        
        # Calcula o que DEVERIA ser expenses_paid
        # REGRA: apenas itens com payment_date == d_iso, soma: amount_paid + interest
        expenses_paid_correto = 0.0
        itens_com_pagamento = []
        
        for item in items:
            payment_date_str = item.get("payment_date")
            amount_paid = float(item.get("amount_paid", 0))
            interest = float(item.get("interest", 0))
            
            # Se tem payment_date e é igual ao dia atual, conta
            if payment_date_str and payment_date_str == d_iso:
                valor_item = amount_paid + interest
                expenses_paid_correto += valor_item
                itens_com_pagamento.append({
                    "supplier": item.get("supplier", "N/A"),
                    "amount_paid": amount_paid,
                    "interest": interest,
                    "total": valor_item,
                    "due_date": item.get("due_date")
                })
        
        # Compara
        diferenca = abs(expenses_paid_banco - expenses_paid_correto)
        esta_correto = diferenca < 0.01  # Tolerância de 1 centavo
        
        if not esta_correto:
            problemas.append({
                "date": d_iso,
                "banco": expenses_paid_banco,
                "correto": expenses_paid_correto,
                "diferenca": diferenca,
                "itens": itens_com_pagamento
            })
        else:
            acertos.append({
                "date": d_iso,
                "valor": expenses_paid_correto,
                "itens": len(itens_com_pagamento)
            })
    
    # Relatório
    print("=" * 100)
    print("📋 RELATÓRIO DE VALIDAÇÃO")
    print("=" * 100)
    print()
    
    if problemas:
        print(f"❌ PROBLEMAS ENCONTRADOS: {len(problemas)} dias com cálculos incorretos")
        print()
        for p in problemas:
            print(f"🔴 Data: {p['date']} ({date.fromisoformat(p['date']).strftime('%d/%m/%Y')})")
            print(f"   ❌ Banco: {format_currency(p['banco'])}")
            print(f"   ✅ Correto: {format_currency(p['correto'])}")
            print(f"   ⚠️  Diferença: {format_currency(p['diferenca'])}")
            if p['itens']:
                print(f"   📝 Itens com payment_date neste dia ({len(p['itens'])}):")
                for item in p['itens']:
                    print(f"      • {item['supplier']}: Pago {format_currency(item['amount_paid'])} + Juros {format_currency(item['interest'])} = {format_currency(item['total'])} (Venc: {item['due_date']})")
            else:
                print(f"   ⚠️  Nenhum item com payment_date neste dia (deveria ser 0)")
            print()
    else:
        print(f"✅ SUCESSO: Todos os {len(acertos)} dias estão corretos!")
        print()
    
    if acertos and not problemas:
        print("📊 Resumo dos dias com despesas pagas:")
        dias_com_despesas = [a for a in acertos if a['valor'] > 0.01]
        for a in dias_com_despesas[:10]:  # Mostra primeiros 10
            print(f"   • {a['date']}: {format_currency(a['valor'])} ({a['itens']} itens)")
        if len(dias_com_despesas) > 10:
            print(f"   ... e mais {len(dias_com_despesas) - 10} dias")
        print()
    
    # Estatísticas
    print("=" * 100)
    print("📊 ESTATÍSTICAS")
    print("=" * 100)
    
    # Itens com payment_date
    itens_com_payment_date = [i for i in items if i.get("payment_date")]
    print(f"📝 Total de expense_items com payment_date: {len(itens_com_payment_date)}")
    
    # Itens sem payment_date
    itens_sem_payment_date = [i for i in items if not i.get("payment_date")]
    print(f"📝 Total de expense_items SEM payment_date: {len(itens_sem_payment_date)}")
    
    # Soma total de expenses_paid correto
    total_expenses_paid_correto = sum(
        float(d.get("expenses_paid", 0)) 
        for d in days 
        if d.get("expenses_paid", 0) > 0.01
    )
    print(f"💰 Total expenses_paid no mês (se estiver correto): {format_currency(total_expenses_paid_correto)}")
    print()
    
    if problemas:
        print("⚠️  AÇÃO NECESSÁRIA:")
        print("   Execute 'Atualizar Fluxo' novamente para recalcular expenses_paid corretamente.")
        print("   A função _recalculate_expenses_from_items() deve corrigir esses valores.")
        sys.exit(1)
    else:
        print("✅ Validação concluída com sucesso!")
        sys.exit(0)

if __name__ == "__main__":
    main()

