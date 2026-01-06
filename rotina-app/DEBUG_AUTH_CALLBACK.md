# 🔍 Debug: Erro auth_failed no Callback

## Problema
Mesmo após adicionar as URLs no Supabase, ainda dá erro `auth_failed`.

---

## ✅ Verificações Necessárias

### 1. Verificar se as URLs Foram Salvas Corretamente

No Supabase Dashboard:
1. Vá em **Authentication** > **URL Configuration**
2. Verifique se as URLs estão **exatamente** como abaixo:

```
https://rotina-five.vercel.app/auth/callback
https://rotina-five.vercel.app/auth/callback?next=/app
```

**⚠️ IMPORTANTE**: 
- Não pode ter espaços extras
- Deve ser `https://` (não `http://`)
- Deve terminar com `/auth/callback` (sem barra no final, a menos que tenha query params)

### 2. Verificar Variáveis de Ambiente no Vercel

1. No Vercel Dashboard, vá em **Settings** > **Environment Variables**
2. Verifique se estão configuradas:
   - `NEXT_PUBLIC_SUPABASE_URL` - deve ser a URL do seu projeto Supabase
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` - deve ser a chave anon do Supabase

3. **IMPORTANTE**: Verifique se estão marcadas para **Production**

### 3. Verificar Logs do Vercel

1. No Vercel Dashboard, vá em **Deployments**
2. Clique no último deploy
3. Vá em **Functions** > **View Function Logs**
4. Procure por erros relacionados a:
   - `exchangeCodeForSession`
   - `auth/callback`
   - `Supabase`

### 4. Verificar se o Código Está Sendo Usado Duas Vezes

Os códigos de autenticação do Supabase são **single-use** (uso único). Se você clicar no link duas vezes, a segunda vez dará erro.

**Solução**: Use um link novo do email.

### 5. Verificar Tempo de Expiração

Os códigos expiram após alguns minutos. Se o link for muito antigo, não funcionará.

**Solução**: Envie um novo email de login.

---

## 🔧 Teste Passo a Passo

### Passo 1: Limpar Cache e Cookies

1. Abra o navegador em **modo anônimo/privado**
2. Ou limpe cookies e cache do site

### Passo 2: Enviar Novo Email

1. Acesse: `https://rotina-five.vercel.app/login`
2. Digite seu email
3. Clique em "Enviar Magic Link"
4. **Aguarde o email chegar**

### Passo 3: Verificar o Link do Email

O link deve ser algo como:
```
https://rotina-five.vercel.app/auth/callback?code=XXXXX&next=/app
```

**Verifique**:
- Começa com `https://rotina-five.vercel.app` (não localhost)
- Tem `/auth/callback` no caminho
- Tem `code=` na query string

### Passo 4: Clicar no Link

1. Clique no link do email
2. **IMPORTANTE**: Clique apenas uma vez
3. Aguarde o redirecionamento

---

## 🛠️ Soluções Alternativas

### Solução 1: Verificar Site URL no Supabase

No Supabase Dashboard:
1. Vá em **Authentication** > **URL Configuration**
2. Em **Site URL**, configure:

```
https://rotina-five.vercel.app
```

Isso garante que o Supabase use a URL correta como base.

### Solução 2: Verificar se Há Erro Específico

No console do navegador (F12):
1. Abra DevTools
2. Vá na aba **Console**
3. Veja se há erros específicos do Supabase

### Solução 3: Testar com URL Direta

Tente acessar diretamente:
```
https://rotina-five.vercel.app/auth/callback?code=TEST&next=/app
```

Se der erro diferente, pode ajudar a identificar o problema.

---

## 📋 Checklist de Debug

- [ ] URLs adicionadas no Supabase (verificadas manualmente)
- [ ] URLs salvas corretamente (sem espaços, com https://)
- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] Variáveis marcadas para Production
- [ ] Novo email de login enviado
- [ ] Link do email verificado (aponta para rotina-five.vercel.app)
- [ ] Link clicado apenas uma vez
- [ ] Logs do Vercel verificados
- [ ] Console do navegador verificado (F12)

---

## 🔍 Informações para Debug

Se ainda não funcionar, me envie:

1. **URL exata do link do email** (pode mascarar o code)
2. **Mensagem de erro completa** da URL (ex: `?error=auth_failed&message=...`)
3. **Logs do Vercel** (se houver erros)
4. **Erros do console do navegador** (F12 > Console)

---

## 🎯 Possíveis Causas

1. **URL não está na lista de Redirect URLs** - Verifique novamente
2. **Código já foi usado** - Envie novo email
3. **Código expirou** - Envie novo email
4. **Variáveis de ambiente incorretas** - Verifique no Vercel
5. **Problema com cookies** - Limpe cache/cookies
6. **Problema com CORS** - Verifique configuração do Supabase

---

## ✅ Próximos Passos

1. Verifique todos os itens do checklist acima
2. Envie um novo email de login
3. Teste em modo anônimo/privado
4. Verifique os logs do Vercel
5. Me envie as informações de debug se ainda não funcionar







