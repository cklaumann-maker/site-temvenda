# 📋 Resumo dos Ajustes Implementados - Baseado na Agenda de 19/12/2025

## ✅ Mudanças Implementadas

### 1. **Cálculo de Saída Real Corrigido** ✅
- **Problema:** Valor de saída real deve incluir "valor pago" + juros, condicionado à "data do pagamento"
- **Solução:**
  - Criada função `_recalculate_expenses_from_items()` que recalcula `expenses_paid` e `expenses_planned` baseado em `expense_items`
  - `expenses_paid` = soma de (amount_paid + interest) apenas para itens com `payment_date` preenchido
  - `expenses_planned` = soma de (amount + interest) para itens sem `payment_date` ou com `payment_date` futuro
  - Função é chamada automaticamente após inserir `expense_items` no `refresh_month()`

### 2. **Lógica de Compras - Regime de Caixa** ✅
- **Problema:** Compras à vista devem impactar caixa imediatamente, compras a prazo entram na saída prevista
- **Solução:**
  - Adicionado campo `purchases_credit` na tabela `finance_daily` (compras a prazo)
  - `purchases_planned` = compras à vista (impacto imediato no caixa)
  - `purchases_credit` = compras a prazo (saída prevista)
  - Atualizado cálculo de `cash_out_planned` para incluir `purchases_credit`
  - Atualizado cálculo de `cash_out_real` para incluir apenas `purchases_planned` (à vista)

### 3. **Despesas de Loja - Estrutura Criada** ✅
- **Problema:** Necessário consolidar retiradas de caixa, premiações semanais, teleentregas
- **Solução:**
  - Criada tabela `store_expenses` com campos:
    - `category`: 'descontão' ou 'mix_transformer'
    - `expense_type`: 'retirada_caixa', 'premiacao', 'teleentrega', 'outro'
  - Adicionado campo `store_expenses_total` na tabela `finance_daily`
  - Criados schemas `StoreExpenseCreateRequest`, `StoreExpenseOut`, `StoreExpensesResponse`
  - Trigger SQL para recalcular `store_expenses_total` automaticamente

### 4. **Projeção de 60 Dias Atualizada** ✅
- **Problema:** Projeção precisa considerar todas as saídas corretamente
- **Solução:**
  - Atualizado `refresh_projection()` para incluir:
    - `purchases_credit` (compras a prazo)
    - `store_expenses_total` (despesas de loja)
  - Saídas reais agora incluem todos os componentes

## 📝 Arquivos Modificados

### Backend
1. **`backend/migrations/006_store_expenses_and_purchase_types.sql`** (NOVO)
   - Migration para criar tabela `store_expenses`
   - Adicionar campos `purchases_credit` e `store_expenses_total` em `finance_daily`
   - Funções e triggers SQL para recálculo automático

2. **`backend/app/schemas.py`**
   - Adicionado `purchases_credit` e `store_expenses_total` em `FinanceDailyOut`
   - Adicionado `purchases_credit` em `ManagementEntryRequest`
   - Criados schemas para `StoreExpenseCreateRequest`, `StoreExpenseOut`, `StoreExpensesResponse`

3. **`backend/app/finance_service.py`**
   - Adicionada função `_recalculate_expenses_from_items()` para recalcular expenses baseado em expense_items
   - Atualizado `refresh_month()` para chamar recálculo após inserir expense_items
   - Atualizado cálculos de `cash_out_planned` e `cash_out_real` para incluir novos campos
   - Atualizado `refresh_projection()` para considerar todas as saídas
   - Atualizado `process_excel_month()` para incluir novos campos nos registros

## ⚠️ Pendências (Próximos Passos)

### 1. **Endpoints para Store Expenses** 🔲
- Criar endpoint `POST /api/finance/store-expenses` para criar despesa de loja
- Criar endpoint `GET /api/finance/store-expenses?month_code=XX-YY` para listar despesas
- Criar endpoint `PUT /api/finance/store-expenses/{id}` para atualizar despesa
- Criar endpoint `DELETE /api/finance/store-expenses/{id}` para deletar despesa

### 2. **Frontend - Interface de Despesas de Loja** 🔲
- Adicionar botão "Despesa de Loja" na interface
- Criar modal para cadastrar despesa (valor, descrição, categoria, tipo)
- Adicionar coluna "Despesas Loja" na tabela de fluxo de caixa
- Criar aba "Consolidação Mensal" para visualizar despesas por categoria

### 3. **Frontend - Compras à Vista vs A Prazo** 🔲
- Atualizar modal de "Compras" para incluir campo "Tipo de Compra" (à vista / a prazo)
- Se à vista: preencher `purchases_planned`
- Se a prazo: preencher `purchases_credit`

### 4. **Executar Migration** 🔲
- Executar `backend/migrations/006_store_expenses_and_purchase_types.sql` no Supabase

### 5. **Testes** 🔲
- Testar recálculo de expenses após atualizar expense_items
- Testar criação de despesas de loja
- Testar compras à vista vs a prazo
- Testar projeção de 60 dias com todas as saídas

## 📌 Notas Importantes

1. **Recálculo de Expenses:** A função `_recalculate_expenses_from_items()` é chamada automaticamente após inserir expense_items, mas também pode ser chamada manualmente se necessário.

2. **Triggers SQL:** Os triggers SQL na migration garantem que `store_expenses_total` seja recalculado automaticamente quando despesas de loja forem inseridas/atualizadas.

3. **Compatibilidade:** Os novos campos têm valores padrão (0.0), então não quebra compatibilidade com dados existentes.

4. **Regime de Caixa:** A lógica agora diferencia claramente:
   - **Compras à vista** (`purchases_planned`): Impactam caixa imediatamente (entram em `cash_out_real`)
   - **Compras a prazo** (`purchases_credit`): Entram apenas em `cash_out_planned` até serem pagas

