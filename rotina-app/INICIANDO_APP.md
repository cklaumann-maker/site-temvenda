# 🚀 Iniciando Aplicativo

## Comando Executado

```bash
cd rotina-app
pnpm dev
```

---

## O que Esperar

### ✅ Inicialização Bem-Sucedida

Você deve ver algo como:

```
▲ Next.js 14.0.4
- Local:        http://localhost:3001
- Ready in XXXms

✓ Compiled successfully
```

### ⚠️ Se Houver Erros

O Next.js pode mostrar erros de compilação. Veja troubleshooting abaixo.

---

## Verificar se Está Funcionando

### 1. Acessar no Navegador

Abra: **http://localhost:3001**

**Esperado**: Página de login aparece (tela escura com "Rotina" e campo de email)

### 2. Verificar Console do Terminal

- Compilação bem-sucedida
- Servidor rodando na porta 3001
- Sem erros críticos

### 3. Verificar Console do Navegador (F12)

- Abra DevTools (F12)
- Vá em **Console**
- Verifique se há erros em vermelho

---

## ⚠️ Problemas Comuns

### Erro: "Cannot find module '@rotina/shared'"

**Solução**: 
- Os packages já foram buildados
- Se persistir, reinicie o servidor (Ctrl+C e `pnpm dev` novamente)

### Erro: "Invalid API key"

**Solução**: 
1. Verifique se `.env.local` existe e está correto
2. Reinicie o servidor após criar/editar `.env.local`

### Erro: "Port 3001 already in use"

**Solução**: 
1. Pare o processo na porta 3001:
   ```bash
   lsof -ti:3001 | xargs kill -9
   ```
2. Ou mude a porta em `apps/web/package.json`

### Erro: "Failed to compile"

**Solução**: 
- Verifique os erros no terminal
- Pode ser problema de tipos TypeScript
- Os packages já foram buildados, então deve funcionar

---

## 🔐 Configurar URLs no Supabase (OBRIGATÓRIO)

**Antes de testar login**, configure:

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Settings** → **Authentication**
3. Role até **URL Configuration**
4. Em **Site URL**, adicione:
   ```
   http://localhost:3001
   ```
5. Em **Redirect URLs**, adicione:
   ```
   http://localhost:3001/**
   http://localhost:3001/app/today
   ```
6. Clique em **Save**

**Sem isso, o login NÃO funcionará!**

---

## 🧪 Testar Login

Após iniciar o app e configurar URLs:

1. Acesse: http://localhost:3001/login
2. Digite um email válido
3. Clique em "Enviar Magic Link"
4. Verifique seu email (pode estar na pasta spam)
5. Clique no link do email
6. **Deve redirecionar** para `/app/today`

---

## ✅ Checklist

- [x] Packages buildados
- [ ] App iniciado sem erros (`pnpm dev`)
- [ ] Acessa http://localhost:3001 sem erros
- [ ] Página de login aparece
- [ ] URLs configuradas no Supabase Auth
- [ ] Login funciona (magic link)
- [ ] Redirecionamento funciona

---

## 📊 Status Esperado

Após seguir todos os passos:

✅ App rodando em http://localhost:3001  
✅ Página de login carregando  
✅ Sem erros críticos no console  
✅ URLs configuradas no Supabase  
✅ Login funcionando  

**Pronto para usar!** 🎉

---

## 🆘 Se Algo Não Funcionar

1. **Verifique logs no terminal** - erros aparecem lá
2. **Verifique console do navegador** (F12) - erros de JavaScript
3. **Verifique `.env.local`** - credenciais corretas?
4. **Verifique URLs no Supabase** - configuradas?
5. **Reinicie o servidor** - `Ctrl+C` e `pnpm dev` novamente

---

## 📚 Próximos Passos Após App Funcionando

1. Criar usuário de teste (via login)
2. Criar organização/programa (via SQL ou interface admin)
3. Criar enrollment para o usuário
4. Testar funcionalidades:
   - Marcar refeições
   - Fazer check-in
   - Ver dashboard
   - Exportar CSV

