#!/bin/bash
# Script para iniciar o backend local

cd "$(dirname "$0")"

echo "🚀 Iniciando backend local..."
echo ""

# Verificar se o venv existe
if [ ! -f ".venv/bin/activate" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
else
    echo "✅ Ativando ambiente virtual..."
    source .venv/bin/activate
fi

echo ""
echo "✅ Iniciando servidor na porta 8001..."
echo "   Acesse: http://localhost:8001/health"
echo "   Para parar: Ctrl+C"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

