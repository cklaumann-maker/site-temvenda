# 🔧 Gerar Refeições no Calendário

## ❌ Problema

As refeições não aparecem no calendário porque:
- ✅ As refeições estão em `plan_templates` (template geral)
- ❌ Mas não foram geradas em `daily_meals` (refeições específicas do usuário)
- ❌ O usuário precisa ter um enrollment ativo
- ❌ A função precisa ser chamada para gerar as refeições

---

## ✅ Solução Rápida

### Opção 1: Script SQL (Recomendado)

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/gerar_refeicoes_usuario.sql`
4. **Substitua** `'SEU_EMAIL_AQUI'` pelo email que você usou para fazer login
5. **Execute** (Run)

Este script vai:
- ✅ Encontrar seu usuário pelo email
- ✅ Criar seu perfil se não existir
- ✅ Criar enrollment no programa demo
- ✅ Gerar refeições para os próximos 30 dias

---

### Opção 2: Usar a Função RPC Diretamente

Execute este SQL substituindo pelo seu email:

```sql
-- 1. Encontrar seu user_id
SELECT id, email FROM auth.users WHERE email = 'seu@email.com';

-- 2. Criar enrollment (substitua USER_ID pelo ID acima)
INSERT INTO public.enrollments (user_id, program_id, start_date, active)
VALUES (
  'USER_ID_AQUI',
  '00000000-0000-0000-0000-000000000002',
  CURRENT_DATE,
  true
)
ON CONFLICT (user_id, program_id) WHERE active = true DO UPDATE
SET start_date = CURRENT_DATE;

-- 3. Gerar refeições para hoje (substitua USER_ID)
SELECT public.generate_daily_meals(
  'USER_ID_AQUI'::UUID,
  CURRENT_DATE
);

-- 4. Gerar refeições para os próximos 30 dias
DO $$
DECLARE
  v_user_id UUID := 'USER_ID_AQUI'::UUID; -- ⚠️ ALTERE AQUI
  v_date DATE;
BEGIN
  FOR i IN 0..29 LOOP
    v_date := CURRENT_DATE + i;
    PERFORM public.generate_daily_meals(v_user_id, v_date);
  END LOOP;
END $$;
```

---

## 🔍 Verificar se Funcionou

Execute este SQL:

```sql
-- Verificar suas refeições (substitua pelo seu email)
SELECT 
  dm.date,
  dm.meal_type,
  dm.opt1,
  dm.option_selected
FROM public.daily_meals dm
JOIN auth.users u ON u.id = dm.user_id
WHERE u.email = 'seu@email.com'
ORDER BY dm.date, dm.meal_type
LIMIT 20;
```

**Deve mostrar:** Refeições para os próximos dias

---

## 🧪 Teste no App

1. **Recarregue a página:** http://localhost:3001/app/today
2. **Você deve ver:**
   - ✅ Calendário com dias marcados
   - ✅ Refeições do dia atual na seção inferior
   - ✅ Checkboxes funcionando

---

## ⚠️ Se Ainda Não Funcionar

### Problema: "User is not enrolled in any program"

Execute este SQL primeiro:

```sql
-- Criar enrollment (substitua pelo seu email)
DO $$
DECLARE
  v_user_id UUID;
  v_email TEXT := 'seu@email.com'; -- ⚠️ ALTERE AQUI
BEGIN
  SELECT id INTO v_user_id FROM auth.users WHERE email = v_email;
  
  INSERT INTO public.enrollments (user_id, program_id, start_date, active)
  VALUES (
    v_user_id,
    '00000000-0000-0000-0000-000000000002',
    CURRENT_DATE,
    true
  )
  ON CONFLICT (user_id, program_id) WHERE active = true DO NOTHING;
  
  RAISE NOTICE '✅ Enrollment criado para: %', v_email;
END $$;
```

---

## 📋 Ordem Correta

1. ✅ **Primeiro:** Execute `gerar_refeicoes_usuario.sql` (substitua o email)
2. ✅ **Depois:** Recarregue o app
3. ✅ **Por último:** Veja as refeições no calendário

---

## 🎯 Arquivos Criados

1. ✅ `supabase/gerar_refeicoes_usuario.sql` (NOVO)
   - Script completo para gerar refeições
   - Cria enrollment automaticamente
   - Gera refeições para 30 dias

2. ✅ `apps/web/src/app/app/today/TodayCalendar.tsx` (ATUALIZADO)
   - Agora tenta gerar refeições automaticamente ao carregar

---

Execute o script `gerar_refeicoes_usuario.sql` substituindo o email e depois recarregue o app! 🚀

