# 🔒 Prioridade de Valores Manuais sobre Planilha

## ✅ Problema Resolvido

**ANTES:**
- ❌ Quando você atualizava o fluxo, os valores manuais eram perdidos
- ❌ A planilha sobrescrevia tudo, incluindo entradas cadastradas manualmente

**AGORA:**
- ✅ Valores manuais têm **PRIORIDADE** sobre valores da planilha
- ✅ Quando você atualiza o fluxo, os valores manuais são preservados
- ✅ A planilha só preenche campos que não foram cadastrados manualmente

---

## 🔄 Como Funciona Agora

### Processo de "Atualizar Fluxo":

1. **Salva valores manuais:**
   - Sistema identifica quais dias têm valores cadastrados manualmente
   - Salva: entradas (money, pix, card, convenio), compras, vendas, futuras entradas

2. **Apaga e recria da planilha:**
   - Apaga registros antigos
   - Importa novos dados da planilha
   - Cria registros com valores da planilha

3. **Restaura valores manuais:**
   - Para cada dia que tinha valores manuais, restaura esses valores
   - **Sobrescreve** os valores da planilha com os valores manuais
   - Recalcula saldos com os valores manuais preservados

---

## 📊 Valores que São Preservados

### ✅ Entradas Manuais (têm prioridade):
- `cash_in_actual_money` - Dinheiro cadastrado
- `cash_in_actual_pix` - PIX cadastrado
- `cash_in_actual_card` - Cartão cadastrado
- `cash_in_actual_convenio` - Convênio cadastrado

### ✅ Compras Manuais (têm prioridade):
- `purchases_planned` - Valor disponibilizado para compras

### ✅ Outros Valores Manuais:
- `future_in_confirmed` - Futuras entradas confirmadas
- `sales` - Vendas cadastradas

### ⚠️ Valores da Planilha (usados apenas se não houver manual):
- `expenses_planned` - Despesas planejadas (da planilha)
- `expenses_paid` - Despesas pagas (da planilha)
- `cash_in_forecast_total` - Previsão de entradas (da planilha)

---

## 🧪 Como Testar

### Teste 1: Entrada Manual Preservada

1. Cadastre uma entrada do dia (ex: R$ 100 em dinheiro)
2. Clique em "🔄 Atualizar Fluxo"
3. Verifique se o valor de R$ 100 ainda está lá
4. ✅ **Resultado esperado:** Valor preservado

### Teste 2: Compra Manual Preservada

1. Cadastre uma compra do dia (ex: R$ 50)
2. Clique em "🔄 Atualizar Fluxo"
3. Verifique se o valor de R$ 50 ainda está lá
4. ✅ **Resultado esperado:** Valor preservado

### Teste 3: Planilha Atualiza Apenas Campos Vazios

1. Deixe um dia sem entrada manual
2. Clique em "🔄 Atualizar Fluxo"
3. Verifique se a planilha preencheu os campos vazios
4. ✅ **Resultado esperado:** Campos vazios preenchidos pela planilha

---

## 📋 Exemplo Prático

### Cenário:

**Dia 15/12/2025:**
- Você cadastrou manualmente: R$ 200 em PIX
- Planilha tem: R$ 150 em PIX

**Ao clicar em "🔄 Atualizar Fluxo":**

1. Sistema salva: `cash_in_actual_pix = 200` (manual)
2. Sistema apaga e recria da planilha: `cash_in_actual_pix = 150` (planilha)
3. Sistema restaura: `cash_in_actual_pix = 200` (manual) ✅
4. **Resultado final:** `cash_in_actual_pix = 200` (valor manual preservado)

---

## ⚠️ Importante

### O que é preservado:
- ✅ Valores cadastrados manualmente (entradas, compras, vendas)
- ✅ Saldos recalculados com valores manuais

### O que é atualizado da planilha:
- ✅ Despesas planejadas e pagas
- ✅ Previsões de entradas (apenas se não houver entrada manual)
- ✅ Itens de despesa detalhados

### O que acontece se você quiser usar valor da planilha:
- Se você cadastrou manualmente e quer usar o valor da planilha:
  1. Zere o valor manual (digite 0)
  2. Salve
  3. Atualize o fluxo
  4. O valor da planilha será usado

---

## 🔍 Verificação no Banco

### Como verificar se está funcionando:

1. **Antes de atualizar:**
   - Cadastre uma entrada manual
   - Anote o valor (ex: `cash_in_actual_pix = 200`)

2. **Atualize o fluxo:**
   - Clique em "🔄 Atualizar Fluxo"

3. **Verifique no Supabase:**
   - Vá em Table Editor → `finance_daily`
   - Filtre por data
   - Veja se `cash_in_actual_pix` ainda é 200 ✅

---

## 💡 Dica

Se você quiser **resetar** um valor manual e usar o da planilha:
1. Zere o campo manualmente (digite 0)
2. Salve
3. Atualize o fluxo
4. O valor da planilha será usado

---

## ✅ Resumo

- ✅ Valores manuais têm **PRIORIDADE TOTAL**
- ✅ Planilha só preenche campos vazios
- ✅ Atualizar fluxo não perde mais dados manuais
- ✅ Saldos são recalculados corretamente

