# ✅ Tudo Pronto para Importar o Plano Alimentar

## 📋 Resumo

✅ **Script SQL gerado:** `supabase/import_plano_alimentar_atualizado.sql`
✅ **84 refeições processadas** corretamente
✅ **Parser atualizado** para suportar formato com ponto e vírgula
✅ **Página de importação** atualizada para o novo formato
✅ **Valores completos** preservados (ex: "Bolo; pão; doce")

---

## 🚀 Importar no Banco (PASSO A PASSO)

### Passo 1: Importar Templates

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/import_plano_alimentar_atualizado.sql`
4. **Copie TODO o conteúdo** (1100 linhas)
5. **Cole no SQL Editor**
6. **Execute** (Run)

**Resultado esperado:**
- ✅ 84 refeições inseridas
- ✅ Templates limpos e recriados

---

### Passo 2: Gerar Refeições para o Usuário

1. **Ainda no SQL Editor**
2. **Abra o arquivo:** `rotina-app/supabase/gerar_refeicoes_usuario.sql`
3. **Substitua** `'SEU_EMAIL_AQUI'` pelo email que você usou para fazer login
4. **Execute** (Run)

**Resultado esperado:**
- ✅ Refeições geradas para os próximos 30 dias
- ✅ Baseadas nos templates importados

---

### Passo 3: Verificar no App

1. **Recarregue:** http://localhost:3001/app/today
2. **Você deve ver:**
   - ✅ Calendário semanal
   - ✅ Refeições do dia atual
   - ✅ Checkboxes funcionando

---

## 📊 Estrutura do Plano Importado

### 14 Dias (2 Semanas)
- **Semana 1:** Segunda a Domingo (7 dias)
- **Semana 2:** Segunda (Semana 2) a Domingo (Semana 2) (7 dias)

### 6 Refeições por Dia
1. **Pré-treino** (`pre`) - Ex: "Venom + água"
2. **Pós-treino** (`post`) - Ex: "Whey + banana + água de coco"
3. **Café da manhã** (`cafe`) - Ex: "Ovos mexidos (2-3) + 1 pão + requeijão"
4. **Almoço** (`almoco`) - Ex: "Arroz + feijão + carne"
5. **Lanche da tarde** (`lanche_tarde`) - Ex: "Ovos + maçã"
6. **Jantar** (`jantar`) - Ex: "Frango ou peixe"

**Total:** 84 refeições

---

## 🔄 Funcionalidades Disponíveis

### 1. Replicar Plano (`/app/plan-manager`)
- Replica as últimas 14 refeições para os próximos 14 dias
- Mantém toda a estrutura
- Um clique e pronto!

### 2. Importar Novo Plano (`/app/plan-manager`)
- Importa arquivo CSV
- Suporta formato com ponto e vírgula
- Remove prefixos automaticamente
- Mapeia tipos em português

---

## ✅ Verificação Final

Execute este SQL para confirmar:

```sql
-- Total de refeições (deve ser 84)
SELECT COUNT(*) as total FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002';

-- Verificar valores completos
SELECT meal_type, opt1, avoid 
FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002'
AND week_index = 1 
AND day_of_week = 1 
AND meal_type = 'post';
-- avoid deve ser: 'Bolo; pão; doce'
```

---

## 📁 Arquivos Importantes

1. ✅ `supabase/import_plano_alimentar_atualizado.sql` - **EXECUTE ESTE**
2. ✅ `supabase/gerar_refeicoes_usuario.sql` - Execute depois (substitua email)
3. ✅ `apps/web/src/app/app/plan-manager/page.tsx` - Página de gerenciamento
4. ✅ `scripts/import_plano_csv.py` - Script Python (já executado)

---

## 🎯 Próximos Passos Após Importar

1. ✅ Execute o SQL de importação
2. ✅ Gere refeições para seu usuário
3. ✅ Teste o calendário (`/app/today`)
4. ✅ Teste replicação (`/app/plan-manager`)
5. ✅ Teste importação CSV (`/app/plan-manager`)

---

**Execute o SQL `import_plano_alimentar_atualizado.sql` no Supabase agora!** 🚀







