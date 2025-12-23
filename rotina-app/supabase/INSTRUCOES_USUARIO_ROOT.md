# Instruções para Configurar Usuário Root

## 📋 Resumo

Foi implementado um sistema completo de administração de usuários com acesso root. Apenas usuários com `is_root = TRUE` podem acessar a tela de administração.

## 🚀 Passos para Criar o Usuário Root

### 1. Executar Migration

Execute a migration que adiciona o campo `is_root`:

```sql
-- Arquivo: rotina-app/supabase/migrations/20240101000010_add_root_user_support.sql
```

Execute este arquivo no SQL Editor do Supabase.

### 2. Criar Função RPC (Opcional mas Recomendado)

Execute a função que permite listar usuários:

```sql
-- Arquivo: rotina-app/supabase/funcao_listar_usuarios.sql
```

Isso permite que a API liste todos os usuários com seus emails.

### 3. Criar Usuário no Supabase Dashboard

1. Acesse: https://supabase.com/dashboard
2. Vá em: **Authentication > Users**
3. Clique em: **"Add user"**
4. Preencha:
   - **Email**: `root@rotina.app` (ou o email que você preferir)
   - **Password**: `root` (ou a senha que você preferir)
   - **Auto Confirm User**: ✅ **SIM** (importante!)
5. Clique em: **"Create user"**

### 4. Executar Script para Configurar Root

Execute o script SQL para marcar o usuário como root:

```sql
-- Arquivo: rotina-app/supabase/criar_usuario_root.sql
```

**IMPORTANTE**: Antes de executar, edite o script e altere o email na linha:

```sql
root_email TEXT := 'root@rotina.app'; -- ALTERE AQUI COM O EMAIL DO ROOT
```

Para o email que você usou ao criar o usuário no passo 3.

### 5. Verificar se Funcionou

Execute esta consulta para verificar:

```sql
SELECT 
  u.id,
  u.email,
  up.name,
  up.is_root
FROM auth.users u
INNER JOIN public.user_profiles up ON up.user_id = u.id
WHERE up.is_root = TRUE;
```

Você deve ver o usuário root listado.

## 🔐 Como Fazer Login como Root

1. Acesse: `/login`
2. Digite o **email** do root (ex: `root@rotina.app`)
3. Digite a **senha** do root (ex: `root`)
4. Clique em **"Entrar"**

## 📱 Acessar Tela de Administração

Após fazer login como root:

1. Clique no link **"Admin"** no menu superior (ao lado do seu email)
2. Ou acesse diretamente: `/app/admin/users`

## ✨ Funcionalidades da Tela de Admin

### Listar Usuários
- Ver todos os usuários cadastrados
- Ver status de confirmação de email
- Ver se o usuário é root
- Ver data de criação

### Adicionar Usuário
- Clique em **"+ Adicionar Usuário"**
- Preencha:
  - **Email** (obrigatório)
  - **Senha** (obrigatório, mínimo 6 caracteres)
  - **Nome** (opcional)
- Clique em **"Criar Usuário"**

### Deletar Usuário
- Clique em **"Deletar"** ao lado do usuário
- Confirme a ação
- **Nota**: O usuário será deletado das tabelas relacionadas, mas você precisará deletar manualmente de `auth.users` no Dashboard do Supabase

## 🔒 Segurança

- Apenas usuários com `is_root = TRUE` podem acessar `/app/admin/users`
- O middleware protege a rota automaticamente
- Usuários root não podem ser deletados pela interface
- A API verifica permissões em todas as operações

## 📝 Arquivos Criados

### Migrations
- `20240101000010_add_root_user_support.sql` - Adiciona campo `is_root` e políticas RLS

### Scripts SQL
- `criar_usuario_root.sql` - Script para configurar usuário como root
- `funcao_listar_usuarios.sql` - Função RPC para listar usuários

### Frontend
- `apps/web/src/app/app/admin/users/page.tsx` - Página de admin
- `apps/web/src/app/app/admin/users/UsersAdminClient.tsx` - Componente principal

### API Routes
- `apps/web/src/app/api/admin/users/route.ts` - GET (listar) e POST (criar)
- `apps/web/src/app/api/admin/users/[userId]/route.ts` - DELETE (deletar)

### Middleware
- `apps/web/src/middleware.ts` - Protege rotas `/app/admin/*` apenas para root

## ⚠️ Notas Importantes

1. **Criar usuário via API**: A criação de usuário via API (`signUp`) pode enviar email de confirmação. Para evitar isso em produção, você pode criar uma função RPC no Supabase que use `service_role_key`.

2. **Deletar de auth.users**: A API deleta todos os registros relacionados, mas para deletar de `auth.users`, você precisa usar o Dashboard do Supabase ou criar uma função RPC com `service_role_key`.

3. **Função RPC**: A função `list_users_for_admin` é opcional mas recomendada, pois permite listar usuários com seus emails corretamente.

## 🐛 Troubleshooting

### Erro: "Acesso negado"
- Verifique se o usuário tem `is_root = TRUE` na tabela `user_profiles`
- Execute o script `criar_usuario_root.sql` novamente

### Erro: "Função não encontrada"
- Execute o arquivo `funcao_listar_usuarios.sql` no SQL Editor

### Usuários não aparecem na lista
- Verifique se a função RPC foi criada
- Verifique os logs do console do navegador
- Verifique os logs do servidor (Vercel)

### Não consigo criar usuário
- Verifique se está logado como root
- Verifique os logs do console
- Verifique se o email já não está cadastrado

