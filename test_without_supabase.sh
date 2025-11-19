#!/bin/bash
# 🧪 Teste simulando GitHub Actions SEM Supabase instalado

echo "🧪 TESTE: Simular GitHub Actions SEM Supabase"
echo "=============================================="
echo ""

# Criar ambiente virtual temporário
VENV_DIR="/tmp/test_github_env_$$"
echo "📦 Criando ambiente virtual temporário: $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo ""
echo "🔍 Verificando que Supabase NÃO está instalado..."
python3 -c "import supabase" 2>/dev/null && echo "❌ Supabase está instalado (não deveria estar)" || echo "✅ Supabase NÃO está instalado (correto)"

echo ""
echo "📦 Instalando dependências do requirements.txt..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install --no-cache-dir -r requirements.txt

echo ""
echo "🔍 Verificando se Supabase foi instalado..."
python3 -c "import supabase; print('✅ Supabase instalado:', supabase.__version__)" 2>&1

echo ""
echo "🧪 Testando importação do news_collector.py..."
python3 -c "
import sys
import os
sys.path.insert(0, os.getcwd())
try:
    from news_collector import NewsCollector
    print('✅ news_collector.py importado com sucesso!')
    print('✅ Todas as dependências estão corretas!')
except Exception as e:
    print(f'❌ Erro: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" 2>&1

echo ""
echo "🧹 Limpando ambiente virtual..."
deactivate
rm -rf "$VENV_DIR"

echo ""
echo "=============================================="
echo "✅ TESTE CONCLUÍDO!"
echo ""

