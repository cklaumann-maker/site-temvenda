# ✅ Após Instalar Dependências

## O que esperar

Após executar `pnpm install`, você deve ver:

```
Packages: +XXX
++++++++++++++++++++++++++++++++++++++++++++++++++
Progress: resolved XXX, reused XXX, downloaded XXX
```

## Próximos Passos

### 1. ✅ Build dos Packages (se necessário)

```bash
pnpm --filter shared build
pnpm --filter ui build
```

**Nota**: Se der erro, pode pular e ir direto para `pnpm dev` - o Next.js compila automaticamente.

### 2. 🔐 Configurar URLs no Supabase Auth (OBRIGATÓRIO)

**Sem isso, o login NÃO funcionará!**

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Vá em **Settings** → **Authentication**
3. Role até **URL Configuration**
4. Em **Site URL**, adicione:
   ```
   http://localhost:3001
   ```
5. Em **Redirect URLs**, adicione (uma por linha):
   ```
   http://localhost:3001/**
   http://localhost:3001/app/today
   ```
6. Clique em **Save**

### 3. 🚀 Iniciar Aplicativo

```bash
pnpm dev
```

**Esperado**:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3001
```

### 4. 🧪 Testar Login

1. Acesse: http://localhost:3001/login
2. Digite um email válido
3. Clique em "Enviar Magic Link"
4. Verifique seu email (pode estar na pasta spam)
5. Clique no link do email
6. **Deve redirecionar** para `/app/today`

---

## ⚠️ Problemas Comuns

### Erro: "Cannot find module '@rotina/shared'"

**Solução**: Build dos packages primeiro
```bash
pnpm --filter shared build
pnpm --filter ui build
```

Ou tente iniciar direto - Next.js pode compilar automaticamente:
```bash
pnpm dev
```

### Erro: "Invalid API key"

**Solução**: 
1. Verifique se `.env.local` existe e está correto
2. Reinicie o servidor após criar/editar `.env.local`

### Erro: "Failed to fetch" no login

**Solução**: 
1. Verifique URLs permitidas no Supabase Auth (passo 2 acima)
2. Verifique se o projeto está ativo no Supabase

---

## 📋 Checklist Final

- [ ] Dependências instaladas (`pnpm install`)
- [ ] Packages buildados (ou pulou para iniciar direto)
- [ ] URLs permitidas configuradas no Supabase Auth
- [ ] Arquivo `.env.local` criado e configurado
- [ ] App iniciado (`pnpm dev`)
- [ ] Login testado com sucesso

---

## 🎯 Comandos Rápidos

```bash
# 1. Instalar (já executando)
pnpm install

# 2. Build packages (opcional)
pnpm --filter shared build
pnpm --filter ui build

# 3. Configurar URLs no Supabase Dashboard
#    Settings > Auth > URL Configuration

# 4. Iniciar app
pnpm dev

# 5. Acessar: http://localhost:3001/login
```

---

## ✅ Status Esperado

Após seguir todos os passos:

✅ App rodando em http://localhost:3001  
✅ Login funcionando  
✅ Redirecionamento funcionando  
✅ Tela "/app/today" carregando  

**Pronto para usar!** 🚀

