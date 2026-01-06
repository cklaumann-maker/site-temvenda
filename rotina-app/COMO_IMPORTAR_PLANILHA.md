# 📋 Como Importar Planilha para o Banco de Dados

## ✅ Fluxo Completo

### 1. **Estrutura da Planilha CSV**

A planilha deve ter as seguintes colunas (em qualquer ordem, mas com esses nomes):

```
day_label,meal_type,opt1,opt2,opt3,avoid
```

**Exemplo:**
```csv
day_label,meal_type,opt1,opt2,opt3,avoid
Segunda,Pré-treino,Venom + água,,,"Comer sólido"
Segunda,Pós-treino,"Whey + banana + água de coco","Whey + morango","Whey + 1/2 banana","Bolo, pão, doce"
```

### 2. **Mapeamento de Valores**

#### **Dias da Semana:**
- `Segunda` → day_of_week = 1
- `Terça` → day_of_week = 2
- `Quarta` → day_of_week = 3
- `Quinta` → day_of_week = 4
- `Sexta` → day_of_week = 5
- `Sábado` → day_of_week = 6
- `Domingo` → day_of_week = 7

**Para Semana 2:**
- `Segunda (Semana 2)` ou `Segunda (S2)` → week_index = 2
- Sem indicação de semana → week_index = 1

#### **Tipos de Refeição:**
- `Pré-treino` → `pre`
- `Pós-treino` → `post`
- `Café da manhã` → `cafe`
- `Almoço` → `almoco`
- `Lanche da tarde` → `lanche_tarde`
- `Jantar` → `jantar`
- `Ceia` → `ceia`

### 3. **Processo de Importação**

Quando você importa a planilha através de `/app/plan-manager`:

1. **Parse do CSV:**
   - Detecta automaticamente se usa `;` ou `,` como delimitador
   - Limpa prefixos como "Opção 1 (Principal):", "Evitar:", etc.
   - Mapeia dias e tipos de refeição

2. **Salva em `plan_templates`:**
   - Limpa templates antigos do programa
   - Insere novos templates em lotes (batches de 50)
   - Cada template tem: `program_id`, `week_index`, `day_of_week`, `meal_type`, `opt1`, `opt2`, `opt3`, `avoid`

3. **Gera `daily_meals`:**
   - Chama `generate_daily_meals()` para os próximos 30 dias
   - A função busca os templates corretos baseado em:
     - `program_id` do enrollment ativo
     - `week_index` calculado (cicla entre 1 e 2)
     - `day_of_week` da data

### 4. **Função `generate_daily_meals`**

A função SQL faz o seguinte:

```sql
1. Busca o enrollment ativo do usuário
2. Calcula o week_index baseado na data de início do enrollment
3. Cicla o week_index: se > 2, usa módulo para alternar entre 1 e 2
4. Busca templates que correspondem:
   - program_id = enrollment.program_id
   - week_index = week_index calculado (ciclando)
   - day_of_week = dia da semana da data
5. Insere ou atualiza daily_meals com opt1, opt2, opt3, avoid dos templates
```

### 5. **Verificação**

Após importar, você pode verificar:

```sql
-- Ver templates importados
SELECT week_index, day_of_week, meal_type, opt1, opt2, opt3, avoid
FROM plan_templates
WHERE program_id = '00000000-0000-0000-0000-000000000002'
ORDER BY week_index, day_of_week, meal_type;

-- Ver refeições geradas
SELECT date, meal_type, opt1, opt2, opt3, avoid, option_selected
FROM daily_meals
WHERE user_id = 'SEU_USER_ID'
ORDER BY date, meal_type;
```

## 🔧 Troubleshooting

### Problema: Opções não aparecem na tela

**Causa:** Templates não foram importados corretamente ou refeições não foram geradas.

**Solução:**
1. Verifique se os templates existem:
   ```sql
   SELECT COUNT(*) FROM plan_templates WHERE program_id = '00000000-0000-0000-0000-000000000002';
   ```

2. Regere as refeições manualmente:
   ```sql
   SELECT public.generate_daily_meals('SEU_USER_ID', CURRENT_DATE);
   ```

3. Verifique se o enrollment está ativo:
   ```sql
   SELECT * FROM enrollments WHERE user_id = 'SEU_USER_ID' AND active = true;
   ```

### Problema: CSV não é lido corretamente

**Causa:** Formato do CSV não está correto ou delimitador errado.

**Solução:**
1. Certifique-se de que o CSV tem as colunas corretas
2. Use `;` ou `,` como delimitador (não misture)
3. Valores com vírgulas devem estar entre aspas: `"Bolo, pão, doce"`

### Problema: Semana 2 não funciona

**Causa:** O formato do `day_label` não está sendo reconhecido.

**Solução:**
- Use `Segunda (Semana 2)` ou `Segunda (S2)` no CSV
- A função limpa automaticamente e identifica como week_index = 2

## 📝 Exemplo Completo de CSV

```csv
day_label,meal_type,opt1,opt2,opt3,avoid
Segunda,Pré-treino,Venom + água,,,"Comer sólido"
Segunda,Pós-treino,"Whey + banana + água de coco","Whey + morango","Whey + 1/2 banana","Bolo, pão, doce"
Segunda,Café da manhã,"Ovos mexidos (2-3) + 1 pão + requeijão","Omelete de queijo + pão","Whey + banana + pão","Bolo, cuca, doce de leite"
Segunda,Almoço,"Arroz + feijão + carne","Macarrão + frango","Batata + peixe","Arroz + batata juntos"
Segunda,Lanche da tarde,"Ovos + maçã","Whey + pera","Frango + uva","Bolacha, cavaquinho, bolo"
Segunda,Jantar,"Frango ou peixe","Ovos mexidos","1 pão + ovos","Doce à noite"
Segunda (Semana 2),Pré-treino,Venom + água,,,"Comer sólido"
Segunda (Semana 2),Pós-treino,"Whey + banana + água de coco","Whey + morango","Whey + 1/2 banana","Bolo, pão, doce"
```

## 🚀 Próximos Passos

1. Importe a planilha através de `/app/plan-manager`
2. Verifique se as refeições aparecem em `/app/today`
3. Se não aparecerem, execute a função SQL manualmente ou verifique os logs do console







