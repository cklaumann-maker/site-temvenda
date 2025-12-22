# 🚀 Executar Migrations no Supabase Produção

## 📋 Método: SQL Editor do Supabase Dashboard

### Passo 1: Acessar SQL Editor

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. No menu lateral, clique em **SQL Editor**
3. Clique em **New Query**

---

## 📝 Ordem de Execução (CRÍTICA)

Execute os comandos **na ordem abaixo**, um arquivo por vez.

---

### Migration 1: Schema Inicial

**Arquivo**: `supabase/migrations/20240101000001_initial_schema.sql`

**Copie e cole TODO o conteúdo** do arquivo no SQL Editor e execute:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable RLS
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret';

-- Profiles table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organizations table
CREATE TABLE IF NOT EXISTS public.orgs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organization members (roles: OWNER, COACH, MEMBER)
CREATE TABLE IF NOT EXISTS public.org_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  org_id UUID NOT NULL REFERENCES public.orgs(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('OWNER', 'COACH', 'MEMBER')),
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(org_id, user_id)
);

-- Programs table
CREATE TABLE IF NOT EXISTS public.programs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  org_id UUID NOT NULL REFERENCES public.orgs(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enrollments table
CREATE TABLE IF NOT EXISTS public.enrollments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  program_id UUID NOT NULL REFERENCES public.programs(id) ON DELETE CASCADE,
  start_date DATE NOT NULL DEFAULT CURRENT_DATE,
  end_date DATE,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, program_id, active) WHERE active = true
);

-- Rulesets table
CREATE TABLE IF NOT EXISTS public.rulesets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  program_id UUID NOT NULL REFERENCES public.programs(id) ON DELETE CASCADE,
  weekday_sweets_mode TEXT NOT NULL DEFAULT 'HARD_BLOCK' CHECK (weekday_sweets_mode IN ('HARD_BLOCK', 'EXCEPTION_WITH_COST', 'ALLOW')),
  hard_block_days INTEGER NOT NULL DEFAULT 7 CHECK (hard_block_days >= 0),
  weekly_exception_limit INTEGER NOT NULL DEFAULT 2 CHECK (weekly_exception_limit >= 0),
  pizza_limit INTEGER CHECK (pizza_limit >= 0),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(program_id)
);

-- Plan templates table
CREATE TABLE IF NOT EXISTS public.plan_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  program_id UUID NOT NULL REFERENCES public.programs(id) ON DELETE CASCADE,
  week_index INTEGER NOT NULL CHECK (week_index >= 1),
  day_of_week INTEGER NOT NULL CHECK (day_of_week >= 1 AND day_of_week <= 7),
  meal_type TEXT NOT NULL,
  opt1 TEXT,
  opt2 TEXT,
  opt3 TEXT,
  avoid TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(program_id, week_index, day_of_week, meal_type)
);

-- Daily meals table (generated per user per day)
CREATE TABLE IF NOT EXISTS public.daily_meals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  meal_type TEXT NOT NULL,
  opt1 TEXT,
  opt2 TEXT,
  opt3 TEXT,
  avoid TEXT,
  option_selected TEXT CHECK (option_selected IN ('opt1', 'opt2', 'opt3')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date, meal_type)
);

-- Daily checkins table
CREATE TABLE IF NOT EXISTS public.daily_checkins (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  weight_kg DECIMAL(5,2) CHECK (weight_kg > 0 AND weight_kg < 500),
  workout_done BOOLEAN NOT NULL DEFAULT false,
  cardio_min INTEGER NOT NULL DEFAULT 0 CHECK (cardio_min >= 0 AND cardio_min <= 300),
  functional BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);

-- Rule events table (audit trail)
CREATE TABLE IF NOT EXISTS public.rule_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  event_type TEXT NOT NULL CHECK (event_type IN ('SWEET_BLOCKED', 'SWEET_EXCEPTION_USED', 'PIZZA_CONSUMED', 'PIZZA_LIMIT_EXCEEDED')),
  date DATE NOT NULL,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_org_members_org_id ON public.org_members(org_id);
CREATE INDEX IF NOT EXISTS idx_org_members_user_id ON public.org_members(user_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_user_id ON public.enrollments(user_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_program_id ON public.enrollments(program_id);
CREATE INDEX IF NOT EXISTS idx_daily_meals_user_date ON public.daily_meals(user_id, date);
CREATE INDEX IF NOT EXISTS idx_daily_checkins_user_date ON public.daily_checkins(user_id, date);
CREATE INDEX IF NOT EXISTS idx_rule_events_user_date ON public.rule_events(user_id, date);
CREATE INDEX IF NOT EXISTS idx_plan_templates_program_week ON public.plan_templates(program_id, week_index);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orgs_updated_at BEFORE UPDATE ON public.orgs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_org_members_updated_at BEFORE UPDATE ON public.org_members
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_programs_updated_at BEFORE UPDATE ON public.programs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_enrollments_updated_at BEFORE UPDATE ON public.enrollments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rulesets_updated_at BEFORE UPDATE ON public.rulesets
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plan_templates_updated_at BEFORE UPDATE ON public.plan_templates
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_daily_meals_updated_at BEFORE UPDATE ON public.daily_meals
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_daily_checkins_updated_at BEFORE UPDATE ON public.daily_checkins
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

**✅ Verificar**: Deve criar 10 tabelas. Vá em **Table Editor** e confira.

---

### Migration 2: RLS Policies

**Arquivo**: `supabase/migrations/20240101000002_rls_policies.sql`

**Copie e cole TODO o conteúdo** do arquivo no SQL Editor e execute.

**⚠️ IMPORTANTE**: Este arquivo é muito grande. Copie o arquivo completo:
`supabase/migrations/20240101000002_rls_policies.sql`

**✅ Verificar**: Execute esta query para verificar policies:

```sql
SELECT COUNT(*) as total_policies FROM pg_policies WHERE schemaname = 'public';
```

Deve retornar várias policies (cada tabela tem múltiplas).

---

### Migration 3: Functions

**Arquivo**: `supabase/migrations/20240101000003_functions.sql`

**Copie e cole TODO o conteúdo** do arquivo no SQL Editor e execute.

**⚠️ IMPORTANTE**: Este arquivo também é grande. Copie o arquivo completo:
`supabase/migrations/20240101000003_functions.sql`

**✅ Verificar**: Execute esta query para verificar functions:

```sql
SELECT routine_name FROM information_schema.routines 
WHERE routine_schema = 'public' AND routine_type = 'FUNCTION' 
ORDER BY routine_name;
```

Deve retornar:
- calculate_adherence
- check_sweet_permission
- generate_daily_meals
- get_week_index
- is_owner_or_coach
- can_access_member

---

### Seed (Opcional): Dados de Demonstração

**Arquivo**: `supabase/seed.sql`

**Copie e cole TODO o conteúdo** do arquivo no SQL Editor e execute.

**O que faz**: Cria organização demo, programa demo e templates de semana 1 e 2.

---

## 🔍 Verificações Finais

Execute estas queries para verificar se tudo está OK:

### 1. Verificar Tabelas

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

**Esperado**: 10 tabelas listadas

### 2. Verificar RLS Habilitado

```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

**Esperado**: Todas as tabelas com `rowsecurity = true`

### 3. Verificar Policies

```sql
SELECT tablename, COUNT(*) as policy_count
FROM pg_policies 
WHERE schemaname = 'public'
GROUP BY tablename
ORDER BY tablename;
```

**Esperado**: Várias policies por tabela

### 4. Verificar Functions

```sql
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND routine_type = 'FUNCTION'
ORDER BY routine_name;
```

**Esperado**: 6 funções listadas

---

## 📋 Checklist de Execução

- [ ] Migration 1 executada (Schema inicial)
- [ ] Migration 2 executada (RLS Policies)
- [ ] Migration 3 executada (Functions)
- [ ] Seed executado (opcional)
- [ ] 10 tabelas criadas
- [ ] RLS habilitado em todas as tabelas
- [ ] Policies criadas
- [ ] Functions criadas

---

## 🐛 Troubleshooting

### Erro: "relation already exists"
- **Causa**: Tabela já existe
- **Solução**: Use `DROP TABLE IF EXISTS` antes ou ignore (se já está criada)

### Erro: "function already exists"
- **Causa**: Function já existe
- **Solução**: O `CREATE OR REPLACE` deve resolver, mas se persistir, ignore

### Erro: "permission denied"
- **Causa**: Sem permissões
- **Solução**: Verifique se está usando Service Role Key ou tem permissões de admin

### Erro: "syntax error"
- **Causa**: SQL mal formatado
- **Solução**: Copie o arquivo completo, não apenas parte

---

## 🎯 Resumo Rápido

1. **Acesse**: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah/sql
2. **Execute Migration 1**: Copie `20240101000001_initial_schema.sql` completo
3. **Execute Migration 2**: Copie `20240101000002_rls_policies.sql` completo
4. **Execute Migration 3**: Copie `20240101000003_functions.sql` completo
5. **Execute Seed** (opcional): Copie `seed.sql` completo
6. **Verifique**: Use as queries de verificação acima

---

## ✅ Próximo Passo

Após executar as migrations:

1. Configure URLs permitidas no Auth (Settings > Authentication > URL Configuration)
2. Adicione: `http://localhost:3001`
3. Teste o app: `pnpm dev`

