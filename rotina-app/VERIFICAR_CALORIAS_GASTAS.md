# 🔍 Verificar Calorias Gastas no Banco de Dados

## Consulta SQL Completa

Execute o arquivo `verificar_calorias_gastas.sql` no Supabase SQL Editor.

**IMPORTANTE**: Substitua `'SEU_USER_ID_AQUI'` pelo seu UUID em todas as queries.

---

## 📊 O Que Cada Query Mostra

### 1. Check-ins dos Últimos 7 Dias
Mostra todos os check-ins com:
- Data
- Se fez treino
- Calorias gastas
- Minutos de cardio
- Peso

### 2. Resumo por Dia
Agrupa por dia mostrando:
- Total de check-ins
- Dias com treino
- Total de calorias gastas
- Média de calorias gastas
- Máximo de calorias gastas

### 3. Verificar Hoje Especificamente
Mostra apenas os dados de hoje

### 4. Verificar Ontem
Mostra apenas os dados de ontem (para comparação)

### 5. Resumos de Calorias
Mostra os resumos calculados automaticamente:
- Calorias consumidas
- Calorias gastas
- Máximo de calorias
- Saldo líquido
- Déficit/Superávit

### 6. Comparação Check-ins vs Resumos
Verifica se os dados estão sincronizados:
- ✅ Sincronizado = dados iguais
- ⚠️ Check-in faltando = tem resumo mas não tem check-in
- ⚠️ Resumo faltando = tem check-in mas não tem resumo
- ❌ Diferente = valores diferentes

---

## 🎯 Interpretação dos Resultados

### Se aparecer dados:
- ✅ As calorias gastas estão gravadas
- Verifique se a data está correta
- Verifique se o valor está correto

### Se não aparecer dados:
- ❌ Não há calorias gastas gravadas
- Execute o script `corrigir_calorias_gastas.sql`
- Ou adicione manualmente no aplicativo

### Se aparecer "❌ Diferente":
- Os dados não estão sincronizados
- Execute: `SELECT public.calculate_and_save_daily_calorie_summary('SEU_USER_ID'::UUID, CURRENT_DATE);`

---

## 📝 Exemplo de Resultado Esperado

```
data        | treino_feito | calorias_gastas | minutos_cardio
------------|--------------|-----------------|----------------
2025-12-23  | true         | 466            | 30
2025-12-22  | true         | 500            | 45
2025-12-21  | false        | 0              | 0
```

---

## 🔧 Se Precisar Corrigir

1. **Se não há dados de hoje**: Execute `corrigir_calorias_gastas.sql`
2. **Se os dados estão diferentes**: Execute a função de recálculo
3. **Se há dados mas não aparecem no app**: Verifique o deploy no Vercel







