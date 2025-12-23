-- =====================================================
-- CRIAR PERFIL AUTOMATICAMENTE PARA ROOT (TRIGGER)
-- =====================================================
-- Este script cria um trigger que automaticamente cria
-- um perfil básico quando um usuário root faz login pela primeira vez
-- =====================================================

-- Função para criar perfil automaticamente se não existir
CREATE OR REPLACE FUNCTION public.ensure_user_profile()
RETURNS TRIGGER AS $$
BEGIN
  -- Verificar se o usuário já tem perfil
  IF NOT EXISTS (
    SELECT 1 FROM public.user_profiles 
    WHERE user_id = NEW.id
  ) THEN
    -- Criar perfil básico
    INSERT INTO public.user_profiles (
      user_id,
      name,
      is_root,
      max_daily_calories
    ) VALUES (
      NEW.id,
      COALESCE(NEW.raw_user_meta_data->>'name', 'Usuário'),
      FALSE, -- Por padrão não é root, será atualizado manualmente
      2000
    );
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Remover trigger antigo se existir
DROP TRIGGER IF EXISTS trigger_ensure_user_profile ON auth.users;

-- Criar trigger que executa após inserção de usuário
CREATE TRIGGER trigger_ensure_user_profile
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.ensure_user_profile();

-- Comentário
COMMENT ON FUNCTION public.ensure_user_profile() IS 'Cria perfil automaticamente quando um novo usuário é criado no auth.users';

-- =====================================================
-- CRIAR PERFIL PARA USUÁRIOS EXISTENTES SEM PERFIL
-- =====================================================
-- Execute esta parte para criar perfis para usuários que já existem
-- mas não têm perfil ainda

INSERT INTO public.user_profiles (
  user_id,
  name,
  is_root,
  max_daily_calories
)
SELECT 
  u.id,
  COALESCE(u.raw_user_meta_data->>'name', 'Usuário'),
  FALSE,
  2000
FROM auth.users u
WHERE NOT EXISTS (
  SELECT 1 FROM public.user_profiles up
  WHERE up.user_id = u.id
)
ON CONFLICT (user_id) DO NOTHING;

-- Verificar quantos perfis foram criados
SELECT COUNT(*) as perfis_criados
FROM public.user_profiles
WHERE created_at > NOW() - INTERVAL '1 minute';

