# ✅ Configuração Final do Vercel - CORRIGIDA

## ⚠️ AJUSTE NECESSÁRIO NO DASHBOARD DO VERCEL

### 1. Root Directory
**Configurar como:** `rotina-app`

**NÃO usar:** `rotina-app/apps/web` ❌

**Motivo:** O Vercel precisa estar na raiz do monorepo para:
- Acessar o `pnpm-workspace.yaml`
- Construir os packages compartilhados
- Executar comandos do pnpm workspace

---

### 2. Framework Settings

#### Build Command
```
cd apps/web && pnpm install && cd ../.. && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
```

**OU** (mais simples, se o Root Directory for `rotina-app`):
```
pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
```

#### Output Directory
**Configurar como:** `apps/web/.next`

**Motivo:** Se o Root Directory é `rotina-app`, então o Output Directory deve ser relativo a ele: `apps/web/.next`

#### Install Command
```
pnpm install
```

#### Development Command
Deixar vazio ou como padrão do Next.js

---

### 3. Outras Configurações

- **Include files outside the root directory in the Build Step:** ✅ **Enabled**
- **Skip deployments when there are no changes:** Pode deixar como está

---

## Passos para Corrigir AGORA

1. Acesse: **Settings** > **General**
2. **Root Directory**: Altere de `rotina-app/apps/web` para `rotina-app`
3. **Output Directory**: Configure como `apps/web/.next`
4. **Build Command**: Use o comando completo acima
5. Clique em **Save**
6. Faça um novo deploy

---

## Por que essa configuração?

- **Root Directory = `rotina-app`**: Permite acesso ao monorepo completo
- **Output Directory = `apps/web/.next`**: Relativo ao Root Directory, aponta para onde o Next.js cria os arquivos
- **Build Command**: Constrói packages compartilhados antes do app web

