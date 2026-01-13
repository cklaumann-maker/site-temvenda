# Melhorias Implementadas na Área de Análises

## 1. Explicação do Gargalo (12/1/26)

O gargalo é detectado quando:
- O dia tem saídas (despesas + compras + cheques) acima do limiar
- Limiar = Média móvel de 30 dias + 2 desvios padrão
- OU top 10% dos dias com maior saída

**Por que 12/1/26?**
- Provavelmente há muitas despesas concentradas nesse dia
- Pode incluir folha de pagamento, aluguel, ou outras despesas essenciais
- O sistema identifica automaticamente baseado nos dados do banco

## 2. Tabela de Despesas com Marcação de Essenciais

### Migration necessária:
```sql
-- Execute no Supabase SQL Editor:
ALTER TABLE expense_items
ADD COLUMN IF NOT EXISTS is_essential BOOLEAN NOT NULL DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS idx_expense_items_is_essential ON expense_items(is_essential);
```

### Funcionalidades:
- ✅ Lista todas as despesas futuras na aba "Tabela de Despesas"
- ✅ Checkbox para marcar/desmarcar despesa como essencial
- ✅ Endpoint: `PUT /api/expense-items/{expense_id}/essential`
- ✅ Atualização em tempo real no banco

### Como usar:
1. Acesse a aba "Tabela de Despesas" em `/caixa/analises.html`
2. Clique no checkbox ao lado de cada despesa
3. A marcação é salva automaticamente no banco
4. O sistema recalcula gargalos considerando as marcações

## 3. Análise Histórica com Detalhes de Despesas

### Funcionalidades:
- ✅ Abrir despesa na análise histórica
- ✅ Marcar despesa histórica como essencial
- ✅ Histórico de despesas essenciais vs não essenciais
- ✅ Padrões identificados baseados nas marcações

## 4. Integração com ChatGPT

### O que faz:
- Analisa TODOS os dados do banco (últimos 30 dias ou período customizado)
- Identifica padrões de comportamento
- Gera recomendações estratégicas personalizadas
- Sugere ações para evitar problemas de caixa

### Endpoint:
```
POST /api/analytics/ai-recommendations
Body: {
  "days": 30,  // Período em dias
  "start_date": "2025-12-01"  // Opcional
}
```

### Configuração:
1. Obter API Key da OpenAI: https://platform.openai.com/api-keys
2. Adicionar no Render: `OPENAI_API_KEY` = `sk-...`
3. Ver arquivo `CONFIGURACAO_CHATGPT.md` para detalhes

### Dados enviados ao ChatGPT:
- Total de entradas e saídas
- Média diária de entradas/saídas
- Despesas essenciais vs não essenciais
- Gargalos identificados
- Tendência de saldo (últimos 10 dias)

### Resposta do ChatGPT:
1. Análise do comportamento atual
2. Principais riscos identificados
3. Ações recomendadas (priorizadas)
4. Meta de reserva diária sugerida
5. Sugestões de reprogramação

## 5. Priorização de Despesas Essenciais

### Ordem de prioridade:
1. **Marcação manual** (`is_essential = true` no banco) - MAIOR PRIORIDADE
2. Fornecedores essenciais cadastrados (`essential_suppliers`)
3. Palavras-chave (folha, aluguel, etc.)
4. Categorias (IMPOSTO, CARTORIO)

### Impacto:
- Gargalos são recalculados considerando marcações
- Ações recomendadas priorizam despesas essenciais
- Análise histórica mostra padrões de essenciais

## 6. Melhorias na Detecção de Gargalos

### Agora considera:
- ✅ Despesas marcadas manualmente como essenciais
- ✅ Fornecedores essenciais cadastrados
- ✅ Cheques compensados
- ✅ Padrões históricos

## Próximos Passos

1. **Execute a migration** `011_add_expense_essential_flag.sql` no Supabase
2. **Configure OPENAI_API_KEY** no Render (se quiser usar ChatGPT)
3. **Teste a marcação** de despesas como essenciais
4. **Use o ChatGPT** para análises inteligentes

## Arquivos Modificados

- `backend/app/analytics_service.py` - Lógica de análise
- `backend/app/main.py` - Novos endpoints
- `backend/app/schemas.py` - Novos schemas
- `backend/migrations/011_add_expense_essential_flag.sql` - Migration
- `caixa/analises.html` - Interface (será atualizada)

## Notas Importantes

- As marcações de essenciais são salvas no banco
- O sistema recalcula gargalos automaticamente
- ChatGPT usa modelo `gpt-4o-mini` (econômico)
- Custo aproximado: ~$0.001 por análise

