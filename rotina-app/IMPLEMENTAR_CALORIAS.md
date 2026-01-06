# 🔥 Implementação de Controle de Calorias

## ✅ O que foi feito até agora:

### 1. **Migration criada** (`20240101000005_add_calories.sql`)
- ✅ Adiciona campos `kcal_opt1`, `kcal_opt2`, `kcal_opt3` em `plan_templates` e `daily_meals`
- ✅ Adiciona campos `kcal_other` e `other_description` em `daily_meals` (para opção "outros")
- ✅ Adiciona campo `workout_calories` em `daily_checkin`
- ✅ Cria função `calculate_daily_calories()` para calcular saldo calórico
- ✅ Cria índices para melhorar performance

### 2. **Scripts atualizados**
- ✅ `import_plano_csv.py` atualizado para ler calorias
- ✅ `import_plano_com_calorias.py` criado (versão específica para CSV com calorias)
- ✅ Função `generate_daily_meals` atualizada para copiar calorias dos templates

### 3. **Types atualizados**
- ✅ `DailyMeal` agora inclui campos de calorias
- ✅ `DailyCheckin` agora inclui `workout_calories`

## 📋 Próximos passos:

### 1. **Executar Migration no Supabase**
```sql
-- Execute o arquivo: supabase/migrations/20240101000005_add_calories.sql
```

### 2. **Importar CSV com Calorias**

Crie o arquivo `plano_calorias.csv` com o conteúdo fornecido e execute:

```bash
python3 scripts/import_plano_com_calorias.py plano_calorias.csv
```

Isso gerará um arquivo SQL que você deve executar no Supabase.

### 3. **Atualizar Frontend**

Ainda falta:
- [ ] Atualizar `TodayCalendar.tsx` para mostrar calorias
- [ ] Adicionar opção "Outros" com campo de calorias
- [ ] Criar componente de resumo do dia
- [ ] Simplificar componente de check-in
- [ ] Mostrar saldo calórico (consumo - gasto)

---

## 📝 Estrutura do CSV esperada:

```csv
date,day_label,meal_type,option_selected,opt1,opt2,opt3,avoid,kcal_opt1,kcal_opt2,kcal_opt3
,Segunda,Pré-treino,,Opção 1 (Principal): Venom + água,...,...,...,...,0,0,0
```

---

**Execute a migration primeiro, depois me informe para continuarmos com o frontend!** ✅







