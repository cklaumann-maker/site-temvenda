# 📋 Executar SQL em Ordem Correta

## ⚠️ Erro Encontrado

```
ERROR: 42P01: relation "public.programs" does not exist
```

Isso significa que as tabelas não foram criadas na ordem correta ou não foram criadas completamente.

---

## ✅ Solução Completa

### Passo 1: Criar TODAS as Tabelas

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/criar_todas_tabelas.sql`
4. **Copie TODO o conteúdo** e cole no SQL Editor
5. **Execute** (Run)

Este script cria **TODAS** as tabelas na ordem correta:
- ✅ profiles
- ✅ orgs
- ✅ org_members
- ✅ programs ← **Esta estava faltando!**
- ✅ enrollments
- ✅ rulesets
- ✅ plan_templates
- ✅ daily_meals
- ✅ daily_checkins
- ✅ rule_events

Também cria:
- ✅ Organização demo
- ✅ Programa demo "Disciplina Total"
- ✅ Ruleset demo
- ✅ Índices para performance

---

### Passo 2: Importar Plano Alimentar

**Após executar o passo 1 com sucesso:**

1. **Ainda no SQL Editor**
2. **Abra o arquivo:** `rotina-app/supabase/import_meal_plan.sql`
3. **Copie TODO o conteúdo** e cole no SQL Editor
4. **Execute** (Run)

Agora deve funcionar! ✅

---

## 🔍 Verificar se Funcionou

Execute este SQL para verificar:

```sql
-- Verificar todas as tabelas criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
  'profiles', 'orgs', 'org_members', 'programs', 
  'enrollments', 'rulesets', 'plan_templates', 
  'daily_meals', 'daily_checkins', 'rule_events'
)
ORDER BY table_name;

-- Verificar programa demo
SELECT id, name, active 
FROM public.programs 
WHERE id = '00000000-0000-0000-0000-000000000002';

-- Verificar quantas refeições foram importadas
SELECT COUNT(*) as total_refeicoes 
FROM public.plan_templates;
```

**Resultado esperado:**
- ✅ 10 tabelas listadas
- ✅ Programa "Disciplina Total" encontrado (active = true)
- ✅ 84 refeições importadas

---

## 📋 Ordem Correta de Execução

1. ✅ **Primeiro:** Execute `criar_todas_tabelas.sql`
   - Cria todas as tabelas
   - Cria dados demo (org, program, ruleset)

2. ✅ **Depois:** Execute `import_meal_plan.sql`
   - Importa 84 refeições do plano alimentar

3. ✅ **Por último:** Recarregue o app
   - Acesse `/app/today`
   - Veja o calendário com seu plano

---

## ⚠️ Se Ainda Der Erro

### Erro: "relation auth.users does not exist"
- Isso é normal se você ainda não fez login
- O Supabase cria `auth.users` automaticamente quando você faz login
- Continue mesmo assim, a tabela será criada quando necessário

### Erro: "permission denied"
- Verifique se você está usando o SQL Editor do Supabase
- Certifique-se de que tem permissões de administrador

### Erro: "duplicate key value"
- Significa que os dados já existem
- Isso é OK, o script usa `ON CONFLICT DO NOTHING`
- Continue para o próximo passo

---

## 🎯 Arquivos Criados

1. ✅ `supabase/criar_todas_tabelas.sql` (NOVO - COMPLETO)
   - Cria TODAS as tabelas na ordem correta
   - Cria dados demo
   - Cria índices

2. ✅ `EXECUTAR_EM_ORDEM.md` (Este guia)

---

## 🚀 Resumo Rápido

```bash
1. Execute: criar_todas_tabelas.sql
2. Execute: import_meal_plan.sql
3. Recarregue o app
```

Execute primeiro o `criar_todas_tabelas.sql` (que cria TODAS as tabelas incluindo `programs`) e depois o `import_meal_plan.sql`! 🎉







