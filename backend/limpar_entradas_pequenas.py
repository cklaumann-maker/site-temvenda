#!/usr/bin/env python3
"""
Script para limpar valores muito pequenos (provavelmente erros) das entradas reais.
Remove valores menores que 0.10 das entradas reais.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Erro: SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY devem estar configurados")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

print("=" * 80)
print("Limpando valores muito pequenos das entradas reais")
print("=" * 80)
print()

# Buscar todos os registros de dezembro/2025
resp = supabase.table("finance_daily").select("*").eq("month_code", "12-25").order("date").execute()

if not resp.data:
    print("⚠️  Nenhum registro encontrado para o mês 12-25")
    exit(0)

cleaned_count = 0
total_checked = 0

for day in resp.data:
    total_checked += 1
    date = day.get("date")
    
    # Verificar se há valores muito pequenos
    cash_in_actual_money = float(day.get("cash_in_actual_money", 0) or 0)
    cash_in_actual_pix = float(day.get("cash_in_actual_pix", 0) or 0)
    cash_in_actual_card = float(day.get("cash_in_actual_card", 0) or 0)
    cash_in_actual_convenio = float(day.get("cash_in_actual_convenio", 0) or 0)
    
    total_actual = cash_in_actual_money + cash_in_actual_pix + cash_in_actual_card + cash_in_actual_convenio
    
    # Se o total for menor que 0.10, limpar todos os valores
    if 0 < total_actual < 0.10:
        update_data = {
            "cash_in_actual_money": 0.0,
            "cash_in_actual_pix": 0.0,
            "cash_in_actual_card": 0.0,
            "cash_in_actual_convenio": 0.0
        }
        
        # Recalcular saldos
        cash_in_forecast_total = float(day.get("cash_in_forecast_total", 0) or 0)
        cash_in_used = cash_in_forecast_total  # Agora usa forecast
        cash_in_total = cash_in_used + float(day.get("future_in_confirmed", 0) or 0)
        cash_out_planned = float(day.get("expenses_planned", 0) or 0) + float(day.get("purchases_planned", 0) or 0) + float(day.get("old_debts_paid", 0) or 0)
        cash_out_real = float(day.get("expenses_paid", 0) or 0) + float(day.get("purchases_planned", 0) or 0) + float(day.get("old_debts_paid", 0) or 0)
        
        update_data["balance_projected"] = float(day.get("sales", 0) or 0) + cash_in_total - cash_out_planned
        update_data["balance_real"] = cash_in_total - cash_out_real
        
        supabase.table("finance_daily").update(update_data).eq("id", day["id"]).execute()
        
        print(f"✅ {date}: Limpado R$ {total_actual:.2f} (valores muito pequenos)")
        cleaned_count += 1

print()
print("=" * 80)
print(f"✅ Concluído:")
print(f"   - {total_checked} registro(s) verificado(s)")
print(f"   - {cleaned_count} registro(s) limpo(s)")
print("=" * 80)

