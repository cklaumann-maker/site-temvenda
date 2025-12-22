# 🔐 Como Fazer Login

## Sistema de Autenticação

O aplicativo usa **Magic Link** do Supabase Auth. Isso significa:

1. **Qualquer email válido funciona** - não precisa estar pré-cadastrado
2. **Você recebe um link por email** - clique no link para fazer login
3. **Não precisa de senha** - o link é sua autenticação

---

## 📧 Passo a Passo

### 1. Acesse a página de login

Vá para: http://localhost:3001/login

### 2. Digite seu email

Use **qualquer email válido** que você tenha acesso:
- Seu email pessoal
- Email de teste
- Qualquer email que você possa verificar

**Exemplo:**
```
seu@email.com
```

### 3. Clique em "Enviar Magic Link"

### 4. Verifique seu email

- Procure um email do Supabase
- Pode estar na pasta **Spam/Lixo Eletrônico**
- O assunto será algo como: "Confirme seu email"

### 5. Clique no link do email

Isso vai:
- Confirmar seu email
- Fazer login automaticamente
- Redirecionar para `/app/today`

---

## ⚠️ Importante

### Primeira vez usando um email?

Quando você faz login pela primeira vez com um email:

1. ✅ O usuário é criado automaticamente no Supabase Auth
2. ❌ Mas você **não terá acesso aos dados** ainda

### Para ter acesso completo aos dados:

Você precisa ser **adicionado como membro** de uma organização. Veja o arquivo `CRIAR_USUARIO_TESTE.md` para criar um usuário completo com acesso aos dados.

---

## 🧪 Email de Teste Recomendado

Para desenvolvimento local, você pode usar:

- Seu email pessoal (recomendado)
- Um email de teste que você tenha acesso
- Qualquer email válido

**Não precisa criar nada antes!** O sistema cria o usuário automaticamente.

---

## 🔧 Configuração Necessária

Certifique-se de que configurou as URLs no Supabase:

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Settings → Authentication → URL Configuration
3. Site URL: `http://localhost:3001`
4. Redirect URLs: `http://localhost:3001/**`

---

## ❓ Problemas Comuns

### "Link não chegou no email"
- Verifique a pasta Spam
- Aguarde alguns minutos
- Verifique se o email está correto

### "Erro ao enviar link"
- Verifique se as URLs estão configuradas no Supabase
- Verifique se o `.env.local` está correto
- Reinicie o servidor

### "Login funciona mas não vejo dados"
- Você precisa ser adicionado como membro de uma organização
- Veja `CRIAR_USUARIO_TESTE.md` para criar um usuário completo

