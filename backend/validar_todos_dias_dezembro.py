#!/usr/bin/env python3
"""
Script para validar expenses_paid para TODOS os dias de dezembro.
Compara o que está no banco com o que DEVERIA estar baseado nos expense_items.
"""

import sys
import os
from datetime import date
from collections import defaultdict

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from supabase import create_client
    from app.config import get_settings
    
    def get_supabase():
        settings = get_settings()
        return create_client(settings.supabase_url, settings.supabase_service_role_key)
        
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    month_code = "12-25"
    year, month = 2025, 12
    last_day = 31
    
    supabase = get_supabase()
    
    print("=" * 120)
    print(f"🔍 VALIDAÇÃO COMPLETA - TODOS OS DIAS DE DEZEMBRO 2025")
    print("=" * 120)
    print()
    
    # Busca expense_items
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    # Busca finance_daily
    days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    days = days_resp.data or []
    
    print(f"📊 Total expense_items: {len(items)}")
    print(f"📅 Total dias finance_daily: {len(days)}")
    print()
    
    # Agrupa itens por payment_date
    itens_por_payment_date = defaultdict(list)
    itens_sem_payment_date = []
    
    for item in items:
        payment_date = item.get("payment_date")
        if payment_date:
            itens_por_payment_date[payment_date].append(item)
        else:
            itens_sem_payment_date.append(item)
    
    print(f"✅ Itens COM payment_date: {sum(len(v) for v in itens_por_payment_date.values())}")
    print(f"❌ Itens SEM payment_date: {len(itens_sem_payment_date)}")
    print(f"📅 Datas de pagamento únicas: {len(itens_por_payment_date)}")
    print()
    
    # Validação dia a dia
    problemas = []
    acertos = []
    dias_com_pagamentos = []
    
    for day_num in range(1, last_day + 1):
        d = date(year, month, day_num)
        d_iso = d.isoformat()
        
        day_record = next((d for d in days if d.get("date") == d_iso), None)
        if not day_record:
            continue
        
        expenses_paid_banco = float(day_record.get("expenses_paid", 0))
        
        # Calcula o que DEVERIA ser (baseado em payment_date)
        expenses_paid_esperado = 0.0
        itens_com_pagamento = []
        
        for item in items:
            payment_date_str = item.get("payment_date")
            amount_paid = float(item.get("amount_paid", 0))
            interest = float(item.get("interest", 0))
            
            if payment_date_str and payment_date_str == d_iso:
                valor_item = amount_paid + interest
                expenses_paid_esperado += valor_item
                itens_com_pagamento.append({
                    "supplier": item.get("supplier", "N/A"),
                    "category": item.get("category", "N/A"),
                    "amount_paid": amount_paid,
                    "interest": interest,
                    "total": valor_item,
                    "due_date": item.get("due_date")
                })
        
        diferenca = abs(expenses_paid_banco - expenses_paid_esperado)
        esta_correto = diferenca < 0.01
        
        if expenses_paid_esperado > 0.01:
            dias_com_pagamentos.append({
                "date": d_iso,
                "valor_esperado": expenses_paid_esperado,
                "valor_banco": expenses_paid_banco,
                "itens": itens_com_pagamento,
                "correto": esta_correto,
                "diferenca": diferenca
            })
        
        if not esta_correto:
            problemas.append({
                "date": d_iso,
                "banco": expenses_paid_banco,
                "esperado": expenses_paid_esperado,
                "diferenca": diferenca,
                "itens": itens_com_pagamento
            })
        else:
            acertos.append({
                "date": d_iso,
                "valor": expenses_paid_esperado,
                "itens": len(itens_com_pagamento)
            })
    
    # RELATÓRIO
    print("=" * 120)
    print("📋 RELATÓRIO DE VALIDAÇÃO")
    print("=" * 120)
    print()
    
    if dias_com_pagamentos:
        print(f"💰 DIAS COM PAGAMENTOS REGISTRADOS ({len(dias_com_pagamentos)} dias):")
        print()
        
        for dia in sorted(dias_com_pagamentos, key=lambda x: x['date']):
            d_obj = date.fromisoformat(dia['date'])
            status = "✅" if dia['correto'] else "❌"
            print(f"{status} {dia['date']} ({d_obj.strftime('%d/%m/%Y - %A')})")
            print(f"   Esperado (payment_date): {format_currency(dia['valor_esperado'])}")
            print(f"   Banco (expenses_paid): {format_currency(dia['valor_banco'])}")
            if not dia['correto']:
                print(f"   ⚠️  DIFERENÇA: {format_currency(dia['diferenca'])}")
            print(f"   Itens ({len(dia['itens'])}):")
            
            # Agrupa por categoria
            por_categoria = defaultdict(list)
            for item in dia['itens']:
                por_categoria[item['category']].append(item)
            
            for cat, itens_cat in por_categoria.items():
                total_cat = sum(i['total'] for i in itens_cat)
                print(f"      [{cat}] {len(itens_cat)} itens = {format_currency(total_cat)}")
                # Mostra alguns exemplos
                for item in itens_cat[:3]:
                    print(f"         • {item['supplier']}: {format_currency(item['amount_paid'])} + {format_currency(item['interest'])} = {format_currency(item['total'])}")
                if len(itens_cat) > 3:
                    print(f"         ... e mais {len(itens_cat) - 3} itens")
            print()
    else:
        print("⚠️  NENHUM DIA COM PAGAMENTOS encontrado!")
        print("   Isso significa que nenhum expense_item tem payment_date preenchido.")
        print()
    
    print("=" * 120)
    print()
    
    if problemas:
        print(f"❌ PROBLEMAS: {len(problemas)} dias com valores incorretos")
        print(f"✅ ACERTOS: {len(acertos)} dias corretos")
        print()
        print("⚠️  AÇÃO: Execute 'Atualizar Fluxo' novamente após verificar a coluna 'Data pag' na planilha.")
    else:
        print(f"✅ SUCESSO: Todos os {len(acertos)} dias estão corretos!")
    
    print()
    
    # Resumo por categoria
    if itens_por_payment_date:
        print("=" * 120)
        print("📊 RESUMO POR CATEGORIA")
        print("=" * 120)
        
        dist_items = [i for items_list in itens_por_payment_date.values() for i in items_list if i.get("category") == "DIST"]
        desp_items = [i for items_list in itens_por_payment_date.values() for i in items_list if i.get("category") == "DESP"]
        
        print(f"DIST com payment_date: {len(dist_items)} itens")
        print(f"DESP com payment_date: {len(desp_items)} itens")
        print()
        
        total_dist = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in dist_items)
        total_desp = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in desp_items)
        
        print(f"Total DIST (valor_pago + juros): {format_currency(total_dist)}")
        print(f"Total DESP (valor_pago + juros): {format_currency(total_desp)}")
        print(f"TOTAL GERAL: {format_currency(total_dist + total_desp)}")
        print()

if __name__ == "__main__":
    main()

