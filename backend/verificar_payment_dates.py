#!/usr/bin/env python3
"""
Script para verificar quais payment_date estão registrados no banco.
"""

import sys
import os
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
    
    supabase = get_supabase()
    
    print("=" * 120)
    print("🔍 VERIFICAÇÃO DE PAYMENT_DATES NO BANCO")
    print("=" * 120)
    print()
    
    # Busca expense_items
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    print(f"📊 Total de expense_items: {len(items)}")
    print()
    
    # Agrupa por payment_date
    por_payment_date = defaultdict(list)
    itens_sem_payment_date = []
    
    for item in items:
        payment_date = item.get("payment_date")
        if payment_date:
            por_payment_date[payment_date].append(item)
        else:
            itens_sem_payment_date.append(item)
    
    print(f"✅ Itens COM payment_date: {sum(len(v) for v in por_payment_date.values())}")
    print(f"❌ Itens SEM payment_date: {len(itens_sem_payment_date)}")
    print(f"📅 Datas de pagamento únicas: {len(por_payment_date)}")
    print()
    
    if por_payment_date:
        print("=" * 120)
        print("📅 DATAS DE PAGAMENTO ENCONTRADAS")
        print("=" * 120)
        print()
        
        for payment_date in sorted(por_payment_date.keys()):
            itens_dia = por_payment_date[payment_date]
            total_dia = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens_dia)
            
            print(f"📆 {payment_date} ({len(itens_dia)} itens)")
            print(f"   Total: {format_currency(total_dia)}")
            
            # Agrupa por categoria
            por_categoria = defaultdict(list)
            for item in itens_dia:
                por_categoria[item.get("category", "N/A")].append(item)
            
            for cat, itens_cat in por_categoria.items():
                total_cat = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens_cat)
                print(f"   [{cat}] {len(itens_cat)} itens = {format_currency(total_cat)}")
            
            # Mostra alguns exemplos
            print(f"   Exemplos:")
            for item in itens_dia[:3]:
                supplier = item.get("supplier", "N/A")
                amount_paid = float(item.get("amount_paid", 0))
                interest = float(item.get("interest", 0))
                due_date = item.get("due_date")
                print(f"      • {supplier}: {format_currency(amount_paid)} + {format_currency(interest)} = {format_currency(amount_paid + interest)} (Venc: {due_date})")
            if len(itens_dia) > 3:
                print(f"      ... e mais {len(itens_dia) - 3} itens")
            print()
    else:
        print("⚠️  Nenhum expense_item tem payment_date preenchido!")
        print()
    
    # Verifica especificamente o dia 1/12/2025
    print("=" * 120)
    print("🔍 VERIFICAÇÃO ESPECÍFICA - DIA 1/12/2025")
    print("=" * 120)
    print()
    
    dia_1_items = por_payment_date.get("2025-12-01", [])
    if dia_1_items:
        desp_items = [i for i in dia_1_items if i.get("category") == "DESP"]
        dist_items = [i for i in dia_1_items if i.get("category") == "DIST"]
        
        desp_total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in desp_items)
        dist_total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in dist_items)
        total_dia1 = desp_total + dist_total
        
        print(f"✅ DIA 1/12/2025 ENCONTRADO!")
        print(f"   DESP 12-25: {format_currency(desp_total)} ({len(desp_items)} itens)")
        print(f"   DIST 12-25: {format_currency(dist_total)} ({len(dist_items)} itens)")
        print(f"   TOTAL: {format_currency(total_dia1)}")
        print()
        
        # Valores esperados
        desp_esperado = 5828.10
        dist_esperado = 11969.75
        total_esperado = 17797.85
        
        print(f"   Valores ESPERADOS:")
        print(f"      DESP: {format_currency(desp_esperado)}")
        print(f"      DIST: {format_currency(dist_esperado)}")
        print(f"      TOTAL: {format_currency(total_esperado)}")
        print()
        
        desp_ok = abs(desp_total - desp_esperado) < 0.01
        dist_ok = abs(dist_total - dist_esperado) < 0.01
        total_ok = abs(total_dia1 - total_esperado) < 0.01
        
        if desp_ok and dist_ok and total_ok:
            print("   ✅ VALIDAÇÃO CORRETA!")
        else:
            print("   ❌ VALIDAÇÃO INCORRETA!")
            if not desp_ok:
                print(f"      DESP: diferença de {format_currency(abs(desp_total - desp_esperado))}")
            if not dist_ok:
                print(f"      DIST: diferença de {format_currency(abs(dist_total - dist_esperado))}")
            if not total_ok:
                print(f"      TOTAL: diferença de {format_currency(abs(total_dia1 - total_esperado))}")
    else:
        print("   ⚠️  Dia 1/12/2025 não encontrado!")
        print(f"   Datas disponíveis: {sorted(por_payment_date.keys())[:10]}")
        if len(por_payment_date) > 10:
            print(f"   ... e mais {len(por_payment_date) - 10} datas")
    print()

if __name__ == "__main__":
    main()

