#!/bin/bash

# Script para criar arquivo .env.local

cd "$(dirname "$0")"

if [ -f "apps/web/.env.local" ]; then
    echo "✅ Arquivo .env.local já existe!"
    echo ""
    echo "Conteúdo atual:"
    cat apps/web/.env.local
else
    echo "📝 Criando arquivo .env.local..."
    cp apps/web/env.local.CONFIGURAR apps/web/.env.local
    echo "✅ Arquivo .env.local criado com sucesso!"
    echo ""
    echo "Conteúdo:"
    cat apps/web/.env.local
fi

