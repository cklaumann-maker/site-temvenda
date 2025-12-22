#!/bin/bash
set -e

# Instalar dependências na raiz do monorepo
cd "$(dirname "$0")"
pnpm install

# Construir packages compartilhados
pnpm --filter @rotina/shared build
pnpm --filter @rotina/ui build

# Construir app web
pnpm --filter web build

