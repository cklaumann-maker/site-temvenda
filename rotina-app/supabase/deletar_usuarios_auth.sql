-- =====================================================
-- DELETAR USUÁRIOS DO AUTH.USERS
-- =====================================================
-- ATENÇÃO: Esta operação é IRREVERSÍVEL!
-- Execute com cuidado e certifique-se de que deseja deletar estes usuários.
-- 
-- IMPORTANTE: Este script requer permissões de administrador.
-- Se não funcionar via SQL Editor, use o Dashboard do Supabase.
-- =====================================================

-- IDs dos usuários a serem deletados
DO $$
DECLARE
  user_ids UUID[] := ARRAY[
    'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
    'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
    '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
  ];
  current_user_id UUID;
  deleted_count INTEGER;
  i INTEGER;
BEGIN
  RAISE NOTICE '=== DELETANDO USUÁRIOS DO AUTH.USERS ===';
  RAISE NOTICE 'Total de usuários a deletar: %', array_length(user_ids, 1);
  RAISE NOTICE '';
  
  -- Verificar quais usuários existem antes de deletar
  RAISE NOTICE '=== VERIFICANDO USUÁRIOS EXISTENTES ===';
  FOR i IN 1..array_length(user_ids, 1)
  LOOP
    current_user_id := user_ids[i];
    IF EXISTS (SELECT 1 FROM auth.users WHERE id = current_user_id) THEN
      RAISE NOTICE '✅ Usuário encontrado: % - Email: %', 
        current_user_id, 
        (SELECT email FROM auth.users WHERE id = current_user_id);
    ELSE
      RAISE NOTICE '⚠️ Usuário NÃO encontrado: %', current_user_id;
    END IF;
  END LOOP;
  
  RAISE NOTICE '';
  RAISE NOTICE '=== DELETANDO USUÁRIOS ===';
  
  -- Deletar usuários do auth.users
  FOR i IN 1..array_length(user_ids, 1)
  LOOP
    current_user_id := user_ids[i];
    
    BEGIN
      DELETE FROM auth.users WHERE id = current_user_id;
      GET DIAGNOSTICS deleted_count = ROW_COUNT;
      
      IF deleted_count > 0 THEN
        RAISE NOTICE '✅ Usuário deletado: %', current_user_id;
      ELSE
        RAISE NOTICE '⚠️ Usuário não encontrado ou já deletado: %', current_user_id;
      END IF;
    EXCEPTION
      WHEN insufficient_privilege THEN
        RAISE NOTICE '❌ ERRO: Permissões insuficientes para deletar usuário %', current_user_id;
        RAISE NOTICE '   Use o Dashboard do Supabase: Authentication > Users';
      WHEN OTHERS THEN
        RAISE NOTICE '❌ ERRO ao deletar usuário %: %', current_user_id, SQLERRM;
    END;
  END LOOP;
  
  RAISE NOTICE '';
  RAISE NOTICE '=== DELEÇÃO CONCLUÍDA ===';
  RAISE NOTICE '';
  RAISE NOTICE 'Se alguns usuários não foram deletados devido a permissões,';
  RAISE NOTICE 'use o Dashboard do Supabase:';
  RAISE NOTICE '1. Acesse: https://supabase.com/dashboard';
  RAISE NOTICE '2. Vá em: Authentication > Users';
  RAISE NOTICE '3. Procure pelos emails e delete manualmente';
  
END $$;

-- =====================================================
-- VERIFICAÇÃO APÓS DELEÇÃO
-- =====================================================
-- Execute esta consulta para verificar se os usuários foram deletados

SELECT 
  id,
  email,
  created_at,
  CASE 
    WHEN email_confirmed_at IS NOT NULL THEN 'SIM' 
    ELSE 'NÃO' 
  END as email_confirmado
FROM auth.users
WHERE id IN (
  'e1c58e77-3faf-4d36-93a1-9f120e8648e9'::UUID,
  'd9702e29-f758-4abb-a7c0-454ba6b48b70'::UUID,
  '3ed462f1-c250-4a8b-8fd9-ceacf03a4949'::UUID
);

-- Se a consulta acima retornar 0 linhas, os usuários foram deletados com sucesso!

