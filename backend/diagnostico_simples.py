#!/usr/bin/env python3
"""
Script simples para verificar o estado atual do banco
sem depender de pandas ou outras bibliotecas pesadas.
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.supabase_client import get_supabase

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    month_code = "12-25"
    supabase = get_supabase()
    
    print("=" * 100)
    print("🔍 DIAGNÓSTICO SIMPLES - Estado Atual do Banco")
    print("=" * 100)
    print()
    
    # 1. Verifica expense_items
    print("1️⃣ EXPENSE_ITEMS COM PAYMENT_DATE")
    print("-" * 100)
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    items_com_payment_date = [item for item in items if item.get("payment_date")]
    items_sem_payment_date = [item for item in items if not item.get("payment_date")]
    
    print(f"   Total: {len(items)}")
    print(f"   ✅ Com payment_date: {len(items_com_payment_date)}")
    print(f"   ❌ Sem payment_date: {len(items_sem_payment_date)}")
    
    if items_com_payment_date:
        # Agrupa por payment_date
        por_data = {}
        for item in items_com_payment_date:
            pd = item.get("payment_date")
            if pd not in por_data:
                por_data[pd] = []
            por_data[pd].append(item)
        
        print(f"   📅 Datas únicas: {len(por_data)}")
        print()
        print("   Datas encontradas:")
        for pd in sorted(por_data.keys()):
            itens = por_data[pd]
            total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens)
            print(f"      • {pd}: {len(itens)} itens = {format_currency(total)}")
    else:
        print("   ⚠️  NENHUM item tem payment_date!")
    print()
    
    # 2. Verifica expenses_paid em finance_daily
    print("2️⃣ EXPENSES_PAID EM FINANCE_DAILY")
    print("-" * 100)
    days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    days = days_resp.data or []
    
    dias_com_expenses_paid = [d for d in days if float(d.get("expenses_paid", 0)) > 0.01]
    
    print(f"   Total de dias: {len(days)}")
    print(f"   ✅ Dias com expenses_paid > 0: {len(dias_com_expenses_paid)}")
    print()
    
    if dias_com_expenses_paid:
        print("   Primeiros 10 dias com expenses_paid:")
        for d in dias_com_expenses_paid[:10]:
            date_str = d.get("date")
            expenses_paid = float(d.get("expenses_paid", 0))
            print(f"      • {date_str}: {format_currency(expenses_paid)}")
    else:
        print("   ⚠️  NENHUM dia tem expenses_paid > 0!")
    print()
    
    # 3. Verifica dia 1/12/2025 especificamente
    print("3️⃣ DIA 1/12/2025 - VALIDAÇÃO ESPECÍFICA")
    print("-" * 100)
    
    dia_1 = next((d for d in days if d.get("date") == "2025-12-01"), None)
    items_dia1 = [item for item in items_com_payment_date if item.get("payment_date") == "2025-12-01"]
    
    if dia_1:
        expenses_paid_dia1 = float(dia_1.get("expenses_paid", 0))
        print(f"   expenses_paid no banco: {format_currency(expenses_paid_dia1)}")
    else:
        print("   ⚠️  Dia 1/12/2025 não encontrado em finance_daily!")
        expenses_paid_dia1 = 0
    
    print(f"   expense_items com payment_date=2025-12-01: {len(items_dia1)}")
    
    if items_dia1:
        total_esperado = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in items_dia1)
        print(f"   Total esperado (soma dos itens): {format_currency(total_esperado)}")
        
        # Separa por categoria
        desp_items = [i for i in items_dia1 if i.get("category") == "DESP"]
        dist_items = [i for i in items_dia1 if i.get("category") == "DIST"]
        
        desp_total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in desp_items)
        dist_total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in dist_items)
        
        print(f"      DESP: {format_currency(desp_total)} ({len(desp_items)} itens)")
        print(f"      DIST: {format_currency(dist_total)} ({len(dist_items)} itens)")
        print(f"      TOTAL: {format_currency(total_esperado)}")
        
        if abs(expenses_paid_dia1 - total_esperado) < 0.01:
            print()
            print("   ✅ CORRETO! expenses_paid bate com a soma dos expense_items!")
        else:
            print()
            print(f"   ❌ INCORRETO! Diferença: {format_currency(abs(expenses_paid_dia1 - total_esperado))}")
            print()
            print("   ⚠️  AÇÃO NECESSÁRIA:")
            print("      1. Execute 'Atualizar Fluxo' novamente na interface")
            print("      2. Aguarde o processamento terminar")
            print("      3. Execute este script novamente")
    else:
        print("   ⚠️  Nenhum expense_item com payment_date=2025-12-01 encontrado!")
        print()
        print("   ⚠️  AÇÃO NECESSÁRIA:")
        print("      1. Verifique se o deploy no Render foi concluído")
        print("      2. Execute 'Atualizar Fluxo' novamente na interface")
        print("      3. Execute este script novamente")
    print()
    
    print("=" * 100)
    print("📋 RESUMO")
    print("=" * 100)
    print(f"   Expense_items com payment_date: {len(items_com_payment_date)}")
    print(f"   Dias com expenses_paid > 0: {len(dias_com_expenses_paid)}")
    print(f"   Dia 1/12/2025: expenses_paid = {format_currency(expenses_paid_dia1)}")
    print()

if __name__ == "__main__":
    main()

