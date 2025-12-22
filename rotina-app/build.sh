#!/bin/bash
set -e

# Navegar para a raiz do monorepo (se executado de apps/web)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/pnpm-workspace.yaml" ]; then
  ROOT_DIR="$SCRIPT_DIR"
else
  # Se estamos em apps/web, subir dois níveis
  ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

cd "$ROOT_DIR"

# Instalar dependências
pnpm install

# Construir packages compartilhados
pnpm --filter @rotina/shared build
pnpm --filter @rotina/ui build

# Construir app web
pnpm --filter web build

