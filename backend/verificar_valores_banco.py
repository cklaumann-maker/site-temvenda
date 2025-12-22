#!/usr/bin/env python3
"""
Script para verificar valores de forecast no banco de dados.
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

# Verificar alguns dias específicos
dates_to_check = [
    "2025-12-01",  # Segunda - deveria ser 77403.01
    "2025-12-02",  # Terça - deveria ser 35229.42
    "2025-12-03",  # Quarta - deveria ser 35229.42
    "2025-12-05",  # Sexta - deveria ser 35229.42
    "2025-12-08",  # Segunda - deveria ser 77403.01
]

print("=" * 80)
print("Verificando valores no banco de dados")
print("=" * 80)
print()

for date in dates_to_check:
    resp = supabase.table("finance_daily").select("*").eq("date", date).limit(1).execute()
    
    if resp.data:
        day = resp.data[0]
        forecast = day.get("cash_in_forecast_total", 0)
        actual_money = day.get("cash_in_actual_money", 0) or 0
        actual_pix = day.get("cash_in_actual_pix", 0) or 0
        actual_card = day.get("cash_in_actual_card", 0) or 0
        actual_convenio = day.get("cash_in_actual_convenio", 0) or 0
        actual_total = actual_money + actual_pix + actual_card + actual_convenio
        
        print(f"📅 {date} ({day.get('weekday', 'Unknown')}):")
        print(f"   Forecast: R$ {forecast:,.2f}")
        print(f"   Actual Money: R$ {actual_money:,.2f}")
        print(f"   Actual PIX: R$ {actual_pix:,.2f}")
        print(f"   Actual Card: R$ {actual_card:,.2f}")
        print(f"   Actual Convênio: R$ {actual_convenio:,.2f}")
        print(f"   Actual Total: R$ {actual_total:,.2f}")
        print(f"   → Valor usado: R$ {actual_total if actual_total > 0 else forecast:,.2f}")
        print()
    else:
        print(f"⚠️  {date}: Não encontrado no banco")
        print()

