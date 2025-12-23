#!/usr/bin/env python3
"""
Script rápido para testar a leitura da coluna 'Data pag' direto da planilha,
sem depender do estado atual do banco.
"""

import os
import sys
from datetime import date

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.finance_service import process_expense_items, parse_month_code
from app.supabase_client import get_supabase
from app.finance_service import download_excel_from_drive


def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    month_code = "12-25"
    year, month = parse_month_code(month_code)
    print("========================================================================================================================")
    print(f"🔍 TESTE DE LEITURA DA COLUNA 'Data pag' - MÊS {month_code}")
    print("========================================================================================================================")
    print()

    # Baixa a planilha do mesmo jeito que o refresh_month
    print("⬇️  Baixando planilha do Google Drive (arquivo padrão de fluxo)...")
    excel_bytes = download_excel_from_drive()
    print(f"✅ Planilha baixada ({len(excel_bytes)} bytes)")
    print()

    # Processa apenas expense_items em memória (NÃO grava no banco)
    print("⚙️  Processando expense_items em memória...")
    items = process_expense_items(excel_bytes, month_code)
    print(f"✅ {len(items)} expense_items gerados a partir da planilha")
    print()

    # Filtra itens que têm payment_date preenchido
    itens_com_payment_date = [i for i in items if i.get("payment_date")]
    print(f"✅ Itens COM payment_date: {len(itens_com_payment_date)}")
    print()

    if not itens_com_payment_date:
        print("❌ NENHUM item com payment_date foi lido da planilha!")
        return

    # Agrupa por payment_date
    por_data = {}
    for item in itens_com_payment_date:
        pd = item.get("payment_date")
        por_data.setdefault(pd, []).append(item)

    print(f"📅 Datas de pagamento únicas lidas da planilha: {len(por_data)}")
    print()

    for pd in sorted(por_data.keys()):
        itens = por_data[pd]
        total = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens)
        print(f"📆 {pd}: {len(itens)} itens = {format_currency(total)}")

    print()
    # Foco específico em 2025-12-01
    alvo = "2025-12-01"
    itens_1201 = por_data.get(alvo, [])
    print("========================================================================================================================")
    print("🔍 VALIDAÇÃO ESPECÍFICA - 01/12/2025 (2025-12-01)")
    print("========================================================================================================================")
    print()
    print(f"Itens com payment_date = {alvo}: {len(itens_1201)}")
    total_1201 = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in itens_1201)
    print(f"Soma amount_paid + interest (planilha -> memória): {format_currency(total_1201)}")
    print()


if __name__ == "__main__":
    main()


