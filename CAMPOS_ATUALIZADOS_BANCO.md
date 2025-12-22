# 📊 Campos Atualizados no Banco de Dados

## ✅ Sim, está atualizando no banco de dados!

Quando você cadastra **Entradas do Dia** e **Compras do Dia**, os dados são salvos na tabela `finance_daily` do Supabase.

---

## 💰 Entradas do Dia

### Endpoint: `POST /api/days/{date}/cash-entry`

### Campos atualizados na tabela `finance_daily`:

1. **`cash_in_actual_money`** - Valor em dinheiro
2. **`cash_in_actual_pix`** - Valor via PIX
3. **`cash_in_actual_card`** - Valor via Cartão (Débito + Crédito somados)
4. **`cash_in_actual_convenio`** - Valor via Convênio
5. **`balance_projected`** - Saldo projetado (recalculado automaticamente)
6. **`balance_real`** - Saldo real (recalculado automaticamente)

### Como funciona:

```python
# O sistema:
1. Recebe os valores (money, pix, card, convenio)
2. Atualiza os campos cash_in_actual_* na tabela finance_daily
3. Recalcula automaticamente:
   - cash_in_total = soma de todas as entradas reais
   - balance_projected = sales + cash_in_total - cash_out_planned
   - balance_real = cash_in_total - cash_out_real
4. Salva tudo no banco
```

---

## 🛒 Compras do Dia

### Endpoint: `POST /api/days/{date}/management`

### Campos atualizados na tabela `finance_daily`:

1. **`purchases_planned`** - Valor disponibilizado para compras no dia
2. **`future_in_confirmed`** - Futuras entradas confirmadas (se você preencher)
3. **`balance_projected`** - Saldo projetado (recalculado automaticamente)
4. **`balance_real`** - Saldo real (recalculado automaticamente)

### Como funciona:

```python
# O sistema:
1. Recebe o valor de purchases_planned
2. Atualiza o campo purchases_planned na tabela finance_daily
3. Recalcula automaticamente:
   - cash_out_planned = expenses_planned + purchases_planned + old_debts_paid
   - cash_out_real = expenses_paid + purchases_planned + old_debts_paid
   - balance_projected = sales + cash_in_total - cash_out_planned
   - balance_real = cash_in_total - cash_out_real
4. Salva tudo no banco
```

---

## 📋 Estrutura da Tabela `finance_daily`

```sql
CREATE TABLE finance_daily (
    id uuid PRIMARY KEY,
    month_code text NOT NULL,
    date date NOT NULL,
    weekday text NOT NULL,
    
    -- Entradas
    cash_in_forecast_total numeric(14,2),  -- Previsão (da planilha)
    cash_in_actual_money numeric(14,2),    -- ✅ Atualizado quando você cadastra entradas
    cash_in_actual_pix numeric(14,2),     -- ✅ Atualizado quando você cadastra entradas
    cash_in_actual_card numeric(14,2),     -- ✅ Atualizado quando você cadastra entradas
    cash_in_actual_convenio numeric(14,2), -- ✅ Atualizado quando você cadastra entradas
    future_in_confirmed numeric(14,2),    -- ✅ Atualizado quando você cadastra compras/ajustes
    
    -- Saídas
    expenses_planned numeric(14,2),       -- Da planilha
    expenses_paid numeric(14,2),          -- Da planilha
    purchases_planned numeric(14,2),       -- ✅ Atualizado quando você cadastra compras
    old_debts_paid numeric(14,2),         -- De dívidas antigas
    
    -- Saldos (recalculados automaticamente)
    balance_projected numeric(14,2),       -- ✅ Recalculado automaticamente
    balance_real numeric(14,2),           -- ✅ Recalculado automaticamente
    
    -- Outros
    sales numeric(14,2),
    updated_at timestamptz
);
```

---

## 🔄 Fluxo Completo

### Quando você cadastra "Entradas do Dia":

1. ✅ Frontend envia: `{money: 100, pix: 200, card: 300, convenio: 50}`
2. ✅ Backend atualiza na tabela `finance_daily`:
   - `cash_in_actual_money = 100`
   - `cash_in_actual_pix = 200`
   - `cash_in_actual_card = 300`
   - `cash_in_actual_convenio = 50`
3. ✅ Backend recalcula:
   - `cash_in_total = 100 + 200 + 300 + 50 = 650`
   - `balance_projected = sales + 650 - cash_out_planned`
   - `balance_real = 650 - cash_out_real`
4. ✅ Salva tudo no banco
5. ✅ Frontend atualiza a tela com os novos valores

### Quando você cadastra "Compras do Dia":

1. ✅ Frontend envia: `{purchases_planned: 500}`
2. ✅ Backend atualiza na tabela `finance_daily`:
   - `purchases_planned = 500`
3. ✅ Backend recalcula:
   - `cash_out_planned = expenses_planned + 500 + old_debts_paid`
   - `cash_out_real = expenses_paid + 500 + old_debts_paid`
   - `balance_projected = sales + cash_in_total - cash_out_planned`
   - `balance_real = cash_in_total - cash_out_real`
4. ✅ Salva tudo no banco
5. ✅ Frontend atualiza a tela com os novos valores

---

## ✅ Verificação

### Como verificar se está salvando:

1. **No Supabase Dashboard:**
   - Vá em Table Editor → `finance_daily`
   - Filtre por data
   - Veja os campos `cash_in_actual_*` e `purchases_planned`

2. **Na tela do sistema:**
   - Cadastre uma entrada
   - Recarregue a página
   - Os valores devem estar lá

3. **No console do navegador:**
   - Abra F12 → Network
   - Cadastre uma entrada
   - Veja a requisição POST para `/api/days/{date}/cash-entry`
   - Deve retornar `{"status": "ok"}`

---

## 📝 Notas Importantes

### ✅ O que é persistido:
- Todas as entradas do dia (money, pix, card, convenio)
- Compras do dia (purchases_planned)
- Saldos recalculados automaticamente

### ⚠️ O que NÃO é persistido:
- Valores temporários que você digita mas não salva
- Valores que dão erro ao salvar

### 🔄 Sincronização:
- Os dados são salvos **imediatamente** quando você clica em "Salvar"
- Não precisa clicar em "Atualizar Fluxo" novamente
- Os dados ficam no banco mesmo se você fechar o navegador

---

## 🧪 Teste Rápido

1. Cadastre uma entrada do dia (ex: R$ 100 em dinheiro)
2. Verifique no Supabase se o campo `cash_in_actual_money` foi atualizado
3. Cadastre uma compra do dia (ex: R$ 50)
4. Verifique no Supabase se o campo `purchases_planned` foi atualizado
5. Veja se os saldos foram recalculados automaticamente

---

## 💡 Dica

Se quiser ver os dados em tempo real, você pode:
- Abrir o Supabase Dashboard em outra aba
- Cadastrar uma entrada no sistema
- Atualizar a tabela no Supabase
- Ver os valores atualizados instantaneamente!

