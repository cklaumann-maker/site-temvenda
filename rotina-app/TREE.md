# Estrutura do Repositório

```
rotina-app/
├── apps/
│   ├── mobile/                    # React Native Expo App
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   └── login.tsx      # Tela de login mobile
│   │   │   └── _layout.tsx        # Layout raiz
│   │   ├── lib/
│   │   │   └── supabase.ts        # Cliente Supabase mobile
│   │   ├── app.json               # Config Expo
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── web/                       # Next.js Web App
│       ├── src/
│       │   ├── app/
│       │   │   ├── app/           # Rotas /app/* (usuário)
│       │   │   │   ├── today/     # Tela "Hoje"
│       │   │   │   ├── plan/      # Plano completo
│       │   │   │   ├── dashboard/ # Dashboard
│       │   │   │   └── checkin/   # Check-in diário
│       │   │   ├── admin/         # Rotas /admin/* (coach/admin)
│       │   │   │   └── members/   # Lista de membros
│       │   │   ├── api/
│       │   │   │   └── export/    # Endpoints de exportação
│       │   │   ├── login/         # Login
│       │   │   ├── layout.tsx     # Layout raiz
│       │   │   └── globals.css    # Estilos globais
│       │   ├── lib/
│       │   │   ├── supabase/      # Clientes Supabase
│       │   │   └── auth.ts        # Helpers de autenticação
│       │   └── middleware.ts      # Middleware de proteção de rotas
│       ├── next.config.js
│       ├── tailwind.config.js
│       ├── tsconfig.json
│       └── package.json
│
├── packages/
│   ├── shared/                    # Package compartilhado
│   │   ├── src/
│   │   │   ├── types.ts           # Tipos TypeScript
│   │   │   ├── schemas.ts         # Schemas Zod
│   │   │   ├── constants.ts       # Constantes
│   │   │   ├── utils.ts           # Utilitários (CSV, datas, etc)
│   │   │   └── index.ts           # Exports
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── ui/                        # Componentes UI compartilhados
│       ├── src/
│       │   ├── Button.tsx
│       │   ├── Card.tsx
│       │   └── index.ts
│       ├── package.json
│       └── tsconfig.json
│
├── supabase/
│   ├── migrations/
│   │   ├── 20240101000001_initial_schema.sql    # Schema inicial
│   │   ├── 20240101000002_rls_policies.sql      # RLS policies
│   │   └── 20240101000003_functions.sql          # Funções database
│   └── seed.sql                   # Dados de seed
│
├── docs/
│   └── ARCHITECTURE.md            # Documentação de arquitetura
│
├── PRD.md                         # Product Requirements Document
├── WIREFRAMES.md                  # Wireframes de texto
├── RULES.md                       # Regras de negócio
├── DEPLOYMENT.md                  # Plano de deploy
├── VALIDATION.md                  # Validações pré-deploy
├── README.md                      # README principal
├── package.json                   # Root package.json
├── pnpm-workspace.yaml            # Config workspace
└── .gitignore
```

## Estatísticas

- **Total de arquivos principais**: ~60+
- **Linhas de código**: ~5000+
- **Migrations SQL**: 3
- **Rotas web**: 10+
- **Packages compartilhados**: 2
- **Documentação**: 6 arquivos MD

## Principais Entidades

1. **profiles** - Perfis de usuário
2. **orgs** - Organizações
3. **org_members** - Membros de organizações (roles)
4. **programs** - Programas
5. **enrollments** - Inscrições de usuários
6. **rulesets** - Regras de disciplina
7. **plan_templates** - Templates de plano alimentar
8. **daily_meals** - Refeições diárias (geradas)
9. **daily_checkins** - Check-ins diários
10. **rule_events** - Eventos de regras (auditoria)

## Rotas Principais

### Web App (/app/*)
- `/login` - Login
- `/app/today` - Plano do dia
- `/app/plan` - Plano completo
- `/app/dashboard` - Dashboard
- `/app/checkin` - Check-in

### Admin (/admin/*)
- `/admin/members` - Lista de membros
- `/admin/members/[id]` - Detalhes do membro
- `/admin/programs` - Programas
- `/admin/templates` - Templates
- `/admin/rulesets` - Regras

### API (/api/*)
- `/api/export/plan` - Exportar plano do usuário
- `/api/export/adherence` - Exportar aderência
- `/api/export/template` - Exportar template (admin)

