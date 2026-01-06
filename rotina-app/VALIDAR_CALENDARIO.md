# 🔍 Validar Calendário - Instruções

## ✅ O que foi implementado

1. **Logs de Debug** - Console do navegador mostrará:
   - `📊 Meals loaded from DB:` - Dados brutos do banco
   - `✅ Meals sorted:` - Ordem aplicada
   - `📅 Meals for [data]:` - Refeições do dia selecionado
   - `✅ Sorted meals for [data]:` - Ordem final

2. **Ordenação** - Ordem configurada:
   - Pré-treino (1)
   - Pós-treino (2)
   - Café da manhã (3)
   - Almoço (4)
   - Lanche da tarde (5)
   - Jantar (6)

3. **Carregamento do Banco** - Carrega diretamente de `daily_meals`

## 📋 Passos para Validar

### 1. Abrir Console do Navegador

1. Acesse `http://localhost:3001/app/today`
2. Pressione **F12** (ou **Cmd+Option+I** no Mac)
3. Vá para a aba **Console**

### 2. Verificar Logs

Você deve ver logs como:
```
📊 Meals loaded from DB: {total: X, sample: [...]}
✅ Meals sorted: {total: X, order: [...]}
📅 Meals for 2024-12-23: {count: X, meals: [...]}
✅ Sorted meals for 2024-12-23: ['pre (order: 1)', 'post (order: 2)', ...]
```

### 3. Verificar no Banco de Dados

Execute este SQL no Supabase SQL Editor:

```sql
-- Verificar templates da segunda-feira (Semana 1)
SELECT 
  meal_type,
  opt1,
  opt2,
  opt3,
  avoid
FROM plan_templates
WHERE program_id = '00000000-0000-0000-0000-000000000002'
  AND week_index = 1
  AND day_of_week = 1
ORDER BY 
  CASE meal_type
    WHEN 'pre' THEN 1
    WHEN 'post' THEN 2
    WHEN 'cafe' THEN 3
    WHEN 'almoco' THEN 4
    WHEN 'lanche_tarde' THEN 5
    WHEN 'jantar' THEN 6
    ELSE 999
  END;
```

**Resultado esperado (Segunda-feira, Semana 1):**
1. `pre` - Pré-treino: "Venom + água"
2. `post` - Pós-treino: "Whey + banana + água de coco"
3. `cafe` - Café da manhã: "Ovos mexidos (2-3) + 1 pão + requeijão"
4. `almoco` - Almoço: "Arroz + feijão + carne"
5. `lanche_tarde` - Lanche da tarde: "Ovos + maçã"
6. `jantar` - Jantar: "Frango ou peixe"

### 4. Verificar Refeições Geradas

```sql
-- Encontrar próxima segunda-feira
SELECT 
  CURRENT_DATE + (8 - EXTRACT(DOW FROM CURRENT_DATE)::INTEGER) % 7 AS proxima_segunda;

-- Verificar refeições geradas para segunda-feira
SELECT 
  date,
  meal_type,
  opt1,
  opt2,
  opt3,
  avoid
FROM daily_meals
WHERE user_id = auth.uid()
  AND date = (
    SELECT CURRENT_DATE + (8 - EXTRACT(DOW FROM CURRENT_DATE)::INTEGER) % 7
  )
ORDER BY 
  CASE meal_type
    WHEN 'pre' THEN 1
    WHEN 'post' THEN 2
    WHEN 'cafe' THEN 3
    WHEN 'almoco' THEN 4
    WHEN 'lanche_tarde' THEN 5
    WHEN 'jantar' THEN 6
    ELSE 999
  END;
```

## 🔍 Comparação

Compare:
1. **Templates no banco** (SQL acima) com
2. **O que aparece no calendário** (visualmente)
3. **Logs no console** (dados carregados)

## ⚠️ Se não corresponder

1. **Verifique se os templates foram importados:**
   ```sql
   SELECT COUNT(*) FROM plan_templates 
   WHERE program_id = '00000000-0000-0000-0000-000000000002';
   ```
   Deve retornar 84 refeições (14 dias × 6 refeições)

2. **Verifique se as refeições foram geradas:**
   ```sql
   SELECT COUNT(*) FROM daily_meals 
   WHERE user_id = auth.uid();
   ```

3. **Regere as refeições:**
   ```sql
   SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE);
   SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 1);
   -- ... para os próximos dias
   ```

4. **Verifique os logs no console** para ver o que está sendo carregado

---

**Execute os passos acima e me informe:**
1. O que aparece no console do navegador
2. O que aparece no banco de dados (SQL)
3. O que aparece visualmente no calendário

Com essas informações, posso identificar exatamente onde está o problema! 🔍







