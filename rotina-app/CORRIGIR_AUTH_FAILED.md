# 🔧 Corrigir Erro auth_failed no Callback

## Problema
Ao fazer login, está redirecionando para `/login?error=auth_failed` após o callback.

---

## ✅ Solução: Configurar URL do Vercel no Supabase

### Passo 1: Adicionar URL do Vercel como Redirect URL

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Authentication** > **URL Configuration**
4. Em **Redirect URLs**, adicione:

```
https://rotina-five.vercel.app/auth/callback
https://rotina-five.vercel.app/auth/callback?next=/app
https://rotina-five.vercel.app/auth/callback?next=/app/today
https://rotina-five.vercel.app/auth/callback?next=/app/dashboard
```

**⚠️ IMPORTANTE**: Adicione TODAS as URLs acima!

### Passo 2: Configurar Site URL (Opcional mas Recomendado)

Na mesma página, em **Site URL**, você pode configurar:

```
https://rotina-five.vercel.app
```

Ou deixe como `https://rotina.temvenda.com.br` se já estiver configurado.

### Passo 3: Salvar

1. Clique em **Save**
2. Aguarde alguns segundos

---

## 🔍 Verificar Variáveis de Ambiente no Vercel

Certifique-se de que as variáveis estão configuradas:

1. No Vercel Dashboard, vá em **Settings** > **Environment Variables**
2. Verifique se estão configuradas:
   - ✅ `NEXT_PUBLIC_SUPABASE_URL`
   - ✅ `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - ✅ `SUPABASE_SERVICE_ROLE_KEY` (se necessário)

3. Marque todas como **Production**, **Preview** e **Development**

---

## 🧪 Testar

1. Acesse: `https://rotina-five.vercel.app/login`
2. Digite seu email
3. Clique em "Enviar Magic Link"
4. Verifique o email
5. Clique no link
6. Deve redirecionar para `https://rotina-five.vercel.app/app` (sem erro)

---

## 🛠️ Troubleshooting

### Problema: Ainda dá erro auth_failed

**Solução 1**: Verifique se a URL exata está nas Redirect URLs:
- A URL deve ser **exatamente** como está no link do email
- Sem espaços extras
- Com `https://` (não `http://`)

**Solução 2**: Verifique os logs do Vercel:
1. No Vercel Dashboard, vá em **Deployments**
2. Clique no último deploy
3. Veja os **Function Logs**
4. Procure por erros relacionados ao callback

**Solução 3**: Verifique o console do navegador:
1. Abra DevTools (F12)
2. Vá na aba **Console**
3. Veja se há erros relacionados ao Supabase

### Problema: Código expira muito rápido

**Solução**:
1. No Supabase Dashboard, vá em **Authentication** > **Settings**
2. Verifique o **JWT expiry** (tempo de expiração)
3. Pode aumentar se necessário

### Problema: Erro "Invalid redirect URL"

**Solução**:
1. Verifique se a URL está **exatamente** como configurada no Supabase
2. Certifique-se de que está usando `https://` (não `http://`)
3. Adicione a URL exata que está sendo usada

---

## 📋 Checklist

- [ ] URL do Vercel adicionada nas Redirect URLs do Supabase
- [ ] Todas as variações da URL adicionadas (`/auth/callback`, `/auth/callback?next=/app`, etc.)
- [ ] Configurações salvas no Supabase
- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] Testado envio de novo email de login
- [ ] Link do email funciona corretamente
- [ ] Redireciona para `/app` sem erros

---

## 🎯 URLs que Precisam Estar Configuradas

### No Supabase Dashboard > Authentication > URL Configuration > Redirect URLs:

```
https://rotina-five.vercel.app/auth/callback
https://rotina-five.vercel.app/auth/callback?next=/app
https://rotina-five.vercel.app/auth/callback?next=/app/today
https://rotina-five.vercel.app/auth/callback?next=/app/dashboard
https://rotina.temvenda.com.br/auth/callback
https://rotina.temvenda.com.br/auth/callback?next=/app
https://rotina.temvenda.com.br/auth/callback?next=/app/today
https://rotina.temvenda.com.br/auth/callback?next=/app/dashboard
http://localhost:3001/auth/callback
http://localhost:3001/auth/callback?next=/app
```

**⚠️ IMPORTANTE**: Adicione TODAS essas URLs!

---

## 🔗 Links Úteis

- **Supabase Dashboard**: https://supabase.com/dashboard
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Documentação Supabase Auth**: https://supabase.com/docs/guides/auth

---

## ✅ Após Configurar

1. Aguarde alguns segundos para o Supabase processar
2. Envie um novo email de login
3. Clique no link
4. Deve funcionar corretamente!

Se ainda não funcionar, verifique os logs do Vercel para ver o erro exato.

