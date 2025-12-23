# 📅 Corrigir Dados Salvos com Data Errada

## Problema
Os dados de hoje foram salvos com a data de ontem. Precisamos mover esses dados para a data correta (hoje).

---

## ✅ Solução: Script SQL

Criei scripts SQL para corrigir os dados. Siga os passos abaixo:

### 🎯 Passo 1: Obter seu User ID

1. Acesse o Supabase Dashboard
2. Vá em **SQL Editor**
3. Execute o script `OBTER_USER_ID.sql`:
   - Substitua `'seu@email.com'` pelo seu email
   - Execute e copie o `user_id` (UUID)

**OU** acesse diretamente:
- **Authentication** > **Users**
- Encontre seu usuário e copie o **UUID**

### 🎯 Passo 2: Executar Script de Correção

1. No **SQL Editor**, abra o arquivo `corrigir_data_hoje_com_userid.sql`
2. **Substitua** `'SEU_USER_ID_AQUI'` pelo UUID obtido no passo 1
3. Execute o script
4. Verifique as mensagens de NOTICE para confirmar a correção

### 🔧 Opção 2: Script com User ID Manual

Se preferir usar seu User ID manualmente:

1. Obtenha seu User ID:
   - Vá em **Authentication** > **Users**
   - Copie seu **UUID** (ex: `9ca6a4e9-4bdd-4cdf-9426-813e10ca6280`)

2. Execute o script:
   - Vá em **SQL Editor**
   - Abra `rotina-app/supabase/corrigir_data_hoje.sql`
   - Substitua `'SEU_USER_ID'` pelo seu UUID em **todas** as ocorrências
   - Execute o script

### Passo 3: Verificar Resultado

O script mostra:
- Quantos registros foram encontrados com data de ontem
- Quantos foram atualizados
- Os dados finais após a correção

---

## 🔍 O Que o Script Faz

1. **Verifica** quais dados estão com data de ontem
2. **Atualiza** `daily_meals` de ontem para hoje (se não houver conflito)
3. **Atualiza** `daily_checkins` de ontem para hoje (se não houver conflito)
4. **Atualiza** `daily_calorie_summaries` de ontem para hoje (se não houver conflito)
5. **Recalcula** o resumo de calorias para hoje
6. **Mostra** o resultado final

---

## ⚠️ Importante

- O script **não sobrescreve** dados que já existem para hoje
- Se já houver dados para hoje, os dados de ontem serão mantidos
- Se quiser **substituir** os dados de hoje pelos de ontem, use a versão alternativa abaixo

---

## 🔄 Versão Alternativa: Substituir Dados de Hoje

Se você quiser **substituir** os dados de hoje pelos dados de ontem (ao invés de apenas mover), use este script:

```sql
-- ATENÇÃO: Isso vai DELETAR os dados de hoje e mover os de ontem!

-- 1. Deletar dados de hoje (se existirem)
DELETE FROM public.daily_meals
WHERE user_id = 'SEU_USER_ID'::UUID
  AND date = CURRENT_DATE;

DELETE FROM public.daily_checkins
WHERE user_id = 'SEU_USER_ID'::UUID
  AND date = CURRENT_DATE;

DELETE FROM public.daily_calorie_summaries
WHERE user_id = 'SEU_USER_ID'::UUID
  AND date = CURRENT_DATE;

-- 2. Mover dados de ontem para hoje
UPDATE public.daily_meals
SET date = CURRENT_DATE,
    updated_at = NOW()
WHERE user_id = 'SEU_USER_ID'::UUID
  AND date = CURRENT_DATE - INTERVAL '1 day';

UPDATE public.daily_checkins
SET date = CURRENT_DATE,
    updated_at = NOW()
WHERE user_id = 'SEU_USER_ID'::UUID
  AND date = CURRENT_DATE - INTERVAL '1 day';

UPDATE public.daily_calorie_summaries
SET date = CURRENT_DATE,
    updated_at = NOW()
WHERE user_id = 'SEU_USER_ID'::UUID
  AND date = CURRENT_DATE - INTERVAL '1 day';

-- 3. Recalcular resumo
SELECT public.calculate_and_save_daily_calorie_summary('SEU_USER_ID'::UUID, CURRENT_DATE);
```

---

## 📋 Checklist

- [ ] User ID obtido do Supabase
- [ ] Script atualizado com seu User ID
- [ ] Script executado no SQL Editor
- [ ] Resultados verificados
- [ ] Dados de hoje aparecem corretamente no aplicativo

---

## 🎯 Após Corrigir

1. Acesse o aplicativo
2. Vá em `/app/today`
3. Verifique se os dados de hoje estão corretos
4. Se ainda houver problemas, verifique o timezone do banco de dados

---

## 🔧 Verificar Timezone do Banco

Se o problema continuar, pode ser um problema de timezone:

```sql
-- Verificar timezone atual
SHOW timezone;

-- Verificar data atual no banco
SELECT CURRENT_DATE, NOW();

-- Se necessário, ajustar timezone (exemplo para Brasil)
SET timezone = 'America/Sao_Paulo';
```

---

## 📝 Arquivos dos Scripts

- **Obter User ID**: `rotina-app/OBTER_USER_ID.sql` (execute primeiro)
- **Script de Correção**: `rotina-app/supabase/corrigir_data_hoje_com_userid.sql` (use este)
- **Script Simplificado** (pode não funcionar no SQL Editor): `rotina-app/supabase/corrigir_data_hoje_simples.sql`

---

## ⚡ Execução Rápida

1. Acesse: https://supabase.com/dashboard
2. Faça login
3. Vá em **SQL Editor** > **New Query**
4. Cole o conteúdo de `corrigir_data_hoje_simples.sql`
5. Clique em **Run**
6. Pronto! ✅

