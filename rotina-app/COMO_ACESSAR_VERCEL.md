# 🌐 Como Acessar a Aplicação no Vercel

## 1. URL Automática do Vercel

Após o deploy bem-sucedido, o Vercel cria automaticamente uma URL para sua aplicação:

### Encontrar a URL:

1. **Acesse o Dashboard do Vercel**: https://vercel.com/dashboard
2. **Clique no seu projeto** (`rotina`)
3. **Na página do projeto**, você verá:
   - **Production**: Uma URL como `https://rotina-xxxxx.vercel.app`
   - **Preview Deployments**: URLs para cada commit

### Exemplo de URL:
```
https://rotina-xxxxx.vercel.app
```

---

## 2. Acessar a Aplicação

### URL Principal:
```
https://rotina-xxxxx.vercel.app
```

### Rotas Disponíveis:
- **Home**: `https://rotina-xxxxx.vercel.app/`
- **Login**: `https://rotina-xxxxx.vercel.app/login`
- **App Principal**: `https://rotina-xxxxx.vercel.app/app`
- **Hoje**: `https://rotina-xxxxx.vercel.app/app/today`
- **Dashboard**: `https://rotina-xxxxx.vercel.app/app/dashboard`
- **Check-in**: `https://rotina-xxxxx.vercel.app/app/checkin`
- **Plano**: `https://rotina-xxxxx.vercel.app/app/plan`
- **Perfil**: `https://rotina-xxxxx.vercel.app/app/profile`

---

## 3. Configurar Domínio Personalizado (Opcional)

Se você quiser usar um domínio próprio (ex: `rotina.temvenda.com.br`):

### Passos:

1. **No Dashboard do Vercel**:
   - Vá em **Settings** > **Domains**
   - Clique em **Add Domain**
   - Digite seu domínio: `rotina.temvenda.com.br`
   - Clique em **Add**

2. **Configure o DNS**:
   - No seu provedor de DNS (onde está configurado `temvenda.com.br`)
   - Adicione um registro **CNAME**:
     - **Nome**: `rotina`
     - **Valor**: `cname.vercel-dns.com` (ou o valor fornecido pelo Vercel)
     - **TTL**: 3600 (ou padrão)

3. **Aguarde a propagação DNS** (pode levar alguns minutos)

4. **Acesse**: `https://rotina.temvenda.com.br`

---

## 4. Verificar Status do Deploy

### No Dashboard do Vercel:

1. **Deployments**: Veja todos os deploys
2. **Status**: ✅ **Ready** = Deploy concluído com sucesso
3. **URL**: Clique na URL para acessar

### Indicadores:
- 🟢 **Ready**: Deploy concluído e funcionando
- 🟡 **Building**: Ainda em construção
- 🔴 **Error**: Erro no deploy (veja os logs)

---

## 5. Primeiro Acesso

1. **Acesse a URL do Vercel** (ex: `https://rotina-xxxxx.vercel.app`)
2. **Você será redirecionado para `/login`**
3. **Faça login** com seu email do Supabase
4. **Use o Magic Link** ou senha (se configurada no perfil)

---

## 6. Verificar Variáveis de Ambiente

Certifique-se de que as variáveis estão configuradas:

1. **Settings** > **Environment Variables**
2. Verifique se estão todas configuradas:
   - ✅ `NEXT_PUBLIC_SUPABASE_URL`
   - ✅ `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - ✅ `SUPABASE_SERVICE_ROLE_KEY`

---

## 7. Troubleshooting

### Se a aplicação não carregar:

1. **Verifique os logs do deploy**:
   - Vá em **Deployments** > Clique no deploy > **Build Logs**

2. **Verifique as variáveis de ambiente**:
   - Certifique-se de que estão configuradas para **Production**

3. **Verifique o console do navegador**:
   - Abra o DevTools (F12)
   - Veja se há erros no Console

4. **Verifique a URL do Supabase**:
   - Certifique-se de que a URL está correta nas variáveis

---

## 📱 Próximos Passos

1. ✅ Acesse a URL do Vercel
2. ✅ Faça login
3. ✅ Teste as funcionalidades
4. ✅ Configure domínio personalizado (opcional)
5. ✅ Compartilhe com usuários

---

## 🔗 Links Úteis

- **Dashboard Vercel**: https://vercel.com/dashboard
- **Documentação Vercel**: https://vercel.com/docs
- **Supabase Dashboard**: https://supabase.com/dashboard







