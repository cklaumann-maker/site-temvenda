# Armazenamento de Dados de Calorias no Banco de Dados

## 📋 Resumo

Este documento explica como os dados de calorias são armazenados no banco de dados e o que precisa ser feito para garantir que tudo funcione corretamente.

## ✅ O que já está implementado

### 1. **Campo de Calorias Máximas no Perfil**

- **Tabela**: `user_profiles`
- **Campo**: `max_daily_calories` (INTEGER, padrão: 2000)
- **Status**: ✅ Campo criado com valor padrão de 2000 kcal

**O que acontece:**
- Quando um novo perfil é criado, automaticamente recebe `max_daily_calories = 2000`
- Perfis existentes que não têm esse valor precisam ser atualizados (veja abaixo)

### 2. **Tabela de Resumos Diários**

- **Tabela**: `daily_calorie_summaries`
- **Campos armazenados**:
  - `calories_consumed`: Total de calorias consumidas no dia
  - `calories_burned`: Total de calorias gastas no dia
  - `max_daily_calories`: Meta de calorias do dia (do perfil)
  - `net_balance`: Saldo líquido (consumidas - gastas)
  - `deficit_surplus`: Déficit (positivo) ou Superávit (negativo)

**Status**: ✅ Tabela criada com triggers automáticos

### 3. **Cálculo Automático**

- **Função**: `calculate_and_save_daily_calorie_summary(user_id, date)`
- **Triggers automáticos**:
  - Quando uma refeição é salva/atualizada → recalcula o resumo do dia
  - Quando um check-in é salvo/atualizado → recalcula o resumo do dia
  - Quando o perfil é atualizado (mudança de max_daily_calories) → recalcula os últimos 30 dias

**Status**: ✅ Implementado com triggers

## 🔧 O que precisa ser feito

### Passo 1: Executar Migrations no Supabase

Execute as seguintes migrations na ordem:

#### 1.1. Adicionar campo max_daily_calories (se ainda não executado)
```sql
-- Migration: 20240101000007_add_max_daily_calories.sql
ALTER TABLE public.user_profiles
ADD COLUMN IF NOT EXISTS max_daily_calories INTEGER DEFAULT 2000;
```

#### 1.2. Atualizar perfis existentes
```sql
-- Migration: 20240101000008_update_existing_profiles_max_calories.sql
UPDATE public.user_profiles
SET max_daily_calories = 2000
WHERE max_daily_calories IS NULL;
```

#### 1.3. Criar tabela de resumos e triggers
```sql
-- Migration: 20240101000009_create_daily_calorie_summaries.sql
-- (Execute o arquivo completo)
```

### Passo 2: Recalcular Resumos Existentes (Opcional)

Se você já tem dados históricos e quer calcular os resumos para os últimos dias:

```sql
-- Recalcular resumos dos últimos 30 dias para todos os usuários
DO $$
DECLARE
  v_user_id UUID;
  v_date DATE;
BEGIN
  FOR v_user_id IN SELECT DISTINCT user_id FROM public.daily_meals LOOP
    FOR v_date IN 
      SELECT DISTINCT date 
      FROM public.daily_meals 
      WHERE user_id = v_user_id 
      AND date >= CURRENT_DATE - INTERVAL '30 days'
    LOOP
      PERFORM calculate_and_save_daily_calorie_summary(v_user_id, v_date);
    END LOOP;
  END LOOP;
END $$;
```

## 📊 Como funciona

### Fluxo de Dados

1. **Usuário seleciona uma refeição** (`/app/today`)
   - Frontend salva em `daily_meals` (campo `option_selected`)
   - **Trigger automático** → Recalcula e salva em `daily_calorie_summaries`

2. **Usuário insere calorias manuais**
   - Frontend salva em `daily_meals` (campos `kcal_other`, `other_description`)
   - **Trigger automático** → Recalcula e salva em `daily_calorie_summaries`

3. **Usuário faz check-in** (`/app/checkin`)
   - Frontend salva em `daily_checkins` (campo `workout_calories`)
   - **Trigger automático** → Recalcula e salva em `daily_calorie_summaries`

4. **Usuário atualiza calorias máximas** (`/app/profile`)
   - Frontend salva em `user_profiles` (campo `max_daily_calories`)
   - **Trigger automático** → Recalcula resumos dos últimos 30 dias

### Fórmulas de Cálculo

```sql
-- Saldo líquido
net_balance = calories_consumed - calories_burned

-- Déficit/Superávit
deficit_surplus = max_daily_calories - net_balance

-- Onde:
-- deficit_surplus > 0 = DÉFICIT (está abaixo da meta)
-- deficit_surplus < 0 = SUPERÁVIT (está acima da meta)
```

## 🔍 Verificações

### Verificar se os dados estão sendo salvos

```sql
-- Ver resumos dos últimos 7 dias
SELECT 
  date,
  calories_consumed,
  calories_burned,
  max_daily_calories,
  net_balance,
  deficit_surplus
FROM public.daily_calorie_summaries
WHERE user_id = auth.uid()
ORDER BY date DESC
LIMIT 7;
```

### Verificar se os triggers estão funcionando

```sql
-- Testar cálculo manual
SELECT calculate_and_save_daily_calorie_summary(
  auth.uid(),
  CURRENT_DATE
);

-- Verificar se foi salvo
SELECT * FROM public.daily_calorie_summaries
WHERE user_id = auth.uid()
AND date = CURRENT_DATE;
```

## 📝 Notas Importantes

1. **Valor Padrão**: O campo `max_daily_calories` tem valor padrão de 2000 kcal. Se o usuário não definir um valor personalizado, será usado esse padrão.

2. **Recálculo Automático**: Os resumos são recalculados automaticamente sempre que há mudanças em refeições ou check-ins. Não é necessário fazer nada manualmente.

3. **Performance**: Os triggers são otimizados e não devem causar lentidão. A tabela `daily_calorie_summaries` tem índices para consultas rápidas.

4. **Histórico**: Os resumos são mantidos indefinidamente. Você pode consultar qualquer dia histórico desde que os dados existam em `daily_meals` e `daily_checkins`.

## 🚀 Próximos Passos

Após executar as migrations:
1. ✅ Os dados serão calculados e salvos automaticamente
2. ✅ Você pode consultar resumos históricos
3. ✅ O dashboard pode usar `daily_calorie_summaries` para consultas mais rápidas
4. ✅ Relatórios mensais podem ser gerados facilmente

