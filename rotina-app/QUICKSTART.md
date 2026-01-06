# 🚀 Quick Start - Rodar Localmente

## Passo a Passo Rápido

### 1. Instalar Dependências

```bash
cd rotina-app
pnpm install
```

### 2. Configurar Variáveis de Ambiente

Crie o arquivo `apps/web/.env.local`:

```bash
# Copiar exemplo
cp apps/web/env.example apps/web/.env.local
```

Edite `apps/web/.env.local` e adicione suas credenciais do Supabase:

```env
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-aqui
```

### 3. Build dos Packages Compartilhados

```bash
pnpm --filter shared build
pnpm --filter ui build
```

### 4. Executar Migrations (Supabase)

**Opção A: Supabase Remoto (Recomendado)**
```bash
cd supabase
supabase link --project-ref <seu-project-ref>
supabase db push
```

**Opção B: Supabase Local**
```bash
./scripts/supabase-local.sh
cd supabase
supabase db reset
```

### 5. Iniciar Desenvolvimento

```bash
# Na raiz do projeto
pnpm dev
```

O app estará rodando em: **http://localhost:3001** 🎉

---

## ✅ Verificação Rápida

Após iniciar, verifique:

1. ✅ App carrega em http://localhost:3001
2. ✅ Página de login aparece
3. ✅ Magic link funciona (verifique email)
4. ✅ Após login, redireciona para /app/today

---

## 🐛 Problemas Comuns

### "Cannot find module '@rotina/shared'"
```bash
pnpm --filter shared build
pnpm --filter ui build
```

### "Port 3001 already in use"
Mude a porta em `apps/web/package.json`:
```json
"dev": "next dev -p 3002"
```

### "Invalid API key"
Verifique se `.env.local` está configurado corretamente.

---

## 📚 Mais Informações

- [LOCAL_SETUP.md](./LOCAL_SETUP.md) - Guia completo de setup local
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deploy para produção







