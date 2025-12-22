# 🧪 Teste Local - Backend Financeiro

## ✅ Passo 1: Configurar API URL para Local

O arquivo `caixa/config-api.js` está apontando para produção. Para testar localmente, você tem duas opções:

### Opção A: Comentar a linha de produção (Recomendado)

Edite `caixa/config-api.js`:

```javascript
// window.FINANCE_API_URL = "https://temvenda-finance-api.onrender.com"; // Comentar esta linha

// Descomentar para desenvolvimento local:
window.FINANCE_API_URL = "http://localhost:8001";
```

### Opção B: O código já tem fallback

O código em `caixa/index.html` já tem um fallback:
```javascript
const API_URL = window.FINANCE_API_URL || "http://localhost:8001";
```

Se você **não carregar** o `config-api.js` ou comentar a linha, ele usará `http://localhost:8001` automaticamente.

---

## ✅ Passo 2: Verificar Backend Local

### 2.1. Verificar se o backend está rodando

```bash
# Verificar se há processo rodando na porta 8001
lsof -i :8001
# ou
ps aux | grep uvicorn
```

### 2.2. Iniciar o backend (se não estiver rodando)

```bash
cd backend
source .venv/bin/activate  # ou: python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## ✅ Passo 3: Verificar Variáveis de Ambiente Locais

Crie/verifique o arquivo `backend/.env`:

```bash
cd backend
cat .env
```

O arquivo deve conter:

```env
# Auth
APP_PASSWORD=sua-senha-aqui
JWT_SECRET_KEY=sua-chave-secreta-aqui
JWT_ACCESS_EXPIRES_HOURS=8

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key

# Google Drive
DRIVE_FILE_ID=id-do-arquivo-excel
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}  # JSON em uma linha

# CORS (opcional para local)
FRONTEND_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

---

## ✅ Passo 4: Testar Endpoint de Health

Abra no navegador ou use curl:

```bash
curl http://localhost:8001/health
```

Deve retornar:
```json
{
  "status": "ok",
  "api": "running",
  "database": "ok",
  ...
}
```

---

## ✅ Passo 5: Testar Login

### 5.1. Via Frontend

1. Acesse `http://localhost:8000/caixa/`
2. Digite a senha configurada em `APP_PASSWORD`
3. Clique em "Entrar"

### 5.2. Via cURL (para debug)

```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"sua-senha-aqui"}'
```

Deve retornar um token JWT.

---

## ✅ Passo 6: Testar Refresh do Mês

### 6.1. Via Frontend

1. Após fazer login, selecione o mês (ex: `12-25`)
2. Clique em "🔄 Atualizar Fluxo"
3. Verifique o console do navegador (F12) para ver erros

### 6.2. Via cURL (para debug)

```bash
# Primeiro, faça login e copie o token
TOKEN="seu-token-jwt-aqui"

# Depois, teste o refresh
curl -X POST "http://localhost:8001/api/admin/refresh?monthCode=12-25" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔍 Diagnóstico de Problemas

### Problema: "Failed to fetch" ou "Network error"

**Causa:** Backend não está rodando ou porta errada.

**Solução:**
1. Verificar se o backend está rodando: `lsof -i :8001`
2. Iniciar o backend: `uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload`
3. Verificar se a URL no frontend está correta: `http://localhost:8001`

---

### Problema: "401 Unauthorized" no login

**Causa:** Senha incorreta ou `APP_PASSWORD` não configurado.

**Solução:**
1. Verificar `APP_PASSWORD` no `.env`
2. Usar a mesma senha no frontend

---

### Problema: "500 Internal Server Error" no refresh

**Causa:** Variáveis de ambiente não configuradas ou erros no processamento.

**Solução:**
1. Verificar logs do backend (terminal onde está rodando)
2. Verificar se `DRIVE_FILE_ID` e `GOOGLE_SERVICE_ACCOUNT_JSON` estão no `.env`
3. Verificar se o Service Account tem permissão no arquivo do Google Drive

---

### Problema: "DRIVE_FILE_ID não configurado"

**Causa:** Variável `DRIVE_FILE_ID` não está no `.env`.

**Solução:**
1. Adicionar `DRIVE_FILE_ID=id-do-arquivo` no `backend/.env`
2. Reiniciar o backend

---

### Problema: "Credenciais de service account não configuradas"

**Causa:** `GOOGLE_SERVICE_ACCOUNT_JSON` não está no `.env` ou formato incorreto.

**Solução:**
1. Converter o JSON para uma linha:
   ```bash
   cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))"
   ```
2. Copiar o resultado e colar no `.env`:
   ```env
   GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
   ```
3. Reiniciar o backend

---

## 📋 Checklist de Teste Local

- [ ] Backend rodando em `http://localhost:8001`
- [ ] `/health` retorna `{"status":"ok","database":"ok"}`
- [ ] Login funciona no frontend
- [ ] `config-api.js` comentado ou usando `localhost:8001`
- [ ] Frontend acessível em `http://localhost:8000/caixa/`
- [ ] Variáveis de ambiente configuradas no `backend/.env`
- [ ] "Atualizar Fluxo" funciona sem erros
- [ ] Dados aparecem na tabela após refresh

---

## 🚀 Comandos Rápidos

```bash
# Iniciar backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Em outro terminal: Iniciar frontend
cd /Users/cesark/site-temvenda
python3 -m http.server 8000

# Testar health
curl http://localhost:8001/health

# Testar login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"sua-senha"}'
```

