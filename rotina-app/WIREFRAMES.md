# WIREFRAMES - Rotina App

## Mapa de Rotas

### Web App (rotina.temvenda.com.br)
```
/app/*
  /login                    - Login com email
  /app/today               - Tela "Hoje" (plano do dia)
  /app/plan                - Plano completo (14 dias)
  /app/dashboard           - Dashboard com aderência
  /app/checkin             - Check-in diário
  /app/export              - Exportar dados

/admin/*
  /admin/login             - Login admin (mesmo auth, verifica role)
  /admin/orgs              - Lista de organizações (Owner apenas)
  /admin/programs          - Lista de programas
  /admin/programs/[id]     - Detalhes do programa
  /admin/members           - Lista de membros
  /admin/members/[id]      - Detalhe do membro (gráficos, eventos)
  /admin/templates         - Editor de templates de plano
  /admin/rulesets          - Configuração de regras
  /admin/export            - Exportar templates/relatórios
```

### Mobile App
```
/auth/login                - Login com email
/today                     - Tela "Hoje"
/plan                      - Plano completo
/dashboard                 - Dashboard
/checkin                   - Check-in
```

---

## WIREFRAMES - Mobile App

### Tela: Login (/auth/login)
```
┌─────────────────────────┐
│                         │
│    [Logo App]           │
│                         │
│  ┌───────────────────┐  │
│  │  Email            │  │
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │ Enviar Magic Link │  │
│  └───────────────────┘  │
│                         │
│  Verifique seu email    │
│  para continuar         │
│                         │
└─────────────────────────┘
```

### Tela: Hoje (/today)
```
┌─────────────────────────┐
│ ☰  Hoje    [Perfil]    │
├─────────────────────────┤
│                         │
│  Segunda, 15 Jan 2024   │
│                         │
│  ┌───────────────────┐  │
│  │ 📊 Aderência: 83%│  │
│  └───────────────────┘  │
│                         │
│  REFEIÇÕES DE HOJE      │
│                         │
│  ☐ Café da Manhã        │
│     Opção 1: Aveia...   │
│     Opção 2: Ovos...    │
│     Opção 3: Frutas...   │
│     Evitar: Pão...      │
│                         │
│  ☑ Lanche da Manhã      │
│     ✓ Selecionado: ... │
│                         │
│  ☐ Almoço               │
│     Opção 1: Salada...  │
│     ...                 │
│                         │
│  [Fazer Check-in]       │
│                         │
└─────────────────────────┘
```

### Tela: Plano (/plan)
```
┌─────────────────────────┐
│ ←  Meu Plano            │
├─────────────────────────┤
│                         │
│  Semana 1               │
│                         │
│  Segunda-feira          │
│  ┌───────────────────┐  │
│  │ Café: Opção 1     │  │
│  │ Almoço: Opção 2    │  │
│  │ ...                │  │
│  └───────────────────┘  │
│                         │
│  Terça-feira            │
│  ┌───────────────────┐  │
│  │ ...                │  │
│  └───────────────────┘  │
│                         │
│  [Exportar para CSV]    │
│                         │
└─────────────────────────┘
```

### Tela: Dashboard (/dashboard)
```
┌─────────────────────────┐
│ ←  Dashboard            │
├─────────────────────────┤
│                         │
│  ┌───────────────────┐  │
│  │ Aderência: 85%    │  │
│  │ ↑ 5% esta semana  │  │
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │ Peso: 75.2 kg     │  │
│  │ [Gráfico linha]   │  │
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │ Cardio: 120 min    │  │
│  │ esta semana        │  │
│  └───────────────────┘  │
│                         │
│  [Exportar Relatório]   │
│                         │
└─────────────────────────┘
```

### Tela: Check-in (/checkin)
```
┌─────────────────────────┐
│ ←  Check-in Diário      │
├─────────────────────────┤
│                         │
│  Data: 15/01/2024       │
│                         │
│  Peso (kg)              │
│  ┌───────────────────┐  │
│  │ 75.2              │  │
│  └───────────────────┘  │
│                         │
│  Exercício              │
│  ☐ Fiz exercício hoje   │
│                         │
│  Cardio (minutos)       │
│  ┌───────────────────┐  │
│  │ 30                │  │
│  └───────────────────┘  │
│                         │
│  Funcional              │
│  ☐ Fiz funcional hoje   │
│                         │
│  ┌───────────────────┐  │
│  │ Salvar Check-in   │  │
│  └───────────────────┘  │
│                         │
└─────────────────────────┘
```

---

## WIREFRAMES - Web App (/app/*)

### Tela: /app/today
```
┌─────────────────────────────────────────┐
│ ☰ Rotina    [Perfil]                    │
├─────────────────────────────────────────┤
│                                         │
│  Hoje - Segunda, 15 de Janeiro de 2024 │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Aderência Hoje: 83%               │ │
│  │ 5 de 6 refeições concluídas       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  REFEIÇÕES DE HOJE                      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ ☐ Café da Manhã                   │ │
│  │    Opção 1: Aveia com frutas      │ │
│  │    Opção 2: Ovos mexidos          │ │
│  │    Opção 3: Smoothie verde         │ │
│  │    ⚠️ Evitar: Pão branco, açúcar  │ │
│  │    [Marcar como feito]             │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ ☑ Lanche da Manhã                 │ │
│  │    ✓ Selecionado: Frutas          │ │
│  │    [Desmarcar]                     │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Fazer Check-in Diário]                │
│                                         │
└─────────────────────────────────────────┘
```

### Tela: /app/plan
```
┌─────────────────────────────────────────┐
│ ← Meu Plano                             │
├─────────────────────────────────────────┤
│                                         │
│  Semana 1 - Programa: Disciplina Total  │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Segunda-feira                     │ │
│  │ Café: Opção 1                     │ │
│  │ Lanche Manhã: Opção 2             │ │
│  │ Almoço: Opção 1                   │ │
│  │ Lanche Tarde: Opção 3             │ │
│  │ Jantar: Opção 2                   │ │
│  │ Ceia: Opção 1                     │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Exportar Próximos 14 Dias (CSV)]     │
│                                         │
└─────────────────────────────────────────┘
```

### Tela: /app/dashboard
```
┌─────────────────────────────────────────┐
│ ← Dashboard                             │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ Aderência    │  │ Peso Atual   │   │
│  │ 85%          │  │ 75.2 kg      │   │
│  │ ↑ 5%         │  │ ↓ 1.2 kg     │   │
│  └──────────────┘  └──────────────┘   │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Peso ao Longo do Tempo            │ │
│  │ [Gráfico de linha]                │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Aderência Semanal                 │ │
│  │ [Gráfico de barras]               │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Exportar Relatório de Aderência]     │
│                                         │
└─────────────────────────────────────────┘
```

---

## WIREFRAMES - Admin/Coach (/admin/*)

### Tela: /admin/members
```
┌─────────────────────────────────────────┐
│ Admin    [Sair]                          │
├─────────────────────────────────────────┤
│                                         │
│  Membros                                │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Buscar membro...                  │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ João Silva                        │ │
│  │ Aderência: 85% | Peso: 75.2 kg    │ │
│  │ [Ver Detalhes]                    │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Maria Santos                      │ │
│  │ Aderência: 62% ⚠️ | Peso: 68.5 kg │ │
│  │ [Ver Detalhes]                    │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Convidar Novo Membro]                │
│                                         │
└─────────────────────────────────────────┘
```

### Tela: /admin/members/[id]
```
┌─────────────────────────────────────────┐
│ ← João Silva                            │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ Aderência    │  │ Peso Atual   │   │
│  │ 85%          │  │ 75.2 kg      │   │
│  └──────────────┘  └──────────────┘   │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Progresso de Peso                 │ │
│  │ [Gráfico]                         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  EVENTOS DE REGRAS                      │
│  ┌───────────────────────────────────┐ │
│  │ 14/01 - Tentativa de doce (bloq)  │ │
│  │ 13/01 - Exceção usada (doce)      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Exportar Dados do Membro]            │
│                                         │
└─────────────────────────────────────────┘
```

### Tela: /admin/templates
```
┌─────────────────────────────────────────┐
│ ← Templates de Plano                     │
├─────────────────────────────────────────┤
│                                         │
│  Programa: Disciplina Total             │
│                                         │
│  Semana 1                               │
│  ┌───────────────────────────────────┐ │
│  │ Segunda-feira                     │ │
│  │ Café: [Editar]                    │ │
│  │   Opção 1: [Input]                │ │
│  │   Opção 2: [Input]                 │ │
│  │   Opção 3: [Input]                 │ │
│  │   Evitar: [Input]                  │ │
│  │ [Salvar]                           │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Exportar Template (CSV)]             │
│  [Salvar Semana 1]                     │
│                                         │
└─────────────────────────────────────────┘
```

### Tela: /admin/programs
```
┌─────────────────────────────────────────┐
│ ← Programas                             │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Disciplina Total                  │ │
│  │ Membros: 12 | Aderência média: 78%│ │
│  │ [Gerenciar]                       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Transformação Completa            │ │
│  │ Membros: 8 | Aderência média: 82% │ │
│  │ [Gerenciar]                       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Criar Novo Programa]                 │
│                                         │
└─────────────────────────────────────────┘
```

### Tela: /admin/rulesets
```
┌─────────────────────────────────────────┐
│ ← Regras de Disciplina                  │
├─────────────────────────────────────────┤
│                                         │
│  Programa: Disciplina Total             │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Período de Bloqueio Rígido        │ │
│  │ Dias: [7]                         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Doces em Dias Úteis               │ │
│  │ [ ] HARD_BLOCK                    │ │
│  │ [x] EXCEPTION_WITH_COST           │ │
│  │ [ ] ALLOW                         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Limite de Exceções Semanais       │ │
│  │ [2]                               │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Salvar Regras]                       │
│                                         │
└─────────────────────────────────────────┘
```

---

## Navegação Mobile

### Bottom Tab Bar
```
┌─────────────────────────────────────────┐
│                                         │
│              [Conteúdo]                 │
│                                         │
├─────────────────────────────────────────┤
│  Hoje  │  Plano  │  Dashboard  │ Perfil│
└─────────────────────────────────────────┘
```

### Menu Lateral (Drawer)
```
┌─────────────────────────┐
│ [Fechar]                │
├─────────────────────────┤
│                         │
│  João Silva             │
│  joao@email.com         │
│                         │
│  ───────────────────    │
│                         │
│  Hoje                   │
│  Meu Plano              │
│  Dashboard              │
│  Check-in               │
│  Exportar Dados         │
│                         │
│  ───────────────────    │
│                         │
│  Sair                   │
│                         │
└─────────────────────────┘
```

---

## Navegação Web (/app)

### Header
```
┌─────────────────────────────────────────┐
│ ☰ Rotina    [Hoje] [Plano] [Dashboard] │
│              [Check-in] [Perfil]        │
└─────────────────────────────────────────┘
```

### Navegação Admin (/admin)

### Sidebar
```
┌─────────────────────────┐
│ Admin                   │
├─────────────────────────┤
│                         │
│  Programas              │
│  Membros                │
│  Templates              │
│  Regras                 │
│  Exportar               │
│                         │
│  ───────────────────    │
│                         │
│  Sair                   │
│                         │
└─────────────────────────┘
```







