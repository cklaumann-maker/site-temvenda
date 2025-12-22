# 🔥 Importar Calorias Atualizado - Instruções

## ✅ SQL Gerado com Sucesso!

O arquivo `plano_calorias_com_calorias.sql` foi gerado com **42 refeições** e todas as calorias.

## 📋 Próximos Passos:

### **PASSO 1: Executar SQL no Supabase**

1. Abra o arquivo `plano_calorias_com_calorias.sql` na pasta `rotina-app/`
2. Copie **TODO o conteúdo**
3. Cole no **Supabase SQL Editor**
4. Execute o SQL

Este SQL vai:
- Deletar templates antigos
- Inserir novos templates com calorias

### **PASSO 2: Verificar Templates**

Execute este SQL para verificar se as calorias foram importadas:

```sql
-- Verificar templates com calorias
SELECT 
  day_of_week,
  meal_type,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3,
  COUNT(*) as total
FROM plan_templates
WHERE program_id = '00000000-0000-0000-0000-000000000002'
GROUP BY day_of_week, meal_type, kcal_opt1, kcal_opt2, kcal_opt3
ORDER BY day_of_week, 
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

**Resultado esperado:** Você deve ver valores de calorias (não zeros) para cada refeição.

### **PASSO 3: Deletar e Regerar Refeições**

Após importar os templates, execute este SQL para regerar as refeições com calorias:

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

### **PASSO 4: Verificar Refeições com Calorias**

```sql
-- Verificar refeições geradas com calorias
SELECT 
  date,
  meal_type,
  LEFT(opt1, 40) as opt1_preview,
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

**Resultado esperado:** Você deve ver valores de calorias em `kcal_opt1`, `kcal_opt2`, `kcal_opt3` para cada refeição.

---

## 📊 Exemplo de Calorias Esperadas (Segunda-feira):

- **Pré-treino:** 0, 0, 0 kcal
- **Pós-treino:** 265, 152, 170 kcal
- **Café da manhã:** 270, 305, 295 kcal
- **Almoço:** 570, 550, 415 kcal
- **Lanche da tarde:** 235, 220, 270 kcal
- **Jantar:** 230, 140, 210 kcal

---

**Execute os passos acima e me informe quando estiver pronto para continuar com o frontend!** ✅

