# 📋 Checklist Completo - Setup Projeção D+60

## 1️⃣ Banco de Dados (Supabase)

### Executar Migrations SQL

Execute **na ordem** no Supabase SQL Editor:

1. **`backend/migrations/004_finance_projection.sql`**
   - Cria tabela `finance_settings` (caixa inicial)
   - Cria tabela `finance_projection_daily` (projeção por dia)
   - Cria índices necessários

2. **Se ainda não executou:**
   - `backend/migrations/003_expense_items.sql` (ou `003_expense_items_add_fields.sql` se a tabela já existe)
   - `backend/migrations/002_debts.sql`

### Verificar Tabelas Criadas

```sql
-- Verificar se as tabelas existem
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('finance_settings', 'finance_projection_daily', 'expense_items', 'debts');
```

### Configurar Caixa Inicial (Opcional)

```sql
-- Inserir valor inicial de caixa (ajuste o valor conforme necessário)
INSERT INTO finance_settings (starting_cash, updated_at)
VALUES (0.00, NOW())
ON CONFLICT (id) DO UPDATE SET starting_cash = EXCLUDED.starting_cash;
```

---

## 2️⃣ Google Drive - Planilha de Projeção

### Criar Planilha de Projeção

1. **Criar nova planilha no Google Drive** (ou usar uma existente)
2. **Criar aba chamada `PROJECAO`** (exatamente esse nome)
3. **Estrutura da aba:**

| Data | Entrada_prevista | Saida_prevista | Observacao |
|------|------------------|----------------|------------|
| 2025-01-15 | 50000.00 | 20000.00 | Pagamento fornecedor X |
| 2025-01-20 | 45000.00 | 0 | - |
| 2025-01-25 | 60000.00 | 15000.00 | Salários |

**Colunas esperadas:**
- **Data**: formato `YYYY-MM-DD` ou `dd/mm/aaaa` (o sistema tenta ambos)
- **Entrada_prevista**: valor numérico (entradas de caixa previstas para o dia)
- **Saida_prevista**: valor numérico (saídas extras previstas, além do baseline)
- **Observacao**: texto livre (opcional)

### Compartilhar Planilha com Service Account

1. **Obter o email do Service Account:**
   - Se você já tem `GOOGLE_SERVICE_ACCOUNT_JSON`, o email está em `client_email`
   - Exemplo: `id-drive-reader@noticias-site-476917.iam.gserviceaccount.com`

2. **Compartilhar a planilha:**
   - Abrir a planilha no Google Drive
   - Clicar em "Compartilhar"
   - Adicionar o email do Service Account com permissão de **"Visualizador"**

3. **Obter o File ID:**
   - Abrir a planilha no navegador
   - URL será algo como: `https://docs.google.com/spreadsheets/d/1ABC123XYZ789/edit`
   - O File ID é: `1ABC123XYZ789` (parte entre `/d/` e `/edit`)

---

## 3️⃣ Variáveis de Ambiente (Backend)

### Arquivo `.env` no diretório `backend/`

Adicione/atualize as seguintes variáveis:

```bash
# Autenticação
APP_PASSWORD=descontao
JWT_SECRET_KEY=TV_financeiro_secret_923847923847923847
JWT_ACCESS_EXPIRES_HOURS=8

# Supabase
SUPABASE_URL=https://mgcoyeohqelystqmytah.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua_service_role_key_aqui

# CORS (frontend)
FRONTEND_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Google Drive - Planilha Principal (fluxo operacional)
DRIVE_FILE_ID=1pZ7etpHO3hVrRHyFtSARZ9KEH42UrtnXA6ERQsi7ORs
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}

# Google Drive - Planilha de Projeção D+60 (NOVA)
GOOGLE_PROJECTION_FILE_ID=SEU_FILE_ID_AQUI
```

**⚠️ IMPORTANTE:**
- Substitua `SEU_FILE_ID_AQUI` pelo File ID da planilha de projeção que você criou
- Se já tem `GOOGLE_SERVICE_ACCOUNT_JSON`, pode reutilizar (mesmo Service Account)
- Se não tem, pode usar `GOOGLE_APPLICATION_CREDENTIALS` apontando para arquivo JSON

---

## 4️⃣ Instalar Dependências (Backend)

```bash
cd backend

# Ativar ambiente virtual (se já existe)
source .venv/bin/activate

# OU criar novo ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar/atualizar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

**Verificar instalação:**
```bash
python -c "import fastapi, pandas, supabase; print('OK')"
```

---

## 5️⃣ Rodar Backend

```bash
cd backend
source .venv/bin/activate

# Rodar servidor FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --env-file .env
```

**Verificar se está rodando:**
- Abrir: `http://localhost:8001/health`
- Deve retornar: `{"status":"ok","database":"ok"}`

---

## 6️⃣ Testar Endpoints (Opcional)

### Testar Login
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"descontao"}'
```

### Testar Projeção (após login)
```bash
# 1. Obter token do login acima
TOKEN="seu_token_aqui"

# 2. Atualizar projeção
curl -X POST "http://localhost:8001/api/admin/projection/refresh?days=60" \
  -H "Authorization: Bearer $TOKEN"

# 3. Buscar projeção
curl -X GET "http://localhost:8001/api/projection?days=60" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 7️⃣ Frontend (HTML Estático)

### Rodar Servidor Local

```bash
# Na raiz do projeto (site-temvenda)
cd financeiro

# Usar Python HTTP server
python3 -m http.server 8000

# OU usar qualquer servidor estático
# Exemplo com Node.js: npx serve -p 8000
```

**Acessar:**
- Abrir: `http://localhost:8000/financeiro/index.html`
- Ou: `http://localhost:8000/` (se configurado)

---

## 8️⃣ Fluxo de Uso no Frontend

### Primeira Vez

1. **Login:**
   - Senha: `descontao` (ou a que você configurou em `APP_PASSWORD`)

2. **Carregar Mês Atual:**
   - Digite o mês no formato `MM-YY` (ex: `12-25`)
   - Clique em "Carregar mês"

3. **Atualizar Fluxo da Planilha Principal:**
   - Clique em "Atualizar da planilha"
   - Aguarde processamento (pode demorar alguns segundos)

4. **Configurar Caixa Inicial:**
   - Digite o valor inicial de caixa (ex: `100000.00`)
   - Clique em "Salvar caixa inicial"

5. **Atualizar Projeção D+60:**
   - Clique em "Atualizar projeção"
   - Aguarde processamento (lê planilha PROJECAO e calcula 60 dias)

6. **Visualizar Projeção:**
   - Clique na aba "Projeção 60 dias"
   - Veja a tabela com horizonte de 60 dias
   - Saldos negativos aparecem em vermelho

---

## 9️⃣ Troubleshooting

### Erro: "GOOGLE_PROJECTION_FILE_ID não configurado"
- Verifique se adicionou `GOOGLE_PROJECTION_FILE_ID` no `.env`
- Reinicie o backend após alterar `.env`

### Erro: "Aba PROJECAO não encontrada"
- Verifique se a aba se chama exatamente `PROJECAO` (maiúsculas)
- Verifique se a planilha foi compartilhada com o Service Account

### Erro: "Permission denied" no Google Drive
- Verifique se compartilhou a planilha com o email do Service Account
- Permissão mínima: "Visualizador"

### Erro: "Table finance_projection_daily does not exist"
- Execute a migration `004_finance_projection.sql` no Supabase

### Projeção não aparece no frontend
- Verifique se clicou em "Atualizar projeção" primeiro
- Verifique o console do navegador (F12) para erros
- Verifique se o backend está rodando na porta 8001

### Saldo acumulado começa errado
- Verifique o valor de `starting_cash` em `finance_settings`
- Use o botão "Salvar caixa inicial" para ajustar

---

## 🔟 Checklist Rápido

- [ ] Executou migration `004_finance_projection.sql` no Supabase
- [ ] Criou planilha de projeção no Google Drive com aba `PROJECAO`
- [ ] Compartilhou planilha com Service Account
- [ ] Adicionou `GOOGLE_PROJECTION_FILE_ID` no `.env` do backend
- [ ] Instalou dependências do backend (`pip install -r requirements.txt`)
- [ ] Backend rodando em `http://localhost:8001`
- [ ] Frontend acessível em `http://localhost:8000/financeiro`
- [ ] Fez login no frontend
- [ ] Carregou mês atual
- [ ] Atualizou fluxo da planilha principal
- [ ] Configurou caixa inicial
- [ ] Atualizou projeção D+60
- [ ] Visualizou projeção na aba "Projeção 60 dias"

---

## 📚 Documentação Adicional

- **README-financeiro.md**: Documentação geral do módulo financeiro
- **backend/app/finance_service.py**: Lógica de cálculo da projeção
- **backend/app/main.py**: Endpoints da API

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs do backend (terminal onde rodou `uvicorn`)
2. Verifique o console do navegador (F12 → Console)
3. Verifique se todas as migrations foram executadas
4. Verifique se as variáveis de ambiente estão corretas

