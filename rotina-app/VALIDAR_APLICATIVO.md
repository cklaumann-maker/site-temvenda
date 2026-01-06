# ✅ Validar se o Aplicativo Está Carregando do Banco

## 🔍 Verificações

### 1. **Verificar no Banco de Dados**

Execute este SQL no Supabase para verificar se as refeições foram geradas:

```sql
-- Verificar total de refeições geradas
SELECT 
  COUNT(*) as total_refeicoes,
  COUNT(DISTINCT date) as total_dias
FROM daily_meals
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND date >= CURRENT_DATE;

-- Verificar refeições por tipo
SELECT 
  meal_type,
  COUNT(*) as total
FROM daily_meals
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND date >= CURRENT_DATE
GROUP BY meal_type
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
- `total_refeicoes`: 42 (6 refeições × 7 dias)
- `total_dias`: 7
- Tipos: `pre`, `post`, `cafe`, `almoco`, `lanche_tarde`, `jantar` (6 tipos)

---

### 2. **Verificar no Console do Navegador**

1. Acesse `http://localhost:3001/app/today`
2. Abra o console (F12)
3. Procure pelos logs:
   - `📊 Meals loaded from DB:` - deve mostrar `total: 42` (ou próximo)
   - `✅ Meals sorted:` - deve mostrar ordem correta
   - `📅 Meals for [data]:` - deve mostrar 6 refeições por dia
   - `✅ Sorted meals for [data]:` - deve mostrar: `['pre (order: 1)', 'post (order: 2)', 'cafe (order: 3)', 'almoco (order: 4)', 'lanche_tarde (order: 5)', 'jantar (order: 6)']`

---

### 3. **Verificar Visualmente**

No calendário, você deve ver:

**Para cada dia da semana:**
1. **Pré-treino** - "Venom + água"
2. **Pós-treino** - "Whey + banana + água de coco"
3. **Café da Manhã** - "Ovos mexidos (2-3) + 1 pão + requeijão"
4. **Almoço** - "Arroz + feijão + carne"
5. **Lanche da Tarde** - "Ovos + maçã"
6. **Jantar** - "Frango ou peixe"

**Na ordem correta** (de cima para baixo)

---

## ⚠️ Se não estiver funcionando:

### Problema 1: Não aparece nenhuma refeição
- Verifique se as refeições foram geradas no banco (SQL acima)
- Verifique se o enrollment está ativo
- Recarregue a página (Ctrl+Shift+R)

### Problema 2: Aparecem tipos errados (`ceia`, `lanche_manha`)
- Execute: `UPDATE plan_templates SET meal_type = 'pre' WHERE meal_type = 'lanche_manha';`
- Delete e regenere as refeições

### Problema 3: Ordem está errada
- Verifique os logs no console
- Verifique se `MEAL_TYPE_ORDER` está correto no código
- Verifique se `sortMealsByType` está sendo chamado

---

## 📋 Checklist Final

- [ ] SQL mostra 42 refeições geradas
- [ ] SQL mostra 6 tipos corretos (pre, post, cafe, almoco, lanche_tarde, jantar)
- [ ] Console mostra `total: 42` (ou próximo)
- [ ] Console mostra ordem correta: `pre (order: 1)`, `post (order: 2)`, etc.
- [ ] Visualmente aparecem 6 refeições por dia
- [ ] Visualmente a ordem está correta (Pré-treino primeiro, depois Pós-treino, etc.)

---

**Execute as verificações acima e me informe o resultado!** ✅







