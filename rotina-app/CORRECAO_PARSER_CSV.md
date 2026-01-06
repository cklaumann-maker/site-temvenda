# 🔧 Correção do Parser CSV e Ordenação

## ✅ Correções Implementadas

### 1. **Parser CSV Melhorado**

- ✅ Função `parseCSVLine` robusta que lida com valores entre aspas
- ✅ Remove corretamente prefixos como "Opção 1 (Principal):", "Opção 2 (Substituição):", "Evitar:"
- ✅ Trata valores vazios e traços (—, -)
- ✅ Suporta tanto vírgula quanto ponto e vírgula como delimitador

### 2. **Limpeza de Prefixos**

A função `cleanOptionText` agora remove:
- `Opção 1 (Principal): ` → removido
- `Opção 2 (Substituição): ` → removido
- `Opção 3 (Substituição): ` → removido
- `Evitar: ` → removido

**Exemplo:**
- Entrada: `"Opção 1 (Principal): Venom + água"`
- Saída: `"Venom + água"`

### 3. **Ordenação das Refeições**

A ordem está configurada exatamente como na planilha:

1. **Pré-treino** (`pre`) - ordem 1
2. **Pós-treino** (`post`) - ordem 2
3. **Café da manhã** (`cafe`) - ordem 3
4. **Almoço** (`almoco`) - ordem 4
5. **Lanche da tarde** (`lanche_tarde`) - ordem 5
6. **Jantar** (`jantar`) - ordem 6

### 4. **Mapeamento de Tipos**

O parser mapeia corretamente:
- `Pré-treino` → `pre`
- `Pós-treino` → `post`
- `Café da manhã` → `cafe`
- `Almoço` → `almoco`
- `Lanche da tarde` → `lanche_tarde`
- `Jantar` → `jantar`

## 🔍 Debug

O código agora inclui logs de debug que mostram as primeiras 3 refeições parseadas no console do navegador. Isso ajuda a verificar se os prefixos estão sendo removidos corretamente.

## 📋 Como Testar

1. **Importe a planilha novamente:**
   - Vá para `/app/plan-manager`
   - Faça upload do CSV
   - Abra o console do navegador (F12) para ver os logs de debug

2. **Verifique no calendário:**
   - Acesse `/app/today`
   - As refeições devem aparecer na ordem correta:
     - Pré-treino
     - Pós-treino
     - Café da manhã
     - Almoço
     - Lanche da tarde
     - Jantar

3. **Verifique as opções:**
   - Cada refeição deve mostrar as 3 opções sem prefixos
   - O campo "Evitar" deve aparecer sem o prefixo "Evitar:"

## ⚠️ Se ainda não funcionar

1. **Verifique o console do navegador** para ver os logs de debug
2. **Verifique no banco de dados:**
   ```sql
   SELECT meal_type, opt1, opt2, opt3, avoid
   FROM plan_templates
   WHERE program_id = '00000000-0000-0000-0000-000000000002'
   ORDER BY week_index, day_of_week, meal_type
   LIMIT 10;
   ```

3. **Se os prefixos ainda aparecerem no banco:**
   - Limpe os templates antigos
   - Importe novamente

---

**As correções estão implementadas!** Teste importando a planilha novamente. 🚀







