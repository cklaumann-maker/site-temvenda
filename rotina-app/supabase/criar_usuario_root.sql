-- =====================================================
-- CRIAR USUÁRIO ROOT
-- =====================================================
-- Este script configura um usuário existente como root
-- IMPORTANTE: Você precisa criar o usuário primeiro!
-- =====================================================

-- ⚠️ ANTES DE EXECUTAR ESTE SCRIPT:
-- 
-- OPÇÃO 1: Criar via Dashboard (RECOMENDADO)
-- 1. Acesse: https://supabase.com/dashboard
-- 2. Vá em: Authentication > Users
-- 3. Clique em: "Add user"
-- 4. Preencha:
--    - Email: root@rotina.app
--    - Password: root
--    - Auto Confirm User: ✅ SIM
-- 5. Clique em: "Create user"
--
-- OPÇÃO 2: Criar via SQL (veja script criar_usuario_root_completo.sql)
-- Execute o script criar_usuario_root_completo.sql que cria tudo automaticamente

DO $$
DECLARE
  root_email TEXT := 'root@rotina.app'; -- ALTERE AQUI COM O EMAIL DO ROOT
  root_user_id UUID;
  user_exists BOOLEAN := FALSE;
BEGIN
  RAISE NOTICE '=== VERIFICANDO USUÁRIO ROOT ===';
  RAISE NOTICE 'Procurando usuário com email: %', root_email;
  
  -- Buscar ID do usuário root pelo email
  SELECT id INTO root_user_id
  FROM auth.users
  WHERE email = root_email;
  
  IF root_user_id IS NULL THEN
    RAISE NOTICE '';
    RAISE NOTICE '❌ ERRO: Usuário com email % não encontrado!', root_email;
    RAISE NOTICE '';
    RAISE NOTICE '📋 INSTRUÇÕES:';
    RAISE NOTICE '1. Acesse: https://supabase.com/dashboard';
    RAISE NOTICE '2. Vá em: Authentication > Users';
    RAISE NOTICE '3. Clique em: "Add user"';
    RAISE NOTICE '4. Preencha:';
    RAISE NOTICE '   - Email: %', root_email;
    RAISE NOTICE '   - Password: root (ou a senha que você preferir)';
    RAISE NOTICE '   - Auto Confirm User: ✅ SIM';
    RAISE NOTICE '5. Clique em: "Create user"';
    RAISE NOTICE '6. Execute este script novamente';
    RAISE NOTICE '';
    RAISE NOTICE 'OU execute o script: criar_usuario_root_completo.sql';
    RAISE EXCEPTION 'Usuário não encontrado. Siga as instruções acima.';
  END IF;
  
  user_exists := TRUE;
  RAISE NOTICE '✅ Usuário encontrado!';
  RAISE NOTICE '   ID: %', root_user_id;
  RAISE NOTICE '';
  RAISE NOTICE '=== CRIANDO/ATUALIZANDO PERFIL ROOT ===';
  
  -- Criar ou atualizar perfil do root
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
  RAISE NOTICE '';
  RAISE NOTICE 'Agora você pode fazer login com:';
  RAISE NOTICE '  Email: %', root_email;
  RAISE NOTICE '  Senha: (a senha que você definiu)';
  RAISE NOTICE '';
  RAISE NOTICE 'E acessar a tela de admin em: /app/admin/users';
  
END $$;

-- =====================================================
-- VERIFICAR SE ROOT FOI CRIADO CORRETAMENTE
-- =====================================================
SELECT 
  u.id,
  u.email,
  up.name,
  up.is_root,
  up.created_at
FROM auth.users u
INNER JOIN public.user_profiles up ON up.user_id = u.id
WHERE up.is_root = TRUE;

