#!/bin/bash

# Script para verificar erros de TypeScript antes do deploy
# Uso: ./scripts/verificar-typescript.sh

set -e

echo "🔍 Verificando erros de TypeScript..."

cd "$(dirname "$0")/.."

# Verificar TypeScript no projeto web
echo ""
echo "📦 Verificando apps/web..."
cd apps/web
pnpm exec tsc --noEmit

echo ""
echo "✅ Nenhum erro de TypeScript encontrado!"
echo ""
echo "💡 Dica: Execute este script antes de fazer push para evitar erros no deploy."

