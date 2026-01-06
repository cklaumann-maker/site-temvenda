# 🗄️ Comandos Supabase - Ordem de Execução

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ Supabase CLI instalado
- ✅ Projeto criado no Supabase
- ✅ Credenciais configuradas no `.env.local`

### Instalar Supabase CLI (se necessário)

```bash
# macOS
brew install supabase/tap/supabase

# ou via npm
npm install -g supabase
```

---

## 🚀 Ordem de Execução Completa

### 1. Verificar Instalação do Supabase CLI

```bash
supabase --version
```

**Esperado**: Versão do Supabase CLI (ex: `1.x.x`)

---

### 2. Navegar para Diretório de Migrations

```bash
cd rotina-app/supabase
```

---

### 3. Linkar Projeto Local ao Remoto

```bash
supabase link --project-ref mgcoyeohqelystqmytah
```

**O que faz**: Conecta seu projeto local ao projeto remoto no Supabase

**Saída esperada**:
```
> Loading project...
> Linked to project mgcoyeohqelystqmytah
```

**Se pedir credenciais**:
- Você pode precisar fazer login: `supabase login`
- Ou usar o Service Role Key se solicitado

---

### 4. Verificar Status do Projeto

```bash
supabase status
```

**O que faz**: Mostra informações sobre o projeto linkado

**Saída esperada**: Informações sobre o projeto remoto

---

### 5. Executar Migrations (ORDEM CRÍTICA)

Execute as migrations **na ordem correta**:

#### 5.1. Schema Inicial

```bash
supabase db push
```

**OU** execute manualmente cada migration:

```bash
# Migration 1: Schema inicial
supabase db execute --file migrations/20240101000001_initial_schema.sql

# Migration 2: RLS Policies
supabase db execute --file migrations/20240101000002_rls_policies.sql

# Migration 3: Functions
supabase db execute --file migrations/20240101000003_functions.sql
```

**O que faz**: Cria todas as tabelas, índices, triggers e funções

**Verificar**: Deve criar 10 tabelas:
- profiles
- orgs
- org_members
- programs
- enrollments
- rulesets
- plan_templates
- daily_meals
- daily_checkins
- rule_events

---

### 6. Executar Seed (Dados de Demonstração) - OPCIONAL

```bash
supabase db execute --file seed.sql
```

**O que faz**: Insere dados de demonstração (org, programa, templates)

**Nota**: Opcional, mas útil para testar

---

### 7. Verificar Migrations Aplicadas

```bash
supabase migration list
```

**O que faz**: Lista todas as migrations aplicadas

**Esperado**: Ver as 3 migrations listadas

---

### 8. Verificar Tabelas Criadas

No Supabase Dashboard:
1. Vá em **Table Editor**
2. Deve ver as 10 tabelas criadas

Ou via SQL:

```bash
supabase db execute --query "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
```

---

### 9. Verificar RLS Policies

```bash
supabase db execute --query "SELECT tablename, policyname FROM pg_policies WHERE schemaname = 'public' ORDER BY tablename, policyname;"
```

**Esperado**: Ver várias policies para cada tabela

---

### 10. Verificar Functions Criadas

```bash
supabase db execute --query "SELECT routine_name FROM information_schema.routines WHERE routine_schema = 'public' AND routine_type = 'FUNCTION' ORDER BY routine_name;"
```

**Esperado**: Ver as funções:
- calculate_adherence
- generate_daily_meals
- check_sweet_permission
- get_week_index
- is_owner_or_coach
- can_access_member

---

## 📝 Comandos Completos em Sequência

### Opção A: Automático (Recomendado)

```bash
# 1. Ir para diretório
cd rotina-app/supabase

# 2. Linkar projeto
supabase link --project-ref mgcoyeohqelystqmytah

# 3. Executar todas as migrations
supabase db push

# 4. Executar seed (opcional)
supabase db execute --file seed.sql

# 5. Verificar status
supabase status
```

### Opção B: Manual (Mais Controle)

```bash
# 1. Ir para diretório
cd rotina-app/supabase

# 2. Linkar projeto
supabase link --project-ref mgcoyeohqelystqmytah

# 3. Executar migrations uma por uma
supabase db execute --file migrations/20240101000001_initial_schema.sql
supabase db execute --file migrations/20240101000002_rls_policies.sql
supabase db execute --file migrations/20240101000003_functions.sql

# 4. Executar seed (opcional)
supabase db execute --file seed.sql

# 5. Verificar
supabase migration list
```

---

## 🔍 Comandos de Verificação

### Verificar Conexão

```bash
supabase status
```

### Verificar Tabelas

```bash
supabase db execute --query "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
```

### Verificar RLS Habilitado

```bash
supabase db execute --query "SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';"
```

**Esperado**: Todas as tabelas com `rowsecurity = true`

### Verificar Policies

```bash
supabase db execute --query "SELECT COUNT(*) as total_policies FROM pg_policies WHERE schemaname = 'public';"
```

**Esperado**: Várias policies (cada tabela tem múltiplas)

### Testar Function

```bash
# Testar calculate_adherence (precisa de dados primeiro)
supabase db execute --query "SELECT public.calculate_adherence('00000000-0000-0000-0000-000000000000'::uuid, CURRENT_DATE);"
```

---

## 🐛 Troubleshooting

### Erro: "Project not found"

```bash
# Verificar se o project-ref está correto
supabase projects list

# Ou fazer login novamente
supabase login
```

### Erro: "Migration already applied"

```bash
# Verificar migrations aplicadas
supabase migration list

# Se necessário, marcar como não aplicada (cuidado!)
# supabase migration repair <migration-name> --status reverted
```

### Erro: "Permission denied"

```bash
# Verificar se está usando Service Role Key
# Ou fazer login
supabase login
```

### Erro: "Connection refused"

```bash
# Verificar se o projeto está ativo no Supabase Dashboard
# Verificar credenciais no .env.local
```

---

## 📊 Checklist Pós-Execução

Após executar os comandos, verifique:

- [ ] Migrations aplicadas (3 migrations)
- [ ] Tabelas criadas (10 tabelas)
- [ ] RLS habilitado em todas as tabelas
- [ ] Policies criadas (múltiplas por tabela)
- [ ] Functions criadas (6 funções)
- [ ] Seed executado (se aplicável)
- [ ] Pode fazer queries no Supabase Dashboard

---

## 🎯 Ordem Resumida (Copy-Paste)

```bash
# 1. Navegar
cd rotina-app/supabase

# 2. Linkar
supabase link --project-ref mgcoyeohqelystqmytah

# 3. Executar migrations
supabase db push

# 4. Seed (opcional)
supabase db execute --file seed.sql

# 5. Verificar
supabase status
supabase migration list
```

---

## 📚 Comandos Úteis Adicionais

### Ver Logs

```bash
supabase logs
```

### Reset Database (CUIDADO - apaga tudo!)

```bash
supabase db reset
```

### Criar Nova Migration

```bash
supabase migration new nome_da_migration
```

### Ver Diferenças

```bash
supabase db diff
```

### Backup

```bash
# No Supabase Dashboard: Settings > Database > Backups
# Ou via CLI (se disponível)
```

---

## ✅ Próximo Passo Após Configurar Supabase

Depois de executar os comandos acima:

1. ✅ Configurar URLs permitidas no Auth (Dashboard)
2. ✅ Build dos packages: `pnpm --filter shared build`
3. ✅ Testar app: `pnpm dev`

---

## 📞 Referências

- [Supabase CLI Docs](https://supabase.com/docs/reference/cli)
- [Supabase Migrations](https://supabase.com/docs/guides/cli/local-development#database-migrations)







