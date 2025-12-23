#!/usr/bin/env python3
"""
Script para validar o dia 1/12/2025 com valores esperados específicos:
- DESP 12-25: R$ 5.828,10 (valor pago + juros)
- DIST 12-25: R$ 11.969,75 (valor pago + juros)
- Total esperado: R$ 17.797,85
"""

import sys
import os
from datetime import date

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
    target_date = date(2025, 12, 1)
    target_date_str = target_date.isoformat()
    
    # Valores esperados
    desp_esperado = 5828.10
    dist_esperado = 11969.75
    total_esperado = 17797.85
    
    print("=" * 120)
    print(f"🔍 VALIDAÇÃO DIA 1/12/2025 - VALORES ESPERADOS")
    print("=" * 120)
    print()
    print(f"📊 Valores esperados:")
    print(f"   DESP 12-25: {format_currency(desp_esperado)}")
    print(f"   DIST 12-25: {format_currency(dist_esperado)}")
    print(f"   TOTAL ESPERADO: {format_currency(total_esperado)}")
    print()
    
    supabase = get_supabase()
    
    # Busca expense_items com payment_date = 01/12/2025
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).eq("payment_date", target_date_str).execute()
    items = items_resp.data or []
    
    print(f"📊 Itens encontrados no banco com payment_date = {target_date_str}: {len(items)}")
    print()
    
    if len(items) == 0:
        print("❌ PROBLEMA: Nenhum expense_item tem payment_date = 01/12/2025!")
        print("   A coluna 'Data pag' não está sendo lida da planilha.")
        print()
        print("   AÇÃO: Execute 'Atualizar Fluxo' novamente após o deploy.")
        return
    
    # Agrupa por categoria
    desp_items = [i for i in items if i.get("category") == "DESP"]
    dist_items = [i for i in items if i.get("category") == "DIST"]
    
    # Calcula totais
    desp_total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in desp_items)
    dist_total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in dist_items)
    total_calculado = desp_total + dist_total
    
    print("=" * 120)
    print("📊 VALORES CALCULADOS DO BANCO")
    print("=" * 120)
    print()
    print(f"   DESP 12-25: {format_currency(desp_total)} ({len(desp_items)} itens)")
    print(f"   DIST 12-25: {format_currency(dist_total)} ({len(dist_items)} itens)")
    print(f"   TOTAL CALCULADO: {format_currency(total_calculado)}")
    print()
    
    # Compara
    print("=" * 120)
    print("🔍 COMPARAÇÃO")
    print("=" * 120)
    print()
    
    desp_diff = abs(desp_total - desp_esperado)
    dist_diff = abs(dist_total - dist_esperado)
    total_diff = abs(total_calculado - total_esperado)
    
    print(f"   DESP:")
    print(f"      Esperado: {format_currency(desp_esperado)}")
    print(f"      Calculado: {format_currency(desp_total)}")
    if desp_diff < 0.01:
        print(f"      ✅ CORRETO!")
    else:
        print(f"      ❌ DIFERENÇA: {format_currency(desp_diff)}")
    print()
    
    print(f"   DIST:")
    print(f"      Esperado: {format_currency(dist_esperado)}")
    print(f"      Calculado: {format_currency(dist_total)}")
    if dist_diff < 0.01:
        print(f"      ✅ CORRETO!")
    else:
        print(f"      ❌ DIFERENÇA: {format_currency(dist_diff)}")
    print()
    
    print(f"   TOTAL:")
    print(f"      Esperado: {format_currency(total_esperado)}")
    print(f"      Calculado: {format_currency(total_calculado)}")
    if total_diff < 0.01:
        print(f"      ✅ CORRETO!")
    else:
        print(f"      ❌ DIFERENÇA: {format_currency(total_diff)}")
    print()
    
    # Verifica expenses_paid no finance_daily
    day_resp = supabase.table("finance_daily").select("expenses_paid").eq("month_code", month_code).eq("date", target_date_str).limit(1).execute()
    expenses_paid_banco = float(day_resp.data[0].get("expenses_paid", 0)) if day_resp.data else 0.0
    
    print("=" * 120)
    print("🔍 VERIFICAÇÃO EM FINANCE_DAILY")
    print("=" * 120)
    print()
    print(f"   expenses_paid no banco: {format_currency(expenses_paid_banco)}")
    print(f"   Total esperado: {format_currency(total_esperado)}")
    
    if abs(expenses_paid_banco - total_esperado) < 0.01:
        print(f"   ✅ CORRETO! O valor em finance_daily está correto.")
    else:
        print(f"   ❌ INCORRETO! Diferença: {format_currency(abs(expenses_paid_banco - total_esperado))}")
        print()
        print("   AÇÃO: Execute 'Atualizar Fluxo' novamente para recalcular expenses_paid.")
    print()
    
    # Detalhamento dos itens
    if desp_items or dist_items:
        print("=" * 120)
        print("📋 DETALHAMENTO DOS ITENS")
        print("=" * 120)
        print()
        
        if desp_items:
            print(f"DESP 12-25 ({len(desp_items)} itens):")
            for item in desp_items[:10]:
                supplier = item.get("supplier", "N/A")
                amount_paid = float(item.get("amount_paid", 0))
                interest = float(item.get("interest", 0))
                total = amount_paid + interest
                print(f"   • {supplier}: {format_currency(amount_paid)} + {format_currency(interest)} = {format_currency(total)}")
            if len(desp_items) > 10:
                print(f"   ... e mais {len(desp_items) - 10} itens")
            print()
        
        if dist_items:
            print(f"DIST 12-25 ({len(dist_items)} itens):")
            for item in dist_items[:10]:
                supplier = item.get("supplier", "N/A")
                amount_paid = float(item.get("amount_paid", 0))
                interest = float(item.get("interest", 0))
                total = amount_paid + interest
                print(f"   • {supplier}: {format_currency(amount_paid)} + {format_currency(interest)} = {format_currency(total)}")
            if len(dist_items) > 10:
                print(f"   ... e mais {len(dist_items) - 10} itens")
            print()

if __name__ == "__main__":
    main()

