# 🔧 Corrigir Problema das Refeições

## ⚠️ Problema Identificado

Os logs do console mostram que estão aparecendo:
- `cafe`, `almoco`, `lanche_tarde`, `jantar`, `ceia`, `lanche_manha`

Mas deveria aparecer:
- `pre`, `post`, `cafe`, `almoco`, `lanche_tarde`, `jantar`

## 🔍 Causa

Os templates no banco podem ter tipos incorretos (`lanche_manha` e `ceia` em vez de `pre` e `post`), ou as refeições foram geradas antes da correção dos templates.

## ✅ Solução

### 1. **Corrigir Templates no Banco**

Execute este SQL no Supabase SQL Editor:

```sql
-- 1. Verificar templates existentes
SELECT 
  meal_type,
  COUNT(*) as total
FROM plan_templates
WHERE program_id = '00000000-0000-0000-0000-000000000002'
GROUP BY meal_type
ORDER BY meal_type;

-- 2. CORRIGIR: Se houver 'lanche_manha', deve ser 'pre' (Pré-treino)
UPDATE plan_templates
SET meal_type = 'pre'
WHERE program_id = '00000000-0000-0000-0000-000000000002'
  AND meal_type = 'lanche_manha';

-- 3. Verificar se há 'ceia' que deveria ser outra coisa
-- Se houver 'ceia' onde deveria estar 'post', corrigir manualmente
-- Ou deletar se não for necessário

-- 4. Verificar templates da segunda-feira após correção
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

**Resultado esperado:**
1. `pre` - Pré-treino: "Venom + água"
2. `post` - Pós-treino: "Whey + banana + água de coco"
3. `cafe` - Café da manhã: "Ovos mexidos (2-3) + 1 pão + requeijão"
4. `almoco` - Almoço: "Arroz + feijão + carne"
5. `lanche_tarde` - Lanche da tarde: "Ovos + maçã"
6. `jantar` - Jantar: "Frango ou peixe"

### 2. **Deletar e Regerar Refeições Diárias**

```sql
-- CUIDADO: Isso apaga todas as refeições geradas!
-- Execute apenas se quiser regerar tudo
DELETE FROM public.daily_meals WHERE user_id = auth.uid();

-- Regerar refeições para a semana atual
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 1);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 2);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 3);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 4);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 5);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 6);
```

### 3. **Verificar Refeições Geradas**

```sql
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
    -- Encontrar próxima segunda-feira
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

### 4. **Recarregar a Página**

Após executar os SQLs acima:
1. Recarregue a página `/app/today` (Ctrl+Shift+R ou Cmd+Shift+R)
2. Abra o console (F12)
3. Verifique os logs - agora deve mostrar:
   - `pre (order: 1)`
   - `post (order: 2)`
   - `cafe (order: 3)`
   - `almoco (order: 4)`
   - `lanche_tarde (order: 5)`
   - `jantar (order: 6)`

## 📋 Checklist

- [ ] Executar SQL para corrigir templates
- [ ] Verificar que templates estão corretos (6 refeições: pre, post, cafe, almoco, lanche_tarde, jantar)
- [ ] Deletar refeições diárias antigas (opcional, mas recomendado)
- [ ] Regerar refeições para a semana atual
- [ ] Verificar refeições geradas no banco
- [ ] Recarregar página no navegador
- [ ] Verificar console - ordem deve estar correta
- [ ] Verificar visualmente - refeições devem aparecer na ordem correta

---

**Execute os passos acima e me informe se funcionou!** ✅

