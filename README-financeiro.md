## Módulo Financeiro – Fluxo de Caixa (MVP)

Este módulo adiciona um backend em FastAPI e um frontend em Next.js para visualizar e operar o fluxo de caixa diário usando uma planilha do Google Drive como fonte principal.

### Estrutura do projeto

- `backend/` – API em FastAPI (Python)
  - `app/main.py` – aplicação FastAPI e endpoints
  - `app/config.py` – configuração via variáveis de ambiente
  - `app/db.py` – conexão com Postgres (Supabase)
  - `app/models.py` – modelos SQLAlchemy (`finance_daily`, `finance_month_runs`)
  - `app/finance_service.py` – regras de negócio (forecast, parser de Excel, refresh)
  - `app/google_drive.py` – download do Excel do Google Drive via Service Account
  - `app/auth.py` – autenticação com senha única + JWT
  - `app/schemas.py` – modelos Pydantic dos endpoints
  - `migrations/001_init_finance.sql` – script SQL para criar tabelas no Supabase
  - `tests/test_forecast.py` – testes mínimos das regras de forecast e monthCode
- `frontend/` – app Next.js com página `/financeiro`
  - `app/financeiro/page.tsx` – UI de login, dashboard e formulários de lançamento

### Variáveis de ambiente – Backend

Crie um arquivo `.env` dentro de `backend/` (ou configure no ambiente) com:

- `APP_PASSWORD` – senha única de acesso ao módulo financeiro (ex.: `MinhaSenhaForte123`)
- `JWT_SECRET_KEY` – chave secreta para assinar JWT
- `JWT_ACCESS_EXPIRES_HOURS` – horas de expiração do token (ex.: `8`)
- `DATABASE_URL` – string de conexão do Supabase Postgres com asyncpg, por exemplo:
  - `postgresql+asyncpg://usuario:senha@host:5432/banco`
- `FRONTEND_ORIGIN` – origem permitida para CORS, ex.: `http://localhost:3000`
- `DRIVE_FILE_ID` – ID do arquivo da planilha no Google Drive
- **Credenciais Google (escolha UMA opção)**:
  - `GOOGLE_SERVICE_ACCOUNT_JSON` – JSON completo da service account em uma única string
  - **ou** `GOOGLE_APPLICATION_CREDENTIALS` – caminho absoluto para o arquivo `.json` da service account

A planilha deve conter abas no padrão:

- `DIST {MM-YY}` e `DESP {MM-YY}` – por exemplo `DIST 12-25`, `DESP 12-25`

Colunas esperadas (com tolerância a nomes/ordem):

- Em `DIST`:
  - `Vencimento` (ou 1ª coluna)
  - `Valor` (ou 5ª coluna)
  - `Valor pago` (ou 6ª coluna)
- Em `DESP`:
  - `Vencimento` (ou 1ª coluna)
  - `Valor` (ou 6ª coluna)
  - `Valor pago` (ou 7ª coluna)

### Variáveis de ambiente – Frontend

Crie um `.env.local` dentro de `frontend/` com:

- `NEXT_PUBLIC_FINANCE_API_URL` – URL base do backend, ex.:
  - `http://localhost:8001`

### Configurando o Supabase

No painel do Supabase, execute o conteúdo de `backend/migrations/001_init_finance.sql` na aba SQL:

- Cria as tabelas:
  - `finance_month_runs`
  - `finance_daily`
- Garante índices e unique index em `(month_code, date)`.

Não é necessário criar políticas RLS se o acesso for apenas pelo backend (via `DATABASE_URL` com service key).

### Como rodar localmente – Backend

1. Entre na pasta do backend:

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure o `.env` com as variáveis descritas acima.

3. Inicialize o servidor:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

4. Teste o healthcheck:

   - `GET http://localhost:8001/health` → `{ "status": "ok" }`

### Como rodar localmente – Frontend (/financeiro)

1. Entre na pasta `frontend`:

   ```bash
   cd frontend
   npm install
   # ou
   pnpm install
   ```

2. Crie `.env.local` com:

   ```bash
   NEXT_PUBLIC_FINANCE_API_URL=http://localhost:8001
   ```

3. Rode o servidor de desenvolvimento:

   ```bash
   npm run dev
   # ou
   pnpm dev
   ```

4. Abra no navegador:

   - `http://localhost:3000/financeiro`

### Fluxo típico de uso

1. Acesse `/financeiro`, digite a **senha única** definida em `APP_PASSWORD`.
2. Escolha o mês no formato `MM-YY` (ex.: `12-25`).
3. Clique em **“Carregar mês”** para buscar os dados consolidados do banco (`finance_daily`).
4. Se for o primeiro uso ou se desejar reprocessar a partir da planilha:
   - Clique em **“Atualizar da planilha”** → chama `POST /api/admin/refresh?monthCode=MM-YY`
   - Isso:
     - Apaga todos os registros de `finance_daily` para o `month_code`
     - Baixa o Excel da planilha do Drive e reprocessa o mês
     - Recria os registros do mês com forecast + despesas da planilha (sem lançamentos manuais)
5. No dashboard:
   - Veja o horizonte diário com vendas, entradas, despesas, compras, dívidas e saldo.
   - Clique em um dia para selecionar.
6. Aba **“Entrada do dia”**:
   - Lance Dinheiro, PIX, Cartão e Convênio reais.
   - O backend recalcula `cash_in_used` (substituindo a previsão, se houver valor real) e atualiza os saldos.
7. Aba **“Ajustes”**:
   - Informe Compras do dia, Dívidas antigas pagas e Futuras entradas confirmadas.

### Endpoints principais (backend)

- `POST /api/auth/login` – body `{ "password": "..." }` → `{ "access_token": "..." }`
- `GET /api/months/current?monthCode=12-25` – retorna `{ month_code, days: [...] }`
- `POST /api/days/{date}/cash-entry` – salva entradas reais (Dinheiro, PIX, Cartão, Convênio)
- `POST /api/days/{date}/management` – salva compras, dívidas e futuras entradas
- `POST /api/days/{date}/sales` – salva vendas do dia
- `POST /api/admin/refresh?monthCode=12-25` – reprocessa o mês a partir da planilha
- `GET /health` – simples verificação de status

### Módulo de Dívidas Antigas Parceladas

Tabelas criadas em `backend/migrations/002_debts.sql`:

- `debts` – cabeçalho da dívida antiga
- `debt_installments` – parcelas geradas automaticamente
- `debt_installment_adjustments` – histórico de ajustes de valor de parcelas
- `debt_payments` – pagamentos realizados

Regras:

- Dívidas antigas **não impactam o caixa** até que uma parcela seja paga.
- Cada pagamento de parcela:
  - Marca a parcela como `PAGA`
  - Cria um registro em `debt_payments`
  - Soma o valor pago em `finance_daily.old_debts_paid` na data real do pagamento
  - Recalcula `balance_projected` e `balance_real` do dia
- Status da dívida:
  - `Quitada`: todas as parcelas pagas
  - `Inadimplente`: existe parcela não paga com vencimento anterior a hoje
  - `Parcialmente paga`: alguma parcela paga e nenhuma em atraso
  - `Aberta`: nenhuma paga e sem atraso

Endpoints:

- `POST /api/debts` – cadastra uma dívida antiga e gera parcelas automaticamente
- `GET /api/debts` – lista dívidas com total, valor pago e saldo restante
- `GET /api/debts/{id}` – detalhes da dívida + parcelas
- `PUT /api/debts/{id}` – atualiza dados básicos da dívida (categoria, credor, descrição, data inicial)
- `POST /api/debts/{id}/installments/{installment_id}/adjust` – ajusta valor de uma parcela (registra histórico)
- `POST /api/debts/{id}/installments/{installment_id}/pay` – registra pagamento de parcela e integra no fluxo diário
- `GET /api/debts/{id}/history` – histórico combinado de ajustes e pagamentos por dívida

Importante:

- Antes de pagar uma parcela, o mês correspondente deve ter sido atualizado/refrescado em `finance_daily` (`/api/admin/refresh`), para que o dia exista no fluxo.

Todos os endpoints (exceto `/health` e `/api/auth/login`) exigem header:

```http
Authorization: Bearer {token}
```

### Testes rápidos

Dentro de `backend/`:

```bash
pytest
```

Há testes cobrindo:

- Conversão de `monthCode` (`parse_month_code`)
- Regras de forecast por dia da semana (`build_forecast_for_day`)


