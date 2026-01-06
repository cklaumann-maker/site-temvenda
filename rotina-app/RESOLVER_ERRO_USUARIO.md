# 🔧 Resolver Erro: Usuário Não Encontrado

## ❌ Erro Encontrado

```
ERROR: P0001: Usuário não encontrado. Faça login primeiro no app com o email: cesar@temvenda.com.br
```

Isso significa que o usuário **não existe** no `auth.users` do Supabase.

---

## ✅ Solução

### Opção 1: Fazer Login Primeiro (Recomendado)

O Supabase cria o usuário automaticamente quando você faz login:

1. **Acesse:** http://localhost:3001/login
2. **Digite seu email:** `cesar@temvenda.com.br`
3. **Clique em:** "Enviar Magic Link"
4. **Verifique seu email** e clique no link
5. **Depois execute novamente:** `criar_usuario_e_refeicoes.sql`

---

### Opção 2: Verificar Usuários Existentes

Execute este SQL para ver quais usuários existem:

```sql
-- Ver todos os usuários
SELECT id, email, created_at 
FROM auth.users
ORDER BY created_at DESC;
```

**Depois:**
- Se encontrar seu email, use o `id` retornado
- Se não encontrar, faça login primeiro (Opção 1)

---

### Opção 3: Usar Script Completo

Execute o novo script que verifica e cria tudo:

1. **Acesse:** SQL Editor no Supabase
2. **Abra:** `rotina-app/supabase/criar_usuario_e_refeicoes.sql`
3. **Substitua** `'cesar@temvenda.com.br'` pelo email correto (se necessário)
4. **Execute** (Run)

Este script vai:
- ✅ Verificar se o usuário existe
- ✅ Dar instruções se não existir
- ✅ Criar perfil e enrollment se existir
- ✅ Gerar refeições para 30 dias

---

## 🔍 Verificar Status do Usuário

Execute este SQL para ver o status completo:

```sql
-- Ver status completo
SELECT 
  u.email,
  u.id as user_id,
  CASE WHEN p.id IS NOT NULL THEN '✅' ELSE '❌' END as perfil,
  CASE WHEN e.id IS NOT NULL THEN '✅' ELSE '❌' END as enrollment,
  (SELECT COUNT(*) FROM public.daily_meals WHERE user_id = u.id) as refeicoes
FROM auth.users u
LEFT JOIN public.profiles p ON p.id = u.id
LEFT JOIN public.enrollments e ON e.user_id = u.id AND e.active = true
ORDER BY u.created_at DESC;
```

---

## 📋 Ordem Correta de Execução

1. ✅ **Primeiro:** Faça login no app (`http://localhost:3001/login`)
   - Isso cria o usuário no `auth.users`

2. ✅ **Depois:** Execute `criar_usuario_e_refeicoes.sql`
   - Isso cria perfil, enrollment e refeições

3. ✅ **Por último:** Verifique no app
   - Acesse `/app/today` e veja o calendário

---

## ⚠️ Se Ainda Não Funcionar

### Problema: Email não confirma

1. Verifique a pasta **Spam** do seu email
2. Aguarde alguns minutos
3. Tente novamente

### Problema: Link expirado

1. Volte para `/login`
2. Digite o email novamente
3. Clique em "Enviar Magic Link"

### Problema: Usuário existe mas script não encontra

Execute este SQL para verificar:

```sql
-- Verificar usuário específico
SELECT id, email, email_confirmed_at 
FROM auth.users 
WHERE email = 'cesar@temvenda.com.br';
```

Se retornar um resultado, o usuário existe. Use o `id` retornado.

---

## 🎯 Arquivos Criados

1. ✅ `supabase/criar_usuario_e_refeicoes.sql` (NOVO)
   - Script completo que verifica usuário
   - Cria perfil e enrollment
   - Gera refeições

2. ✅ `supabase/verificar_usuario.sql` (NOVO)
   - Script para verificar status dos usuários
   - Lista todos os usuários
   - Mostra status de perfil e enrollment

---

## 🚀 Solução Rápida

**Execute na ordem:**

1. **Faça login:** http://localhost:3001/login (email: cesar@temvenda.com.br)
2. **Execute:** `criar_usuario_e_refeicoes.sql` no Supabase
3. **Verifique:** `/app/today` no app

---

**Faça login primeiro no app e depois execute o script novamente!** 🚀







