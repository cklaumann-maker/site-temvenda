# 🔧 Corrigir Enrollment por Email

## ⚠️ Problema

O `auth.uid()` retorna `null` no SQL Editor porque não há contexto de autenticação. Precisamos usar o email para encontrar o `user_id`.

## ✅ Solução

Execute este SQL completo no Supabase SQL Editor:

```sql
-- Criar enrollment por email
-- IMPORTANTE: Substitua 'cesar@temvenda.com.br' pelo seu email

DO $$
DECLARE
  v_user_id UUID;
  v_program_id UUID := '00000000-0000-0000-0000-000000000002';
  v_email TEXT := 'cesar@temvenda.com.br'; -- SUBSTITUA PELO SEU EMAIL
BEGIN
  -- Buscar user_id pelo email
  SELECT id INTO v_user_id
  FROM auth.users
  WHERE email = v_email
  LIMIT 1;
  
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'Usuário com email % não encontrado. Verifique o email.', v_email;
  END IF;
  
  RAISE NOTICE 'Usuário encontrado: % (ID: %)', v_email, v_user_id;
  
  -- Criar enrollment
  INSERT INTO public.enrollments (user_id, program_id, start_date, active)
  VALUES (v_user_id, v_program_id, CURRENT_DATE, true)
  ON CONFLICT (user_id, program_id) 
  DO UPDATE SET
    active = true,
    start_date = COALESCE(excluded.start_date, CURRENT_DATE);
  
  RAISE NOTICE 'Enrollment criado/atualizado com sucesso!';
  
  -- Corrigir templates
  UPDATE plan_templates
  SET meal_type = 'pre'
  WHERE program_id = v_program_id
    AND meal_type = 'lanche_manha';
  
  RAISE NOTICE 'Templates corrigidos!';
  
  -- Deletar refeições antigas
  DELETE FROM public.daily_meals WHERE user_id = v_user_id;
  
  RAISE NOTICE 'Refeições antigas deletadas!';
  
  -- Regerar refeições
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE);
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE + 1);
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE + 2);
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE + 3);
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE + 4);
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE + 5);
  PERFORM public.generate_daily_meals(v_user_id, CURRENT_DATE + 6);
  
  RAISE NOTICE 'Refeições regeradas!';
END $$;
```

## 📋 Passos

1. **Substitua o email** na linha `v_email TEXT := 'cesar@temvenda.com.br';` pelo seu email
2. **Execute o SQL** completo acima
3. **Verifique o resultado** executando este SQL:

```sql
-- Verificar enrollment criado
SELECT 
  e.id,
  e.user_id,
  u.email,
  e.program_id,
  e.start_date,
  e.active,
  (SELECT COUNT(*) FROM daily_meals WHERE user_id = e.user_id) as total_refeicoes
FROM public.enrollments e
JOIN auth.users u ON u.id = e.user_id
WHERE u.email = 'cesar@temvenda.com.br' -- SUBSTITUA PELO SEU EMAIL
ORDER BY e.created_at DESC;

-- Verificar refeições geradas
SELECT 
  dm.date,
  dm.meal_type,
  dm.opt1,
  dm.opt2,
  dm.opt3,
  dm.avoid
FROM daily_meals dm
JOIN auth.users u ON u.id = dm.user_id
WHERE u.email = 'cesar@temvenda.com.br' -- SUBSTITUA PELO SEU EMAIL
  AND dm.date >= CURRENT_DATE
ORDER BY dm.date, 
  CASE dm.meal_type
    WHEN 'pre' THEN 1
    WHEN 'post' THEN 2
    WHEN 'cafe' THEN 3
    WHEN 'almoco' THEN 4
    WHEN 'lanche_tarde' THEN 5
    WHEN 'jantar' THEN 6
    ELSE 999
  END;
```

## 🔍 Se não souber seu email

Execute este SQL para listar todos os usuários:

```sql
SELECT 
  id,
  email,
  created_at
FROM auth.users
ORDER BY created_at DESC;
```

Depois use o email correto no script acima.

---

**Execute o SQL e me informe o resultado!** ✅

