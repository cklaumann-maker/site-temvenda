# 🚀 Deploy no Vercel - Guia Completo

## ✅ SIM, funciona perfeitamente no Vercel!

O projeto está configurado como monorepo e funciona perfeitamente no Vercel. Este guia mostra como fazer o deploy.

---

## 📋 Pré-requisitos

- [ ] Conta no Vercel (gratuita): https://vercel.com
- [ ] Projeto no GitHub (recomendado) ou GitLab/Bitbucket
- [ ] Credenciais do Supabase em produção

---

## 🔧 Passo 1: Configurar Projeto no Vercel

### Opção A: Via Dashboard (Recomendado)

1. **Acesse**: https://vercel.com/new
2. **Importe seu repositório**:
   - Conecte GitHub/GitLab/Bitbucket
   - Selecione o repositório `rotina-app`
3. **Configure o projeto**:
   - **Framework Preset**: Next.js (detectado automaticamente)
   - **Root Directory**: Deixe vazio (raiz do repositório) ⚠️ **IMPORTANTE**
   - O arquivo `vercel.json` já está configurado corretamente!
   - **Build Command**: Será usado do `vercel.json` (não precisa configurar)
   - **Output Directory**: Será usado do `vercel.json` (não precisa configurar)
   - **Install Command**: Será usado do `vercel.json` (não precisa configurar)

### Opção B: Via CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# No diretório do projeto
cd rotina-app

# Deploy (primeira vez)
vercel

# Deploy em produção
vercel --prod
```

---

## ⚙️ Passo 2: Configurar Variáveis de Ambiente

No dashboard do Vercel:

1. Vá em **Settings** > **Environment Variables**
2. Adicione as seguintes variáveis:

```
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-aqui
```

**⚠️ IMPORTANTE**: 
- Marque todas como **Production**, **Preview** e **Development**
- `NEXT_PUBLIC_*` são expostas no cliente
- `SUPABASE_SERVICE_ROLE_KEY` é apenas para server-side

---

## 📝 Passo 3: Arquivo de Configuração do Vercel

✅ **O arquivo `vercel.json` já está criado** na raiz do projeto (`rotina-app/vercel.json`)!

Ele contém a configuração correta para o monorepo:

```json
{
  "buildCommand": "pnpm install && pnpm --filter web build",
  "outputDirectory": "apps/web/.next",
  "installCommand": "pnpm install",
  "framework": "nextjs",
  "rootDirectory": "apps/web"
}
```

**O Vercel detectará automaticamente esta configuração!** Não é necessário configurar manualmente no dashboard, mas se preferir:

- **Root Directory**: `apps/web`
- **Build Command**: `pnpm install && pnpm --filter web build`
- **Output Directory**: `.next`
- **Install Command**: `pnpm install`

---

## 🎯 Passo 4: Configurar Monorepo no Vercel

Como o projeto usa **pnpm workspaces**, você precisa configurar:

### No Dashboard do Vercel:

1. **Settings** > **General**
2. **Root Directory**: `apps/web`
3. **Build & Development Settings**:
   - **Framework Preset**: Next.js
   - **Build Command**: `cd ../.. && pnpm install && pnpm --filter web build`
   - **Output Directory**: `.next`
   - **Install Command**: `cd ../.. && pnpm install`
   - **Node.js Version**: 18.x ou 20.x

### Ou criar `vercel.json` na raiz:

```json
{
  "buildCommand": "cd ../.. && pnpm install && pnpm --filter web build",
  "outputDirectory": ".next",
  "installCommand": "cd ../.. && pnpm install",
  "framework": "nextjs"
}
```

**⚠️ IMPORTANTE**: O arquivo `vercel.json` deve estar em `apps/web/` se você configurar Root Directory como `apps/web`.

---

## 🌐 Passo 5: Configurar Domínio Personalizado

### 5.1. No Vercel Dashboard

1. Vá em **Settings** > **Domains**
2. Adicione seu domínio: `rotina.temvenda.com.br`
3. O Vercel mostrará instruções de DNS

### 5.2. Configurar DNS

No seu provedor de DNS (onde está configurado `temvenda.com.br`):

**Opção A: CNAME (Recomendado)**
```
Tipo: CNAME
Nome: rotina
Valor: cname.vercel-dns.com
TTL: 3600
```

**Opção B: A Record**
```
Tipo: A
Nome: rotina
Valor: 76.76.21.21
TTL: 3600
```

### 5.3. Verificar SSL

O Vercel configura SSL automaticamente via Let's Encrypt. Aguarde alguns minutos após configurar o DNS.

---

## ✅ Passo 6: Verificar Deploy

### 6.1. Testar Build Localmente

```bash
cd rotina-app

# Instalar dependências
pnpm install

# Build
pnpm --filter web build

# Verificar se build foi bem-sucedido
ls -la apps/web/.next
```

### 6.2. Verificar no Vercel

1. Acesse o dashboard do Vercel
2. Vá em **Deployments**
3. Verifique se o build foi bem-sucedido
4. Clique no deployment para ver logs

### 6.3. Testar Aplicação

- [ ] Acesse a URL do Vercel (ex: `rotina-app.vercel.app`)
- [ ] Teste login
- [ ] Teste rotas `/app/*`
- [ ] Verifique se dados estão sendo salvos no Supabase

---

## 🔄 Passo 7: Deploy Automático (GitHub Integration)

### 7.1. Conectar ao GitHub

1. No dashboard do Vercel, vá em **Settings** > **Git**
2. Conecte seu repositório GitHub
3. Configure:
   - **Production Branch**: `main` ou `master`
   - **Auto-deploy**: Ativado

### 7.2. Deploy Automático

Agora, sempre que você fizer push para o branch principal:

```bash
git add .
git commit -m "Atualização"
git push origin main
```

O Vercel fará deploy automaticamente! 🎉

---

## 🐛 Troubleshooting

### Problema: Build falha com erro de workspace

**Solução**: Certifique-se de que:
- Root Directory está configurado como `apps/web`
- Build Command inclui `cd ../..` para voltar à raiz do monorepo
- `pnpm-workspace.yaml` está na raiz

### Problema: Erro "Cannot find module '@rotina/shared'"

**Solução**: 
- Verifique se `transpilePackages` está em `next.config.js` ✅ (já está)
- Certifique-se de que o build está sendo executado na raiz do monorepo

### Problema: Variáveis de ambiente não funcionam

**Solução**:
- Verifique se variáveis começam com `NEXT_PUBLIC_` para serem expostas no cliente
- Verifique se estão marcadas para Production/Preview/Development
- Faça um novo deploy após adicionar variáveis

### Problema: Erro de CORS no Supabase

**Solução**:
1. No Supabase Dashboard, vá em **Settings** > **API**
2. Em **Allowed URLs**, adicione:
   - `https://rotina.temvenda.com.br`
   - `https://rotina-app.vercel.app`
   - `https://*.vercel.app` (para previews)

---

## 📊 Monitoramento

### Logs em Tempo Real

```bash
# Via CLI
vercel logs

# Ou no dashboard
# Vercel Dashboard > Deployments > [Seu Deployment] > Logs
```

### Analytics

O Vercel fornece analytics básicos gratuitamente:
- **Dashboard** > **Analytics**
- Visualizações de página
- Performance metrics

---

## 🎯 Resumo Rápido

1. **Criar projeto no Vercel**: https://vercel.com/new
2. **Configurar Root Directory**: `apps/web`
3. **Configurar Build Command**: `cd ../.. && pnpm install && pnpm --filter web build`
4. **Adicionar variáveis de ambiente**: Supabase URL e Keys
5. **Configurar domínio**: Adicionar `rotina.temvenda.com.br`
6. **Configurar DNS**: CNAME para `cname.vercel-dns.com`
7. **Deploy**: Automático via GitHub ou manual via CLI

---

## ✅ Vantagens do Vercel

- ✅ **Deploy automático** via GitHub
- ✅ **SSL gratuito** automático
- ✅ **CDN global** (rápido em qualquer lugar)
- ✅ **Preview deployments** para cada PR
- ✅ **Rollback fácil** com um clique
- ✅ **Logs em tempo real**
- ✅ **Plano gratuito generoso**

---

## 🚀 Próximos Passos

Após deploy bem-sucedido:

1. ✅ Testar todas as funcionalidades
2. ✅ Configurar domínio personalizado
3. ✅ Configurar deploy automático
4. ✅ Monitorar logs e performance
5. ✅ Configurar alertas (opcional)

---

**🎉 Pronto! Sua aplicação estará no ar em minutos!**

