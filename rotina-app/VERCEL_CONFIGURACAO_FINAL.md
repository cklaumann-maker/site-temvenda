# ✅ Configuração Final do Vercel - SOLUÇÃO DEFINITIVA

## ⚠️ CONFIGURAÇÃO CORRETA NO DASHBOARD DO VERCEL

### Opção 1: Root Directory = `rotina-app/apps/web` (RECOMENDADO)

Esta é a configuração mais simples e que funciona melhor com o Vercel:

#### 1. Root Directory
**Configurar como:** `rotina-app/apps/web`

**Motivo:** O Vercel precisa encontrar o `package.json` que contém o Next.js.

#### 2. Framework Settings

##### Build Command
```
cd ../../ && pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
```

**OU** (mais simples):
```
cd ../.. && pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
```

##### Output Directory
**Deixar VAZIO** ou configurar como: `.next`

**Motivo:** Se o Root Directory é `rotina-app/apps/web`, o Output Directory deve ser `.next` (relativo ao root).

##### Install Command
```
cd ../.. && pnpm install
```

##### Development Command
Deixar vazio ou como padrão do Next.js

---

### Opção 2: Root Directory = `rotina-app` (ALTERNATIVA)

Se preferir manter na raiz do monorepo:

#### 1. Root Directory
**Configurar como:** `rotina-app`

#### 2. Framework Settings

##### Build Command
```
pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
```

##### Output Directory
**Configurar como:** `apps/web/.next`

##### Install Command
```
pnpm install
```

---

## ⚠️ IMPORTANTE: Escolha UMA das opções acima

**Recomendação:** Use a **Opção 1** (`rotina-app/apps/web` como Root Directory) porque:
- O Vercel detecta automaticamente o Next.js
- Menos configuração manual
- Mais compatível com a detecção automática do framework

---

## Passos para Configurar (Opção 1 - RECOMENDADA)

1. Acesse: **Settings** > **General**
2. **Root Directory**: Configure como `rotina-app/apps/web`
3. **Output Directory**: Deixe VAZIO ou configure como `.next`
4. **Build Command**: 
   ```
   cd ../.. && pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
   ```
5. **Install Command**:
   ```
   cd ../.. && pnpm install
   ```
6. **Include files outside the root directory**: ✅ **Enabled**
7. Clique em **Save**
8. Faça um novo deploy

---

## Por que essa configuração funciona?

- **Root Directory = `rotina-app/apps/web`**: O Vercel encontra o `package.json` com Next.js
- **Build Command com `cd ../..`**: Volta à raiz do monorepo para executar comandos do pnpm workspace
- **Output Directory vazio ou `.next`**: O Next.js cria automaticamente em `.next` dentro do root directory
