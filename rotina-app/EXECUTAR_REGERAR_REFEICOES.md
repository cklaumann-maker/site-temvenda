# ✅ Regerar Refeições - SQL Completo

## Execute este SQL completo no Supabase:

```sql
-- Regerar refeições para a semana atual
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 1);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 2);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 3);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 4);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 5);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 6);
```

## Verificar resultado:

```sql
-- Verificar refeições geradas
SELECT 
  date,
  meal_type,
  opt1,
  opt2,
  opt3,
  avoid
FROM daily_meals
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND date >= CURRENT_DATE
ORDER BY date, 
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

## Resultado esperado:

Para cada dia, você deve ver 6 refeições na ordem:
1. `pre` - Pré-treino
2. `post` - Pós-treino
3. `cafe` - Café da manhã
4. `almoco` - Almoço
5. `lanche_tarde` - Lanche da tarde
6. `jantar` - Jantar

---

**Execute o SQL acima e depois recarregue a página `/app/today`!** ✅

