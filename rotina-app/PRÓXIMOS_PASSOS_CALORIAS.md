# 📋 Próximos Passos - Implementação de Calorias

## ✅ O que já foi feito:

1. ✅ Migration criada (`20240101000005_add_calories.sql`)
2. ✅ Scripts de importação atualizados
3. ✅ Types TypeScript atualizados
4. ✅ Função SQL para calcular saldo calórico criada

## 🔄 O que precisa ser feito agora:

### **PASSO 1: Executar Migration no Supabase**

Execute o arquivo `supabase/migrations/20240101000005_add_calories.sql` no Supabase SQL Editor.

### **PASSO 2: Criar e Importar CSV**

1. Crie o arquivo `plano_calorias.csv` na raiz do projeto com o conteúdo fornecido
2. Execute:
   ```bash
   python3 scripts/import_plano_com_calorias.py plano_calorias.csv
   ```
3. Isso gerará `plano_calorias_com_calorias.sql`
4. Execute esse SQL no Supabase

### **PASSO 3: Regerar Refeições**

Após importar os templates com calorias, regenere as refeições:

```sql
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE);
SELECT public.generate_daily_meals('9ca6a4e9-4bdd-4cdf-9426-813e10ca6280'::UUID, CURRENT_DATE + 1);
-- ... para os próximos dias
```

### **PASSO 4: Atualizar Frontend** (vou fazer depois)

- [ ] Atualizar `TodayCalendar.tsx` para mostrar calorias
- [ ] Adicionar opção "Outros" com campo de calorias
- [ ] Criar componente de resumo do dia
- [ ] Simplificar componente de check-in
- [ ] Mostrar saldo calórico

---

**Execute os passos 1-3 primeiro e me informe quando estiver pronto para continuar com o frontend!** ✅

