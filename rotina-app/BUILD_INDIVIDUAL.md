# 🔧 Build Individual dos Packages

## Comandos para Build Individual

Execute estes comandos **na ordem**:

```bash
# 1. Build shared
cd rotina-app/packages/shared
pnpm install
pnpm build

# 2. Build ui
cd ../ui
pnpm install
pnpm build

# 3. Voltar para raiz
cd ../..
```

---

## O que Esperar

### Build Bem-Sucedido

**Shared**:
```
> @rotina/shared@1.0.0 build
> tsc

✅ Sem erros
```

**UI**:
```
> @rotina/ui@1.0.0 build
> tsc

✅ Sem erros
```

### Verificar Arquivos Gerados

```bash
# Verificar shared
ls packages/shared/dist/
# Deve mostrar: index.js, index.d.ts, types.js, types.d.ts, etc.

# Verificar ui
ls packages/ui/dist/
# Deve mostrar: index.js, index.d.ts, Button.js, Button.d.ts, etc.
```

---

## Problemas Comuns

### Erro: "Cannot find module 'zod'"

**Solução**: Instalar dependências
```bash
cd packages/shared
pnpm install
```

### Erro: "Cannot find module '@rotina/shared'"

**Solução**: Build shared primeiro, depois ui
```bash
# 1. Build shared primeiro
cd packages/shared
pnpm install
pnpm build

# 2. Depois build ui
cd ../ui
pnpm install
pnpm build
```

### Erro: "Type error"

**Solução**: Verificar tipos
```bash
cd packages/shared
pnpm typecheck
```

### Erro: "Command not found: pnpm"

**Solução**: Instalar pnpm
```bash
npm install -g pnpm
```

---

## Alternativa: Pular Build

Se o build continuar dando problemas, você pode **pular e iniciar direto**:

```bash
cd rotina-app
pnpm dev
```

O Next.js compila automaticamente em desenvolvimento.

---

## Próximos Passos Após Build

1. ✅ Verificar se `dist/` foi criado
2. 🔐 Configurar URLs no Supabase Auth
3. 🚀 Iniciar app: `pnpm dev`
4. 🧪 Testar: http://localhost:3001/login

---

## Checklist

- [ ] `pnpm install` executado em shared
- [ ] `pnpm build` executado em shared (sem erros)
- [ ] `pnpm install` executado em ui
- [ ] `pnpm build` executado em ui (sem erros)
- [ ] `packages/shared/dist/` existe
- [ ] `packages/ui/dist/` existe







