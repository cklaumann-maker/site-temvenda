#!/usr/bin/env python3
"""
Script para atualizar valores previstos de entradas (cash_in_forecast_total) no banco.

Este script atualiza os valores de forecast baseado nos dados fornecidos.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
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
    print("❌ Erro: SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY devem estar configurados no .env")
    sys.exit(1)

# Conectar ao Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def parse_brazilian_number(value_str: str) -> float:
    """Converte número brasileiro (77.403,01) para float (77403.01)"""
    if not value_str or value_str.strip() == '':
        return 0.0
    # Remove espaços e converte
    value_str = value_str.strip().replace('.', '').replace(',', '.')
    try:
        return float(value_str)
    except ValueError:
        print(f"⚠️  Aviso: Valor inválido: {value_str}")
        return 0.0

def parse_date(date_str: str) -> str:
    """Converte data DD/MM/YYYY para YYYY-MM-DD"""
    try:
        # Formato: 01/12/2025
        parts = date_str.strip().split('/')
        if len(parts) == 3:
            day, month, year = parts
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            raise ValueError(f"Formato de data inválido: {date_str}")
    except Exception as e:
        print(f"⚠️  Erro ao parsear data {date_str}: {e}")
        return None

def update_forecast(date: str, forecast_value: float):
    """Atualiza o valor de forecast para uma data específica"""
    # Buscar o registro existente
    resp = supabase.table("finance_daily").select("*").eq("date", date).limit(1).execute()
    
    if not resp.data:
        print(f"⚠️  Aviso: Dia {date} não encontrado no banco. Pulando...")
        return False
    
    day = resp.data[0]
    
    # Atualizar apenas o forecast
    update_data = {
        "cash_in_forecast_total": forecast_value
    }
    
    # Recalcular saldos apenas se não houver entrada real
    cash_in_actual_total = (
        float(day.get("cash_in_actual_money", 0) or 0)
        + float(day.get("cash_in_actual_pix", 0) or 0)
        + float(day.get("cash_in_actual_card", 0) or 0)
        + float(day.get("cash_in_actual_convenio", 0) or 0)
    )
    
    # Se não houver entrada real, recalcula usando o forecast
    if cash_in_actual_total == 0:
        cash_in_used = forecast_value
        cash_in_total = cash_in_used + float(day.get("future_in_confirmed", 0) or 0)
        cash_out_planned = float(day.get("expenses_planned", 0) or 0) + float(day.get("purchases_planned", 0) or 0) + float(day.get("old_debts_paid", 0) or 0)
        cash_out_real = float(day.get("expenses_paid", 0) or 0) + float(day.get("purchases_planned", 0) or 0) + float(day.get("old_debts_paid", 0) or 0)
        
        update_data["balance_projected"] = float(day.get("sales", 0) or 0) + cash_in_total - cash_out_planned
        update_data["balance_real"] = cash_in_total - cash_out_real
    
    # Atualizar no banco
    supabase.table("finance_daily").update(update_data).eq("id", day["id"]).execute()
    
    print(f"✅ {date}: R$ {forecast_value:,.2f}")
    return True

def main():
    # Dados fornecidos pelo usuário
    data = """01/12/2025	77.403,01
02/12/2025	35.229,42
03/12/2025	35.229,42
04/12/2025	35.229,42
05/12/2025	35.229,42
06/12/2025	0,00
07/12/2025	0,00
08/12/2025	77.403,01
09/12/2025	35.229,42
10/12/2025	35.229,42
11/12/2025	35.229,42
12/12/2025	35.229,42
13/12/2025	0,00
14/12/2025	0,00
15/12/2025	77.403,01
16/12/2025	35.229,42
17/12/2025	35.229,42
18/12/2025	35.229,42
19/12/2025	35.229,42
20/12/2025	0,00
21/12/2025	0,00
22/12/2025	77.403,01
23/12/2025	35.229,42
24/12/2025	35.229,42
25/12/2025	35.229,42
26/12/2025	35.229,42
27/12/2025	0,00
28/12/2025	0,00
29/12/2025	77.403,01
30/12/2025	35.229,42
31/12/2025	35.229,42
01/01/2026	35.229,42
02/01/2026	35.229,42
03/01/2026	0,00
04/01/2026	0,00
05/01/2026	77.403,01
06/01/2026	35.229,42
07/01/2026	35.229,42
08/01/2026	35.229,42
09/01/2026	35.229,42
10/01/2026	0,00
11/01/2026	0,00
12/01/2026	77.403,01
13/01/2026	35.229,42
14/01/2026	35.229,42
15/01/2026	35.229,42
16/01/2026	35.229,42
17/01/2026	0,00
18/01/2026	0,00
19/01/2026	77.403,01
20/01/2026	35.229,42
21/01/2026	35.229,42
22/01/2026	35.229,42
23/01/2026	35.229,42
24/01/2026	0,00
25/01/2026	0,00
26/01/2026	77.403,01
27/01/2026	35.229,42
28/01/2026	35.229,42
29/01/2026	35.229,42
30/01/2026	35.229,42
31/01/2026	0,00
01/02/2026	0,00
02/02/2026	77.403,01
03/02/2026	35.229,42
04/02/2026	35.229,42
05/02/2026	35.229,42
06/02/2026	35.229,42
07/02/2026	0,00
08/02/2026	0,00
09/02/2026	77.403,01
10/02/2026	35.229,42
11/02/2026	35.229,42
12/02/2026	35.229,42
13/02/2026	35.229,42
14/02/2026	0,00
15/02/2026	0,00
16/02/2026	77.403,01
17/02/2026	35.229,42
18/02/2026	35.229,42
19/02/2026	35.229,42
20/02/2026	35.229,42
21/02/2026	0,00"""
    
    print("=" * 60)
    print("📝 Atualizando Valores Previstos de Entradas")
    print("=" * 60)
    print()
    
    # Processar dados
    entries = []
    for line in data.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            date_str = parts[0].strip()
            value_str = parts[1].strip()
            
            date_iso = parse_date(date_str)
            value = parse_brazilian_number(value_str)
            
            if date_iso:
                entries.append((date_iso, value))
    
    print(f"📊 Processando {len(entries)} data(s)...")
    print()
    
    success_count = 0
    error_count = 0
    not_found_count = 0
    
    for date_iso, forecast_value in entries:
        try:
            resp = supabase.table("finance_daily").select("id").eq("date", date_iso).limit(1).execute()
            if not resp.data:
                print(f"⚠️  {date_iso}: Não encontrado no banco")
                not_found_count += 1
                continue
            
            if update_forecast(date_iso, forecast_value):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Erro ao atualizar {date_iso}: {e}")
            error_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Concluído:")
    print(f"   - {success_count} atualizado(s) com sucesso")
    print(f"   - {not_found_count} não encontrado(s) no banco")
    print(f"   - {error_count} erro(s)")
    print("=" * 60)
    print()
    print("💡 Dica: Se alguns dias não foram encontrados, execute 'Atualizar Fluxo'")
    print("   no aplicativo para criar os registros do mês primeiro.")

if __name__ == "__main__":
    main()

