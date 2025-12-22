# 🔧 Como Configurar Conexão com Supabase

## 📋 Informações Necessárias

Você precisa de **3 informações** do Supabase para configurar a conexão:

1. **Project URL** (NEXT_PUBLIC_SUPABASE_URL)
2. **Anon/Public Key** (NEXT_PUBLIC_SUPABASE_ANON_KEY)
3. **Service Role Key** (SUPABASE_SERVICE_ROLE_KEY) - Opcional, mas recomendado

---

## 🎯 Passo a Passo para Obter as Credenciais

### 1. Acessar o Dashboard do Supabase

1. Acesse [https://supabase.com](https://supabase.com)
2. Faça login na sua conta
3. Selecione seu projeto (ou crie um novo)

### 2. Obter Project URL

1. No dashboard do Supabase, vá em **Settings** (⚙️) no menu lateral
2. Clique em **API** na submenu
3. Na seção **Project URL**, você verá algo como:
   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```
4. **Copie essa URL completa** - essa é sua `NEXT_PUBLIC_SUPABASE_URL`

### 3. Obter Anon/Public Key

1. Na mesma página **Settings > API**
2. Na seção **Project API keys**
3. Procure por **`anon` `public`** key
4. Você verá algo como:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHh4eHh4eHgiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY0NzE5MjgwMCwiZXhwIjoxOTYyNzY4ODAwfQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
5. Clique no ícone de **copiar** (📋) ao lado da chave
6. **Essa é sua `NEXT_PUBLIC_SUPABASE_ANON_KEY`**

### 4. Obter Service Role Key (Opcional mas Recomendado)

1. Na mesma página **Settings > API**
2. Na seção **Project API keys**
3. Procure por **`service_role` `secret`** key
4. ⚠️ **ATENÇÃO**: Esta chave tem acesso total ao banco (bypassa RLS)
5. Clique em **Reveal** para mostrar a chave
6. Você verá algo como:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHh4eHh4eHgiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjQ3MTkyODAwLCJleHAiOjE5NjI3Njg4MDB9.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
7. Clique no ícone de **copiar** (📋)
8. **Essa é sua `SUPABASE_SERVICE_ROLE_KEY`**

---

## 📝 Exemplo de Arquivo .env.local

Depois de obter as credenciais, seu arquivo `apps/web/.env.local` deve ficar assim:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHh4eHh4eHgiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY0NzE5MjgwMCwiZXhwIjoxOTYyNzY4ODAwfQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHh4eHh4eHgiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjQ3MTkyODAwLCJleHAiOjE5NjI3Njg4MDB9.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Porta do servidor (padrão: 3001)
PORT=3001
```

---

## 🖼️ Onde Encontrar no Dashboard (Visual)

```
Supabase Dashboard
├── ⚙️ Settings (menu lateral)
    └── 📡 API
        ├── Project URL ──────────────> NEXT_PUBLIC_SUPABASE_URL
        └── Project API keys
            ├── anon public ──────────> NEXT_PUBLIC_SUPABASE_ANON_KEY
            └── service_role secret ──> SUPABASE_SERVICE_ROLE_KEY
```

---

## ✅ Checklist de Configuração

- [ ] Criei/tenho projeto no Supabase
- [ ] Copiei o **Project URL**
- [ ] Copiei a **anon/public key**
- [ ] Copiei a **service_role key** (opcional)
- [ ] Criei arquivo `apps/web/.env.local`
- [ ] Colei as credenciais no arquivo
- [ ] Salvei o arquivo

---

## 🔒 Segurança

### ⚠️ IMPORTANTE:

1. **NUNCA** commite o arquivo `.env.local` no Git
2. O arquivo já está no `.gitignore` (seguro)
3. **Service Role Key** tem acesso total - mantenha segura
4. **Anon Key** é pública (pode estar no código), mas protegida por RLS

### O que cada chave faz:

- **Anon Key**: Usada no cliente (browser/mobile), protegida por RLS
- **Service Role Key**: Usada apenas server-side, bypassa RLS (cuidado!)

---

## 🧪 Testar Conexão

Após configurar, teste a conexão:

```bash
# Iniciar desenvolvimento
pnpm dev

# Acessar
http://localhost:3001/login

# Tentar fazer login - se funcionar, conexão está OK!
```

---

## 🆘 Problemas Comuns

### Erro: "Invalid API key"
- Verifique se copiou a chave completa (são muito longas)
- Verifique se não há espaços extras
- Verifique se está usando a chave correta (anon vs service_role)

### Erro: "Failed to fetch"
- Verifique se o Project URL está correto
- Verifique se o projeto está ativo no Supabase
- Verifique conexão com internet

### Erro: "RLS policy violation"
- Normal! Significa que RLS está funcionando
- Execute as migrations primeiro (veja próximo passo)

---

## 📚 Próximos Passos

Após configurar as credenciais:

1. **Executar Migrations**:
   ```bash
   cd supabase
   supabase link --project-ref <seu-project-ref>
   supabase db push
   ```

2. **Configurar URLs Permitidas** (Auth):
   - No Supabase Dashboard: Settings > Authentication > URL Configuration
   - Adicionar: `http://localhost:3001`
   - Adicionar: `https://rotina.temvenda.com.br` (produção)

3. **Testar Login**:
   - Acesse http://localhost:3001/login
   - Tente fazer login com magic link

---

## 📞 Precisa de Ajuda?

- [Documentação Supabase](https://supabase.com/docs)
- [Guia de API Keys](https://supabase.com/docs/guides/api/api-keys)
- [Troubleshooting](https://supabase.com/docs/guides/getting-started/troubleshooting)

