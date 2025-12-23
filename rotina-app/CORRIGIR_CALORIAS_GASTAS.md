# 🔥 Corrigir Calorias Gastas (Workout Calories)

## Problema
As calorias gastas (workout_calories) de ontem não foram movidas para hoje junto com os outros dados.

---

## ✅ Solução: Script SQL Específico

### Passo 1: Obter seu User ID

Se ainda não tem, execute:
```sql
SELECT id, email FROM auth.users WHERE email = 'seu@email.com';
```

### Passo 2: Executar Script de Correção

1. No Supabase Dashboard, vá em **SQL Editor**
2. Abra o arquivo: `rotina-app/supabase/corrigir_calorias_gastas.sql`
3. **Substitua** `'SEU_USER_ID_AQUI'` pelo seu UUID
4. Execute o script

---

## 🔍 O Que o Script Faz

1. **Verifica** se há calorias gastas em ontem
2. **Cria ou atualiza** o check-in de hoje com essas calorias
3. **Recalcula** o resumo de calorias para hoje

---

## ✅ Garantias para Próximos Dias

### 1. Código Já Corrigido ✅

O código já está usando `formatDateLocal()` que usa timezone local:
- ✅ `checkin/page.tsx` - usa `formatDateLocal(selectedDate)`
- ✅ `TodayCalendar.tsx` - usa `formatDateLocal(selectedDate)`
- ✅ `TodaySummary.tsx` - usa `getTodayLocal()`

### 2. Verificação de Timezone

O sistema agora sempre usa a data local do navegador, não UTC. Isso garante que:
- A data sempre será a correta independente do timezone
- Não haverá mais diferença de um dia

### 3. Scripts de Correção Disponíveis

Se acontecer novamente (improvável), você tem scripts prontos:
- `corrigir_data_hoje_com_userid.sql` - corrige todos os dados
- `corrigir_calorias_gastas.sql` - corrige apenas calorias gastas

---

## 📋 Checklist

- [ ] User ID obtido
- [ ] Script `corrigir_calorias_gastas.sql` executado
- [ ] Calorias gastas aparecem corretamente em `/app/today`
- [ ] Resumo de calorias recalculado corretamente

---

## 🎯 Após Corrigir

1. Acesse `/app/today`
2. Verifique se as calorias gastas aparecem corretamente
3. Verifique se o resumo de calorias está correto
4. Teste salvando um novo check-in para garantir que funciona

---

## 🔧 Se Ainda Não Funcionar

Execute também o script completo:
```sql
-- Execute o corrigir_data_hoje_com_userid.sql novamente
-- Isso garante que todos os dados estejam sincronizados
```

