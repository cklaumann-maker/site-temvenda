# 🔧 Corrigir Erro: Tabela Não Existe

## ❌ Erro Encontrado

```
ERROR: 42P01: relation "public.plan_templates" does not exist
```

Isso significa que as **migrations não foram executadas** ou a tabela não foi criada.

---

## ✅ Solução

### Passo 1: Criar Tabelas Necessárias

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/verificar_e_criar_tabelas.sql`
4. **Copie todo o conteúdo** e cole no SQL Editor
5. **Execute** (Run)

Este script vai:
- ✅ Criar a tabela `plan_templates` se não existir
- ✅ Criar a tabela `daily_meals` se não existir
- ✅ Criar outras tabelas necessárias (`programs`, `orgs`, `profiles`)
- ✅ Criar o programa demo "Disciplina Total"
- ✅ Criar a organização demo

---

### Passo 2: Importar Plano Alimentar

**Após executar o passo 1:**

1. **Ainda no SQL Editor**
2. **Abra o arquivo:** `rotina-app/supabase/import_meal_plan.sql`
3. **Copie todo o conteúdo** e cole no SQL Editor
4. **Execute** (Run)

Agora deve funcionar! ✅

---

## 🔍 Verificar se Funcionou

Execute este SQL para verificar:

```sql
-- Verificar se as tabelas existem
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('plan_templates', 'daily_meals', 'programs', 'orgs');

-- Verificar quantas refeições foram importadas
SELECT COUNT(*) as total_refeicoes 
FROM public.plan_templates;

-- Verificar o programa demo
SELECT * FROM public.programs 
WHERE id = '00000000-0000-0000-0000-000000000002';
```

**Resultado esperado:**
- ✅ 4 tabelas listadas
- ✅ 84 refeições importadas
- ✅ Programa "Disciplina Total" encontrado

---

## 📋 Ordem Correta de Execução

1. ✅ **Primeiro:** Execute `verificar_e_criar_tabelas.sql`
2. ✅ **Depois:** Execute `import_meal_plan.sql`
3. ✅ **Por último:** Recarregue o app e veja o calendário

---

## ⚠️ Se Ainda Der Erro

### Erro: "relation auth.users does not exist"
- Isso significa que o Supabase Auth não está configurado
- Verifique se você está usando o projeto correto do Supabase

### Erro: "permission denied"
- Verifique se você tem permissões de administrador no projeto
- Tente executar como Service Role (não Anon Key)

### Erro: "foreign key constraint"
- Execute primeiro o `verificar_e_criar_tabelas.sql`
- Ele cria todas as dependências necessárias

---

## 🎯 Arquivos Criados

1. ✅ `supabase/verificar_e_criar_tabelas.sql` (NOVO)
   - Cria todas as tabelas necessárias
   - Cria programa e organização demo
   - Cria índices para performance

---

Execute primeiro o `verificar_e_criar_tabelas.sql` e depois o `import_meal_plan.sql`! 🚀







