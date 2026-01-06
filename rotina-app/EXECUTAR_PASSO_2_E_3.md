# 📋 Executar Passo 2 e 3 - Importar CSV e Regerar Refeições

## 🔄 PASSO 2: Criar e Importar CSV com Calorias

### 2.1. Criar o arquivo CSV

Crie um arquivo chamado `plano_calorias.csv` na raiz do projeto (`rotina-app/`) com o conteúdo que você forneceu.

**Opção A: Criar manualmente**
1. Crie um arquivo `plano_calorias.csv` em `rotina-app/`
2. Cole o conteúdo CSV que você forneceu

**Opção B: Usar o terminal**
```bash
cd /Users/cesark/site-temvenda/rotina-app
# Cole o conteúdo CSV no arquivo (você pode usar um editor de texto)
```

### 2.2. Executar o script de importação

```bash
cd /Users/cesark/site-temvenda/rotina-app
python3 scripts/import_plano_com_calorias.py plano_calorias.csv
```

Isso vai gerar um arquivo `plano_calorias_com_calorias.sql` na mesma pasta.

### 2.3. Executar o SQL gerado no Supabase

1. Abra o arquivo `plano_calorias_com_calorias.sql` gerado
2. Copie todo o conteúdo
3. Cole no Supabase SQL Editor
4. Execute o SQL

**Verificar se funcionou:**
```sql
-- Verificar se os templates têm calorias
SELECT 
  meal_type,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3,
  COUNT(*) as total
FROM plan_templates
WHERE program_id = '00000000-0000-0000-0000-000000000002'
GROUP BY meal_type, kcal_opt1, kcal_opt2, kcal_opt3
ORDER BY meal_type
LIMIT 10;
```

Você deve ver valores de calorias (não apenas zeros).

---

## 🔄 PASSO 3: Regerar Refeições com Calorias

Após importar os templates com calorias, você precisa regerar as refeições diárias para que elas tenham as calorias dos templates.

### 3.1. Deletar refeições antigas (opcional, mas recomendado)

```sql
DELETE FROM public.daily_meals 
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID;
```

### 3.2. Regerar refeições para a semana atual

Execute estes comandos SQL no Supabase (um por vez ou todos juntos):

```sql
-- Regerar refeições para os próximos 7 dias
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 1);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 2);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 3);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 4);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 5);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 6);
```

### 3.3. Verificar se as refeições têm calorias

```sql
-- Verificar refeições geradas com calorias
SELECT 
  date,
  meal_type,
  opt1,
  kcal_opt1,
  kcal_opt2,
  kcal_opt3
FROM daily_meals
WHERE user_id = '9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID
  AND date = CURRENT_DATE
ORDER BY 
  CASE meal_type
    WHEN 'pre' THEN 1
    WHEN 'post' THEN 2
    WHEN 'cafe' THEN 3
    WHEN 'almoco' THEN 4
    WHEN 'lanche_tarde' THEN 5
    WHEN 'jantar' THEN 6
    ELSE 999
  END;
```

Você deve ver valores de calorias em `kcal_opt1`, `kcal_opt2`, `kcal_opt3`.

---

## ✅ Checklist

- [ ] PASSO 2.1: Arquivo `plano_calorias.csv` criado
- [ ] PASSO 2.2: Script executado e SQL gerado
- [ ] PASSO 2.3: SQL executado no Supabase
- [ ] PASSO 2.4: Verificação mostra calorias nos templates
- [ ] PASSO 3.1: Refeições antigas deletadas (opcional)
- [ ] PASSO 3.2: Refeições regeradas para 7 dias
- [ ] PASSO 3.3: Verificação mostra calorias nas refeições

---

**Execute os passos acima e me informe quando estiver pronto!** ✅







