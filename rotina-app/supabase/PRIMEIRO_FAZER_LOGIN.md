# ⚠️ IMPORTANTE: Faça Login Primeiro!

## ❌ Erro Atual

```
ERROR: P0001: Usuário não encontrado. Faça login primeiro no app!
```

**Causa:** O usuário não existe no `auth.users` porque você ainda não fez login no app.

---

## ✅ SOLUÇÃO: Fazer Login Primeiro

### Passo 1: Fazer Login no App

1. **Acesse:** http://localhost:3001/login
2. **Digite seu email:** `cesar@temvenda.com.br`
3. **Clique em:** "Enviar Magic Link"
4. **Verifique seu email:**
   - Procure um email do Supabase
   - Pode estar na pasta **Spam/Lixo Eletrônico**
   - Assunto: "Confirme seu email" ou similar
5. **Clique no link do email**
6. **Você será redirecionado** para `/app`

**✅ Isso cria o usuário automaticamente no `auth.users`!**

---

### Passo 2: Verificar se Funcionou

Execute este SQL no Supabase SQL Editor:

```sql
-- Ver todos os usuários
SELECT id, email, created_at, email_confirmed_at
FROM auth.users
ORDER BY created_at DESC;
```

**Você deve ver:** Seu email `cesar@temvenda.com.br` na lista

---

### Passo 3: Gerar Refeições

**Após confirmar que o usuário existe**, execute:

1. **Abra:** `rotina-app/supabase/criar_usuario_e_refeicoes.sql`
2. **O email já está:** `cesar@temvenda.com.br`
3. **Execute** (Run)

---

## 🔍 Verificar Status Completo

Execute este SQL para ver tudo:

```sql
-- Status completo do usuário
SELECT 
  u.email,
  u.id as user_id,
  u.email_confirmed_at,
  CASE WHEN p.id IS NOT NULL THEN '✅' ELSE '❌' END as perfil_existe,
  CASE WHEN e.id IS NOT NULL THEN '✅' ELSE '❌' END as enrollment_existe,
  (SELECT COUNT(*) FROM public.daily_meals WHERE user_id = u.id) as total_refeicoes
FROM auth.users u
LEFT JOIN public.profiles p ON p.id = u.id
LEFT JOIN public.enrollments e ON e.user_id = u.id AND e.active = true
WHERE u.email = 'cesar@temvenda.com.br';
```

---

## 📋 Checklist

- [ ] Fiz login no app (`http://localhost:3001/login`)
- [ ] Cliquei no link do email
- [ ] Fui redirecionado para `/app`
- [ ] Verifiquei que o usuário existe (SQL acima)
- [ ] Executei `criar_usuario_e_refeicoes.sql`

---

## ⚠️ Se o Link Não Chegar

1. **Verifique a pasta Spam**
2. **Aguarde alguns minutos**
3. **Verifique se o email está correto**
4. **Verifique as configurações do Supabase:**
   - Settings → Authentication → URL Configuration
   - Site URL: `http://localhost:3001`
   - Redirect URLs: `http://localhost:3001/**`

---

## 🚀 Depois de Fazer Login

1. ✅ Execute `criar_usuario_e_refeicoes.sql`
2. ✅ Verifique as refeições no calendário (`/app/today`)
3. ✅ Teste a replicação (`/app/plan-manager`)

---

**FAÇA LOGIN PRIMEIRO NO APP ANTES DE EXECUTAR OS SCRIPTS SQL!** 🚀







