# ✅ Adicionar Variáveis de Ambiente no Render

## 🎯 Variáveis Necessárias para Supabase

Você precisa adicionar **2 variáveis obrigatórias**:

1. `SUPABASE_URL`
2. `SUPABASE_SERVICE_ROLE_KEY`

---

## 📍 Passo a Passo

### 1. Acessar o Dashboard do Render

1. Acesse: https://dashboard.render.com
2. Faça login
3. Clique no seu serviço (ex: `temvenda-finance-api`)

### 2. Ir para Environment

1. No menu lateral, clique em **"Environment"**
2. Você verá a lista de variáveis de ambiente

### 3. Adicionar SUPABASE_URL

1. Clique em **"Add Environment Variable"**
2. **Key**: `SUPABASE_URL`
3. **Value**: `https://seu-projeto.supabase.co`
   - ⚠️ Substitua `seu-projeto` pelo ID do seu projeto Supabase
   - ⚠️ **SEM barra no final** (não coloque `/` no final)
4. Clique em **"Save"**

**Exemplo:**
```
Key: SUPABASE_URL
Value: https://abcdefghijklmnop.supabase.co
```

### 4. Adicionar SUPABASE_SERVICE_ROLE_KEY

1. Clique em **"Add Environment Variable"** novamente
2. **Key**: `SUPABASE_SERVICE_ROLE_KEY`
3. **Value**: Cole a service_role key do Supabase
   - ⚠️ É uma string MUITO longa (começa com `eyJ...`)
   - ⚠️ Use a **service_role key**, NÃO a anon key
4. Clique em **"Save"**

**Exemplo:**
```
Key: SUPABASE_SERVICE_ROLE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjE2MjM5MDIyLCJleHAiOjE3NzQwMTUwMjJ9.abc123def456...
```

---

## 🔍 Onde Encontrar no Supabase

### SUPABASE_URL:

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em: **Settings** → **API**
4. Procure por **"Project URL"**
5. Copie o valor (ex: `https://abcdefghijklmnop.supabase.co`)

### SUPABASE_SERVICE_ROLE_KEY:

1. No mesmo lugar (Settings → API)
2. Procure por **"Project API keys"**
3. Encontre a seção **"service_role"** (secret)
4. Clique em **"Reveal"** ou **"Show"** para ver a key
5. Copie a key completa (é muito longa!)

**⚠️ ATENÇÃO:**
- Use a **service_role** key (a que está marcada como "secret")
- **NÃO** use a **anon** key
- A service_role key tem permissões totais, por isso é secreta

---

## ✅ Após Adicionar

1. **Render fará redeploy automático** (aguarde 1-2 minutos)
2. Teste novamente: `https://temvenda-finance-api.onrender.com/health`
3. Deve retornar:
   ```json
   {
     "status": "ok",
     "api": "running",
     "database": "ok",
     "config": {
       "supabase_url_configured": true,
       "supabase_key_configured": true
     }
   }
   ```

---

## 🔧 Verificar se Funcionou

Após adicionar as variáveis e aguardar o redeploy:

1. Acesse: `https://temvenda-finance-api.onrender.com/health`
2. Se `"database": "ok"` → ✅ Funcionando!
3. Se ainda `"database": "error"` → Verificar:
   - Se copiou a URL correta (sem barra no final)
   - Se copiou a service_role key (não a anon key)
   - Se não há espaços extras nas variáveis

---

## 📋 Checklist

- [ ] `SUPABASE_URL` adicionada no Render
- [ ] `SUPABASE_SERVICE_ROLE_KEY` adicionada no Render
- [ ] Aguardou 1-2 minutos para redeploy
- [ ] Testou `/health` e retornou `"database": "ok"`

---

## 💡 Dica

Se você já tinha outras variáveis configuradas, elas continuam lá. Você só precisa adicionar essas duas novas.

