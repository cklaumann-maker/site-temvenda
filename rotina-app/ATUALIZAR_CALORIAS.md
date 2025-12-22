# 🔥 Atualizar Calorias nas Refeições Existentes

## ⚠️ Problema

As refeições foram regeradas mas sem as calorias. Isso acontece porque as refeições foram geradas antes dos templates terem calorias, ou a função não copiou corretamente.

## ✅ Solução

Execute este SQL no Supabase para atualizar as calorias nas refeições existentes:

### **Opção 1: SQL Simples (Recomendado)**

Execute o arquivo `supabase/atualizar_calorias_refeicoes_simples.sql` no Supabase SQL Editor.

Este SQL:
1. Verifica se os templates têm calorias
2. Para cada refeição sem calorias, encontra o template correspondente
3. Atualiza as calorias da refeição com as do template

### **Opção 2: Deletar e Regerar**

Se preferir, você pode deletar e regerar todas as refeições:

```sql
-- Deletar refeições antigas
DELETE FROM public.daily_meals 
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID;

-- Regerar refeições (agora com calorias dos templates)
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 1);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 2);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 3);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 4);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 5);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 6);
```

## 🔍 Verificar se funcionou

Execute este SQL para verificar:

```sql
SELECT 
  date,
  meal_type,
  LEFT(opt1, 40) as opt1_preview,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3
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
  END
LIMIT 20;
```

Você deve ver valores de calorias (não zeros) em `kcal_opt1`, `kcal_opt2`, `kcal_opt3`.

---

**Execute o SQL e me informe o resultado!** ✅

