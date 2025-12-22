# 🔧 Atualizar Função de Gerar Refeições

## ⚠️ IMPORTANTE: Execute esta Migration SQL

Para garantir que as refeições sejam geradas corretamente a partir dos templates importados, você precisa executar a migration SQL que corrige a função `generate_daily_meals`.

### 📋 Passo a Passo

1. **Acesse o Supabase SQL Editor:**
   - Vá para: https://supabase.com/dashboard/project/[SEU_PROJECT_ID]/sql/new

2. **Execute a Migration:**
   - Abra o arquivo: `rotina-app/supabase/migrations/20240101000004_fix_generate_daily_meals.sql`
   - Copie todo o conteúdo
   - Cole no SQL Editor do Supabase
   - Clique em **Run** ou pressione `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac)

3. **Verifique se funcionou:**
   ```sql
   -- Teste a função
   SELECT public.generate_daily_meals('SEU_USER_ID', CURRENT_DATE);
   ```

## ✅ O que foi corrigido?

### **Antes:**
- A função não atualizava refeições existentes
- Não ciclava corretamente entre semana 1 e 2
- Templates importados não eram aplicados às refeições existentes

### **Depois:**
- ✅ Atualiza refeições existentes com novos templates
- ✅ Cicla corretamente entre semana 1 e 2 (se week_index > 2, usa módulo)
- ✅ Garante que templates importados sejam aplicados imediatamente

## 🔄 Fluxo Completo Agora

1. **Importar Planilha:**
   - Vá para `/app/plan-manager`
   - Faça upload do CSV
   - Os templates são salvos em `plan_templates`

2. **Gerar Refeições:**
   - A função `generate_daily_meals` é chamada automaticamente
   - Busca templates corretos baseado em:
     - `program_id` do enrollment
     - `week_index` calculado (ciclando entre 1 e 2)
     - `day_of_week` da data

3. **Visualizar:**
   - As refeições aparecem em `/app/today` e `/app/plan`
   - Todas as opções (opt1, opt2, opt3) são exibidas
   - Você pode selecionar qual opção foi utilizada

## 🧪 Teste Completo

Após executar a migration:

1. **Importe uma planilha nova:**
   ```
   /app/plan-manager → Upload CSV
   ```

2. **Verifique os templates:**
   ```sql
   SELECT COUNT(*) FROM plan_templates 
   WHERE program_id = '00000000-0000-0000-0000-000000000002';
   ```

3. **Regere as refeições:**
   ```sql
   -- Para hoje
   SELECT public.generate_daily_meals('SEU_USER_ID', CURRENT_DATE);
   
   -- Para os próximos 7 dias
   SELECT public.generate_daily_meals('SEU_USER_ID', CURRENT_DATE + 1);
   SELECT public.generate_daily_meals('SEU_USER_ID', CURRENT_DATE + 2);
   -- ... etc
   ```

4. **Verifique no app:**
   - Acesse `/app/today`
   - Você deve ver todas as opções da planilha

## 📝 Notas Importantes

- A função agora **atualiza** refeições existentes, não apenas cria novas
- O `week_index` cicla automaticamente: semana 3 → semana 1, semana 4 → semana 2, etc.
- Se você importar uma nova planilha, as refeições serão atualizadas automaticamente

## 🐛 Se algo não funcionar

1. Verifique se a migration foi executada:
   ```sql
   SELECT proname FROM pg_proc WHERE proname = 'generate_daily_meals';
   ```

2. Verifique se os templates existem:
   ```sql
   SELECT * FROM plan_templates 
   WHERE program_id = '00000000-0000-0000-0000-000000000002'
   LIMIT 5;
   ```

3. Verifique se o enrollment está ativo:
   ```sql
   SELECT * FROM enrollments 
   WHERE user_id = 'SEU_USER_ID' AND active = true;
   ```

4. Teste a função manualmente:
   ```sql
   SELECT public.generate_daily_meals('SEU_USER_ID', CURRENT_DATE);
   ```

---

**Execute a migration SQL antes de importar novas planilhas!** 🚀

