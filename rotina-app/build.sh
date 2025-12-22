#!/bin/bash
set -e

# Se executado de dentro de apps/web, voltar à raiz
if [ -d "../.." ] && [ -f "../../pnpm-workspace.yaml" ]; then
  cd ../..
fi

# Instalar dependências na raiz do monorepo
pnpm install

# Construir packages compartilhados
pnpm --filter @rotina/shared build
pnpm --filter @rotina/ui build

# Construir app web
pnpm --filter web build

