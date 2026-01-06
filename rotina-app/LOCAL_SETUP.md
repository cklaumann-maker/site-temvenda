# LOCAL_SETUP.md - Setup Local

## 🚀 Início Rápido

### Pré-requisitos

- Node.js 18+ 
- pnpm 8+
- Conta Supabase (ou Supabase CLI para local)

### Opção 1: Setup Automático (Recomendado)

```bash
cd rotina-app
chmod +x scripts/*.sh
./scripts/setup.sh
```

Depois configure `.env.local` e execute:

```bash
./scripts/dev.sh
```

### Opção 2: Setup Manual

#### 1. Instalar Dependências

```bash
cd rotina-app
pnpm install
```

#### 2. Configurar Variáveis de Ambiente

```bash
cp apps/web/.env.local.example apps/web/.env.local
```

Edite `apps/web/.env.local` com suas credenciais do Supabase:

```env
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key
```

#### 3. Build dos Packages Compartilhados

```bash
pnpm --filter shared build
pnpm --filter ui build
```

#### 4. Executar Migrations do Supabase

**Se usando Supabase remoto:**

```bash
cd supabase
supabase link --project-ref <seu-project-ref>
supabase db push
```

**Se usando Supabase local:**

```bash
./scripts/supabase-local.sh
# Depois execute as migrations
cd supabase
supabase db reset
```

#### 5. Iniciar Desenvolvimento

```bash
# Na raiz do projeto
pnpm dev

# Ou use o script
./scripts/dev.sh
```

O app estará disponível em: **http://localhost:3001**

---

## 🗄️ Supabase Local (Opcional)

Para desenvolvimento completo offline, você pode rodar Supabase localmente:

### Instalar Supabase CLI

```bash
# macOS
brew install supabase/tap/supabase

# ou via npm
npm install -g supabase
```

### Iniciar Supabase Local

```bash
./scripts/supabase-local.sh
```

Isso iniciará:
- API: http://localhost:54321
- Dashboard: http://localhost:54323
- Database: localhost:54322

### Configurar .env.local para Local

```env
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<veja output do supabase start>
SUPABASE_SERVICE_ROLE_KEY=<veja output do supabase start>
```

---

## 📋 Portas Utilizadas

| Serviço | Porta | URL |
|---------|-------|-----|
| Web App | 3001 | http://localhost:3001 |
| Supabase API (local) | 54321 | http://localhost:54321 |
| Supabase Dashboard (local) | 54323 | http://localhost:54323 |
| Supabase DB (local) | 54322 | localhost:54322 |

**Nota**: Portas 8000, 8001, 8080, 3000 são evitadas para não conflitar.

---

## 🔧 Comandos Úteis

### Desenvolvimento

```bash
# Iniciar web app
pnpm dev

# Iniciar mobile (Expo)
pnpm mobile

# Build completo
pnpm build

# Typecheck
pnpm typecheck

# Lint
pnpm lint
```

### Supabase

```bash
# Ver status (local)
cd supabase
supabase status

# Parar serviços (local)
supabase stop

# Ver logs (local)
supabase logs

# Reset database (local)
supabase db reset
```

---

## 🐛 Troubleshooting

### Erro: "Cannot find module '@rotina/shared'"

**Solução**: Build dos packages primeiro:
```bash
pnpm --filter shared build
pnpm --filter ui build
```

### Erro: "Port 3001 already in use"

**Solução**: Mude a porta em `apps/web/package.json`:
```json
"dev": "next dev -p 3002"
```

### Erro: "Invalid API key" ou "Unauthorized"

**Solução**: 
1. Verifique se `.env.local` está configurado corretamente
2. Verifique se as credenciais do Supabase estão corretas
3. Se usando Supabase local, verifique se está rodando: `supabase status`

### Erro: "RLS policy violation"

**Solução**: 
1. Verifique se as migrations foram executadas: `supabase db push`
2. Verifique se o usuário está autenticado
3. Verifique se o usuário tem role correta em `org_members`

### Erro: "daily_meals not found"

**Solução**: 
1. Verifique se há `plan_templates` para o programa
2. Verifique se o usuário tem `enrollment` ativo
3. A geração automática deve acontecer ao abrir `/app/today`

---

## 📝 Próximos Passos Após Setup

1. **Criar usuário de teste**:
   - Acesse http://localhost:3001/login
   - Use magic link com seu email
   - Crie perfil no Supabase

2. **Criar organização e programa** (via SQL ou admin):
   ```sql
   -- Exemplo básico (ajuste conforme necessário)
   INSERT INTO orgs (name, slug) VALUES ('Test Org', 'test-org');
   INSERT INTO programs (org_id, name) VALUES ('<org-id>', 'Test Program');
   ```

3. **Criar enrollment**:
   ```sql
   INSERT INTO enrollments (user_id, program_id, start_date)
   VALUES ('<user-id>', '<program-id>', CURRENT_DATE);
   ```

4. **Testar funcionalidades**:
   - Login
   - Tela "Hoje"
   - Check-in
   - Dashboard
   - Export CSV

---

## 🔐 Segurança Local

- **Nunca commite** `.env.local` no Git
- Use credenciais de desenvolvimento/teste
- Service Role Key deve ser mantida segura
- Em produção, use variáveis de ambiente do Vercel

---

## 📚 Documentação Adicional

- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deploy para produção
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - Arquitetura técnica
- [VALIDATION.md](./VALIDATION.md) - Validações pré-deploy







