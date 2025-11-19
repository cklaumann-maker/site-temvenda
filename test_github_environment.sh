#!/bin/bash
# 🧪 Script de teste para simular ambiente do GitHub Actions

echo "🧪 TESTANDO AMBIENTE SIMILAR AO GITHUB ACTIONS"
echo "================================================"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para testar
test_step() {
    echo -e "${YELLOW}📋 $1${NC}"
    if eval "$2"; then
        echo -e "${GREEN}✅ PASSOU${NC}"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
    echo ""
}

# Teste 1: Python está disponível
test_step "Teste 1: Python 3 disponível" "python3 --version"

# Teste 2: pip está disponível
test_step "Teste 2: pip disponível" "python3 -m pip --version"

# Teste 3: Limpar cache (simular GitHub Actions)
echo -e "${YELLOW}📋 Teste 3: Limpar cache do pip${NC}"
python3 -m pip cache purge 2>/dev/null || true
echo -e "${GREEN}✅ Cache limpo${NC}"
echo ""

# Teste 4: Atualizar pip
test_step "Teste 4: Atualizar pip" "python3 -m pip install --upgrade pip --quiet"

# Teste 5: Instalar Supabase explicitamente (como no workflow)
echo -e "${YELLOW}📋 Teste 5: Instalar Supabase explicitamente${NC}"
python3 -m pip install --no-cache-dir --upgrade supabase==2.22.2
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Supabase instalado${NC}"
else
    echo -e "${RED}❌ Erro ao instalar Supabase${NC}"
    exit 1
fi
echo ""

# Teste 6: Verificar instalação do Supabase
test_step "Teste 6: Verificar instalação do Supabase" "python3 -m pip show supabase > /dev/null 2>&1"

# Teste 7: Importar Supabase
echo -e "${YELLOW}📋 Teste 7: Importar Supabase${NC}"
python3 -c "import supabase; print('✅ Supabase importado:', supabase.__version__)" 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASSOU${NC}"
else
    echo -e "${RED}❌ FALHOU${NC}"
    exit 1
fi
echo ""

# Teste 8: Instalar outras dependências do requirements.txt
echo -e "${YELLOW}📋 Teste 8: Instalar dependências do requirements.txt${NC}"
python3 -m pip install --no-cache-dir -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências instaladas${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi
echo ""

# Teste 9: Verificar importação completa do Supabase
echo -e "${YELLOW}📋 Teste 9: Importação completa do Supabase${NC}"
python3 -c "import supabase; from supabase import create_client, Client; print('✅ Importação completa OK')" 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASSOU${NC}"
else
    echo -e "${RED}❌ FALHOU${NC}"
    exit 1
fi
echo ""

# Teste 10: Testar importação do news_collector.py
echo -e "${YELLOW}📋 Teste 10: Importar news_collector.py${NC}"
python3 -c "
import sys
import os
sys.path.insert(0, os.getcwd())
try:
    from news_collector import NewsCollector
    print('✅ news_collector.py importado com sucesso!')
except Exception as e:
    print(f'❌ Erro: {e}')
    sys.exit(1)
" 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASSOU${NC}"
else
    echo -e "${RED}❌ FALHOU${NC}"
    exit 1
fi
echo ""

# Resumo final
echo "================================================"
echo -e "${GREEN}✅ TODOS OS TESTES PASSARAM!${NC}"
echo ""
echo "🎯 O ambiente está pronto para executar o script"
echo "💡 Você pode executar: python3 news_collector.py"
echo ""

