# 🔐 Configurar URLs de Redirecionamento no Supabase

## Problema
Os emails de autenticação estão sendo enviados com URLs do `localhost` em vez do domínio de produção `rotina.temvenda.com.br`.

---

## ✅ Solução: Configurar no Supabase Dashboard

### Passo 1: Acessar o Dashboard do Supabase

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Authentication** > **URL Configuration**

### Passo 2: Configurar Site URL

Na seção **Site URL**, configure:

```
https://rotina.temvenda.com.br
```

### Passo 3: Configurar Redirect URLs

Na seção **Redirect URLs**, adicione as seguintes URLs (uma por linha):

```
https://rotina.temvenda.com.br/auth/callback
https://rotina.temvenda.com.br/auth/callback?next=/app
https://rotina.temvenda.com.br/auth/callback?next=/app/today
https://rotina.temvenda.com.br/auth/callback?next=/app/dashboard
http://localhost:3001/auth/callback
http://localhost:3001/auth/callback?next=/app
```

**⚠️ IMPORTANTE**: 
- Adicione **ambas** as URLs (produção e desenvolvimento)
- O Supabase permite múltiplas URLs separadas por vírgula ou uma por linha
- URLs de desenvolvimento são úteis para testes locais

### Passo 4: Salvar Configurações

1. Clique em **Save** (Salvar)
2. Aguarde alguns segundos para a configuração ser aplicada

---

## 🔧 Configuração Adicional: Variáveis de Ambiente

### No Vercel Dashboard:

1. Vá em **Settings** > **Environment Variables**
2. Adicione (se ainda não existir):

```
NEXT_PUBLIC_SITE_URL=https://rotina.temvenda.com.br
```

**⚠️ IMPORTANTE**:
- Marque como **Production**, **Preview** e **Development**
- Isso garante que o código use a URL correta em produção

---

## 📝 URLs que Precisam Estar Configuradas

### Produção:
```
https://rotina.temvenda.com.br/auth/callback
https://rotina.temvenda.com.br/auth/callback?next=/app
https://rotina.temvenda.com.br/auth/callback?next=/app/today
https://rotina.temvenda.com.br/auth/callback?next=/app/dashboard
```

### Desenvolvimento (opcional, mas recomendado):
```
http://localhost:3001/auth/callback
http://localhost:3001/auth/callback?next=/app
```

---

## ✅ Verificação

Após configurar:

1. **Envie um novo email de login**:
   - Acesse `https://rotina.temvenda.com.br/login`
   - Digite seu email
   - Clique em "Enviar Magic Link"

2. **Verifique o email**:
   - O link deve começar com `https://rotina.temvenda.com.br/auth/callback`
   - Não deve mais ter `localhost:3001`

3. **Teste o login**:
   - Clique no link do email
   - Você deve ser redirecionado para `https://rotina.temvenda.com.br/app`

---

## 🛠️ Troubleshooting

### Problema: Link ainda aponta para localhost

**Solução**:
1. Verifique se salvou as configurações no Supabase
2. Aguarde alguns minutos (pode levar tempo para propagar)
3. Limpe o cache do navegador
4. Tente enviar um novo email

### Problema: Erro "Invalid redirect URL"

**Solução**:
1. Verifique se a URL está exatamente como configurada no Supabase
2. Certifique-se de que não há espaços extras
3. Verifique se está usando `https://` (não `http://`) em produção
4. Adicione a URL exata que está sendo usada no erro

### Problema: Link expira muito rápido

**Solução**:
1. No Supabase Dashboard, vá em **Authentication** > **Email Templates**
2. Verifique o tempo de expiração do link
3. Pode ser configurado em **Auth** > **Settings** > **JWT expiry**

---

## 📸 Onde Encontrar no Supabase Dashboard

### Navegação:
```
Dashboard > [Seu Projeto] > Authentication > URL Configuration
```

### Seções Importantes:
- **Site URL**: URL principal do site
- **Redirect URLs**: Lista de URLs permitidas para redirecionamento
- **Email Templates**: Templates dos emails enviados

---

## 🎯 Checklist Final

- [ ] Site URL configurado: `https://rotina.temvenda.com.br`
- [ ] Redirect URLs adicionadas (produção e desenvolvimento)
- [ ] Configurações salvas no Supabase
- [ ] Variável `NEXT_PUBLIC_SITE_URL` configurada no Vercel
- [ ] Testado envio de novo email de login
- [ ] Link do email aponta para `rotina.temvenda.com.br`
- [ ] Login funciona corretamente

---

## 🔗 Links Úteis

- **Supabase Dashboard**: https://supabase.com/dashboard
- **Documentação Supabase Auth**: https://supabase.com/docs/guides/auth
- **Vercel Environment Variables**: https://vercel.com/docs/concepts/projects/environment-variables

---

## ✅ Pronto!

Após completar esses passos, os emails de autenticação usarão automaticamente o domínio de produção `rotina.temvenda.com.br` em vez de `localhost`.

