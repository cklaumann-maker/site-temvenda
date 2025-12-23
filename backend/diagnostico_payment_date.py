#!/usr/bin/env python3
"""
Script de diagnóstico para verificar se payment_date está sendo lido da planilha.
Mostra informações detalhadas sobre os expense_items e o que deveria estar sendo calculado.
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
    print("🔍 DIAGNÓSTICO COMPLETO - payment_date em expense_items")
    print("=" * 120)
    print()
    
    # Busca expense_items
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    print(f"📊 Total de expense_items no banco: {len(items)}")
    print()
    
    # Estatísticas
    itens_com_payment_date = [i for i in items if i.get("payment_date")]
    itens_sem_payment_date = [i for i in items if not i.get("payment_date")]
    itens_com_valor_pago = [i for i in items if float(i.get("amount_paid", 0)) > 0.01]
    
    print(f"✅ Itens COM payment_date: {len(itens_com_payment_date)}")
    print(f"❌ Itens SEM payment_date: {len(itens_sem_payment_date)}")
    print(f"💰 Itens COM valor_pago > 0: {len(itens_com_valor_pago)}")
    print()
    
    # Agrupa por payment_date
    if itens_com_payment_date:
        print("=" * 120)
        print("📅 ITENS COM PAYMENT_DATE (agrupados por data de pagamento)")
        print("=" * 120)
        print()
        
        por_payment_date = defaultdict(list)
        for item in itens_com_payment_date:
            payment_date = item.get("payment_date")
            por_payment_date[payment_date].append(item)
        
        for payment_date in sorted(por_payment_date.keys()):
            itens_dia = por_payment_date[payment_date]
            total_dia = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens_dia)
            
            print(f"📆 {payment_date} ({date.fromisoformat(payment_date).strftime('%d/%m/%Y - %A')})")
            print(f"   Total: {format_currency(total_dia)} ({len(itens_dia)} itens)")
            print()
            
            for item in itens_dia[:5]:  # Mostra até 5 itens
                supplier = item.get("supplier", "N/A")
                amount_paid = float(item.get("amount_paid", 0))
                interest = float(item.get("interest", 0))
                due_date = item.get("due_date")
                category = item.get("category", "N/A")
                print(f"      • [{category}] {supplier}: {format_currency(amount_paid)} + {format_currency(interest)} juros = {format_currency(amount_paid + interest)} (Venc: {due_date})")
            
            if len(itens_dia) > 5:
                print(f"      ... e mais {len(itens_dia) - 5} itens")
            print()
    else:
        print("⚠️  PROBLEMA: Nenhum expense_item tem payment_date preenchido!")
        print()
        print("   Isso significa que:")
        print("   1. A coluna 'data pag' não está sendo encontrada na planilha, OU")
        print("   2. A coluna existe mas está vazia, OU")
        print("   3. O nome da coluna é diferente do esperado")
        print()
        print("   AÇÃO NECESSÁRIA:")
        print("   - Verifique na planilha Google Sheets o nome exato da coluna de data de pagamento")
        print("   - Confirme que a coluna tem dados preenchidos")
        print("   - Execute 'Atualizar Fluxo' novamente após verificar")
        print()
    
    # Mostra itens com valor pago mas sem payment_date
    itens_pagos_sem_data = [i for i in itens_com_valor_pago if not i.get("payment_date")]
    if itens_pagos_sem_data:
        print("=" * 120)
        print(f"⚠️  ITENS COM VALOR PAGO MAS SEM PAYMENT_DATE ({len(itens_pagos_sem_data)} itens)")
        print("=" * 120)
        print()
        print("   Estes itens têm amount_paid > 0 mas não têm payment_date.")
        print("   Eles NÃO serão contabilizados em expenses_paid (Saída Real).")
        print()
        
        total_perdido = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens_pagos_sem_data)
        print(f"   💰 Total não contabilizado: {format_currency(total_perdido)}")
        print()
        
        # Agrupa por fornecedor
        por_fornecedor = defaultdict(list)
        for item in itens_pagos_sem_data:
            supplier = item.get("supplier", "N/A")
            por_fornecedor[supplier].append(item)
        
        print("   Top 10 fornecedores:")
        for supplier, itens in sorted(por_fornecedor.items(), key=lambda x: sum(float(i.get("amount_paid", 0)) for i in x[1]), reverse=True)[:10]:
            total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens)
            print(f"      • {supplier}: {format_currency(total)} ({len(itens)} itens)")
        print()
    
    # Compara com finance_daily
    print("=" * 120)
    print("📊 COMPARAÇÃO: expenses_paid no finance_daily vs. cálculo esperado")
    print("=" * 120)
    print()
    
    days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    days = days_resp.data or []
    
    dias_com_diferenca = []
    dias_corretos = []
    
    for day_record in days:
        d_iso = day_record.get("date")
        if not d_iso:
            continue
        
        expenses_paid_banco = float(day_record.get("expenses_paid", 0))
        
        # Calcula o que DEVERIA ser
        expenses_paid_esperado = 0.0
        for item in itens_com_payment_date:
            if item.get("payment_date") == d_iso:
                expenses_paid_esperado += float(item.get("amount_paid", 0)) + float(item.get("interest", 0))
        
        diferenca = abs(expenses_paid_banco - expenses_paid_esperado)
        if diferenca > 0.01:
            dias_com_diferenca.append({
                "date": d_iso,
                "banco": expenses_paid_banco,
                "esperado": expenses_paid_esperado,
                "diferenca": diferenca
            })
        elif expenses_paid_esperado > 0.01:
            dias_corretos.append({
                "date": d_iso,
                "valor": expenses_paid_esperado
            })
    
    if dias_com_diferenca:
        print(f"❌ {len(dias_com_diferenca)} dias com valores INCORRETOS no banco:")
        print()
        for dia in dias_com_diferenca[:10]:
            d_obj = date.fromisoformat(dia['date'])
            print(f"   {dia['date']} ({d_obj.strftime('%d/%m/%Y')}):")
            print(f"      Banco: {format_currency(dia['banco'])}")
            print(f"      Esperado: {format_currency(dia['esperado'])}")
            print(f"      Diferença: {format_currency(dia['diferenca'])}")
            print()
        
        if len(dias_com_diferenca) > 10:
            print(f"   ... e mais {len(dias_com_diferenca) - 10} dias com problemas")
            print()
    else:
        print("✅ Todos os dias estão corretos!")
        print()
    
    if dias_corretos:
        print(f"✅ {len(dias_corretos)} dias com valores CORRETOS")
        print()
    
    # Resumo final
    print("=" * 120)
    print("📋 RESUMO FINAL")
    print("=" * 120)
    print()
    
    if not itens_com_payment_date:
        print("🔴 PROBLEMA CRÍTICO: Nenhum expense_item tem payment_date!")
        print()
        print("   SOLUÇÃO:")
        print("   1. Verifique na planilha Google Sheets se a coluna 'data pag' existe e tem dados")
        print("   2. Confirme o nome exato da coluna (pode ter espaços extras, acentos, etc.)")
        print("   3. Execute 'Atualizar Fluxo' novamente após verificar")
        print()
    elif dias_com_diferenca:
        print(f"⚠️  {len(dias_com_diferenca)} dias precisam ser recalculados")
        print()
        print("   SOLUÇÃO:")
        print("   Execute 'Atualizar Fluxo' novamente para recalcular expenses_paid")
        print()
    else:
        print("✅ Tudo está correto!")
        print()

if __name__ == "__main__":
    main()

