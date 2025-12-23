#!/usr/bin/env python3
"""
Script para validar especificamente o dia 1/12/2025 baseado nas imagens fornecidas.
Soma Valor pago + Juros para itens com Data pag = 01/12/2025 nas abas DIST e DESP.
"""

import sys
import os
from datetime import date
from collections import defaultdict

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.finance_service import download_excel_from_drive, _find_sheet, _get_column, _get_column_optional, _safe_date, _safe_float
    from supabase import create_client
    from app.config import get_settings
    import pandas as pd
    import io
    
    def get_supabase():
        settings = get_settings()
        return create_client(settings.supabase_url, settings.supabase_service_role_key)
        
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    month_code = "12-25"
    target_date = date(2025, 12, 1)
    target_date_str = target_date.isoformat()
    
    print("=" * 120)
    print(f"🔍 VALIDAÇÃO ESPECÍFICA - DIA 1/12/2025")
    print("=" * 120)
    print()
    
    # 1. Lê a planilha diretamente
    print("📥 Baixando planilha do Google Drive...")
    excel_bytes = download_excel_from_drive()
    xls = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None, engine="openpyxl")
    
    dist_df = _find_sheet(xls, "DIST", month_code)
    desp_df = _find_sheet(xls, "DESP", month_code)
    
    print(f"✅ DIST 12-25: {len(dist_df)} linhas")
    print(f"✅ DESP 12-25: {len(desp_df)} linhas")
    print()
    
    # 2. Identifica colunas
    print("🔍 Identificando colunas...")
    
    # DIST
    dist_paid_col = _get_column(dist_df, ["Valor pago", "Valor Pago", "Pago"], 5)
    dist_interest_col = _get_column_optional(dist_df, ["Juros", "Multa", "Juros/Multa", "Acréscimo"], None)
    dist_payment_date_col = _get_column_optional(dist_df, [
        "data pag", "Data pag", "DATA PAG", "Data Pag", "data pagamento", "Data Pagamento", 
        "Data Pago", "Dt Pagamento", "Dt Pago", "Data Pgto", "Dt Pgto",
        "data de pagamento", "Data de Pagamento", "Data de Pago",
        "pagamento", "Pagamento", "PAGAMENTO"
    ], None)
    
    # DESP
    desp_paid_col = _get_column(desp_df, ["Valor pago", "Valor Pago", "Pago"], 6)
    desp_interest_col = _get_column_optional(desp_df, ["Juros", "Multa", "Juros/Multa", "Acréscimo"], None)
    desp_payment_date_col = _get_column_optional(desp_df, [
        "data pag", "Data pag", "DATA PAG", "Data Pag", "data pagamento", "Data Pagamento", 
        "Data Pago", "Dt Pagamento", "Dt Pago", "Data Pgto", "Dt Pgto",
        "data de pagamento", "Data de Pagamento", "Data de Pago",
        "pagamento", "Pagamento", "PAGAMENTO"
    ], None)
    
    # Debug: mostra nomes das colunas encontradas
    print(f"   DIST - Coluna 'Valor pago': {dist_paid_col.name if dist_paid_col is not None else 'NÃO ENCONTRADA'}")
    print(f"   DIST - Coluna 'Juros': {dist_interest_col.name if dist_interest_col is not None else 'NÃO ENCONTRADA'}")
    print(f"   DIST - Coluna 'Data pag': {dist_payment_date_col.name if dist_payment_date_col is not None else 'NÃO ENCONTRADA'}")
    print()
    print(f"   DESP - Coluna 'Valor pago': {desp_paid_col.name if desp_paid_col is not None else 'NÃO ENCONTRADA'}")
    print(f"   DESP - Coluna 'Juros': {desp_interest_col.name if desp_interest_col is not None else 'NÃO ENCONTRADA'}")
    print(f"   DESP - Coluna 'Data pag': {desp_payment_date_col.name if desp_payment_date_col is not None else 'NÃO ENCONTRADA'}")
    print()
    
    if dist_payment_date_col is None:
        print("⚠️  PROBLEMA: Coluna 'Data pag' não encontrada em DIST 12-25!")
        print(f"   Colunas disponíveis em DIST: {list(dist_df.columns)}")
        print()
    
    if desp_payment_date_col is None:
        print("⚠️  PROBLEMA: Coluna 'Data pag' não encontrada em DESP 12-25!")
        print(f"   Colunas disponíveis em DESP: {list(desp_df.columns)}")
        print()
    
    # 3. Processa DIST - soma para dia 1
    print("=" * 120)
    print("📊 PROCESSANDO DIST 12-25 - DIA 1/12/2025")
    print("=" * 120)
    print()
    
    dist_total_dia_1 = 0.0
    dist_itens_dia_1 = []
    
    for idx in range(len(dist_df)):
        # Lê data de pagamento
        if dist_payment_date_col is not None and idx < len(dist_payment_date_col):
            payment_date = _safe_date(dist_payment_date_col.iloc[idx])
        else:
            payment_date = None
        
        # Se não tem payment_date ou não é dia 1, pula
        if payment_date != target_date:
            continue
        
        # Lê valor pago e juros
        amount_paid = _safe_float(dist_paid_col.iloc[idx] if idx < len(dist_paid_col) else None) or 0.0
        interest = _safe_float(dist_interest_col.iloc[idx] if dist_interest_col is not None and idx < len(dist_interest_col) else None) or 0.0
        
        if amount_paid > 0.01:  # Só conta se tem valor pago significativo
            total_item = amount_paid + interest
            dist_total_dia_1 += total_item
            dist_itens_dia_1.append({
                "idx": idx + 2,  # +2 porque começa na linha 2 (linha 1 é cabeçalho)
                "amount_paid": amount_paid,
                "interest": interest,
                "total": total_item
            })
    
    print(f"✅ DIST 12-25 - Dia 1/12/2025:")
    print(f"   Total encontrado: {format_currency(dist_total_dia_1)}")
    print(f"   Número de itens: {len(dist_itens_dia_1)}")
    print()
    if dist_itens_dia_1:
        print("   Detalhamento dos itens:")
        for item in dist_itens_dia_1[:10]:  # Mostra até 10
            print(f"      Linha {item['idx']}: {format_currency(item['amount_paid'])} + {format_currency(item['interest'])} = {format_currency(item['total'])}")
        if len(dist_itens_dia_1) > 10:
            print(f"      ... e mais {len(dist_itens_dia_1) - 10} itens")
    print()
    
    # 4. Processa DESP - soma para dia 1
    print("=" * 120)
    print("📊 PROCESSANDO DESP 12-25 - DIA 1/12/2025")
    print("=" * 120)
    print()
    
    desp_total_dia_1 = 0.0
    desp_itens_dia_1 = []
    
    for idx in range(len(desp_df)):
        # Lê data de pagamento
        if desp_payment_date_col is not None and idx < len(desp_payment_date_col):
            payment_date = _safe_date(desp_payment_date_col.iloc[idx])
        else:
            payment_date = None
        
        # Se não tem payment_date ou não é dia 1, pula
        if payment_date != target_date:
            continue
        
        # Lê valor pago e juros
        amount_paid = _safe_float(desp_paid_col.iloc[idx] if idx < len(desp_paid_col) else None) or 0.0
        interest = _safe_float(desp_interest_col.iloc[idx] if desp_interest_col is not None and idx < len(desp_interest_col) else None) or 0.0
        
        if amount_paid > 0.01:  # Só conta se tem valor pago significativo
            total_item = amount_paid + interest
            desp_total_dia_1 += total_item
            desp_itens_dia_1.append({
                "idx": idx + 2,  # +2 porque começa na linha 2
                "amount_paid": amount_paid,
                "interest": interest,
                "total": total_item
            })
    
    print(f"✅ DESP 12-25 - Dia 1/12/2025:")
    print(f"   Total encontrado: {format_currency(desp_total_dia_1)}")
    print(f"   Número de itens: {len(desp_itens_dia_1)}")
    print()
    if desp_itens_dia_1:
        print("   Detalhamento dos itens:")
        for item in desp_itens_dia_1[:10]:  # Mostra até 10
            print(f"      Linha {item['idx']}: {format_currency(item['amount_paid'])} + {format_currency(item['interest'])} = {format_currency(item['total'])}")
        if len(desp_itens_dia_1) > 10:
            print(f"      ... e mais {len(desp_itens_dia_1) - 10} itens")
    print()
    
    # 5. Total esperado
    total_esperado = dist_total_dia_1 + desp_total_dia_1
    
    print("=" * 120)
    print("📊 TOTAL ESPERADO PARA DIA 1/12/2025")
    print("=" * 120)
    print()
    print(f"   DIST 12-25: {format_currency(dist_total_dia_1)}")
    print(f"   DESP 12-25: {format_currency(desp_total_dia_1)}")
    print(f"   TOTAL ESPERADO: {format_currency(total_esperado)}")
    print()
    
    # 6. Compara com banco de dados
    print("=" * 120)
    print("🔍 COMPARAÇÃO COM BANCO DE DADOS")
    print("=" * 120)
    print()
    
    supabase = get_supabase()
    
    # Busca no finance_daily
    day_resp = supabase.table("finance_daily").select("expenses_paid").eq("month_code", month_code).eq("date", target_date_str).limit(1).execute()
    expenses_paid_banco = float(day_resp.data[0].get("expenses_paid", 0)) if day_resp.data else 0.0
    
    print(f"   Valor no BANCO (expenses_paid): {format_currency(expenses_paid_banco)}")
    print(f"   Valor ESPERADO (planilha): {format_currency(total_esperado)}")
    print()
    
    diferenca = abs(expenses_paid_banco - total_esperado)
    if diferenca < 0.01:
        print("   ✅ VALIDAÇÃO: CORRETO! Os valores coincidem.")
    else:
        print(f"   ❌ VALIDAÇÃO: INCORRETO! Diferença de {format_currency(diferenca)}")
        print()
        print("   AÇÃO NECESSÁRIA:")
        print("   1. Execute 'Atualizar Fluxo' novamente")
        print("   2. Verifique se a coluna 'Data pag' está sendo lida corretamente")
        print()
    
    # 7. Verifica expense_items no banco
    print("=" * 120)
    print("🔍 VERIFICAÇÃO DE EXPENSE_ITEMS NO BANCO")
    print("=" * 120)
    print()
    
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).eq("payment_date", target_date_str).execute()
    items_banco = items_resp.data or []
    
    total_banco_items = sum(float(i.get("amount_paid", 0)) + float(i.get("interest", 0)) for i in items_banco)
    
    print(f"   Itens no banco com payment_date = {target_date_str}: {len(items_banco)}")
    print(f"   Total calculado dos itens: {format_currency(total_banco_items)}")
    print()
    
    if len(items_banco) == 0:
        print("   ⚠️  PROBLEMA: Nenhum expense_item no banco tem payment_date = 01/12/2025!")
        print("   Isso significa que a coluna 'Data pag' não está sendo lida da planilha.")
        print()
    elif abs(total_banco_items - total_esperado) > 0.01:
        print(f"   ⚠️  Diferença entre banco e planilha: {format_currency(abs(total_banco_items - total_esperado))}")
        print()
    
    print("=" * 120)
    print()

if __name__ == "__main__":
    main()

