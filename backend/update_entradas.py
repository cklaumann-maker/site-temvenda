#!/usr/bin/env python3
"""
Script para atualizar valores de entradas no banco de dados.

Uso:
    python update_entradas.py

Formato dos dados (cole no terminal ou edite o arquivo):
    data:YYYY-MM-DD,money:valor,pix:valor,card:valor,convenio:valor
    ou
    data:YYYY-MM-DD,money:valor,pix:valor,card:valor,convenio:valor
    ...
"""

import os
import sys
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
    print("❌ Erro: SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY devem estar configurados no .env")
    sys.exit(1)

# Conectar ao Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def parse_entry(line: str) -> dict:
    """Parse uma linha no formato: data:YYYY-MM-DD,money:valor,pix:valor,card:valor,convenio:valor"""
    parts = line.strip().split(',')
    entry = {}
    
    for part in parts:
        if ':' in part:
            key, value = part.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'data':
                entry['date'] = value
            elif key in ['money', 'pix', 'card', 'convenio']:
                try:
                    entry[f'cash_in_actual_{key}'] = float(value)
                except ValueError:
                    print(f"⚠️  Aviso: Valor inválido para {key}: {value}")
                    entry[f'cash_in_actual_{key}'] = 0.0
    
    return entry

def update_entry(entry: dict):
    """Atualiza uma entrada no banco de dados"""
    date = entry.get('date')
    if not date:
        print("❌ Erro: Data não fornecida")
        return False
    
    # Buscar o registro existente
    resp = supabase.table("finance_daily").select("*").eq("date", date).limit(1).execute()
    
    if not resp.data:
        print(f"⚠️  Aviso: Dia {date} não encontrado no banco. Criando novo registro...")
        # Criar registro básico se não existir
        month_code = f"{date[5:7]}-{date[2:4]}"  # YYYY-MM-DD -> MM-YY
        new_record = {
            "month_code": month_code,
            "date": date,
            "weekday": "Unknown",
            "sales": 0.0,
            "cash_in_forecast_total": 0.0,
            "cash_in_actual_money": entry.get('cash_in_actual_money', 0.0),
            "cash_in_actual_pix": entry.get('cash_in_actual_pix', 0.0),
            "cash_in_actual_card": entry.get('cash_in_actual_card', 0.0),
            "cash_in_actual_convenio": entry.get('cash_in_actual_convenio', 0.0),
            "future_in_confirmed": 0.0,
            "purchases_planned": 0.0,
            "old_debts_paid": 0.0,
            "expenses_planned": 0.0,
            "expenses_paid": 0.0,
            "balance_projected": 0.0,
            "balance_real": 0.0,
        }
        supabase.table("finance_daily").insert(new_record).execute()
        print(f"✅ Registro criado para {date}")
        return True
    
    # Atualizar registro existente
    day = resp.data[0]
    
    # Preparar dados de atualização
    update_data = {}
    if 'cash_in_actual_money' in entry:
        update_data['cash_in_actual_money'] = entry['cash_in_actual_money']
    if 'cash_in_actual_pix' in entry:
        update_data['cash_in_actual_pix'] = entry['cash_in_actual_pix']
    if 'cash_in_actual_card' in entry:
        update_data['cash_in_actual_card'] = entry['cash_in_actual_card']
    if 'cash_in_actual_convenio' in entry:
        update_data['cash_in_actual_convenio'] = entry['cash_in_actual_convenio']
    
    if not update_data:
        print(f"⚠️  Aviso: Nenhum valor para atualizar em {date}")
        return False
    
    # Recalcular saldos
    cash_in_actual_total = (
        update_data.get('cash_in_actual_money', day.get('cash_in_actual_money', 0) or 0)
        + update_data.get('cash_in_actual_pix', day.get('cash_in_actual_pix', 0) or 0)
        + update_data.get('cash_in_actual_card', day.get('cash_in_actual_card', 0) or 0)
        + update_data.get('cash_in_actual_convenio', day.get('cash_in_actual_convenio', 0) or 0)
    )
    
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day.get('cash_in_forecast_total', 0) or 0)
    cash_in_total = cash_in_used + float(day.get('future_in_confirmed', 0) or 0)
    cash_out_planned = float(day.get('expenses_planned', 0) or 0) + float(day.get('purchases_planned', 0) or 0) + float(day.get('old_debts_paid', 0) or 0)
    cash_out_real = float(day.get('expenses_paid', 0) or 0) + float(day.get('purchases_planned', 0) or 0) + float(day.get('old_debts_paid', 0) or 0)
    
    update_data['balance_projected'] = float(day.get('sales', 0) or 0) + cash_in_total - cash_out_planned
    update_data['balance_real'] = cash_in_total - cash_out_real
    
    # Atualizar no banco
    supabase.table("finance_daily").update(update_data).eq("id", day["id"]).execute()
    
    print(f"✅ Atualizado {date}:")
    if 'cash_in_actual_money' in update_data:
        print(f"   Dinheiro: R$ {update_data['cash_in_actual_money']:,.2f}")
    if 'cash_in_actual_pix' in update_data:
        print(f"   PIX: R$ {update_data['cash_in_actual_pix']:,.2f}")
    if 'cash_in_actual_card' in update_data:
        print(f"   Cartão: R$ {update_data['cash_in_actual_card']:,.2f}")
    if 'cash_in_actual_convenio' in update_data:
        print(f"   Convênio: R$ {update_data['cash_in_actual_convenio']:,.2f}")
    print(f"   Saldo Real: R$ {update_data['balance_real']:,.2f}")
    
    return True

def main():
    print("=" * 60)
    print("📝 Atualizador de Entradas - Fluxo de Caixa")
    print("=" * 60)
    print()
    print("Cole os dados no formato abaixo (uma linha por dia):")
    print("data:YYYY-MM-DD,money:valor,pix:valor,card:valor,convenio:valor")
    print()
    print("Exemplo:")
    print("data:2025-12-01,money:1000.00,pix:500.00,card:200.00,convenio:50.00")
    print("data:2025-12-02,money:1500.00,pix:600.00,card:300.00,convenio:0.00")
    print()
    print("Digite 'fim' quando terminar de colar os dados.")
    print("Ou pressione Ctrl+D (Linux/Mac) ou Ctrl+Z (Windows) para finalizar.")
    print()
    print("-" * 60)
    
    entries = []
    print("Cole os dados aqui:")
    
    try:
        while True:
            line = input().strip()
            if line.lower() == 'fim' or line.lower() == 'fim':
                break
            if line:
                entry = parse_entry(line)
                if entry:
                    entries.append(entry)
    except EOFError:
        pass
    
    if not entries:
        print("❌ Nenhum dado fornecido.")
        return
    
    print()
    print(f"📊 Processando {len(entries)} entrada(s)...")
    print()
    
    success_count = 0
    error_count = 0
    
    for entry in entries:
        try:
            if update_entry(entry):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Erro ao atualizar {entry.get('date', 'desconhecido')}: {e}")
            error_count += 1
        print()
    
    print("=" * 60)
    print(f"✅ Concluído: {success_count} atualizado(s), {error_count} erro(s)")
    print("=" * 60)

if __name__ == "__main__":
    main()

