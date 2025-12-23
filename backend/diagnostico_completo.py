#!/usr/bin/env python3
"""
Script de diagnóstico completo para verificar:
1. Entradas manuais cadastradas
2. Expense_items com payment_date
3. Expenses_paid calculado corretamente
"""

import sys
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.supabase_client import get_supabase

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    month_code = "12-25"
    supabase = get_supabase()
    
    print("=" * 120)
    print("🔍 DIAGNÓSTICO COMPLETO - Dezembro 2025")
    print("=" * 120)
    print()
    
    # 1. Verifica entradas manuais
    print("1️⃣ VERIFICANDO ENTRADAS MANUAIS (cash_in_actual_*)")
    print("-" * 120)
    days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    days = days_resp.data or []
    
    dias_com_entradas_manuais = []
    for day in days:
        money = float(day.get("cash_in_actual_money", 0))
        pix = float(day.get("cash_in_actual_pix", 0))
        card = float(day.get("cash_in_actual_card", 0))
        convenio = float(day.get("cash_in_actual_convenio", 0))
        total = money + pix + card + convenio
        
        if total > 0.01:  # Considera apenas valores significativos
            dias_com_entradas_manuais.append({
                "date": day.get("date"),
                "money": money,
                "pix": pix,
                "card": card,
                "convenio": convenio,
                "total": total
            })
    
    if dias_com_entradas_manuais:
        print(f"✅ Encontrados {len(dias_com_entradas_manuais)} dias com entradas manuais:")
        for d in dias_com_entradas_manuais[:10]:  # Mostra os primeiros 10
            print(f"   📅 {d['date']}: Total = {format_currency(d['total'])} (Dinheiro: {format_currency(d['money'])}, PIX: {format_currency(d['pix'])}, Cartão: {format_currency(d['card'])}, Convênio: {format_currency(d['convenio'])})")
        if len(dias_com_entradas_manuais) > 10:
            print(f"   ... e mais {len(dias_com_entradas_manuais) - 10} dias")
    else:
        print("❌ NENHUMA entrada manual encontrada!")
    print()
    
    # 2. Verifica expense_items com payment_date
    print("2️⃣ VERIFICANDO EXPENSE_ITEMS COM PAYMENT_DATE")
    print("-" * 120)
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    items_com_payment_date = [item for item in items if item.get("payment_date")]
    items_sem_payment_date = [item for item in items if not item.get("payment_date")]
    
    print(f"📊 Total de expense_items: {len(items)}")
    print(f"✅ Com payment_date: {len(items_com_payment_date)}")
    print(f"❌ Sem payment_date: {len(items_sem_payment_date)}")
    
    if items_com_payment_date:
        # Agrupa por payment_date
        por_data = {}
        for item in items_com_payment_date:
            pd = item.get("payment_date")
            if pd not in por_data:
                por_data[pd] = []
            por_data[pd].append(item)
        
        print(f"📅 Datas de pagamento únicas: {len(por_data)}")
        print()
        print("   Primeiras 10 datas com pagamentos:")
        for pd in sorted(por_data.keys())[:10]:
            itens_dia = por_data[pd]
            total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens_dia)
            print(f"   📆 {pd}: {len(itens_dia)} itens = {format_currency(total)}")
    else:
        print("❌ NENHUM expense_item tem payment_date!")
    print()
    
    # 3. Verifica expenses_paid em finance_daily
    print("3️⃣ VERIFICANDO EXPENSES_PAID EM FINANCE_DAILY")
    print("-" * 120)
    dias_com_expenses_paid = []
    dias_sem_expenses_paid = []
    
    for day in days:
        expenses_paid = float(day.get("expenses_paid", 0))
        expenses_planned = float(day.get("expenses_planned", 0))
        date_str = day.get("date")
        
        if expenses_paid > 0.01:
            dias_com_expenses_paid.append({
                "date": date_str,
                "expenses_paid": expenses_paid,
                "expenses_planned": expenses_planned
            })
        else:
            dias_sem_expenses_paid.append(date_str)
    
    print(f"✅ Dias COM expenses_paid > 0: {len(dias_com_expenses_paid)}")
    print(f"❌ Dias SEM expenses_paid (ou = 0): {len(dias_sem_expenses_paid)}")
    print()
    
    if dias_com_expenses_paid:
        print("   Primeiros 10 dias com expenses_paid:")
        for d in dias_com_expenses_paid[:10]:
            print(f"   📅 {d['date']}: expenses_paid = {format_currency(d['expenses_paid'])}, expenses_planned = {format_currency(d['expenses_planned'])}")
    else:
        print("   ⚠️  NENHUM dia tem expenses_paid > 0!")
    print()
    
    # 4. Compara expenses_paid com expense_items
    print("4️⃣ VALIDAÇÃO: EXPENSES_PAID vs EXPENSE_ITEMS")
    print("-" * 120)
    
    problemas = []
    acertos = []
    
    for day in days:
        date_str = day.get("date")
        expenses_paid_banco = float(day.get("expenses_paid", 0))
        
        # Calcula o que deveria ser baseado em expense_items
        expenses_paid_correto = 0.0
        for item in items_com_payment_date:
            if item.get("payment_date") == date_str:
                amount_paid = float(item.get("amount_paid", 0))
                interest = float(item.get("interest", 0))
                expenses_paid_correto += amount_paid + interest
        
        diferenca = abs(expenses_paid_banco - expenses_paid_correto)
        if diferenca > 0.01:
            problemas.append({
                "date": date_str,
                "banco": expenses_paid_banco,
                "correto": expenses_paid_correto,
                "diferenca": diferenca
            })
        elif expenses_paid_correto > 0.01:
            acertos.append({
                "date": date_str,
                "valor": expenses_paid_correto
            })
    
    if problemas:
        print(f"❌ PROBLEMAS: {len(problemas)} dias com cálculos incorretos")
        for p in problemas[:5]:
            print(f"   🔴 {p['date']}: Banco={format_currency(p['banco'])}, Correto={format_currency(p['correto'])}, Diferença={format_currency(p['diferenca'])}")
    else:
        print(f"✅ Todos os cálculos estão corretos!")
    
    if acertos:
        print(f"✅ {len(acertos)} dias com expenses_paid correto")
    print()
    
    # 5. Verifica dia 1/12/2025 especificamente
    print("5️⃣ VERIFICAÇÃO ESPECÍFICA - DIA 1/12/2025")
    print("-" * 120)
    dia_1 = next((d for d in days if d.get("date") == "2025-12-01"), None)
    
    if dia_1:
        expenses_paid_dia1 = float(dia_1.get("expenses_paid", 0))
        items_dia1 = [item for item in items_com_payment_date if item.get("payment_date") == "2025-12-01"]
        total_esperado = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in items_dia1)
        
        print(f"   expenses_paid no banco: {format_currency(expenses_paid_dia1)}")
        print(f"   expense_items com payment_date=2025-12-01: {len(items_dia1)}")
        print(f"   Total esperado (soma dos itens): {format_currency(total_esperado)}")
        
        if abs(expenses_paid_dia1 - total_esperado) < 0.01:
            print("   ✅ CORRETO!")
        else:
            print(f"   ❌ INCORRETO! Diferença: {format_currency(abs(expenses_paid_dia1 - total_esperado))}")
    else:
        print("   ⚠️  Dia 1/12/2025 não encontrado!")
    print()
    
    # Resumo final
    print("=" * 120)
    print("📋 RESUMO")
    print("=" * 120)
    print(f"✅ Entradas manuais: {len(dias_com_entradas_manuais)} dias")
    print(f"✅ Expense_items com payment_date: {len(items_com_payment_date)}")
    print(f"✅ Dias com expenses_paid > 0: {len(dias_com_expenses_paid)}")
    print(f"{'❌' if problemas else '✅'} Validação expenses_paid: {len(problemas)} problemas encontrados")
    print()

if __name__ == "__main__":
    main()

