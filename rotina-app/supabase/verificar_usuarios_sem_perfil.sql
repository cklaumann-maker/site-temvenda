-- =====================================================
-- VERIFICAR USUÁRIOS SEM PERFIL
-- =====================================================
-- Este script lista todos os usuários criados no Supabase Auth
-- que ainda não possuem um registro na tabela 'profiles'
-- =====================================================

-- 1. Listar todos os usuários sem perfil
SELECT 
  u.id,
  u.email,
  u.created_at as usuario_criado_em,
  u.email_confirmed_at as email_confirmado_em,
  u.last_sign_in_at as ultimo_login_em,
  CASE 
    WHEN p.user_id IS NULL THEN 'SEM PERFIL'
    ELSE 'COM PERFIL'
  END as status_perfil
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
WHERE p.user_id IS NULL
ORDER BY u.created_at DESC;

-- 2. Contar total de usuários sem perfil
SELECT 
  COUNT(*) as total_usuarios_sem_perfil,
  COUNT(CASE WHEN u.email_confirmed_at IS NOT NULL THEN 1 END) as usuarios_com_email_confirmado,
  COUNT(CASE WHEN u.email_confirmed_at IS NULL THEN 1 END) as usuarios_sem_email_confirmado
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
WHERE p.user_id IS NULL;

-- 3. Ver detalhes completos de usuários sem perfil (últimos 10)
SELECT 
  u.id,
  u.email,
  u.raw_user_meta_data,
  u.created_at,
  u.email_confirmed_at,
  u.last_sign_in_at,
  u.updated_at
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
WHERE p.user_id IS NULL
ORDER BY u.created_at DESC
LIMIT 10;

-- 4. Verificar se há trigger/função que cria perfil automaticamente
SELECT 
  trigger_name,
  event_manipulation,
  event_object_table,
  action_statement
FROM information_schema.triggers
WHERE event_object_table = 'users'
  AND trigger_schema = 'auth';

-- 5. Ver estrutura da tabela user_profiles (para referência)
SELECT 
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'user_profiles'
ORDER BY ordinal_position;

