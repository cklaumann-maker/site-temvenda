-- =====================================================
-- DELETAR USUÁRIOS ESPECÍFICOS
-- =====================================================
-- ATENÇÃO: Esta operação é IRREVERSÍVEL!
-- Execute com cuidado e certifique-se de que deseja deletar estes usuários.
-- =====================================================

-- IDs dos usuários a serem deletados
DO $$
DECLARE
  user_ids UUID[] := ARRAY[
    'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
    'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
    '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
  ];
  user_id UUID;
  deleted_count INTEGER;
BEGIN
  RAISE NOTICE '=== INICIANDO DELEÇÃO DE USUÁRIOS ===';
  RAISE NOTICE 'Total de usuários a deletar: %', array_length(user_ids, 1);
  
  -- Verificar quais usuários existem antes de deletar
  RAISE NOTICE '';
  RAISE NOTICE '=== VERIFICANDO USUÁRIOS EXISTENTES ===';
  FOR user_id IN SELECT unnest(user_ids)
  LOOP
    IF EXISTS (SELECT 1 FROM auth.users WHERE id = user_id) THEN
      RAISE NOTICE '✅ Usuário encontrado: % - Email: %', 
        user_id, 
        (SELECT email FROM auth.users WHERE id = user_id);
    ELSE
      RAISE NOTICE '⚠️ Usuário NÃO encontrado: %', user_id;
    END IF;
  END LOOP;
  
  RAISE NOTICE '';
  RAISE NOTICE '=== DELETANDO REGISTROS RELACIONADOS ===';
  
  -- 1. Deletar resumos de calorias diárias
  FOR user_id IN SELECT unnest(user_ids)
  LOOP
    DELETE FROM public.daily_calorie_summaries WHERE user_id = user_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    IF deleted_count > 0 THEN
      RAISE NOTICE '  Deletados % resumos de calorias para usuário %', deleted_count, user_id;
    END IF;
  END LOOP;
  
  -- 2. Deletar refeições diárias
  FOR user_id IN SELECT unnest(user_ids)
  LOOP
    DELETE FROM public.daily_meals WHERE user_id = user_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    IF deleted_count > 0 THEN
      RAISE NOTICE '  Deletadas % refeições para usuário %', deleted_count, user_id;
    END IF;
  END LOOP;
  
  -- 3. Deletar check-ins diários
  FOR user_id IN SELECT unnest(user_ids)
  LOOP
    DELETE FROM public.daily_checkins WHERE user_id = user_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    IF deleted_count > 0 THEN
      RAISE NOTICE '  Deletados % check-ins para usuário %', deleted_count, user_id;
    END IF;
  END LOOP;
  
  -- 4. Deletar enrollments (matrículas)
  FOR user_id IN SELECT unnest(user_ids)
  LOOP
    DELETE FROM public.enrollments WHERE user_id = user_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    IF deleted_count > 0 THEN
      RAISE NOTICE '  Deletadas % matrículas para usuário %', deleted_count, user_id;
    END IF;
  END LOOP;
  
  -- 5. Deletar perfis de usuário
  FOR user_id IN SELECT unnest(user_ids)
  LOOP
    DELETE FROM public.user_profiles WHERE user_id = user_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    IF deleted_count > 0 THEN
      RAISE NOTICE '  Deletado perfil para usuário %', user_id;
    END IF;
  END LOOP;
  
  RAISE NOTICE '';
  RAISE NOTICE '=== DELETANDO USUÁRIOS DO AUTH.USERS ===';
  RAISE NOTICE '⚠️ ATENÇÃO: Esta operação requer permissões de administrador!';
  RAISE NOTICE '';
  RAISE NOTICE 'Para deletar os usuários de auth.users, você precisa:';
  RAISE NOTICE '1. Usar a API do Supabase com service_role_key';
  RAISE NOTICE '2. Ou usar o Dashboard do Supabase: Authentication > Users';
  RAISE NOTICE '';
  RAISE NOTICE 'Os registros relacionados já foram deletados acima.';
  RAISE NOTICE '=== DELEÇÃO DE REGISTROS RELACIONADOS CONCLUÍDA ===';
  
END $$;

-- =====================================================
-- VERIFICAÇÃO APÓS DELEÇÃO
-- =====================================================
-- Execute esta consulta para verificar se ainda há registros relacionados

SELECT 
  'daily_calorie_summaries' as tabela,
  COUNT(*) as registros_restantes
FROM public.daily_calorie_summaries
WHERE user_id IN (
  'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
  'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
  '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
)

UNION ALL

SELECT 
  'daily_meals' as tabela,
  COUNT(*) as registros_restantes
FROM public.daily_meals
WHERE user_id IN (
  'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
  'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
  '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
)

UNION ALL

SELECT 
  'daily_checkins' as tabela,
  COUNT(*) as registros_restantes
FROM public.daily_checkins
WHERE user_id IN (
  'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
  'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
  '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
)

UNION ALL

SELECT 
  'enrollments' as tabela,
  COUNT(*) as registros_restantes
FROM public.enrollments
WHERE user_id IN (
  'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
  'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
  '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
)

UNION ALL

SELECT 
  'user_profiles' as tabela,
  COUNT(*) as registros_restantes
FROM public.user_profiles
WHERE user_id IN (
  'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
  'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
  '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
);

-- =====================================================
-- INSTRUÇÕES PARA DELETAR USUÁRIOS DO AUTH.USERS
-- =====================================================
-- 
-- O script acima deleta todos os registros relacionados nas tabelas públicas,
-- mas para deletar os usuários de auth.users, você precisa:
--
-- OPÇÃO 1: Via Supabase Dashboard (RECOMENDADO)
-- 1. Acesse: https://supabase.com/dashboard
-- 2. Vá em: Authentication > Users
-- 3. Procure pelos emails dos usuários
-- 4. Clique nos três pontos (...) ao lado de cada usuário
-- 5. Selecione "Delete user"
--
-- OPÇÃO 2: Via API (se tiver service_role_key)
-- Use a API do Supabase Admin para deletar:
-- DELETE /auth/v1/admin/users/{user_id}
--
-- OPÇÃO 3: Via SQL (requer permissões especiais)
-- DELETE FROM auth.users WHERE id IN (
--   'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
--   'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
--   '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
-- );
--
-- =====================================================

