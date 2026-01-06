#!/bin/bash

# Script para iniciar Supabase local (opcional)
# Porta: 54321 (API), 54322 (DB)

set -e

echo "🗄️  Iniciando Supabase local..."
echo ""

# Verificar se supabase CLI está instalado
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI não encontrado."
    echo "📦 Instale com: brew install supabase/tap/supabase"
    echo "   ou: npm install -g supabase"
    exit 1
fi

cd supabase

# Verificar se já está inicializado
if [ ! -f "config.toml" ]; then
    echo "🔧 Inicializando Supabase local..."
    supabase init
fi

# Iniciar Supabase
echo "🚀 Iniciando serviços..."
supabase start

echo ""
echo "✅ Supabase local rodando!"
echo ""
echo "📊 Dashboard: http://localhost:54323"
echo "🔗 API URL: http://localhost:54321"
echo "🗄️  DB Port: 54322"
echo ""
echo "📝 Configure apps/web/.env.local com:"
echo "   NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321"
echo "   NEXT_PUBLIC_SUPABASE_ANON_KEY=<veja output acima>"
echo ""







