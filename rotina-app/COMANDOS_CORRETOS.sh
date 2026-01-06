#!/bin/bash

# Comandos corretos para iniciar o app
# Você já está em rotina-app, então não precisa fazer cd novamente

echo "📦 Verificando pnpm..."
if ! command -v pnpm &> /dev/null; then
    echo "⚠️  pnpm não encontrado!"
    echo ""
    echo "Instale com uma das opções:"
    echo "  1. brew install pnpm"
    echo "  2. npm install -g pnpm"
    echo "  3. curl -fsSL https://get.pnpm.io/install.sh | sh -"
    echo ""
    echo "Ou use npx (sem instalar):"
    echo "  npx pnpm install"
    echo "  npx pnpm dev"
    exit 1
fi

echo "✅ pnpm encontrado: $(pnpm --version)"
echo ""

# Verificar se está na raiz
if [ ! -f "pnpm-workspace.yaml" ]; then
    echo "⚠️  Você precisa estar na raiz do projeto (rotina-app)"
    echo "Execute: cd rotina-app"
    exit 1
fi

echo "📦 Instalando dependências..."
pnpm install

echo ""
echo "🚀 Iniciando aplicativo..."
echo "   Acesse: http://localhost:3001"
echo ""

pnpm dev







