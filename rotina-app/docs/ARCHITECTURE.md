# ARCHITECTURE.md - Arquitetura Técnica

## Visão Geral

Rotina App é um monorepo multi-plataforma construído com:
- **Web**: Next.js 14 (App Router)
- **Mobile**: React Native Expo
- **Backend**: Supabase (PostgreSQL + Auth + Storage)
- **Deploy**: Vercel (web) + EAS Build (mobile)

---

## Estrutura do Monorepo

```
rotina-app/
├── apps/
│   ├── web/              # Next.js app (rotina.temvenda.com.br)
│   └── mobile/           # React Native Expo app
├── packages/
│   ├── shared/           # Tipos, schemas, utils compartilhados
│   └── ui/               # Componentes UI compartilhados
├── supabase/
│   ├── migrations/       # SQL migrations
│   ├── seed.sql          # Dados de seed
│   └── functions/        # Edge Functions (futuro)
└── docs/                 # Documentação
```

---

## Arquitetura Web App

### Rotas

```
/app/*          # Área do usuário (membro)
  /app/today           # Plano do dia atual
  /app/plan            # Plano completo (14 dias)
  /app/dashboard       # Dashboard com aderência
  /app/checkin         # Check-in diário
  /app/export          # Exportar dados

/admin/*       # Área admin/coach
  /admin/members       # Lista de membros
  /admin/members/[id]  # Detalhes do membro
  /admin/programs      # Programas
  /admin/templates     # Editor de templates
  /admin/rulesets      # Configuração de regras
```

### Middleware

O middleware (`src/middleware.ts`) protege rotas:
- `/admin/*`: Requer autenticação + role OWNER/COACH
- `/app/*`: Requer autenticação
- Redireciona usuários não autenticados para `/login`

### Autenticação

- **Provider**: Supabase Auth
- **Método**: Magic Link (OTP)
- **Sessão**: Cookies gerenciados por `@supabase/ssr`

### RBAC (Role-Based Access Control)

Roles definidas em `org_members`:
- **OWNER**: Acesso total à organização
- **COACH**: Acesso a membros do seu programa
- **MEMBER**: Acesso apenas aos próprios dados

---

## Arquitetura Mobile App

### Navegação

```
/(auth)/
  login.tsx

/(tabs)/
  today.tsx
  plan.tsx
  dashboard.tsx
  checkin.tsx
```

### Autenticação

- Mesmo sistema do web (Supabase Auth)
- Deep linking para magic links
- Sessão persistida localmente

---

## Arquitetura de Dados

### Schema Principal

```
profiles
  └── org_members (roles)
      └── orgs
          └── programs
              ├── enrollments (user_id → program_id)
              ├── rulesets
              └── plan_templates
                  └── daily_meals (gerado por usuário/dia)
                      └── daily_checkins
                          └── rule_events (auditoria)
```

### RLS (Row Level Security)

Todas as tabelas têm RLS habilitado:

1. **Membros**: Acessam apenas seus próprios dados
2. **Coaches**: Acessam dados de membros do seu programa
3. **Owners**: Acessam todos os dados da organização

### Funções Database

- `calculate_adherence(user_id, date)`: Calcula aderência
- `generate_daily_meals(user_id, date)`: Gera refeições do dia
- `check_sweet_permission(user_id, date, meal_type)`: Verifica permissão de doce
- `get_week_index(user_id, date)`: Calcula semana do programa

---

## Fluxos Principais

### 1. Geração de Daily Meals

```
Usuário abre /app/today
  → Server Component verifica se daily_meals existem
  → Se não existem, chama generate_daily_meals()
  → Função busca enrollment → program_id
  → Calcula week_index baseado em start_date
  → Busca plan_templates para week_index + day_of_week
  → Cria daily_meals para o usuário
```

### 2. Check-in Diário

```
Usuário preenche formulário
  → Client Component envia dados
  → API Route valida com Zod schema
  → Insere/atualiza daily_checkins
  → Retorna sucesso
```

### 3. Regra de Doce

```
Usuário tenta marcar refeição com doce
  → Client Component chama API
  → API chama check_sweet_permission()
  → Função verifica:
    - Período rígido? → BLOQUEADO
    - Modo HARD_BLOCK? → BLOQUEADO
    - Modo EXCEPTION_WITH_COST? → Verifica limite semanal
  → Registra em rule_events
  → Retorna permissão
```

### 4. Exportação CSV

```
Usuário clica em "Exportar"
  → Client Component faz GET /api/export/plan
  → API Route busca dados
  → Gera CSV com headers corretos
  → Retorna arquivo para download
```

---

## Segurança

### 1. Autenticação
- Magic Link via Supabase Auth
- Tokens JWT gerenciados automaticamente
- Refresh tokens automáticos

### 2. Autorização
- RLS no banco de dados
- Middleware no Next.js
- Validação server-side de todas as operações

### 3. Validação
- Zod schemas para todas as entradas
- Validação no cliente e servidor
- Sanitização de dados

### 4. CORS
- Configurado no Supabase
- Apenas domínios permitidos

---

## Performance

### 1. Web
- Server Components (Next.js 14)
- Cache de queries (React Query)
- Static generation onde possível
- Edge Network (Vercel)

### 2. Mobile
- Cache local (React Query)
- Lazy loading de telas
- Otimização de imagens

### 3. Database
- Índices em colunas frequentes
- Queries otimizadas
- RLS policies eficientes

---

## Escalabilidade

### 1. Horizontal Scaling
- Vercel escala automaticamente
- Supabase escala automaticamente
- Stateless architecture

### 2. Database
- Connection pooling (Supabase)
- Read replicas (futuro)
- Caching layer (futuro)

### 3. Mobile
- EAS Build distribui builds
- OTA updates via Expo

---

## Monitoramento

### 1. Logs
- Vercel logs (web)
- Supabase logs (database)
- Console logs (mobile)

### 2. Analytics
- Vercel Analytics (web)
- Custom events (futuro)

### 3. Error Tracking
- Vercel error tracking
- Sentry (futuro)

---

## Tecnologias

### Frontend
- **Next.js 14**: Framework web
- **React Native**: Framework mobile
- **Expo**: Toolchain mobile
- **TailwindCSS**: Styling
- **TypeScript**: Type safety

### Backend
- **Supabase**: BaaS (PostgreSQL + Auth)
- **PostgreSQL**: Database
- **Row Level Security**: Segurança de dados

### Tools
- **pnpm**: Package manager
- **Turborepo**: Build system (futuro)
- **Zod**: Validation
- **React Query**: Data fetching

---

## Decisões Arquiteturais

### 1. Monorepo
**Decisão**: Usar monorepo com pnpm workspaces  
**Razão**: Compartilhar código entre web e mobile, versionamento único

### 2. Supabase
**Decisão**: Usar Supabase como BaaS  
**Razão**: RLS nativo, Auth integrado, rápido para MVP

### 3. Next.js App Router
**Decisão**: Usar App Router (não Pages Router)  
**Razão**: Server Components, melhor performance, futuro do Next.js

### 4. Magic Link Auth
**Decisão**: Usar Magic Link (não senha)  
**Razão**: Melhor UX, mais seguro, sem gerenciamento de senhas

### 5. RLS no Database
**Decisão**: RLS no Supabase (não no código)  
**Razão**: Segurança em camada de dados, impossível bypassar

---

## Próximas Melhorias

1. **Edge Functions**: Para lógica server-side complexa
2. **Real-time**: Supabase Realtime para updates em tempo real
3. **Storage**: Supabase Storage para imagens de perfil
4. **Caching**: Redis para cache de queries frequentes
5. **CDN**: Para assets estáticos
6. **Analytics**: Event tracking completo
7. **Push Notifications**: Para lembretes de check-in

---

## Referências

- [Next.js Docs](https://nextjs.org/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Expo Docs](https://docs.expo.dev)
- [React Query Docs](https://tanstack.com/query/latest)







