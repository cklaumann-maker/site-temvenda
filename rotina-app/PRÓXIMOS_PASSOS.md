# ✅ Próximos Passos - Configuração Completa

## 🎉 Credenciais Configuradas!

O arquivo `.env.local` foi criado com suas credenciais do Supabase.

---

## 📋 Checklist de Setup

### 1. ✅ Credenciais do Supabase
- [x] Project URL configurado
- [x] Anon Key configurado
- [x] Service Role Key configurado

### 2. ⏳ Executar Migrations do Banco de Dados

Agora você precisa executar as migrations SQL no Supabase:

#### Opção A: Via Supabase CLI (Recomendado)

```bash
cd rotina-app/supabase

# Linkar projeto local ao remoto
supabase link --project-ref mgcoyeohqelystqmytah

# Executar migrations
supabase db push
```

#### Opção B: Via Dashboard do Supabase

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Vá em **SQL Editor**
3. Execute cada migration em ordem:
   - `supabase/migrations/20240101000001_initial_schema.sql`
   - `supabase/migrations/20240101000002_rls_policies.sql`
   - `supabase/migrations/20240101000003_functions.sql`
4. Depois execute o seed (opcional): `supabase/seed.sql`

### 3. ⏳ Configurar URLs Permitidas (Auth)

1. No Supabase Dashboard, vá em **Settings > Authentication**
2. Role até **URL Configuration**
3. Adicione as seguintes URLs em **Site URL** e **Redirect URLs**:
   - `http://localhost:3001`
   - `http://localhost:3001/**`
   - `rotina://` (para mobile futuro)
   - `exp://` (para desenvolvimento mobile)

### 4. ⏳ Build dos Packages Compartilhados

```bash
cd rotina-app

# Build dos packages
pnpm --filter shared build
pnpm --filter ui build
```

### 5. ⏳ Instalar Dependências (se ainda não fez)

```bash
cd rotina-app
pnpm install
```

### 6. ⏳ Testar Conexão

```bash
# Iniciar desenvolvimento
pnpm dev

# Ou usar o script
./scripts/dev.sh
```

O app deve estar disponível em: **http://localhost:3001**

---

## 🧪 Testar se Está Funcionando

1. **Acesse**: http://localhost:3001/login
2. **Digite um email** e clique em "Enviar Magic Link"
3. **Verifique seu email** (pode estar na pasta spam)
4. **Clique no link** do email
5. **Deve redirecionar** para `/app/today`

Se funcionar, a conexão está OK! ✅

---

## 🐛 Problemas Comuns

### Erro: "Invalid API key"
- ✅ Verifique se o arquivo `.env.local` está correto
- ✅ Reinicie o servidor após mudar `.env.local`

### Erro: "RLS policy violation"
- ⚠️ Normal! Significa que precisa executar as migrations primeiro
- Execute as migrations (passo 2 acima)

### Erro: "Cannot find module '@rotina/shared'"
- Execute: `pnpm --filter shared build`
- Execute: `pnpm --filter ui build`

### Erro: "Failed to fetch" no login
- Verifique se configurou as URLs permitidas (passo 3)
- Verifique se o projeto está ativo no Supabase

---

## 📚 Documentação Útil

- [LOCAL_SETUP.md](./LOCAL_SETUP.md) - Guia completo de setup local
- [CONFIGURAR_SUPABASE.md](./CONFIGURAR_SUPABASE.md) - Configuração Supabase
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deploy para produção

---

## 🎯 Ordem Recomendada de Execução

1. ✅ Credenciais configuradas (FEITO)
2. ⏳ Executar migrations SQL
3. ⏳ Configurar URLs permitidas no Auth
4. ⏳ Build dos packages
5. ⏳ Instalar dependências
6. ⏳ Testar conexão

---

## 💡 Dica

Se tiver problemas, verifique os logs:
- **Console do navegador** (F12)
- **Terminal** onde está rodando `pnpm dev`
- **Supabase Dashboard > Logs**

Boa sorte! 🚀

