# 🔍 Diagnóstico: Erro de Conexão com Supabase

## ❌ Problema

O endpoint `/health` está retornando:
```json
{
  "status": "ok",
  "database": "error"
}
```

Isso significa que o backend está rodando, mas **não consegue conectar ao Supabase**.

---

## ✅ Solução Passo a Passo

### 1. Aguardar Deploy (2-3 minutos)

Após o push, aguarde o Render fazer o deploy automático. Depois, teste novamente:

```
https://temvenda-finance-api.onrender.com/health
```

Agora você verá mais detalhes sobre o erro.

---

### 2. Verificar Variáveis de Ambiente no Render

No dashboard do Render, vá em:
1. **Seu serviço** → **Environment**
2. Verifique se estas variáveis estão configuradas:

#### ✅ Variáveis Obrigatórias:

```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-aqui
```

**⚠️ IMPORTANTE:**
- Use a **service_role key**, NÃO a anon key
- A URL deve ser exatamente: `https://xxxxx.supabase.co` (sem barra no final)
- A service_role key é muito longa (começa com `eyJ...`)

#### 📍 Onde encontrar no Supabase:

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em: **Settings** → **API**
4. **Project URL**: copie o valor (é o `SUPABASE_URL`)
5. **service_role key**: copie o valor (é o `SUPABASE_SERVICE_ROLE_KEY`)
   - ⚠️ Esta key está em "Project API keys" → "service_role" (secret)

---

### 3. Verificar se as Tabelas Existem

As tabelas do módulo financeiro precisam estar criadas no Supabase.

#### Executar Migrações SQL:

No Supabase Dashboard:
1. Vá em: **SQL Editor**
2. Execute os scripts na ordem:

**a) `backend/migrations/001_init_finance.sql`**
- Cria tabelas: `finance_month_runs`, `finance_daily`

**b) `backend/migrations/002_debts.sql`**
- Cria tabelas: `debts`, `debt_payments`

**c) `backend/migrations/003_expense_items.sql`**
- Cria tabela: `expense_items`

**d) `backend/migrations/004_finance_projection.sql`**
- Cria tabelas: `finance_settings`, `finance_projection_daily`

#### Verificar se as Tabelas Foram Criadas:

No SQL Editor, execute:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name LIKE 'finance%' 
  OR table_name LIKE 'debt%'
  OR table_name LIKE 'expense%'
ORDER BY table_name;
```

Deve retornar:
- `finance_daily`
- `finance_month_runs`
- `finance_projection_daily`
- `finance_settings`
- `debts`
- `debt_payments`
- `expense_items`

---

### 4. Testar Novamente

Após configurar as variáveis e criar as tabelas:

1. **Aguarde 1-2 minutos** para o Render recarregar as variáveis
2. Teste: `https://temvenda-finance-api.onrender.com/health`

**Resposta esperada:**
```json
{
  "status": "ok",
  "api": "running",
  "database": "ok",
  "config": {
    "supabase_url_configured": true,
    "supabase_key_configured": true
  },
  "database_tables": "accessible"
}
```

---

## 🔧 Troubleshooting

### Erro: "SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY não configurados"

**Causa:** Variáveis não foram adicionadas no Render

**Solução:**
1. Render Dashboard → Environment
2. Adicionar `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY`
3. Salvar e aguardar redeploy

---

### Erro: "Table 'finance_daily' does not exist"

**Causa:** Tabelas não foram criadas no Supabase

**Solução:**
1. Executar as migrações SQL no Supabase
2. Verificar se as tabelas foram criadas

---

### Erro: "Invalid API key" ou "401 Unauthorized"

**Causa:** Service role key incorreta

**Solução:**
1. Verificar se copiou a **service_role key** (não a anon key)
2. Verificar se não há espaços extras
3. A key deve começar com `eyJ...` e ser muito longa

---

### Erro: "Connection timeout" ou "Network error"

**Causa:** Problema de rede ou URL incorreta

**Solução:**
1. Verificar se `SUPABASE_URL` está correto (sem barra no final)
2. Verificar se o projeto Supabase está ativo
3. Testar a URL diretamente no navegador (deve retornar JSON)

---

## 📋 Checklist de Verificação

Antes de considerar resolvido, verifique:

- [ ] `SUPABASE_URL` configurado no Render
- [ ] `SUPABASE_SERVICE_ROLE_KEY` configurado no Render (service_role, não anon)
- [ ] Tabelas criadas no Supabase (executar migrações)
- [ ] Render fez redeploy após adicionar variáveis
- [ ] `/health` retorna `"database": "ok"`

---

## 🆘 Ainda com Problemas?

Se após seguir todos os passos ainda houver erro:

1. **Verificar logs do Render:**
   - Render Dashboard → Seu serviço → **Logs**
   - Procurar por erros relacionados a Supabase

2. **Testar conexão manualmente:**
   - No Supabase Dashboard → SQL Editor
   - Executar: `SELECT COUNT(*) FROM finance_daily;`
   - Se funcionar, o problema é na configuração do Render

3. **Verificar formato das variáveis:**
   - `SUPABASE_URL`: deve ser `https://xxxxx.supabase.co` (sem `/` no final)
   - `SUPABASE_SERVICE_ROLE_KEY`: deve ser uma string longa começando com `eyJ...`

---

## 💡 Dica

Após adicionar/alterar variáveis de ambiente no Render, o serviço faz **redeploy automático**. Aguarde 1-2 minutos e teste novamente.

