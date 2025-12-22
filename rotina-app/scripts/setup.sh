#!/bin/bash

# Script de setup inicial do projeto

set -e

echo "🔧 Setup inicial do Rotina App"
echo ""

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale Node.js 18+ primeiro."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ é necessário. Versão atual: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) encontrado"

# Verificar pnpm
if ! command -v pnpm &> /dev/null; then
    echo "📦 Instalando pnpm..."
    npm install -g pnpm
else
    echo "✅ pnpm $(pnpm -v) encontrado"
fi

# Instalar dependências
echo ""
echo "📦 Instalando dependências..."
pnpm install

# Criar arquivo .env.local se não existir
if [ ! -f "apps/web/.env.local" ]; then
    echo ""
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
    echo "✅ Arquivo .env.local criado"
    echo ""
    echo "⚠️  IMPORTANTE: Configure as variáveis de ambiente em apps/web/.env.local"
    echo "   Você precisa das credenciais do Supabase:"
    echo "   - NEXT_PUBLIC_SUPABASE_URL"
    echo "   - NEXT_PUBLIC_SUPABASE_ANON_KEY"
    echo "   - SUPABASE_SERVICE_ROLE_KEY"
    echo ""
fi

# Build dos packages
echo ""
echo "🔨 Construindo packages compartilhados..."
pnpm --filter shared build
pnpm --filter ui build

echo ""
echo "✅ Setup completo!"
echo ""
echo "📖 Próximos passos:"
echo "   1. Configure apps/web/.env.local com suas credenciais do Supabase"
echo "   2. Execute as migrations do Supabase (veja DEPLOYMENT.md)"
echo "   3. Execute: ./scripts/dev.sh ou pnpm dev"
echo ""

