#!/bin/bash
# Script para gerar SQL de importação do CSV com calorias

cd "$(dirname "$0")/.."

if [ ! -f "plano_calorias.csv" ]; then
    echo "❌ Arquivo plano_calorias.csv não encontrado!"
    echo "Crie o arquivo plano_calorias.csv na raiz do projeto com o conteúdo CSV fornecido."
    exit 1
fi

echo "📊 Processando plano_calorias.csv..."
python3 scripts/import_plano_com_calorias.py plano_calorias.csv

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SQL gerado com sucesso: plano_calorias_com_calorias.sql"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Abra o arquivo plano_calorias_com_calorias.sql"
    echo "2. Copie todo o conteúdo"
    echo "3. Cole no Supabase SQL Editor"
    echo "4. Execute o SQL"
else
    echo "❌ Erro ao processar CSV"
    exit 1
fi

