# ✅ Verificar Aplicativo - Próximos Passos

## 🎉 Banco de Dados Configurado!

Agora vamos verificar se o aplicativo está funcionando corretamente.

---

## 📋 Checklist de Verificação

### 1. ✅ Configurar URLs Permitidas no Supabase Auth

**IMPORTANTE**: Sem isso, o login não funcionará!

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Vá em **Settings** → **Authentication**
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

---

### 2. ✅ Verificar Arquivo .env.local

Certifique-se de que o arquivo `apps/web/.env.local` existe e está configurado:

```bash
cd rotina-app
cat apps/web/.env.local
```

**Deve conter**:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

Se não existir, crie:
```bash
cp apps/web/env.local.CONFIGURAR apps/web/.env.local
```

---

### 3. ✅ Build dos Packages Compartilhados

```bash
cd rotina-app

# Build dos packages
pnpm --filter shared build
pnpm --filter ui build
```

**Esperado**: Build sem erros

---

### 4. ✅ Instalar Dependências (se necessário)

```bash
cd rotina-app
pnpm install
```

---

### 5. ✅ Iniciar Aplicativo

```bash
cd rotina-app
pnpm dev
```

**Esperado**: 
```
▲ Next.js 14.0.4
- Local:        http://localhost:3001
```

---

### 6. ✅ Testar Login

1. Acesse: http://localhost:3001/login
2. Digite um email válido
3. Clique em "Enviar Magic Link"
4. Verifique seu email (pode estar na pasta spam)
5. Clique no link do email
6. **Deve redirecionar** para `/app/today`

**Se funcionar**: ✅ Autenticação OK!

---

### 7. ✅ Verificar Tela "Hoje"

Após login, você deve ver:
- Tela `/app/today`
- Mensagem "Plano não disponível" (normal se não houver enrollment)
- Ou refeições do dia (se houver enrollment e templates)

---

### 8. ✅ Verificar Console do Navegador

1. Abra DevTools (F12)
2. Vá em **Console**
3. Verifique se há erros em vermelho

**Erros comuns**:
- `Invalid API key` → Verifique `.env.local`
- `RLS policy violation` → Normal se não houver dados/permissões
- `Cannot find module` → Execute build dos packages

---

## 🧪 Testes Adicionais

### Teste 1: Verificar Conexão com Supabase

No console do navegador, execute:
```javascript
// Deve retornar informações do projeto
fetch('https://mgcoyeohqelystqmytah.supabase.co/rest/v1/', {
  headers: {
    'apikey': 'sua-anon-key',
    'Authorization': 'Bearer sua-anon-key'
  }
})
```

### Teste 2: Verificar Tabelas no Dashboard

1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Vá em **Table Editor**
3. Deve ver 10 tabelas:
   - profiles
   - orgs
   - org_members
   - programs
   - enrollments
   - rulesets
   - plan_templates
   - daily_meals
   - daily_checkins
   - rule_events

### Teste 3: Criar Dados de Teste (Opcional)

Se executou o seed, deve ter:
- 1 organização demo
- 1 programa demo
- Templates de semana 1

Verifique no **Table Editor**:
```sql
SELECT * FROM orgs;
SELECT * FROM programs;
SELECT COUNT(*) FROM plan_templates;
```

---

## 🐛 Troubleshooting

### Erro: "Invalid API key"

**Solução**:
1. Verifique `.env.local`
2. Reinicie o servidor: `Ctrl+C` e `pnpm dev` novamente

### Erro: "Cannot find module '@rotina/shared'"

**Solução**:
```bash
pnpm --filter shared build
pnpm --filter ui build
```

### Erro: "RLS policy violation"

**Solução**: 
- Normal se não houver dados
- Crie um perfil primeiro via SQL ou interface

### Erro: "Failed to fetch"

**Solução**:
1. Verifique URLs permitidas no Auth (passo 1)
2. Verifique se o projeto está ativo no Supabase
3. Verifique conexão com internet

### Login não redireciona

**Solução**:
1. Verifique URLs permitidas (passo 1)
2. Verifique console do navegador para erros
3. Tente limpar cookies e fazer login novamente

---

## 📊 Verificações Finais

### ✅ Checklist Completo

- [ ] URLs permitidas configuradas no Auth
- [ ] Arquivo `.env.local` existe e está correto
- [ ] Packages compartilhados buildados
- [ ] Dependências instaladas
- [ ] Aplicativo inicia sem erros (`pnpm dev`)
- [ ] Login funciona (magic link)
- [ ] Redirecionamento após login funciona
- [ ] Tela `/app/today` carrega
- [ ] Console do navegador sem erros críticos
- [ ] Tabelas visíveis no Supabase Dashboard

---

## 🎯 Próximos Passos Após Verificação

### 1. Criar Usuário de Teste Completo

Se o login funcionou, você precisa:

1. **Criar perfil** (pode ser automático via trigger)
2. **Criar organização** (ou usar a demo do seed)
3. **Criar enrollment** para o usuário

### 2. Testar Funcionalidades

- [ ] Marcar refeição como feita
- [ ] Fazer check-in diário
- [ ] Ver dashboard
- [ ] Ver plano completo
- [ ] Exportar CSV

### 3. Testar Admin (se tiver role)

- [ ] Acessar `/admin/members`
- [ ] Ver lista de membros
- [ ] Exportar templates

---

## 📚 Comandos Úteis

### Ver logs do servidor
```bash
# No terminal onde está rodando pnpm dev
# Os logs aparecem automaticamente
```

### Verificar tipos
```bash
pnpm typecheck
```

### Verificar lint
```bash
pnpm lint
```

### Build completo
```bash
pnpm build
```

---

## 🆘 Precisa de Ajuda?

Se encontrar problemas:

1. Verifique os logs no terminal
2. Verifique o console do navegador (F12)
3. Verifique os logs do Supabase Dashboard
4. Consulte `LOCAL_SETUP.md` para mais detalhes

---

## ✅ Status Esperado

Após seguir todos os passos, você deve ter:

✅ App rodando em http://localhost:3001  
✅ Login funcionando  
✅ Redirecionamento funcionando  
✅ Tela "Hoje" carregando  
✅ Sem erros críticos no console  

**Pronto para começar a usar!** 🚀







