# 👤 Criar Usuário de Teste Completo

## 📋 Passo a Passo

### 1. Faça Login no App (Primeira Vez)

1. Acesse: http://localhost:3001/login
2. Digite seu email (ex: `seu@email.com`)
3. Clique em "Enviar Magic Link"
4. Verifique seu email e clique no link
5. Você será redirecionado para `/app/today`

**⚠️ Neste momento você está logado, mas não tem acesso aos dados ainda.**

---

### 2. Criar Perfil e Acesso aos Dados

Agora você precisa executar um SQL no Supabase para criar seu perfil e dar acesso aos dados:

#### Opção A: Via SQL Editor (Recomendado)

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Vá em **SQL Editor**
3. Abra o arquivo: `supabase/create_test_user.sql`
4. **Substitua** `'SEU_EMAIL_AQUI'` pelo email que você usou para fazer login
5. Execute o SQL

**Exemplo:**
```sql
-- Se você usou cesar@temvenda.com.br, altere:
v_email TEXT := 'cesar@temvenda.com.br';
```

#### Opção B: SQL Manual

Execute este SQL no Supabase SQL Editor:

```sql
-- Substitua 'seu@email.com' pelo email que você usou
DO $$
DECLARE
  v_user_id UUID;
  v_email TEXT := 'seu@email.com'; -- ⚠️ ALTERE AQUI
  v_org_id UUID := '00000000-0000-0000-0000-000000000001';
  v_program_id UUID := '00000000-0000-0000-0000-000000000002';
BEGIN
  -- Buscar ID do usuário
  SELECT id INTO v_user_id FROM auth.users WHERE email = v_email;
  
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'Usuário não encontrado. Faça login primeiro!';
  END IF;

  -- Criar perfil
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (v_user_id, v_email, 'Usuário de Teste')
  ON CONFLICT (id) DO UPDATE SET email = v_email;

  -- Adicionar como OWNER
  INSERT INTO public.org_members (org_id, user_id, role, active)
  VALUES (v_org_id, v_user_id, 'OWNER', true)
  ON CONFLICT (org_id, user_id) DO UPDATE SET role = 'OWNER', active = true;

  -- Criar enrollment
  INSERT INTO public.enrollments (user_id, program_id, start_date, active)
  VALUES (v_user_id, v_program_id, CURRENT_DATE, true)
  ON CONFLICT (user_id, program_id) WHERE active = true DO UPDATE SET start_date = CURRENT_DATE;

  RAISE NOTICE '✅ Usuário configurado! Email: %, Role: OWNER', v_email;
END $$;
```

---

### 3. Recarregar o App

1. Volte para: http://localhost:3001/app/today
2. Recarregue a página (F5 ou Cmd+R)
3. Agora você deve ver os dados!

---

## ✅ O que você terá acesso:

- ✅ Perfil criado
- ✅ Role: **OWNER** (acesso total)
- ✅ Organização: **Demo Organization**
- ✅ Programa: **Disciplina Total**
- ✅ Plan Templates: Semana 1 e 2 já configuradas
- ✅ Acesso a `/app/*` (área do usuário)
- ✅ Acesso a `/admin/*` (área admin)

---

## 🧪 Email de Teste Sugerido

Para facilitar, você pode usar:
- Seu email pessoal
- Um email de teste que você tenha acesso

**Exemplo:**
- `cesar@temvenda.com.br`
- `teste@exemplo.com`
- Qualquer email válido

---

## 🔍 Verificar se Funcionou

Execute este SQL para verificar:

```sql
-- Ver seu perfil
SELECT * FROM public.profiles WHERE email = 'seu@email.com';

-- Ver sua role
SELECT om.*, o.name as org_name
FROM public.org_members om
JOIN public.orgs o ON o.id = om.org_id
WHERE om.user_id = (SELECT id FROM auth.users WHERE email = 'seu@email.com');

-- Ver seu enrollment
SELECT e.*, p.name as program_name
FROM public.enrollments e
JOIN public.programs p ON p.id = e.program_id
WHERE e.user_id = (SELECT id FROM auth.users WHERE email = 'seu@email.com');
```

---

## ❓ Problemas

### "Usuário não encontrado"
- Certifique-se de ter feito login primeiro no app
- Verifique se o email está correto (case-sensitive)

### "Ainda não vejo dados"
- Recarregue a página do app
- Verifique se o SQL executou sem erros
- Verifique se você está logado com o mesmo email

### "Erro de permissão"
- Verifique se as RLS policies estão ativas
- Verifique se o usuário foi criado corretamente







