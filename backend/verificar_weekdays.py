#!/usr/bin/env python3
"""
Script para verificar e corrigir weekdays no banco de dados.
"""

import os
import calendar
from datetime import date
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
print("Verificando e corrigindo weekdays no banco")
print("=" * 80)
print()

updated_count = 0

for day in resp.data:
    date_str = day.get("date")
    weekday_in_db = day.get("weekday", "")
    
    # Calcular weekday correto
    try:
        year, month, day_num = map(int, date_str.split('-'))
        d = date(year, month, day_num)
        weekday_correct = calendar.day_name[d.weekday()]  # Monday, Tuesday, etc.
        
        if weekday_in_db != weekday_correct:
            print(f"❌ {date_str}: '{weekday_in_db}' → '{weekday_correct}'")
            supabase.table("finance_daily").update({"weekday": weekday_correct}).eq("id", day["id"]).execute()
            updated_count += 1
        else:
            print(f"✅ {date_str}: {weekday_correct}")
    except Exception as e:
        print(f"⚠️  Erro ao processar {date_str}: {e}")

print()
print("=" * 80)
print(f"✅ Concluído: {updated_count} registro(s) atualizado(s)")
print("=" * 80)

