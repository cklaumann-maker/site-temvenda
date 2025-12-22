# 🔧 Troubleshooting - Build dos Packages

## Problemas Comuns e Soluções

### Erro: "command not found: pnpm"

**Solução 1**: Instalar pnpm
```bash
npm install -g pnpm
```

**Solução 2**: Usar npx
```bash
npx pnpm --filter shared build
npx pnpm --filter ui build
```

**Solução 3**: Usar npm (alternativa)
```bash
cd packages/shared
npm run build
cd ../ui
npm run build
```

---

### Erro: "Cannot find module" ou "Module not found"

**Solução**: Instalar dependências primeiro
```bash
cd rotina-app
pnpm install
```

Depois tente o build novamente:
```bash
pnpm --filter shared build
pnpm --filter ui build
```

---

### Erro: "Type error" ou erros de TypeScript

**Solução**: Verificar se TypeScript está instalado
```bash
cd packages/shared
pnpm install
pnpm build
```

Se persistir, verifique o `tsconfig.json`:
```bash
cat packages/shared/tsconfig.json
```

---

### Erro: "Workspace not found"

**Solução**: Verificar se está na raiz do projeto
```bash
# Certifique-se de estar em rotina-app/
pwd
# Deve mostrar: .../rotina-app

# Verificar se pnpm-workspace.yaml existe
ls pnpm-workspace.yaml
```

---

### Build funciona mas arquivos não aparecem

**Verificar se dist/ foi criado**:
```bash
ls packages/shared/dist/
ls packages/ui/dist/
```

Se não existir, o build pode ter falhado silenciosamente. Verifique os logs.

---

### Pular build e tentar direto

Se o build estiver dando problemas, você pode tentar iniciar o app diretamente:

```bash
cd rotina-app
pnpm dev
```

O Next.js pode compilar os packages automaticamente em desenvolvimento.

---

## Comandos Alternativos

### Build individual (se workspace não funcionar)

```bash
# Build shared
cd packages/shared
pnpm install
pnpm build

# Build ui
cd ../ui
pnpm install
pnpm build

# Voltar para raiz
cd ../..
```

### Verificar se buildou

```bash
# Verificar arquivos gerados
ls packages/shared/dist/
ls packages/ui/dist/

# Deve mostrar arquivos .js e .d.ts
```

---

## Ordem Recomendada de Execução

```bash
# 1. Ir para raiz
cd rotina-app

# 2. Instalar todas as dependências
pnpm install

# 3. Build packages (se necessário)
pnpm --filter shared build
pnpm --filter ui build

# 4. Iniciar app (pode compilar automaticamente)
pnpm dev
```

---

## Se Nada Funcionar

Tente iniciar o app diretamente - o Next.js pode resolver automaticamente:

```bash
cd rotina-app
pnpm dev
```

O Next.js em modo desenvolvimento pode compilar os packages sob demanda.

