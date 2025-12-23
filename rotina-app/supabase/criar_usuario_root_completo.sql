-- =====================================================
-- CRIAR USUÁRIO ROOT COMPLETO (TENTATIVA AUTOMÁTICA)
-- =====================================================
-- Este script tenta criar o usuário root automaticamente
-- usando a função auth.users diretamente.
-- 
-- ⚠️ ATENÇÃO: Isso pode não funcionar sem permissões especiais.
-- Se falhar, use o script criar_usuario_root.sql após criar
-- o usuário manualmente no Dashboard.
-- =====================================================

DO $$
DECLARE
  root_email TEXT := 'root@rotina.app';
  root_password TEXT := 'root';
  root_user_id UUID;
  user_already_exists BOOLEAN := FALSE;
BEGIN
  RAISE NOTICE '=== CRIANDO USUÁRIO ROOT AUTOMATICAMENTE ===';
  RAISE NOTICE 'Email: %', root_email;
  RAISE NOTICE '';
  
  -- Verificar se o usuário já existe
  SELECT id INTO root_user_id
  FROM auth.users
  WHERE email = root_email;
  
  IF root_user_id IS NOT NULL THEN
    user_already_exists := TRUE;
    RAISE NOTICE '✅ Usuário já existe! ID: %', root_user_id;
  ELSE
    RAISE NOTICE '⚠️ Tentando criar usuário...';
    RAISE NOTICE '';
    RAISE NOTICE '❌ Não é possível criar usuário diretamente via SQL sem service_role_key.';
    RAISE NOTICE '';
    RAISE NOTICE '📋 SOLUÇÃO: Crie o usuário manualmente:';
    RAISE NOTICE '1. Acesse: https://supabase.com/dashboard';
    RAISE NOTICE '2. Vá em: Authentication > Users';
    RAISE NOTICE '3. Clique em: "Add user"';
    RAISE NOTICE '4. Preencha:';
    RAISE NOTICE '   - Email: %', root_email;
    RAISE NOTICE '   - Password: %', root_password;
    RAISE NOTICE '   - Auto Confirm User: ✅ SIM';
    RAISE NOTICE '5. Clique em: "Create user"';
    RAISE NOTICE '6. Execute o script: criar_usuario_root.sql';
    RAISE EXCEPTION 'Crie o usuário manualmente primeiro. Veja instruções acima.';
  END IF;
  
  -- Se chegou aqui, o usuário existe - criar/atualizar perfil
  RAISE NOTICE '';
  RAISE NOTICE '=== CRIANDO/ATUALIZANDO PERFIL ROOT ===';
  
  INSERT INTO public.user_profiles (
    user_id,
    name,
    is_root,
    max_daily_calories
  ) VALUES (
    root_user_id,
    'Root Administrator',
    TRUE,
    2000
  )
  ON CONFLICT (user_id) 
  DO UPDATE SET
    is_root = TRUE,
    name = COALESCE(user_profiles.name, 'Root Administrator'),
    updated_at = NOW();
  
  RAISE NOTICE '✅ Perfil root criado/atualizado com sucesso!';
  RAISE NOTICE '';
  RAISE NOTICE '=== CONFIGURAÇÃO CONCLUÍDA ===';
  RAISE NOTICE 'Usuário root configurado:';
  RAISE NOTICE '  Email: %', root_email;
  RAISE NOTICE '  ID: %', root_user_id;
  RAISE NOTICE '  is_root: TRUE';
  
END $$;

-- =====================================================
-- VERIFICAÇÃO FINAL
-- =====================================================
SELECT 
  u.id,
  u.email,
  up.name,
  up.is_root,
  u.email_confirmed_at IS NOT NULL as email_confirmado
FROM auth.users u
INNER JOIN public.user_profiles up ON up.user_id = u.id
WHERE up.is_root = TRUE;

