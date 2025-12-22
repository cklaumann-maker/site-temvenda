# Configurações Corretas do Vercel

## ⚠️ IMPORTANTE: Ajustar no Dashboard do Vercel

### 1. Root Directory
**Configurar como:** `rotina-app`

**NÃO usar:** `rotina-app/apps/web` ❌

**Motivo:** O Vercel precisa estar na raiz do monorepo para construir os packages compartilhados (`@rotina/shared` e `@rotina/ui`).

---

### 2. Framework Settings

#### Build Command
```
pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
```

#### Output Directory
**Deixar VAZIO** ou configurar como: `.next`

**NÃO usar:** `apps/web/.next` ❌

**Motivo:** Se o Root Directory for `rotina-app`, o Output Directory deve ser relativo a ele. O Next.js automaticamente cria `.next` dentro do diretório do app.

#### Install Command
```
pnpm install
```

#### Development Command
Deixar como padrão do Next.js (ou vazio)

---

### 3. Environment Variables (já estão corretas ✅)

- `NEXT_PUBLIC_SUPABASE_URL` = `https://mgcoyeohqelystqmytah.supabase.co`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- `SUPABASE_SERVICE_ROLE_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

## Passos para Corrigir

1. Acesse o projeto no Vercel Dashboard
2. Vá em **Settings** > **General**
3. Na seção **Root Directory**:
   - Altere de `rotina-app/apps/web` para `rotina-app`
   - Marque "Include files outside the root directory in the Build Step" como **Enabled**
4. Na seção **Framework Settings**:
   - **Output Directory**: Deixe VAZIO ou altere para `.next`
   - Certifique-se de que o **Build Command** está completo:
     ```
     pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build
     ```
5. Clique em **Save**
6. Faça um novo deploy

---

## Por que essas configurações?

- **Root Directory = `rotina-app`**: Permite que o Vercel acesse tanto `apps/web` quanto `packages/shared` e `packages/ui`
- **Output Directory vazio ou `.next`**: O Next.js detecta automaticamente onde está o app e cria o `.next` no lugar certo
- **Build Command completo**: Constrói os packages compartilhados antes do app web

