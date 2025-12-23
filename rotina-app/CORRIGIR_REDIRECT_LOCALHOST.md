# 🔧 Corrigir Redirecionamento para Localhost

## Problema
O link de autenticação ainda está direcionando para `http://localhost:3001` mesmo em produção.

---

## ✅ Solução Completa

### 1. Configurar Variável de Ambiente no Vercel

**IMPORTANTE**: Isso é essencial para o código funcionar corretamente!

1. Acesse: https://vercel.com/dashboard
2. Vá em **Settings** > **Environment Variables**
3. Adicione:

```
NEXT_PUBLIC_SITE_URL=https://rotina.temvenda.com.br
```

4. Marque como **Production**, **Preview** e **Development**
5. Clique em **Save**

### 2. Configurar Site URL no Supabase Dashboard

**CRÍTICO**: O Supabase usa a Site URL como fallback se não encontrar a URL permitida.

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Authentication** > **URL Configuration**
4. Configure **Site URL**:

```
https://rotina.temvenda.com.br
```

### 3. Configurar Redirect URLs no Supabase

Na mesma página, em **Redirect URLs**, adicione:

```
https://rotina.temvenda.com.br/auth/callback
https://rotina.temvenda.com.br/auth/callback?next=/app
https://rotina.temvenda.com.br/auth/callback?next=/app/today
https://rotina.temvenda.com.br/auth/callback?next=/app/dashboard
http://localhost:3001/auth/callback
http://localhost:3001/auth/callback?next=/app
```

**⚠️ IMPORTANTE**: 
- Adicione **TODAS** as URLs acima
- Uma por linha ou separadas por vírgula
- Inclua tanto produção quanto desenvolvimento

### 4. Salvar e Aguardar

1. Clique em **Save** no Supabase
2. Aguarde alguns minutos para a configuração propagar
3. Faça um novo deploy no Vercel (ou aguarde o próximo deploy automático)

---

## 🔍 Verificar se Está Funcionando

### No Console do Navegador:

1. Abra o DevTools (F12)
2. Vá na aba **Console**
3. Digite:

```javascript
console.log(window.location.origin)
```

Deve mostrar: `https://rotina.temvenda.com.br`

### Testar Login:

1. Acesse: `https://rotina.temvenda.com.br/login`
2. Digite seu email
3. Clique em "Enviar Magic Link"
4. **Verifique o email**: O link deve começar com `https://rotina.temvenda.com.br/auth/callback`

---

## 🛠️ Troubleshooting

### Problema: Ainda mostra localhost

**Solução 1**: Verifique se a variável de ambiente está configurada:
- No Vercel Dashboard, confirme que `NEXT_PUBLIC_SITE_URL` está definida
- Faça um novo deploy após adicionar a variável

**Solução 2**: Verifique o código no navegador:
- Abra DevTools > Sources
- Procure por `getAuthCallbackUrl` ou `emailRedirectTo`
- Veja qual URL está sendo usada

**Solução 3**: Limpe o cache:
- Limpe o cache do navegador
- Ou use modo anônimo/privado
- Tente novamente

### Problema: Erro "Invalid redirect URL"

**Solução**:
1. Verifique se a URL exata está nas Redirect URLs do Supabase
2. Certifique-se de que não há espaços extras
3. Use `https://` (não `http://`) em produção

### Problema: Link expira muito rápido

**Solução**:
1. No Supabase Dashboard, vá em **Authentication** > **Settings**
2. Verifique o **JWT expiry** (tempo de expiração)
3. Pode aumentar se necessário

---

## 📝 Checklist Final

- [ ] Variável `NEXT_PUBLIC_SITE_URL` configurada no Vercel
- [ ] Site URL configurada no Supabase: `https://rotina.temvenda.com.br`
- [ ] Redirect URLs adicionadas no Supabase (produção e desenvolvimento)
- [ ] Configurações salvas no Supabase
- [ ] Deploy realizado no Vercel (ou aguardando deploy automático)
- [ ] Testado envio de novo email de login
- [ ] Link do email aponta para `rotina.temvenda.com.br`
- [ ] Login funciona corretamente

---

## 🎯 Por Que Isso Acontece?

O Supabase tem duas configurações importantes:

1. **Site URL**: URL padrão usada quando não há `emailRedirectTo` ou quando a URL não está permitida
2. **Redirect URLs**: Lista de URLs permitidas para redirecionamento

Se a Site URL estiver como `localhost`, o Supabase pode usar ela mesmo que você passe `emailRedirectTo` diferente.

**Solução**: Configure ambas corretamente!

---

## 🔗 Links Úteis

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Supabase Dashboard**: https://supabase.com/dashboard
- **Documentação Supabase Auth**: https://supabase.com/docs/guides/auth

---

## ✅ Após Configurar

1. Aguarde alguns minutos
2. Faça um novo teste de login
3. O link deve apontar para `https://rotina.temvenda.com.br`

Se ainda não funcionar, verifique os logs do console do navegador para ver qual URL está sendo usada.

