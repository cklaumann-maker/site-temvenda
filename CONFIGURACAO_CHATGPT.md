# Configuração do ChatGPT para Análises Financeiras

## O que foi implementado

O sistema agora integra ChatGPT para análise inteligente dos dados financeiros e geração de recomendações estratégicas.

## Como funciona

1. **Endpoint**: `POST /api/analytics/ai-recommendations`
2. **Dados analisados**: Todos os dados do banco (finance_daily, expense_items, checks)
3. **Período**: Configurável (padrão: últimos 30 dias)
4. **Análise**: ChatGPT analisa padrões e gera recomendações personalizadas

## Configuração necessária

### 1. Obter API Key da OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Crie uma conta ou faça login
3. Clique em "Create new secret key"
4. Copie a chave gerada

### 2. Configurar no Render

1. Acesse o dashboard do Render
2. Vá em "Environment" do seu serviço backend
3. Adicione a variável:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `sk-...` (sua chave da OpenAI)

### 3. Verificar configuração

Após configurar, o endpoint `/api/analytics/ai-recommendations` estará disponível.

## Uso

### Frontend

```javascript
// Chamar análise com ChatGPT
const response = await fetch(`${API_URL}/api/analytics/ai-recommendations`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    days: 30,  // Período em dias
    start_date: '2025-12-01'  // Opcional: data inicial
  })
});

const data = await response.json();
console.log(data.recommendations);  // Recomendações do ChatGPT
```

### Resposta

```json
{
  "recommendations": "Análise completa em texto...",
  "analysis_period": "2025-12-01 a 2026-01-13",
  "data_summary": {
    "period": {...},
    "cash_flow": {...},
    "expenses": {...},
    "bottlenecks": [...]
  },
  "generated_at": "2026-01-13T18:30:00"
}
```

## Custos

- **Modelo usado**: `gpt-4o-mini` (mais econômico)
- **Custo aproximado**: ~$0.001 por análise
- **Limite de tokens**: 1500 tokens por análise

## Funcionalidades

1. **Análise de comportamento**: Identifica padrões de entradas/saídas
2. **Riscos identificados**: Lista principais riscos financeiros
3. **Ações recomendadas**: Sugestões priorizadas para próximos 30 dias
4. **Meta de reserva**: Sugere reserva diária ideal
5. **Reprogramação**: Sugere ajustes em despesas não essenciais

## Troubleshooting

### Erro: "OPENAI_API_KEY não configurada"
- Verifique se a variável está configurada no Render
- Reinicie o serviço após adicionar a variável

### Erro: "Rate limit exceeded"
- Aguarde alguns minutos e tente novamente
- Considere aumentar o limite na conta OpenAI

### Erro: "Insufficient quota"
- Verifique o saldo da sua conta OpenAI
- Adicione créditos se necessário

