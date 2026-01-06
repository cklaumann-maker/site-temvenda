# DEPLOYMENT.md - Plano de Deploy

## Visão Geral

Este documento descreve o processo completo de deploy do Rotina App para produção.

**Domínio**: `rotina.temvenda.com.br`  
**Plataformas**: 
- Web: Vercel
- Backend: Supabase
- Mobile: EAS Build (Expo)

---

## 1. Pré-requisitos

### 1.1 Contas Necessárias
- [ ] Conta Vercel (vercel.com)
- [ ] Conta Supabase (supabase.com)
- [ ] Conta Expo (expo.dev)
- [ ] Domínio `temvenda.com.br` configurado no DNS

### 1.2 Ferramentas Locais
```bash
# Instalar ferramentas necessárias
npm install -g vercel
npm install -g supabase
npm install -g eas-cli
```

---

## 2. Setup do Supabase

### 2.1 Criar Projeto Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Anote:
   - Project URL
   - Anon Key
   - Service Role Key

### 2.2 Executar Migrations

```bash
cd rotina-app/supabase

# Linkar projeto local ao remoto
supabase link --project-ref <project-ref>

# Executar migrations
supabase db push

# Executar seed (opcional)
supabase db reset --seed
```

### 2.3 Configurar RLS Policies

As policies já estão incluídas em `20240101000002_rls_policies.sql`. Verifique se foram aplicadas:

```sql
-- Verificar policies
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

### 2.4 Configurar Auth

1. No dashboard do Supabase, vá em Authentication > URL Configuration
2. Adicione URLs permitidas:
   - `https://rotina.temvenda.com.br`
   - `rotina://` (para mobile)
   - `exp://` (para desenvolvimento mobile)

---

## 3. Deploy do Web App (Vercel)

### 3.1 Preparação

```bash
cd rotina-app/apps/web

# Instalar dependências
pnpm install

# Build local para testar
pnpm build
```

### 3.2 Configurar Variáveis de Ambiente

No dashboard do Vercel, adicione as seguintes variáveis:

```
NEXT_PUBLIC_SUPABASE_URL=<sua-url-supabase>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<sua-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<sua-service-role-key>
```

### 3.3 Deploy via Vercel CLI

```bash
# Login na Vercel
vercel login

# Deploy
vercel --prod

# Ou conectar ao GitHub e fazer deploy automático
```

### 3.4 Configurar Domínio

1. No dashboard do Vercel, vá em Settings > Domains
2. Adicione `rotina.temvenda.com.br`
3. Configure DNS no seu provedor:
   ```
   Tipo: CNAME
   Nome: rotina
   Valor: cname.vercel-dns.com
   ```

### 3.5 Verificar Deploy

- [ ] Acesse `https://rotina.temvenda.com.br`
- [ ] Teste login
- [ ] Teste rotas `/app/*`
- [ ] Teste rotas `/admin/*` (com usuário admin)

---

## 4. Deploy do Mobile App (Expo)

### 4.1 Configurar Expo

```bash
cd rotina-app/apps/mobile

# Login no Expo
eas login

# Configurar projeto
eas build:configure
```

### 4.2 Configurar Variáveis de Ambiente

Crie arquivo `eas.json`:

```json
{
  "build": {
    "production": {
      "env": {
        "EXPO_PUBLIC_SUPABASE_URL": "<sua-url-supabase>",
        "EXPO_PUBLIC_SUPABASE_ANON_KEY": "<sua-anon-key>"
      }
    }
  }
}
```

### 4.3 Build para Produção

```bash
# iOS
eas build --platform ios --profile production

# Android
eas build --platform android --profile production
```

### 4.4 Submeter para Stores

```bash
# iOS (requer conta Apple Developer)
eas submit --platform ios

# Android (requer conta Google Play)
eas submit --platform android
```

---

## 5. Configuração de DNS

### 5.1 Registro CNAME

No seu provedor de DNS, adicione:

```
Nome: rotina
Tipo: CNAME
Valor: cname.vercel-dns.com
TTL: 3600
```

### 5.2 Verificar DNS

```bash
# Verificar propagação
dig rotina.temvenda.com.br
nslookup rotina.temvenda.com.br
```

---

## 6. CI/CD Setup

### 6.1 GitHub Actions (Opcional)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm --filter web build
```

### 6.2 Vercel GitHub Integration

1. No dashboard do Vercel, vá em Settings > Git
2. Conecte seu repositório GitHub
3. Configure:
   - Production Branch: `main`
   - Build Command: `pnpm --filter web build`
   - Output Directory: `apps/web/.next`

---

## 7. Checklist de Produção

### 7.1 Segurança
- [ ] RLS policies aplicadas e testadas
- [ ] Service Role Key não exposta no cliente
- [ ] CORS configurado corretamente
- [ ] Rate limiting configurado (se necessário)

### 7.2 Performance
- [ ] Build otimizado (`pnpm build` sem erros)
- [ ] Imagens otimizadas
- [ ] Cache configurado
- [ ] CDN ativo (Vercel Edge Network)

### 7.3 Monitoramento
- [ ] Logs configurados (Vercel Analytics)
- [ ] Error tracking (Sentry opcional)
- [ ] Uptime monitoring

### 7.4 Backup
- [ ] Backup automático do Supabase configurado
- [ ] Backup de migrations versionado no Git

---

## 8. Variáveis de Ambiente - Resumo

### Web App (Vercel)
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

### Mobile App (EAS)
```
EXPO_PUBLIC_SUPABASE_URL
EXPO_PUBLIC_SUPABASE_ANON_KEY
```

---

## 9. Comandos de Validação

### 9.1 Pré-Deploy

```bash
# Na raiz do monorepo
pnpm install
pnpm lint
pnpm typecheck
pnpm --filter web build
```

### 9.2 Validação de Migrations

```bash
cd supabase
supabase db diff --schema public
```

### 9.3 Validação de RLS

```sql
-- Verificar se RLS está habilitado
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Verificar policies
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

---

## 10. Troubleshooting

### 10.1 Erro de Build

**Problema**: Build falha no Vercel  
**Solução**: 
- Verificar logs no dashboard do Vercel
- Testar build local: `pnpm --filter web build`
- Verificar variáveis de ambiente

### 10.2 Erro de RLS

**Problema**: Usuário não consegue acessar dados  
**Solução**:
- Verificar policies no Supabase
- Verificar se usuário está autenticado
- Verificar role do usuário em `org_members`

### 10.3 Erro de CORS

**Problema**: Erro de CORS no navegador  
**Solução**:
- Verificar URLs permitidas no Supabase Auth
- Verificar configuração de CORS no Supabase

### 10.4 Domínio não resolve

**Problema**: `rotina.temvenda.com.br` não carrega  
**Solução**:
- Verificar DNS propagation: `dig rotina.temvenda.com.br`
- Aguardar propagação (pode levar até 48h)
- Verificar configuração no Vercel

---

## 11. Rollback

### 11.1 Rollback no Vercel

```bash
# Listar deploys
vercel ls

# Rollback para deploy anterior
vercel rollback <deploy-url>
```

### 11.2 Rollback no Supabase

```bash
# Reverter migration específica
supabase migration repair <migration-name> --status reverted

# Ou restaurar backup
# No dashboard do Supabase: Settings > Database > Backups
```

---

## 12. Pós-Deploy

### 12.1 Testes em Produção

- [ ] Login funciona
- [ ] Rotas `/app/*` funcionam
- [ ] Rotas `/admin/*` funcionam (com RBAC)
- [ ] Exportação CSV funciona
- [ ] Geração de `daily_meals` funciona
- [ ] Check-in funciona
- [ ] Regras de doce funcionam

### 12.2 Monitoramento Inicial

- [ ] Verificar logs de erro
- [ ] Verificar performance
- [ ] Verificar uso de recursos (Supabase)

---

## 13. Manutenção Contínua

### 13.1 Atualizações

```bash
# Atualizar dependências
pnpm update

# Executar migrations novas
supabase db push

# Deploy automático via Vercel (se conectado ao GitHub)
```

### 13.2 Backup Regular

- Backup automático do Supabase (configurar no dashboard)
- Versionar migrations no Git
- Documentar mudanças em CHANGELOG.md

---

## 14. Contatos e Suporte

- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Supabase Support**: [supabase.com/support](https://supabase.com/support)
- **Expo Support**: [expo.dev/support](https://expo.dev/support)

---

## 15. Próximos Passos

Após deploy inicial:

1. Configurar analytics (opcional)
2. Configurar error tracking (Sentry)
3. Configurar monitoramento de uptime
4. Documentar processos de deploy para equipe
5. Criar runbook para incidentes







