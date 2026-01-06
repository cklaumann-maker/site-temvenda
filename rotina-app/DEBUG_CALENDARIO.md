# 🔍 Debug do Calendário

## ⚠️ Problema Reportado

O calendário não está:
1. Mostrando as refeições na ordem correta
2. Mostrando o plano alimentar importado do banco

## 🔧 Correções Aplicadas

### 1. **Logs de Debug Adicionados**

Agora o console do navegador mostrará:
- Quantas refeições foram carregadas do banco
- Amostra das primeiras 3 refeições
- Ordem de classificação aplicada
- Refeições filtradas por data selecionada
- Ordem final das refeições

### 2. **Como Verificar**

1. **Abra o console do navegador (F12)**
2. **Acesse `/app/today`**
3. **Veja os logs:**
   - `📊 Meals loaded from DB:` - mostra o que veio do banco
   - `✅ Meals sorted:` - mostra a ordem aplicada
   - `📅 Meals for [data]:` - mostra refeições do dia selecionado
   - `✅ Sorted meals for [data]:` - mostra ordem final

### 3. **Verificar no Banco de Dados**

Execute este SQL no Supabase:

```sql
-- Verificar templates da segunda-feira
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

-- Verificar refeições geradas para segunda-feira atual
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
    -- Encontrar a próxima segunda-feira
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

## 📋 Checklist de Validação

- [ ] Abrir console do navegador (F12)
- [ ] Acessar `/app/today`
- [ ] Verificar logs no console
- [ ] Comparar com dados do banco (SQL acima)
- [ ] Verificar se a ordem está correta:
  - Pré-treino (1)
  - Pós-treino (2)
  - Café da manhã (3)
  - Almoço (4)
  - Lanche da tarde (5)
  - Jantar (6)

## 🐛 Possíveis Problemas

1. **Se não aparecer refeições:**
   - Verifique se as refeições foram geradas no banco
   - Execute: `SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE);`

2. **Se a ordem estiver errada:**
   - Verifique os logs no console
   - Verifique se `MEAL_TYPE_ORDER` está correto
   - Verifique se `sortMealsByType` está sendo chamado

3. **Se as opções estiverem erradas:**
   - Verifique no banco se `opt1`, `opt2`, `opt3` estão corretos
   - Verifique se os prefixos foram removidos corretamente na importação

---

**Execute os passos acima e me informe o que aparece no console!** 🔍







