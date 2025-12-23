# Guia para Corrigir Calorias em Todas as Refeições

## Problema Identificado
As refeições em `daily_meals` não têm as calorias (`kcal_opt1`, `kcal_opt2`, `kcal_opt3`) copiadas dos `plan_templates`, mesmo que os templates tenham essas informações.

## Solução em 2 Passos

### Passo 1: Corrigir Refeições Existentes

Execute o script `corrigir_todas_calorias_refeicoes.sql`:

1. Abra o Supabase SQL Editor
2. Abra o arquivo: `rotina-app/supabase/corrigir_todas_calorias_refeicoes.sql`
3. **IMPORTANTE**: Substitua `'SEU_USER_ID_AQUI'` pelo seu UUID (use `OBTER_USER_ID.sql` se necessário)
4. Execute o script
5. Verifique os logs de `RAISE NOTICE` para ver quantos registros foram atualizados

**O que este script faz:**
- Atualiza `kcal_opt1`, `kcal_opt2`, `kcal_opt3` em TODAS as refeições existentes
- Copia os valores dos `plan_templates` correspondentes
- Recalcula os resumos de calorias para todas as datas

### Passo 2: Garantir que Refeições Futuras Tenham Calorias

Execute o script `garantir_calorias_sempre.sql`:

1. Abra o Supabase SQL Editor
2. Abra o arquivo: `rotina-app/supabase/garantir_calorias_sempre.sql`
3. Execute o script (não precisa substituir nada)

**O que este script faz:**
- Atualiza a função `generate_daily_meals` para SEMPRE copiar calorias
- Garante que refeições futuras sempre terão calorias dos templates
- Recalcula automaticamente o resumo de calorias ao gerar refeições

## Verificação

Após executar os scripts, verifique:

```sql
-- Verificar se as calorias foram atualizadas
SELECT 
  date,
  meal_type,
  opt1,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3
FROM public.daily_meals
WHERE user_id = 'SEU_USER_ID_AQUI'::UUID
  AND date >= '2025-12-20'::DATE
ORDER BY date DESC, meal_type;
```

Todas as refeições devem ter valores em `kcal_opt1`, `kcal_opt2`, `kcal_opt3` (pelo menos 0, mas preferencialmente os valores dos templates).

## Ordem de Execução

1. ✅ `corrigir_todas_calorias_refeicoes.sql` - Corrige refeições existentes
2. ✅ `garantir_calorias_sempre.sql` - Garante que futuras refeições tenham calorias

## Resultado Esperado

Após executar ambos os scripts:
- ✅ Todas as refeições existentes terão calorias
- ✅ Refeições futuras sempre terão calorias automaticamente
- ✅ Os cálculos de calorias consumidas funcionarão corretamente
- ✅ As calorias aparecerão na interface do aplicativo

