# 🔥 Corrigir Calorias que Estão Zero

## ⚠️ Problema

As refeições estão com calorias zero mesmo após importar os templates.

## ✅ Solução - Execute passo a passo:

### **PASSO 1: Verificar se os templates têm calorias**

Execute este SQL primeiro:

```sql
SELECT 
  day_of_week,
  meal_type,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3
FROM plan_templates
WHERE program_id = '00000000-0000-0000-0000-000000000002'
  AND day_of_week = 1  -- Segunda-feira
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

**Resultado esperado para Segunda-feira:**
- Pré-treino: 0, 0, 0
- Pós-treino: 265, 152, 170
- Café da manhã: 270, 305, 295
- Almoço: 570, 550, 415
- Lanche da tarde: 235, 220, 270
- Jantar: 230, 140, 210

**Se aparecerem ZEROS aqui:**
- Você precisa executar o SQL de importação primeiro (`plano_calorias_com_calorias.sql`)

**Se aparecerem valores corretos:**
- Continue para PASSO 2

---

### **PASSO 2: Atualizar calorias nas refeições**

Execute este SQL:

```sql
UPDATE daily_meals dm
SET 
  kcal_opt1 = pt.kcal_opt1,
  kcal_opt2 = pt.kcal_opt2,
  kcal_opt3 = pt.kcal_opt3,
  updated_at = NOW()
FROM plan_templates pt
WHERE pt.program_id = '00000000-0000-0000-0000-000000000002'
  AND pt.meal_type = dm.meal_type
  AND pt.day_of_week = (
    CASE 
      WHEN EXTRACT(DOW FROM dm.date)::INTEGER = 0 THEN 7  -- Domingo
      ELSE EXTRACT(DOW FROM dm.date)::INTEGER
    END
  )
  AND pt.week_index = 1  -- Semana 1
  AND dm.user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND (dm.kcal_opt1 = 0 OR dm.kcal_opt2 = 0 OR dm.kcal_opt3 = 0);
```

---

### **PASSO 3: Verificar resultado**

```sql
SELECT 
  date,
  meal_type,
  LEFT(opt1, 30) as opt1_preview,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3
FROM daily_meals
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND date = CURRENT_DATE
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

**Agora você deve ver valores de calorias (não zeros)!**

---

## 🔍 Se ainda estiver zero:

1. **Verifique se executou o SQL de importação** (`plano_calorias_com_calorias.sql`)
2. **Verifique se os templates têm calorias** (PASSO 1)
3. **Execute também para semana 2:**

```sql
UPDATE daily_meals dm
SET 
  kcal_opt1 = pt.kcal_opt1,
  kcal_opt2 = pt.kcal_opt2,
  kcal_opt3 = pt.kcal_opt3,
  updated_at = NOW()
FROM plan_templates pt
WHERE pt.program_id = '00000000-0000-0000-0000-000000000002'
  AND pt.meal_type = dm.meal_type
  AND pt.day_of_week = (
    CASE 
      WHEN EXTRACT(DOW FROM dm.date)::INTEGER = 0 THEN 7
      ELSE EXTRACT(DOW FROM dm.date)::INTEGER
    END
  )
  AND pt.week_index = 2  -- Semana 2
  AND dm.user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND (dm.kcal_opt1 = 0 OR dm.kcal_opt2 = 0 OR dm.kcal_opt3 = 0);
```

---

**Execute os passos acima e me informe o resultado!** ✅







