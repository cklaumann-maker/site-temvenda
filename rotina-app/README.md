# Rotina App - Sistema de Controle de Dieta e Calorias

Aplicação completa para controle de dieta, calorias e aderência ao plano alimentar.

## 🚀 Tecnologias

- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Supabase** - Backend (PostgreSQL + Auth + Storage)
- **Tailwind CSS** - Estilização
- **pnpm** - Gerenciador de pacotes (monorepo)

## 📁 Estrutura do Projeto

```
rotina-app/
├── apps/
│   ├── web/          # Aplicação Next.js
│   └── mobile/       # Aplicação React Native (Expo)
├── packages/
│   ├── shared/       # Código compartilhado
│   └── ui/           # Componentes UI compartilhados
├── supabase/
│   └── migrations/   # Migrations do banco de dados
└── scripts/          # Scripts de importação e utilitários
```

## 🛠️ Desenvolvimento Local

### Pré-requisitos

- Node.js 18+
- pnpm 8+
- Conta Supabase

### Instalação

```bash
# Instalar dependências
pnpm install

# Configurar variáveis de ambiente
cd apps/web
cp env.example .env.local
# Edite .env.local com suas credenciais do Supabase

# Iniciar servidor de desenvolvimento
pnpm dev
```

Acesse: http://localhost:3001

## 🗄️ Banco de Dados

### Executar Migrations

As migrations estão em `supabase/migrations/`. Execute na ordem:

1. `20240101000001_initial_schema.sql`
2. `20240101000002_rls_policies.sql`
3. `20240101000003_functions.sql`
4. `20240101000004_fix_generate_daily_meals.sql`
5. `20240101000005_add_calories.sql`
6. `20240101000006_create_user_profiles.sql`
7. `20240101000007_add_max_daily_calories.sql`
8. `20240101000008_update_existing_profiles_max_calories.sql`
9. `20240101000009_create_daily_calorie_summaries.sql`

Execute no SQL Editor do Supabase Dashboard.

## 🚀 Deploy

### Vercel (Recomendado)

1. Conecte o repositório no Vercel
2. Configure Root Directory: `apps/web`
3. Adicione variáveis de ambiente
4. Deploy automático!

Veja `DEPLOY_VERCEL.md` para instruções detalhadas.

### Servidor Próprio

Veja `DEPLOY_SERVIDOR_TEMVENDA.md` para instruções.

## 📚 Documentação

- `DEPLOY_VERCEL.md` - Deploy no Vercel
- `DEPLOY_SERVIDOR_TEMVENDA.md` - Deploy em servidor próprio
- `ARMAZENAMENTO_CALORIAS.md` - Sistema de armazenamento de calorias
- `IMPORTAR_CALORIAS_ATUALIZADO.md` - Importar plano com calorias

## 📝 Funcionalidades

- ✅ Controle de refeições diárias
- ✅ Seleção de opções do plano alimentar
- ✅ Entrada manual de calorias
- ✅ Cálculo de déficit/superávit calórico
- ✅ Check-in diário (peso, treino, calorias gastas)
- ✅ Dashboard com resumo mensal
- ✅ Perfil de usuário com cálculo de IMC
- ✅ Calendário de plano alimentar (90 dias)
- ✅ Gerenciamento de plano alimentar
- ✅ Armazenamento automático de resumos diários

## 🔐 Variáveis de Ambiente

```env
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key
```

## 📄 Licença

Privado - TemVenda
