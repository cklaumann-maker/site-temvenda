-- =====================================================
-- VERIFICAR USUÁRIO ROOT E PERFIL
-- =====================================================
-- Execute este script para verificar se o usuário root
-- foi criado corretamente e tem perfil configurado
-- =====================================================

-- 1. Verificar se o usuário root existe em auth.users
SELECT 
  id,
  email,
  email_confirmed_at,
  created_at,
  last_sign_in_at
FROM auth.users
WHERE email = 'root@rotina.app' -- ALTERE AQUI COM O EMAIL DO ROOT
ORDER BY created_at DESC;

-- 2. Verificar se o perfil root existe e está configurado
SELECT 
  u.id as user_id,
  u.email,
  up.name,
  up.is_root,
  up.created_at as perfil_criado_em,
  up.updated_at as perfil_atualizado_em
FROM auth.users u
LEFT JOIN public.user_profiles up ON up.user_id = u.id
WHERE u.email = 'root@rotina.app' -- ALTERE AQUI COM O EMAIL DO ROOT
ORDER BY u.created_at DESC;

-- 3. Verificar todos os usuários root
SELECT 
  u.id,
  u.email,
  up.name,
  up.is_root,
  u.email_confirmed_at,
  u.last_sign_in_at
FROM auth.users u
INNER JOIN public.user_profiles up ON up.user_id = u.id
WHERE up.is_root = TRUE
ORDER BY u.created_at DESC;

-- 4. Verificar se há usuários sem perfil (incluindo root)
SELECT 
  u.id,
  u.email,
  u.email_confirmed_at,
  CASE 
    WHEN up.user_id IS NULL THEN 'SEM PERFIL'
    WHEN up.is_root = TRUE THEN 'ROOT SEM PERFIL CORRETO'
    ELSE 'COM PERFIL'
  END as status
FROM auth.users u
LEFT JOIN public.user_profiles up ON up.user_id = u.id
WHERE u.email = 'root@rotina.app' -- ALTERE AQUI COM O EMAIL DO ROOT
ORDER BY u.created_at DESC;

