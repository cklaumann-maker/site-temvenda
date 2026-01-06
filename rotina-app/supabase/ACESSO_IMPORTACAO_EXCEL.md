# 🚀 Acesso à Importação de Excel

## 📍 Caminho Exato

### URL Completa:
```
https://seu-dominio.vercel.app/app/admin/food-items/import
```

### Ou via navegação:
1. Faça login como **usuário root**
2. No menu superior, clique em **"Admin Alimentos"**
3. Clique em **"Importar do Excel"**

## 🔐 Usuários Root

### Como Verificar Usuários Root Existentes

Execute no SQL Editor do Supabase:

```sql
-- Arquivo: rotina-app/supabase/verificar_usuarios_root.sql
```

Isso mostrará todos os usuários root com seus emails.

### Usuário Root Padrão

Baseado na documentação, o usuário root padrão é:

- **Email**: `root@rotina.app`
- **Senha**: `root` (ou a senha que você definiu ao criar)

**⚠️ IMPORTANTE**: As senhas são armazenadas de forma criptografada e não podem ser recuperadas via SQL. Se você não sabe a senha:

1. **Opção 1**: Use "Esqueci minha senha" na tela de login
2. **Opção 2**: Redefina no Dashboard do Supabase:
   - Acesse: https://supabase.com/dashboard
   - Vá em: Authentication > Users
   - Selecione o usuário root
   - Clique em "Reset Password"

## 📋 Passos para Acessar

### 1. Verificar se Existe Usuário Root

Execute no Supabase SQL Editor:

```sql
SELECT 
  u.email,
  u.email_confirmed_at IS NOT NULL as email_confirmado,
  up.is_root
FROM auth.users u
LEFT JOIN public.user_profiles up ON up.user_id = u.id
WHERE up.is_root = TRUE;
```

### 2. Se Não Existe, Criar Usuário Root

#### Via Dashboard (Recomendado):

1. Acesse: https://supabase.com/dashboard
2. Vá em: **Authentication > Users**
3. Clique em: **"Add user"**
4. Preencha:
   - **Email**: `root@rotina.app` (ou outro email)
   - **Password**: `root` (ou senha de sua escolha)
   - **Auto Confirm User**: ✅ **SIM** (muito importante!)
5. Clique em: **"Create user"**

#### Depois, Execute o Script SQL:

```sql
-- Arquivo: rotina-app/supabase/criar_usuario_root.sql
```

**IMPORTANTE**: Edite o script e altere o email na linha 25 se necessário:

```sql
root_email TEXT := 'root@rotina.app'; -- ALTERE AQUI
```

### 3. Fazer Login

1. Acesse: `/login`
2. Digite o **email** do root
3. Digite a **senha** do root
4. Clique em **"Entrar"**

### 4. Acessar Importação

**Opção A - Via Menu:**
- Após login, no menu superior clique em **"Admin Alimentos"**
- Clique em **"Importar do Excel"**

**Opção B - URL Direta:**
- Acesse: `/app/admin/food-items/import`

## 🔒 Permissões

- Apenas usuários com `is_root = TRUE` podem acessar
- O middleware protege automaticamente a rota
- Se não for root, será redirecionado para `/app`

## 📝 Estrutura de Rotas

```
/app/admin/food-items          → Página principal (menu)
/app/admin/food-items/import   → Importação do Excel
/app/admin/food-items/list     → Listar alimentos (a ser criada)
```

## 🐛 Troubleshooting

### Erro: "Acesso negado" ou redirecionamento
- Verifique se o usuário tem `is_root = TRUE`
- Execute: `rotina-app/supabase/verificar_usuarios_root.sql`
- Execute: `rotina-app/supabase/criar_usuario_root.sql` novamente

### Não vejo o link "Admin Alimentos"
- Verifique se está logado como root
- Verifique se o perfil tem `is_root = TRUE`
- Limpe o cache do navegador

### Página não encontrada (404)
- Verifique se o deploy foi concluído
- Verifique se a rota está correta: `/app/admin/food-items/import`
- Verifique os logs do Vercel

