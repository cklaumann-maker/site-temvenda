-- Consulta para verificar usuários cadastrados no Supabase Auth
-- Execute esta consulta no SQL Editor do Supabase Dashboard

-- 1. Ver todos os usuários cadastrados
SELECT 
  id,
  email,
  email_confirmed_at,
  created_at,
  updated_at,
  last_sign_in_at,
  confirmed_at,
  raw_user_meta_data,
  raw_app_meta_data
FROM auth.users
ORDER BY created_at DESC;

-- 2. Ver apenas usuários não confirmados
SELECT 
  id,
  email,
  created_at,
  email_confirmed_at,
  CASE 
    WHEN email_confirmed_at IS NULL THEN 'Não confirmado'
    ELSE 'Confirmado'
  END as status
FROM auth.users
WHERE email_confirmed_at IS NULL
ORDER BY created_at DESC;

-- 3. Ver usuários criados nas últimas 24 horas
SELECT 
  id,
  email,
  created_at,
  email_confirmed_at,
  EXTRACT(EPOCH FROM (NOW() - created_at))/3600 as horas_desde_criacao
FROM auth.users
WHERE created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- 4. Verificar se um email específico está cadastrado
-- Substitua 'email@exemplo.com' pelo email que você quer verificar
SELECT 
  id,
  email,
  email_confirmed_at,
  created_at,
  last_sign_in_at,
  confirmed_at
FROM auth.users
WHERE email = 'email@exemplo.com';

-- 5. Contar usuários por status
SELECT 
  CASE 
    WHEN email_confirmed_at IS NULL THEN 'Não confirmado'
    ELSE 'Confirmado'
  END as status,
  COUNT(*) as total
FROM auth.users
GROUP BY 
  CASE 
    WHEN email_confirmed_at IS NULL THEN 'Não confirmado'
    ELSE 'Confirmado'
  END;

