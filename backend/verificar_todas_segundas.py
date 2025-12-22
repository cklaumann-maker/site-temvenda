#!/usr/bin/env python3
"""
Script para verificar valores de forecast para todas as segundas e sextas de dezembro.
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

# Buscar todos os registros de dezembro/2025
resp = supabase.table("finance_daily").select("*").eq("month_code", "12-25").order("date").execute()

if not resp.data:
    print("⚠️  Nenhum registro encontrado")
    exit(0)

print("=" * 80)
print("Verificando Segundas e Sextas de Dezembro/2025")
print("=" * 80)
print()

segundas = []
sextas = []

for day in resp.data:
    date = day.get("date")
    weekday = day.get("weekday", "")
    forecast = float(day.get("cash_in_forecast_total", 0) or 0)
    actual_total = (
        float(day.get("cash_in_actual_money", 0) or 0) +
        float(day.get("cash_in_actual_pix", 0) or 0) +
        float(day.get("cash_in_actual_card", 0) or 0) +
        float(day.get("cash_in_actual_convenio", 0) or 0)
    )
    
    if weekday == "Monday":
        segundas.append((date, forecast, actual_total))
    elif weekday == "Friday":
        sextas.append((date, forecast, actual_total))

print("📅 SEGUNDAS-FEIRAS (deveriam ser R$ 77.403,01):")
print()
for date, forecast, actual in segundas:
    status = "✅" if forecast == 77403.01 else "❌"
    print(f"{status} {date} ({weekday}): Forecast = R$ {forecast:,.2f}, Actual = R$ {actual:,.2f}")

print()
print("📅 SEXTAS-FEIRAS (deveriam ser R$ 35.229,42):")
print()
for date, forecast, actual in sextas:
    status = "✅" if forecast == 35229.42 else "❌"
    print(f"{status} {date} ({weekday}): Forecast = R$ {forecast:,.2f}, Actual = R$ {actual:,.2f}")

