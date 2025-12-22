#!/bin/bash

# Script para iniciar desenvolvimento local
# Porta: 3001 (web)

set -e

echo "🚀 Iniciando Rotina App em modo desenvolvimento..."
echo ""

# Verificar se pnpm está instalado
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm não encontrado. Instale com: npm install -g pnpm"
    exit 1
fi

# Verificar se .env.local existe
if [ ! -f "apps/web/.env.local" ]; then
    echo "⚠️  Arquivo .env.local não encontrado!"
    echo "📝 Criando arquivo .env.local..."
    if [ -f "apps/web/env.local.example" ]; then
        cp apps/web/env.local.example apps/web/.env.local
    elif [ -f "apps/web/env.example" ]; then
        cp apps/web/env.example apps/web/.env.local
    else
        echo "# Configure suas credenciais do Supabase" > apps/web/.env.local
        echo "NEXT_PUBLIC_SUPABASE_URL=" >> apps/web/.env.local
        echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=" >> apps/web/.env.local
        echo "SUPABASE_SERVICE_ROLE_KEY=" >> apps/web/.env.local
    fi
    echo "✅ Arquivo criado. Configure as variáveis de ambiente antes de continuar."
    echo ""
    echo "📖 Edite apps/web/.env.local com suas credenciais do Supabase"
    exit 1
fi

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    pnpm install
fi

# Build dos packages compartilhados
echo "🔨 Construindo packages compartilhados..."
pnpm --filter shared build || echo "⚠️  Build de shared falhou (pode ser normal na primeira vez)"
pnpm --filter ui build || echo "⚠️  Build de ui falhou (pode ser normal na primeira vez)"

echo ""
echo "✅ Tudo pronto!"
echo ""
echo "🌐 Web app rodando em: http://localhost:3001"
echo ""
echo "📱 Para rodar mobile: pnpm mobile"
echo ""

# Iniciar web app
pnpm --filter web dev

