#!/usr/bin/env python3
"""
Script para verificar se a coluna 'data pag' existe na planilha e se tem dados.
"""

import sys
import os
from datetime import date

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.finance_service import download_excel_from_drive
    import pandas as pd
    import io
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def main():
    print("🔍 Verificando coluna 'data pag' na planilha...")
    print("=" * 100)
    print()
    
    # Baixa Excel
    print("📥 Baixando planilha do Google Drive...")
    excel_bytes = download_excel_from_drive()
    print("✅ Planilha baixada")
    print()
    
    # Lê abas DIST e DESP
    excel_file = io.BytesIO(excel_bytes)
    
    print("📋 Lendo aba DIST 12-25...")
    try:
        dist_df = pd.read_excel(excel_file, sheet_name="DIST 12-25", engine="openpyxl")
        print(f"✅ DIST 12-25: {len(dist_df)} linhas, {len(dist_df.columns)} colunas")
        print(f"   Colunas: {list(dist_df.columns)}")
        print()
        
        # Procura coluna de data de pagamento
        payment_cols = [col for col in dist_df.columns if 'pag' in str(col).lower() or 'pago' in str(col).lower()]
        print(f"🔍 Colunas relacionadas a 'pagamento' encontradas: {payment_cols}")
        print()
        
        if payment_cols:
            for col in payment_cols:
                print(f"   Coluna '{col}':")
                # Conta valores não nulos
                non_null = dist_df[col].notna().sum()
                print(f"      - Valores não nulos: {non_null} de {len(dist_df)}")
                # Mostra alguns exemplos
                examples = dist_df[col].dropna().head(5).tolist()
                if examples:
                    print(f"      - Exemplos: {examples}")
                print()
    except Exception as e:
        print(f"❌ Erro ao ler DIST 12-25: {e}")
        print()
    
    # Reset do arquivo para ler outra aba
    excel_file.seek(0)
    
    print("📋 Lendo aba DESP 12-25...")
    try:
        desp_df = pd.read_excel(excel_file, sheet_name="DESP 12-25", engine="openpyxl")
        print(f"✅ DESP 12-25: {len(desp_df)} linhas, {len(desp_df.columns)} colunas")
        print(f"   Colunas: {list(desp_df.columns)}")
        print()
        
        # Procura coluna de data de pagamento
        payment_cols = [col for col in desp_df.columns if 'pag' in str(col).lower() or 'pago' in str(col).lower()]
        print(f"🔍 Colunas relacionadas a 'pagamento' encontradas: {payment_cols}")
        print()
        
        if payment_cols:
            for col in payment_cols:
                print(f"   Coluna '{col}':")
                # Conta valores não nulos
                non_null = desp_df[col].notna().sum()
                print(f"      - Valores não nulos: {non_null} de {len(desp_df)}")
                # Mostra alguns exemplos
                examples = desp_df[col].dropna().head(5).tolist()
                if examples:
                    print(f"      - Exemplos: {examples}")
                print()
    except Exception as e:
        print(f"❌ Erro ao ler DESP 12-25: {e}")
        print()
    
    print("=" * 100)
    print()
    print("💡 Se a coluna 'data pag' não aparecer acima, ela pode ter outro nome.")
    print("   Verifique na planilha o nome exato da coluna de data de pagamento.")

if __name__ == "__main__":
    main()
