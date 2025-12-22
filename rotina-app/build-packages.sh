#!/bin/bash

# Script para build dos packages compartilhados

set -e

echo "🔨 Building packages..."
echo ""

# Verificar se está na raiz
if [ ! -f "pnpm-workspace.yaml" ]; then
    echo "❌ Execute este script da raiz do projeto (rotina-app)"
    exit 1
fi

# Build shared
echo "📦 Building @rotina/shared..."
cd packages/shared

if [ ! -f "package.json" ]; then
    echo "❌ package.json não encontrado em packages/shared"
    exit 1
fi

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências de shared..."
    pnpm install || npm install
fi

# Build
echo "🔨 Compilando shared..."
pnpm build || npm run build || npx tsc

if [ -d "dist" ]; then
    echo "✅ Shared build concluído!"
    ls -la dist/ | head -5
else
    echo "⚠️  Dist não criado, mas continuando..."
fi

# Build ui
echo ""
echo "📦 Building @rotina/ui..."
cd ../ui

if [ ! -f "package.json" ]; then
    echo "❌ package.json não encontrado em packages/ui"
    exit 1
fi

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências de ui..."
    pnpm install || npm install
fi

# Build
echo "🔨 Compilando ui..."
pnpm build || npm run build || npx tsc

if [ -d "dist" ]; then
    echo "✅ UI build concluído!"
    ls -la dist/ | head -5
else
    echo "⚠️  Dist não criado"
fi

# Voltar para raiz
cd ../..

echo ""
echo "✅ Build dos packages concluído!"
echo ""
echo "Verificar:"
echo "  ls packages/shared/dist/"
echo "  ls packages/ui/dist/"

