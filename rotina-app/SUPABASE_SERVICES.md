# Serviços do Supabase Utilizados

## 📋 Resumo

O projeto Rotina App utiliza os seguintes serviços do Supabase:

1. ✅ **Authentication (Auth)** - Autenticação de usuários
2. ✅ **Database (PostgreSQL)** - Banco de dados relacional
3. ✅ **Row Level Security (RLS)** - Segurança em nível de linha
4. ✅ **Database Functions (RPC)** - Funções server-side
5. ❌ **Storage** - Não utilizado (futuro: avatares)
6. ❌ **Edge Functions** - Não utilizado (futuro)
7. ❌ **Realtime** - Não utilizado (futuro: updates em tempo real)

---

## 1. Authentication (Auth) ✅

### Uso Atual

**Serviço**: Supabase Auth  
**Método**: Magic Link (OTP via email)

### Implementação

#### Web App
```typescript
// Login com Magic Link
supabase.auth.signInWithOtp({
  email,
  options: {
    emailRedirectTo: `${window.location.origin}/app/today`,
  },
});

// Verificar usuário autenticado
const { data: { user } } = await supabase.auth.getUser();
```

#### Mobile App
```typescript
// Login com Magic Link
supabase.auth.signInWithOtp({ email });
```

### Arquivos que Utilizam
- `apps/web/src/app/login/page.tsx`
- `apps/web/src/lib/auth.ts`
- `apps/web/src/middleware.ts`
- `apps/mobile/app/(auth)/login.tsx`

### Funcionalidades
- ✅ Login com Magic Link
- ✅ Sessão persistente (cookies SSR)
- ✅ Verificação de usuário autenticado
- ✅ Logout (implícito via limpeza de sessão)

### Configuração Necessária
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- URLs permitidas no Supabase Dashboard (Auth > URL Configuration)

---

## 2. Database (PostgreSQL) ✅

### Uso Atual

**Serviço**: Supabase Database (PostgreSQL)  
**Tabelas**: 10 tabelas principais

### Schema Implementado

1. **profiles** - Perfis de usuário (estende auth.users)
2. **orgs** - Organizações
3. **org_members** - Membros de organizações (roles)
4. **programs** - Programas de disciplina
5. **enrollments** - Inscrições de usuários
6. **rulesets** - Regras de disciplina
7. **plan_templates** - Templates de plano alimentar
8. **daily_meals** - Refeições diárias (geradas)
9. **daily_checkins** - Check-ins diários
10. **rule_events** - Eventos de regras (auditoria)

### Operações Utilizadas

#### SELECT (Leitura)
```typescript
// Buscar dados
const { data } = await supabase
  .from('daily_meals')
  .select('*')
  .eq('user_id', user.id)
  .order('date');
```

#### INSERT (Criação)
```typescript
// Criar registro
await supabase
  .from('daily_checkins')
  .insert({
    user_id: user.id,
    date: today,
    workout_done: true,
  });
```

#### UPDATE (Atualização)
```typescript
// Atualizar registro
await supabase
  .from('daily_meals')
  .update({ option_selected: 'opt1' })
  .eq('id', mealId);
```

#### UPSERT (Criar ou Atualizar)
```typescript
// Criar ou atualizar
await supabase
  .from('daily_checkins')
  .upsert({
    user_id: user.id,
    date: today,
    weight_kg: 75.2,
  }, {
    onConflict: 'user_id,date',
  });
```

### Arquivos que Utilizam
- `apps/web/src/app/app/today/page.tsx`
- `apps/web/src/app/app/dashboard/page.tsx`
- `apps/web/src/app/app/checkin/page.tsx`
- `apps/web/src/app/admin/members/page.tsx`
- `apps/web/src/app/api/export/*/route.ts`

### Migrations
- `supabase/migrations/20240101000001_initial_schema.sql`
- `supabase/migrations/20240101000002_rls_policies.sql`
- `supabase/migrations/20240101000003_functions.sql`

---

## 3. Row Level Security (RLS) ✅

### Uso Atual

**Serviço**: Supabase RLS  
**Status**: Habilitado em todas as tabelas

### Políticas Implementadas

#### Para Membros (MEMBER)
- ✅ Podem ver apenas seus próprios dados
- ✅ Podem atualizar apenas seus próprios dados
- ✅ Não podem ver dados de outros membros

#### Para Coaches (COACH)
- ✅ Podem ver membros do seu programa
- ✅ Podem ver dados de membros (daily_meals, checkins, etc.)
- ✅ Não podem ver membros de outros programas

#### Para Owners (OWNER)
- ✅ Podem ver todos os membros da organização
- ✅ Podem gerenciar programas e templates
- ✅ Acesso completo à organização

### Funções Helper

```sql
-- Verificar se é owner ou coach
CREATE FUNCTION public.is_owner_or_coach(...)

-- Verificar se pode acessar dados de membro
CREATE FUNCTION public.can_access_member(...)
```

### Arquivos de Configuração
- `supabase/migrations/20240101000002_rls_policies.sql`

### Segurança
- ✅ RLS habilitado em todas as 10 tabelas
- ✅ Policies testadas e validadas
- ✅ Isolamento multi-tenant garantido

---

## 4. Database Functions (RPC) ✅

### Uso Atual

**Serviço**: Supabase Database Functions (PostgreSQL Functions)  
**Funções**: 3 funções server-side

### Funções Implementadas

#### 1. `calculate_adherence(user_id, date)`
**Descrição**: Calcula aderência do usuário em uma data específica

**Uso**:
```typescript
const { data: adherence } = await supabase.rpc('calculate_adherence', {
  p_user_id: user.id,
  p_date: today,
});
```

**Retorno**: `DECIMAL` (0-100)

#### 2. `generate_daily_meals(user_id, date)`
**Descrição**: Gera refeições do dia baseado em templates e enrollment

**Uso**:
```typescript
const { data } = await supabase.rpc('generate_daily_meals', {
  p_user_id: user.id,
  p_date: today,
});
```

**Retorno**: `INTEGER` (número de refeições geradas)

#### 3. `check_sweet_permission(user_id, date, meal_type)`
**Descrição**: Verifica se usuário pode consumir doce (regras de negócio)

**Uso**:
```typescript
const { data: permission } = await supabase.rpc('check_sweet_permission', {
  p_user_id: user.id,
  p_date: today,
  p_meal_type: 'doce',
});
```

**Retorno**: `JSONB` com `{ allowed: boolean, message: string }`

### Arquivos de Configuração
- `supabase/migrations/20240101000003_functions.sql`

### Arquivos que Utilizam
- `apps/web/src/lib/supabase/functions.ts`
- `apps/web/src/app/app/dashboard/page.tsx`
- `apps/web/src/app/api/export/adherence/route.ts`

---

## 5. Storage ❌ (Não Utilizado)

### Status
**Não implementado no MVP**

### Uso Futuro Planejado
- Avatares de usuário (`profiles.avatar_url`)
- Imagens de perfil
- Upload de fotos de progresso

### Como Implementar (Futuro)
```typescript
// Upload de avatar
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${user.id}/avatar.jpg`, file);

// Download de avatar
const { data } = await supabase.storage
  .from('avatars')
  .download(`${user.id}/avatar.jpg`);
```

---

## 6. Edge Functions ❌ (Não Utilizado)

### Status
**Não implementado no MVP**

### Uso Futuro Planejado
- Processamento de exportações complexas
- Webhooks externos
- Processamento assíncrono

### Como Implementar (Futuro)
```typescript
// Chamar Edge Function
const { data, error } = await supabase.functions.invoke('export-data', {
  body: { userId, dateRange },
});
```

---

## 7. Realtime ❌ (Não Utilizado)

### Status
**Não implementado no MVP**

### Uso Futuro Planejado
- Updates em tempo real de aderência
- Notificações de coach para membro
- Sincronização multi-dispositivo

### Como Implementar (Futuro)
```typescript
// Escutar mudanças em daily_meals
const channel = supabase
  .channel('daily-meals')
  .on('postgres_changes', {
    event: 'UPDATE',
    schema: 'public',
    table: 'daily_meals',
    filter: `user_id=eq.${user.id}`,
  }, (payload) => {
    console.log('Meal updated:', payload);
  })
  .subscribe();
```

---

## 📊 Resumo de Uso

| Serviço | Status | Uso Atual | Uso Futuro |
|---------|--------|-----------|------------|
| **Auth** | ✅ | Magic Link, Sessão | - |
| **Database** | ✅ | 10 tabelas, CRUD completo | - |
| **RLS** | ✅ | Todas as tabelas protegidas | - |
| **RPC Functions** | ✅ | 3 funções server-side | Mais funções |
| **Storage** | ❌ | - | Avatares, fotos |
| **Edge Functions** | ❌ | - | Processamento assíncrono |
| **Realtime** | ❌ | - | Updates em tempo real |

---

## 🔧 Configuração Necessária

### Variáveis de Ambiente

```env
# Obrigatórias
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key

# Opcional (para operações admin)
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key
```

### Configurações no Supabase Dashboard

1. **Auth > URL Configuration**
   - Adicionar: `http://localhost:3001`
   - Adicionar: `https://rotina.temvenda.com.br`
   - Adicionar: `rotina://` (mobile)

2. **Database > Migrations**
   - Executar migrations em ordem
   - Verificar RLS policies

3. **Database > Functions**
   - Verificar funções criadas
   - Testar funções manualmente

---

## 📈 Custos Estimados (Supabase)

### Plano Free
- ✅ **Auth**: 50.000 MAU (Monthly Active Users)
- ✅ **Database**: 500 MB storage, 2 GB bandwidth
- ✅ **RLS**: Incluído
- ✅ **RPC Functions**: Incluído

### Plano Pro (se necessário)
- **Auth**: 100.000 MAU
- **Database**: 8 GB storage, 50 GB bandwidth
- **Storage**: 100 GB
- **Edge Functions**: 2M invocations/mês

**Nota**: Para MVP, o plano Free deve ser suficiente.

---

## 🔒 Segurança

### Chaves Utilizadas

1. **Anon Key** (Pública)
   - Usada no cliente (browser/mobile)
   - Protegida por RLS
   - Não permite operações admin

2. **Service Role Key** (Privada)
   - Usada apenas server-side
   - Bypassa RLS (cuidado!)
   - Não expor no cliente

### Boas Práticas Implementadas

- ✅ RLS em todas as tabelas
- ✅ Service Role Key apenas server-side
- ✅ Validação server-side de todas as operações
- ✅ Policies testadas e validadas

---

## 📚 Documentação de Referência

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Supabase Database Docs](https://supabase.com/docs/guides/database)
- [Supabase RLS Docs](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase Functions Docs](https://supabase.com/docs/guides/database/functions)







