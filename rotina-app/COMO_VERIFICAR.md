# ✅ Como Verificar se Tudo Funcionou

## 🔍 Verificação no Supabase

### Opção 1: Script de Verificação Completo (Recomendado)

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/verificar_importacao.sql`
4. **Copie TODO o conteúdo** e cole no SQL Editor
5. **Execute** (Run)

Este script vai mostrar:
- ✅ Quantas tabelas foram criadas (deve ser 10)
- ✅ Lista de todas as tabelas
- ✅ Organização demo criada
- ✅ Programa demo criado
- ✅ Ruleset demo criado
- ✅ Total de refeições importadas (deve ser 84)
- ✅ Refeições por semana (deve ser 42 por semana)
- ✅ Tipos de refeição importados
- ✅ Exemplos de refeições
- ✅ Índices criados
- ✅ Resumo final

---

### Opção 2: Verificação Manual Rápida

Execute este SQL simples:

```sql
-- Verificar tabelas
SELECT COUNT(*) as total_tabelas
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
  'profiles', 'orgs', 'org_members', 'programs', 
  'enrollments', 'rulesets', 'plan_templates', 
  'daily_meals', 'daily_checkins', 'rule_events'
);

-- Verificar refeições importadas
SELECT COUNT(*) as total_refeicoes FROM public.plan_templates;

-- Verificar programa demo
SELECT name, active FROM public.programs 
WHERE id = '00000000-0000-0000-0000-000000000002';
```

**Resultado esperado:**
- ✅ `total_tabelas`: 10
- ✅ `total_refeicoes`: 84
- ✅ `name`: "Disciplina Total"
- ✅ `active`: true

---

## ✅ Checklist de Verificação

### Tabelas Criadas (10 no total)
- [ ] `profiles`
- [ ] `orgs`
- [ ] `org_members`
- [ ] `programs`
- [ ] `enrollments`
- [ ] `rulesets`
- [ ] `plan_templates`
- [ ] `daily_meals`
- [ ] `daily_checkins`
- [ ] `rule_events`

### Dados Demo Criados
- [ ] Organização: "Demo Organization"
- [ ] Programa: "Disciplina Total" (active = true)
- [ ] Ruleset: Configurado para o programa

### Plano Alimentar Importado
- [ ] Total de refeições: **84**
- [ ] Semana 1: **42 refeições** (7 dias × 6 refeições)
- [ ] Semana 2: **42 refeições** (7 dias × 6 refeições)
- [ ] Tipos de refeição: `pre`, `post`, `breakfast`, `lunch`, `snack`, `dinner`

---

## 🧪 Verificar no App

### 1. Recarregar o App

1. **Acesse:** http://localhost:3001/app/today
2. **Recarregue a página** (F5 ou Cmd+R)

### 2. Verificar Calendário

Você deve ver:
- ✅ Calendário mensal visual
- ✅ Dias com refeições planejadas
- ✅ Barra de progresso por dia
- ✅ Seção com refeições do dia atual

### 3. Verificar Refeições do Dia

Na seção inferior do calendário, você deve ver:
- ✅ Lista de refeições do dia atual
- ✅ Checkboxes para marcar como feita
- ✅ Opções de refeição (opt1, opt2, opt3)
- ✅ Avisos (avoid) em vermelho

### 4. Testar Marcação

1. **Clique em um checkbox** ao lado de uma refeição
2. **Deve marcar/desmarcar** a refeição
3. **A barra de progresso** deve atualizar automaticamente

---

## 🔍 Verificações Específicas

### Verificar Refeições de um Dia Específico

```sql
-- Ver refeições da Segunda-feira, Semana 1
SELECT 
  meal_type,
  opt1,
  opt2,
  opt3,
  avoid
FROM public.plan_templates
WHERE week_index = 1 
AND day_of_week = 1
ORDER BY 
  CASE meal_type
    WHEN 'pre' THEN 1
    WHEN 'post' THEN 2
    WHEN 'breakfast' THEN 3
    WHEN 'lunch' THEN 4
    WHEN 'snack' THEN 5
    WHEN 'dinner' THEN 6
  END;
```

**Deve mostrar 6 refeições:**
1. Pré-treino: Venom + água
2. Pós-treino: Whey + banana + água de coco
3. Café da Manhã: Ovos mexidos (2-3) + 1 pão + requeijão
4. Almoço: Arroz + feijão + carne
5. Lanche: Ovos + maçã
6. Jantar: Frango ou peixe

---

## ⚠️ Se Algo Estiver Errado

### Problema: Menos de 84 refeições

```sql
-- Verificar quantas refeições faltam
SELECT 
  week_index,
  day_of_week,
  COUNT(*) as refeicoes
FROM public.plan_templates
GROUP BY week_index, day_of_week
HAVING COUNT(*) < 6
ORDER BY week_index, day_of_week;
```

**Solução:** Re-execute o `import_meal_plan.sql`

---

### Problema: Tabelas não aparecem

```sql
-- Verificar se as tabelas existem
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

**Solução:** Re-execute o `criar_todas_tabelas.sql`

---

### Problema: Programa não encontrado

```sql
-- Verificar programas
SELECT * FROM public.programs;
```

**Solução:** Re-execute o `criar_todas_tabelas.sql` (parte final que cria os dados demo)

---

## 📊 Resultados Esperados

### No Supabase SQL Editor

```
✅ Tabelas criadas: 10
✅ Total de refeições: 84
✅ Programa: Disciplina Total (active: true)
✅ Refeições Semana 1: 42
✅ Refeições Semana 2: 42
✅ Tipos de refeição: 6 (pre, post, breakfast, lunch, snack, dinner)
```

### No App

```
✅ Calendário visual funcionando
✅ Refeições aparecendo no calendário
✅ Checkboxes funcionando
✅ Barra de progresso atualizando
✅ Detalhes do dia mostrando refeições
```

---

## 🎯 Próximos Passos

Após verificar que tudo está funcionando:

1. ✅ **Teste o calendário** - Navegue entre meses
2. ✅ **Marque refeições** - Teste os checkboxes
3. ✅ **Veja a adesão** - Observe a barra de progresso
4. ✅ **Teste outras páginas** - `/app/plan`, `/app/dashboard`

---

Execute o script `verificar_importacao.sql` para ver um relatório completo! 🚀

