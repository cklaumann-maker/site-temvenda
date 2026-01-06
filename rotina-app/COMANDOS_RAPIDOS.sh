#!/bin/bash

# Script rápido para executar todos os comandos do Supabase
# Execute: chmod +x COMANDOS_RAPIDOS.sh && ./COMANDOS_RAPIDOS.sh

set -e

echo "🗄️  Configurando Supabase..."
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Verificar se está no diretório correto
if [ ! -d "supabase" ]; then
    echo "${RED}❌ Erro: Execute este script da raiz do projeto (rotina-app)${NC}"
    exit 1
fi

# 2. Navegar para supabase
cd supabase

echo "${YELLOW}1️⃣  Verificando Supabase CLI...${NC}"
if ! command -v supabase &> /dev/null; then
    echo "${RED}❌ Supabase CLI não encontrado${NC}"
    echo "Instale com: brew install supabase/tap/supabase"
    exit 1
fi
echo "${GREEN}✅ Supabase CLI encontrado${NC}"
echo ""

# 3. Linkar projeto
echo "${YELLOW}2️⃣  Linkando projeto...${NC}"
supabase link --project-ref mgcoyeohqelystqmytah || {
    echo "${YELLOW}⚠️  Projeto já linkado ou precisa de login${NC}"
    echo "Execute: supabase login"
}
echo ""

# 4. Executar migrations
echo "${YELLOW}3️⃣  Executando migrations...${NC}"
supabase db push || {
    echo "${RED}❌ Erro ao executar migrations${NC}"
    exit 1
}
echo "${GREEN}✅ Migrations executadas${NC}"
echo ""

# 5. Executar seed (opcional)
read -p "Deseja executar seed.sql (dados de demonstração)? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "${YELLOW}4️⃣  Executando seed...${NC}"
    supabase db execute --file seed.sql || {
        echo "${YELLOW}⚠️  Seed pode ter falhado (pode ser normal se já existir)${NC}"
    }
    echo "${GREEN}✅ Seed executado${NC}"
else
    echo "${YELLOW}4️⃣  Pulando seed${NC}"
fi
echo ""

# 6. Verificar status
echo "${YELLOW}5️⃣  Verificando status...${NC}"
supabase status
echo ""

# 7. Listar migrations
echo "${YELLOW}6️⃣  Migrations aplicadas:${NC}"
supabase migration list
echo ""

echo "${GREEN}✅ Configuração do Supabase concluída!${NC}"
echo ""
echo "📋 Próximos passos:"
echo "   1. Configure URLs permitidas no Supabase Dashboard"
echo "   2. Execute: pnpm --filter shared build"
echo "   3. Execute: pnpm dev"
echo ""







