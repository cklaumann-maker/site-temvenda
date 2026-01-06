# ✅ Correção: Função is_root_user() Não Existe

## 🔧 Problema

Ao executar a migration `20240101000013_fix_user_profiles_rls_recursion.sql`, você recebeu o erro:

```
ERROR: 42883: function public.is_root_user() does not exist
```

## ✅ Solução

A migration foi corrigida! Agora a função `is_root_user()` é criada **ANTES** das políticas RLS que a utilizam.

## 📋 Execute Novamente

Execute a migration corrigida no Supabase SQL Editor:

```sql
-- Arquivo: rotina-app/supabase/migrations/20240101000013_fix_user_profiles_rls_recursion.sql
```

A ordem agora está correta:
1. ✅ **PRIMEIRO**: Cria a função `is_root_user()`
2. ✅ **DEPOIS**: Remove políticas antigas
3. ✅ **DEPOIS**: Cria novas políticas usando a função

## 🔍 Verificar se Funcionou

Após executar, verifique se a função foi criada:

```sql
SELECT 
  proname as nome_funcao,
  prosrc as codigo
FROM pg_proc 
WHERE proname = 'is_root_user';
```

Você deve ver a função listada.

## 🧪 Testar

Depois de executar a migration, teste:

1. Acesse `/app/profile`
2. Preencha os dados do perfil
3. Clique em "Salvar Alterações"
4. **Não deve mais dar erro de recursão!**

## 📝 Nota

Se ainda der erro, execute apenas a criação da função primeiro:

```sql
CREATE OR REPLACE FUNCTION public.is_root_user()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.user_profiles
    WHERE user_id = auth.uid() AND is_root = TRUE
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

Depois execute o resto da migration.

