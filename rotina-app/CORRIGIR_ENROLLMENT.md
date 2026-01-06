# 🔧 Corrigir Enrollment e Regerar Refeições

## ⚠️ Problema

O erro `User is not enrolled in any program` indica que o usuário não está inscrito em nenhum programa ativo.

## ✅ Solução

Execute este SQL completo no Supabase SQL Editor:

```sql
-- 1. Verificar se o usuário tem enrollment ativo
SELECT 
  id,
  user_id,
  program_id,
  start_date,
  end_date,
  active
FROM public.enrollments
WHERE user_id = auth.uid()
ORDER BY start_date DESC;

-- 2. Verificar programas disponíveis
SELECT 
  id,
  name,
  description,
  active
FROM public.programs
WHERE active = true
ORDER BY created_at DESC;

-- 3. Criar enrollment se não existir
INSERT INTO public.enrollments (user_id, program_id, start_date, active)
SELECT 
  auth.uid(),
  '00000000-0000-0000-0000-000000000002', -- ID do programa padrão
  CURRENT_DATE,
  true
WHERE NOT EXISTS (
  SELECT 1 FROM public.enrollments
  WHERE user_id = auth.uid()
    AND active = true
)
RETURNING *;

-- 4. Se o enrollment já existir mas estiver inativo, ativar
UPDATE public.enrollments
SET active = true,
    start_date = COALESCE(start_date, CURRENT_DATE)
WHERE user_id = auth.uid()
  AND program_id = '00000000-0000-0000-0000-000000000002'
  AND active = false;

-- 5. Verificar enrollment criado/ativado
SELECT 
  id,
  user_id,
  program_id,
  start_date,
  end_date,
  active
FROM public.enrollments
WHERE user_id = auth.uid()
ORDER BY start_date DESC;

-- 6. CORRIGIR templates: 'lanche_manha' -> 'pre'
UPDATE plan_templates
SET meal_type = 'pre'
WHERE program_id = '00000000-0000-0000-0000-000000000002'
  AND meal_type = 'lanche_manha';

-- 7. DELETAR refeições diárias antigas (CUIDADO!)
DELETE FROM public.daily_meals WHERE user_id = auth.uid();

-- 8. REGERAR refeições para a semana atual
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 1);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 2);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 3);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 4);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 5);
SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE + 6);

-- 9. Verificar refeições geradas para segunda-feira
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

## 📋 Resultado Esperado

Após executar o SQL acima, você deve ver:

1. **Enrollment criado** com `active = true`
2. **Templates corrigidos** (sem `lanche_manha`)
3. **Refeições geradas** com os tipos corretos:
   - `pre` - Pré-treino
   - `post` - Pós-treino
   - `cafe` - Café da manhã
   - `almoco` - Almoço
   - `lanche_tarde` - Lanche da tarde
   - `jantar` - Jantar

## 🔄 Próximos Passos

1. Execute o SQL acima
2. Recarregue a página `/app/today` (Ctrl+Shift+R)
3. Verifique o console - deve mostrar `pre` e `post` na ordem correta
4. Verifique visualmente - refeições devem aparecer na ordem correta

---

**Execute o SQL e me informe o resultado!** ✅







