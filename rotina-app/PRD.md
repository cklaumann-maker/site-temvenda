# PRD - Rotina App (Habit Discipline MVP)

## 1. Visão Geral

### 1.1 Escopo
MVP de aplicativo multi-tenant para disciplina de hábitos alimentares e exercícios, com suporte a organizações, programas, coaches e membros.

### 1.2 Objetivo
Permitir que organizações criem programas de disciplina onde coaches gerenciam membros, definem planos alimentares semanais e acompanham aderência através de check-ins diários.

### 1.3 Não-Objetivos (Out of Scope)
- Sistema de pagamentos
- Notificações push avançadas
- Chat/mensagens entre coach e membro
- Gamificação além de aderência básica
- Integração com wearables
- Sistema de recompensas/pontos complexo
- App desktop standalone
- Integração com redes sociais

## 2. Personas

### 2.1 Membro (MEMBER)
- **Perfil**: Pessoa que busca disciplina alimentar e de exercícios
- **Necessidades**: 
  - Ver plano do dia atual
  - Registrar refeições consumidas
  - Fazer check-in diário (peso, exercícios)
  - Visualizar progresso e aderência
- **Frustrações**: Processo complexo, falta de clareza nas regras

### 2.2 Coach (COACH)
- **Perfil**: Profissional que gerencia membros em um programa
- **Necessidades**:
  - Criar e editar planos alimentares (templates semanais)
  - Visualizar aderência dos membros
  - Identificar membros com baixa aderência
  - Exportar relatórios
- **Frustrações**: Falta de visibilidade, processos manuais

### 2.3 Owner (OWNER)
- **Perfil**: Administrador da organização
- **Necessidades**:
  - Criar organizações e programas
  - Gerenciar coaches e membros
  - Configurar regras de disciplina
  - Acesso a todos os dados da organização
- **Frustrações**: Controle limitado, falta de relatórios consolidados

## 3. User Stories

### 3.1 Autenticação
- **US-001**: Como usuário, quero fazer login com email e magic link para acessar o app
- **US-002**: Como usuário, quero fazer logout para garantir segurança
- **US-003**: Como membro, quero ver apenas meus próprios dados
- **US-004**: Como coach, quero ver dados dos membros do meu programa

### 3.2 Membro - Visualização
- **US-101**: Como membro, quero ver o plano do dia atual ao abrir o app
- **US-102**: Como membro, quero ver minhas refeições planejadas para hoje
- **US-103**: Como membro, quero ver meu dashboard com aderência e progresso
- **US-104**: Como membro, quero ver meu plano completo para os próximos 14 dias

### 3.3 Membro - Check-in
- **US-201**: Como membro, quero marcar refeições como consumidas
- **US-202**: Como membro, quero registrar meu peso diário
- **US-203**: Como membro, quero registrar se fiz exercício hoje
- **US-204**: Como membro, quero registrar minutos de cardio
- **US-205**: Como membro, quero registrar exercício funcional

### 3.4 Membro - Regras
- **US-301**: Como membro, quero ser bloqueado de consumir doces em dias úteis (primeiros X dias)
- **US-302**: Como membro, quero ver aviso quando tentar consumir item bloqueado
- **US-303**: Como membro, quero usar exceções limitadas após período inicial

### 3.5 Coach/Admin - Gestão
- **US-401**: Como coach, quero criar templates de plano alimentar (semana 1, semana 2, etc.)
- **US-402**: Como coach, quero editar templates de plano
- **US-403**: Como coach, quero convidar membros para o programa
- **US-404**: Como coach, quero ver lista de membros com aderência
- **US-405**: Como coach, quero ver detalhes de um membro (gráficos, eventos de regras)
- **US-406**: Como coach, quero criar organizações e programas
- **US-407**: Como coach, quero configurar regras de disciplina (hard_block_days, limites)

### 3.6 Exportação
- **US-501**: Como coach, quero exportar templates de plano para CSV/Excel
- **US-502**: Como membro, quero exportar meu plano de 14 dias para CSV/Excel
- **US-503**: Como membro, quero exportar relatório de aderência para CSV/Excel

## 4. Acceptance Criteria

### 4.1 Autenticação
- ✅ Login com email + magic link funciona
- ✅ Sessão persiste entre aberturas do app
- ✅ Logout limpa sessão completamente
- ✅ RLS impede acesso a dados de outros usuários

### 4.2 Geração de Dados
- ✅ Ao abrir "Hoje", `daily_meals` são gerados automaticamente se não existirem
- ✅ Geração baseada em `plan_templates` e `week_index` do enrollment
- ✅ Fallback se templates não existirem (mostra mensagem)

### 4.3 Check-in
- ✅ Marcar refeição como feita atualiza `daily_meals.option_selected`
- ✅ Check-in diário cria/atualiza `daily_checkins`
- ✅ Aderência calculada corretamente: `done_count / planned_meal_count`

### 4.4 Regras de Doce
- ✅ Primeiros `hard_block_days` dias: HARD_BLOCK total
- ✅ Após período inicial: segue `weekday_sweets_mode` (HARD_BLOCK/EXCEPTION_WITH_COST/ALLOW)
- ✅ Tentativas bloqueadas registradas em `rule_events`
- ✅ Mensagens de erro claras e comportamentais

### 4.5 Admin/Coach
- ✅ Apenas OWNER/COACH acessam `/admin/*`
- ✅ Coaches veem apenas membros do seu programa
- ✅ Owners veem todos os membros da organização
- ✅ Exportações CSV abrem corretamente no Excel

## 5. Edge Cases

### 5.1 Dados Ausentes
- **Cenário**: Membro sem `daily_meals` para hoje
- **Solução**: Gerar automaticamente ao abrir tela "Hoje"

### 5.2 Templates Incompletos
- **Cenário**: Programa sem `plan_templates` para semana atual
- **Solução**: Mostrar mensagem "Plano não disponível. Entre em contato com seu coach."

### 5.3 Múltiplos Enrollments
- **Cenário**: Membro em múltiplos programas
- **Solução**: MVP suporta apenas 1 enrollment ativo por vez (mais recente)

### 5.4 Timezone
- **Cenário**: Membro em timezone diferente
- **Solução**: Todos os cálculos em America/Sao_Paulo (padrão)

### 5.5 Exportação Vazia
- **Cenário**: Exportar quando não há dados
- **Solução**: CSV com headers apenas + mensagem informativa

## 6. Analytics

### 6.1 Métricas de Membro
- Aderência diária (%)
- Peso ao longo do tempo
- Dias consecutivos de check-in
- Tentativas de violação de regras

### 6.2 Métricas de Coach
- Número de membros ativos
- Aderência média do programa
- Membros com aderência < 70%
- Exportações realizadas

### 6.3 Eventos Rastreados
- `daily_checkin_created`
- `meal_marked_done`
- `rule_violation_attempted`
- `export_generated`

## 7. Assumptions

1. **Timezone**: Todos os usuários estão em America/Sao_Paulo
2. **Refeições padrão**: 6 refeições por dia (café, lanche manhã, almoço, lanche tarde, jantar, ceia)
3. **Período inicial**: Hard block aplicado desde `enrollment.start_date` por `hard_block_days` dias
4. **Multi-tenancy**: Cada organização é isolada (RLS garante)
5. **Mobile-first**: Web app é PWA mobile-first, admin é otimizado para desktop
6. **Branding**: App usa branding neutro (sem menções a TEM VENDA na UI)
7. **Limite de exceções**: Configurável por ruleset, padrão 2 por semana
8. **Pizza rule**: Opcional, apenas domingo, limite de fatias configurável

## 8. Fases de Lançamento

### Fase 1 (MVP)
- Autenticação básica
- Check-in diário
- Visualização de plano
- Regras básicas (hard block inicial)
- Admin básico (criar org/programa, templates)

### Fase 2 (Pós-MVP)
- Regras avançadas (exceções com custo)
- Notificações push
- Gráficos avançados
- Chat coach-membro
- Integração com wearables

## 9. Definições Técnicas

### 9.1 Domínio
- Web: `rotina.temvenda.com.br`
- Rotas: `/app/*` (usuário), `/admin/*` (admin/coach)

### 9.2 Stack
- Frontend Web: Next.js 14 (App Router), TypeScript, TailwindCSS
- Mobile: React Native Expo, TypeScript
- Backend: Supabase (PostgreSQL + Auth + Storage)
- Deploy: Vercel (web), EAS Build (mobile)

### 9.3 Segurança
- RLS (Row Level Security) no Supabase
- RBAC (Role-Based Access Control) nas rotas
- Validação server-side de todas as operações

