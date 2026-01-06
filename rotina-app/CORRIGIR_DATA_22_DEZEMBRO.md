# 📅 Corrigir Dados para 22/12/2025

## Problema
Os dados estão sendo salvos como 23/12 quando hoje é 22/12. Isso acontece porque o banco usa UTC e quando são 22:00 no Brasil, no banco já é 23/12.

---

## ✅ Solução: Script SQL Completo

### Passo 1: Obter seu User ID

Execute:
```sql
SELECT id, email FROM auth.users WHERE email = 'seu@email.com';
```

### Passo 2: Executar Script de Correção

1. No Supabase Dashboard, vá em **SQL Editor**
2. Abra o arquivo: `rotina-app/supabase/corrigir_tudo_22_dezembro.sql`
3. **Substitua** `'SEU_USER_ID_AQUI'` pelo seu UUID em **todas** as ocorrências
4. Execute o script

---

## 🔍 O Que o Script Faz

1. **Verifica** o timezone do banco
2. **Deleta** dados de 23/12 (se existirem)
3. **Move** dados de 23/12 para 22/12
4. **Recalcula** o resumo de calorias para 22/12
5. **Mostra** verificação final
6. **Verifica** se ainda há dados em 23/12

---

## ✅ Garantias para o Aplicativo

### O aplicativo já está correto ✅

O código do aplicativo usa `formatDateLocal()` que sempre usa o timezone local do navegador:

- ✅ `checkin/page.tsx` - usa `formatDateLocal(selectedDate)` ao salvar
- ✅ `TodayCalendar.tsx` - usa `formatDateLocal(selectedDate)` ao buscar
- ✅ Todos os outros arquivos também usam `formatDateLocal()`

**Isso significa que o aplicativo sempre salva e busca usando a data local correta!**

---

## 🎯 Após Executar o Script

1. **Verifique** os resultados na última query do script
2. **Acesse** o aplicativo em `/app/today`
3. **Confirme** que os dados aparecem para 22/12
4. **Teste** salvando um novo check-in ou refeição
5. **Verifique** que salva na data correta (22/12)

---

## 🔧 Se Ainda Aparecer Dados em 23/12

Execute novamente o script. Se persistir, execute manualmente:

```sql
-- Deletar tudo de 23/12
DELETE FROM public.daily_calorie_summaries
WHERE user_id = 'SEU_USER_ID'::UUID AND date = '2025-12-23';

DELETE FROM public.daily_checkins
WHERE user_id = 'SEU_USER_ID'::UUID AND date = '2025-12-23';

DELETE FROM public.daily_meals
WHERE user_id = 'SEU_USER_ID'::UUID AND date = '2025-12-23';

-- Recalcular para 22/12
SELECT public.calculate_and_save_daily_calorie_summary('SEU_USER_ID'::UUID, '2025-12-22'::DATE);
```

---

## 📋 Checklist

- [ ] User ID obtido
- [ ] Script `corrigir_tudo_22_dezembro.sql` executado
- [ ] Verificação final mostra dados em 22/12
- [ ] Não há mais dados em 23/12
- [ ] Aplicativo mostra dados de 22/12 corretamente
- [ ] Teste salvando novo dado e verifica que salva em 22/12

---

## 🎯 Resultado Esperado

Após executar o script:
- ✅ Todos os dados estarão em 22/12
- ✅ Não haverá dados em 23/12
- ✅ O aplicativo mostrará dados de 22/12
- ✅ Novos dados salvos aparecerão em 22/12

---

## ⚠️ Importante

O aplicativo **já está configurado corretamente** para usar a data local. O problema foi apenas nos dados que já estavam salvos com data errada. Após executar o script, tudo funcionará normalmente!







