# ✅ Plano Alimentar Processado e Pronto para Importar

## 📋 Status

✅ **Script Python criado e executado com sucesso**
✅ **SQL gerado:** `supabase/import_plano_alimentar_atualizado.sql`
✅ **84 refeições processadas** (14 dias × 6 refeições)
✅ **Parser atualizado** para suportar formato com ponto e vírgula
✅ **Página de importação atualizada** para suportar o novo formato

---

## 🎯 Próximos Passos

### 1. Importar no Banco de Dados

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/import_plano_alimentar_atualizado.sql`
4. **Copie TODO o conteúdo** e cole no SQL Editor
5. **Execute** (Run)

Este script vai:
- ✅ Limpar templates existentes do programa demo
- ✅ Inserir 84 refeições corretamente formatadas
- ✅ Mapear tipos em português para códigos
- ✅ Limpar prefixos das opções automaticamente

---

### 2. Gerar Refeições para o Usuário

Após importar os templates:

1. **Execute:** `supabase/gerar_refeicoes_usuario.sql`
2. **Substitua** `'SEU_EMAIL_AQUI'` pelo seu email
3. **Execute** o SQL

Isso vai gerar refeições para os próximos 30 dias baseadas nos templates.

---

## 📊 Estrutura do Plano

### 14 Dias (2 Semanas)
- **Semana 1:** Segunda a Domingo (7 dias)
- **Semana 2:** Segunda (Semana 2) a Domingo (Semana 2) (7 dias)

### 6 Refeições por Dia
1. **Pré-treino** (`pre`)
2. **Pós-treino** (`post`)
3. **Café da manhã** (`cafe`)
4. **Almoço** (`almoco`)
5. **Lanche da tarde** (`lanche_tarde`)
6. **Jantar** (`jantar`)

**Total:** 84 refeições

---

## 🔄 Funcionalidades Atualizadas

### 1. Página de Gerenciamento (`/app/plan-manager`)

#### Replicar Plano
- Replica as últimas 14 refeições para os próximos 14 dias
- Mantém a estrutura completa
- Funciona automaticamente

#### Importar CSV
- ✅ Suporta ponto e vírgula (`;`) ou vírgula (`,`)
- ✅ Detecta formato automaticamente
- ✅ Tipos em português: "Pré-treino", "Pós-treino", etc.
- ✅ Remove prefixos: "Opção 1 (Principal):", "Evitar:", etc.
- ✅ Trata valores vazios (`—`) como NULL

---

## 📝 Formato CSV Suportado

O sistema agora suporta o formato do arquivo fornecido:

```csv
date;day_label;meal_type;option_selected;opt1;opt2;opt3;avoid
;Segunda;Pré-treino;;Opção 1 (Principal): Venom + água;...
;Segunda (Semana 2);Pós-treino;;Opção 1 (Principal): Whey + banana...
```

**Características:**
- Separador: Ponto e vírgula (`;`)
- Tipos em português
- Prefixos nas opções
- Valores podem conter ponto e vírgula (ex: "Bolo; pão; doce")

---

## 🔧 Arquivos Criados/Atualizados

1. ✅ `scripts/import_plano_csv.py` (NOVO)
   - Processa CSV com ponto e vírgula
   - Limpa prefixos automaticamente
   - Trata valores com ponto e vírgula interno

2. ✅ `supabase/import_plano_alimentar_atualizado.sql` (GERADO)
   - SQL pronto para executar
   - 84 refeições formatadas corretamente
   - Valores completos (ex: "Bolo; pão; doce")

3. ✅ `apps/web/src/app/app/plan-manager/page.tsx` (ATUALIZADO)
   - Parser CSV melhorado
   - Suporta ponto e vírgula
   - Limpeza automática de prefixos
   - Mapeia tipos em português

---

## 🧪 Teste Agora

1. **Execute o SQL:** `import_plano_alimentar_atualizado.sql` no Supabase
2. **Gere refeições:** Execute `gerar_refeicoes_usuario.sql` (substitua email)
3. **Teste replicação:** Acesse `/app/plan-manager` e clique em "Replicar Plano"
4. **Teste importação:** Importe o arquivo CSV original
5. **Verifique:** Veja as refeições no calendário (`/app/today`)

---

## ✅ Verificação

Execute este SQL para verificar:

```sql
-- Total de refeições
SELECT COUNT(*) FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002';
-- Deve retornar: 84

-- Verificar uma refeição específica
SELECT * FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002'
AND week_index = 1 
AND day_of_week = 1 
AND meal_type = 'post';
-- Deve mostrar: avoid = 'Bolo; pão; doce'
```

---

Execute o SQL `import_plano_alimentar_atualizado.sql` no Supabase para atualizar o banco! 🚀







