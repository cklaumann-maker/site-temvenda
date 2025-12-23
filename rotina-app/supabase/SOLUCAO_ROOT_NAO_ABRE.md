# Solução: Root não consegue abrir o aplicativo

## 🔍 Diagnóstico

Se o root não consegue abrir o aplicativo após fazer login, pode ser por:

1. **Perfil não criado**: O usuário root existe em `auth.users` mas não tem perfil em `user_profiles`
2. **Perfil sem `is_root = TRUE`**: O perfil existe mas não está marcado como root
3. **Erro ao carregar dados**: Alguma query está falhando e bloqueando a renderização

## ✅ Soluções

### Passo 1: Verificar se o root tem perfil

Execute no SQL Editor do Supabase:

```sql
-- Arquivo: rotina-app/supabase/verificar_root_e_perfil.sql
```

Isso vai mostrar:
- Se o usuário root existe
- Se tem perfil criado
- Se `is_root = TRUE`

### Passo 2: Criar perfil para root (se não existir)

Execute no SQL Editor:

```sql
-- Substitua 'root@rotina.app' pelo email do root
DO $$
DECLARE
  root_email TEXT := 'root@rotina.app'; -- ALTERE AQUI
  root_user_id UUID;
BEGIN
  -- Buscar ID do usuário root
  SELECT id INTO root_user_id
  FROM auth.users
  WHERE email = root_email;
  
  IF root_user_id IS NULL THEN
    RAISE EXCEPTION 'Usuário não encontrado. Crie o usuário primeiro no Dashboard!';
  END IF;
  
  -- Criar ou atualizar perfil
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
  
  RAISE NOTICE '✅ Perfil root criado/atualizado!';
END $$;
```

### Passo 3: Criar perfis para todos os usuários sem perfil

Execute no SQL Editor:

```sql
-- Criar perfis para usuários existentes sem perfil
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
```

### Passo 4: Verificar logs do navegador

1. Abra o DevTools (F12)
2. Vá na aba Console
3. Tente fazer login como root
4. Veja se há erros no console

Procure por erros como:
- `PGRST116` - Registro não encontrado (perfil não existe)
- `permission denied` - Problema de RLS
- `network error` - Problema de conexão

### Passo 5: Verificar logs do servidor (Vercel)

1. Acesse o Vercel Dashboard
2. Vá em Deployments > Logs
3. Procure por erros relacionados ao root

## 🐛 Problemas Comuns

### Problema 1: "Perfil não encontrado"
**Solução**: Execute o Passo 2 acima para criar o perfil.

### Problema 2: "Acesso negado" ou erro de RLS
**Solução**: Verifique se a migration `20240101000010_add_root_user_support.sql` foi executada.

### Problema 3: Página fica em branco
**Solução**: 
- Verifique o console do navegador
- Verifique se há erros de JavaScript
- Tente limpar cache e cookies

### Problema 4: Redirecionamento infinito
**Solução**: 
- Verifique se o middleware está funcionando corretamente
- Verifique se há algum redirect loop

## 📋 Checklist de Verificação

- [ ] Usuário root existe em `auth.users`
- [ ] Perfil root existe em `user_profiles`
- [ ] Campo `is_root = TRUE` no perfil
- [ ] Migration `20240101000010_add_root_user_support.sql` executada
- [ ] Sem erros no console do navegador
- [ ] Sem erros nos logs do Vercel
- [ ] Cookies estão sendo salvos corretamente

## 🔧 Teste Rápido

Execute esta query para verificar tudo de uma vez:

```sql
SELECT 
  u.id,
  u.email,
  u.email_confirmed_at IS NOT NULL as email_confirmado,
  up.user_id IS NOT NULL as tem_perfil,
  up.is_root,
  CASE 
    WHEN up.user_id IS NULL THEN '❌ SEM PERFIL'
    WHEN up.is_root IS NOT TRUE THEN '⚠️ PERFIL SEM ROOT'
    ELSE '✅ OK'
  END as status
FROM auth.users u
LEFT JOIN public.user_profiles up ON up.user_id = u.id
WHERE u.email = 'root@rotina.app' -- ALTERE AQUI
ORDER BY u.created_at DESC;
```

Se o status não for `✅ OK`, execute os passos acima para corrigir.

