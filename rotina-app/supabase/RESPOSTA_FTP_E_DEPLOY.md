# Resposta: FTP e Deploy

## ❌ Não Precisa de FTP!

O projeto usa **Git + Vercel** para deploy automático. Não é necessário fazer transferência por FTP.

## 🚀 Como Funciona o Deploy

### Processo Automático:

1. **Você faz commit e push para GitHub:**
   ```bash
   git add .
   git commit -m "sua mensagem"
   git push origin main
   ```

2. **Vercel detecta automaticamente:**
   - O Vercel está conectado ao seu repositório GitHub
   - Quando você faz push, o Vercel detecta automaticamente
   - Inicia um novo deploy automaticamente

3. **Build e Deploy:**
   - Vercel executa `pnpm install`
   - Executa `pnpm run build`
   - Faz deploy da aplicação
   - A URL fica disponível em alguns minutos

### Verificar Status do Deploy:

1. Acesse: https://vercel.com/dashboard
2. Selecione seu projeto
3. Veja a aba "Deployments"
4. Cada commit aparece como um novo deployment

## ⏱️ Tempo de Deploy

- **Primeiro deploy**: 2-5 minutos
- **Deploys subsequentes**: 1-3 minutos
- **Atualizações pequenas**: 30 segundos - 2 minutos

## 🔍 Verificar se Deploy Foi Concluído

### No Vercel Dashboard:
1. Acesse o projeto
2. Veja o último deployment
3. Status deve estar "Ready" (verde)

### Na URL da Aplicação:
- Acesse a URL do Vercel
- Se as mudanças aparecerem, o deploy foi concluído
- Se não aparecerem, pode estar em cache - faça Ctrl+F5

## 🐛 Se as Mudanças Não Aparecerem

### 1. Verificar se o Deploy Foi Concluído
- Veja no Vercel Dashboard se há erros
- Verifique os logs do build

### 2. Limpar Cache do Navegador
- Ctrl+F5 (Windows/Linux)
- Cmd+Shift+R (Mac)
- Ou abra em modo anônimo

### 3. Verificar se o Código Foi Commitado
```bash
git log --oneline -5
```
- Verifique se seu commit está lá

### 4. Forçar Novo Deploy
- No Vercel Dashboard, clique em "Redeploy"
- Ou faça um commit vazio:
  ```bash
  git commit --allow-empty -m "forçar deploy"
  git push origin main
  ```

## 📝 Checklist Antes de Deploy

- [ ] Código commitado: `git status` mostra "nothing to commit"
- [ ] Código enviado: `git push origin main` executado
- [ ] Sem erros de build localmente (se testou)
- [ ] Variáveis de ambiente configuradas no Vercel

## 🔧 Configuração do Vercel

O projeto já está configurado com:
- `vercel.json` na raiz
- `apps/web/vercel.json` para o app Next.js
- Build command: `pnpm run build:vercel`
- Install command: `cd ../.. && pnpm install --no-frozen-lockfile`

## 💡 Dica

Se quiser ver o deploy em tempo real:
1. Abra o Vercel Dashboard
2. Vá em "Deployments"
3. Clique no deployment em andamento
4. Veja os logs em tempo real

## 🎯 Resumo

- ✅ **Não precisa FTP** - tudo é automático via Git
- ✅ **Deploy automático** - push no GitHub = deploy no Vercel
- ✅ **Verificar no Dashboard** - veja status e logs
- ✅ **Limpar cache** - se mudanças não aparecerem

