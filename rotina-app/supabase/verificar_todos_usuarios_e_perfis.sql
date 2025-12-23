-- =====================================================
-- VERIFICAR TODOS OS USUÁRIOS E PERFIS CADASTRADOS
-- =====================================================
-- Este script lista todos os usuários do auth.users
-- e seus perfis correspondentes na tabela user_profiles
-- =====================================================

-- 1. VISÃO GERAL: Todos os usuários com status de perfil
SELECT 
  u.id as user_id,
  u.email,
  u.created_at as usuario_criado_em,
  u.email_confirmed_at as email_confirmado_em,
  u.last_sign_in_at as ultimo_login_em,
  CASE 
    WHEN u.email_confirmed_at IS NOT NULL THEN '✅ Confirmado'
    ELSE '❌ Não Confirmado'
  END as status_email,
  CASE 
    WHEN p.user_id IS NOT NULL THEN '✅ Com Perfil'
    ELSE '❌ Sem Perfil'
  END as status_perfil,
  p.name as nome_perfil,
  p.max_daily_calories as calorias_maximas
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
ORDER BY u.created_at DESC;

-- 2. CONTAGEM GERAL
SELECT 
  COUNT(DISTINCT u.id) as total_usuarios,
  COUNT(DISTINCT CASE WHEN u.email_confirmed_at IS NOT NULL THEN u.id END) as usuarios_confirmados,
  COUNT(DISTINCT CASE WHEN u.email_confirmed_at IS NULL THEN u.id END) as usuarios_nao_confirmados,
  COUNT(DISTINCT p.user_id) as usuarios_com_perfil,
  COUNT(DISTINCT CASE WHEN p.user_id IS NULL THEN u.id END) as usuarios_sem_perfil
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id;

-- 3. TODOS OS IDs DE USUÁRIOS CADASTRADOS
SELECT 
  id as user_id,
  email,
  created_at
FROM auth.users
ORDER BY created_at DESC;

-- 4. TODOS OS PERFIS CADASTRADOS COM DETALHES
SELECT 
  up.user_id,
  u.email,
  up.name as nome,
  up.phone as telefone,
  up.cpf,
  up.city as cidade,
  up.state as estado,
  up.height_cm as altura_cm,
  up.weight_kg as peso_kg,
  up.max_daily_calories as calorias_maximas_dia,
  up.created_at as perfil_criado_em,
  up.updated_at as perfil_atualizado_em
FROM public.user_profiles up
INNER JOIN auth.users u ON u.id = up.user_id
ORDER BY up.created_at DESC;

-- 5. USUÁRIOS SEM PERFIL (detalhado)
SELECT 
  u.id as user_id,
  u.email,
  u.created_at as usuario_criado_em,
  u.email_confirmed_at as email_confirmado_em,
  u.last_sign_in_at as ultimo_login_em,
  CASE 
    WHEN u.email_confirmed_at IS NOT NULL THEN '✅ Confirmado'
    ELSE '❌ Não Confirmado'
  END as status_email
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
WHERE p.user_id IS NULL
ORDER BY u.created_at DESC;

-- 6. USUÁRIOS COM PERFIL MAS SEM EMAIL CONFIRMADO
SELECT 
  u.id as user_id,
  u.email,
  u.created_at as usuario_criado_em,
  u.email_confirmed_at as email_confirmado_em,
  p.name as nome_perfil,
  p.max_daily_calories as calorias_maximas
FROM auth.users u
INNER JOIN public.user_profiles p ON p.user_id = u.id
WHERE u.email_confirmed_at IS NULL
ORDER BY u.created_at DESC;

-- 7. RESUMO POR DATA DE CRIAÇÃO (últimos 30 dias)
SELECT 
  DATE(u.created_at) as data_criacao,
  COUNT(*) as total_usuarios,
  COUNT(CASE WHEN u.email_confirmed_at IS NOT NULL THEN 1 END) as usuarios_confirmados,
  COUNT(CASE WHEN p.user_id IS NOT NULL THEN 1 END) as usuarios_com_perfil
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
WHERE u.created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(u.created_at)
ORDER BY data_criacao DESC;

-- 8. LISTA COMPACTA: IDs, Emails e Status
SELECT 
  u.id,
  u.email,
  CASE WHEN u.email_confirmed_at IS NOT NULL THEN 'SIM' ELSE 'NÃO' END as email_confirmado,
  CASE WHEN p.user_id IS NOT NULL THEN 'SIM' ELSE 'NÃO' END as tem_perfil
FROM auth.users u
LEFT JOIN public.user_profiles p ON p.user_id = u.id
ORDER BY u.created_at DESC;

