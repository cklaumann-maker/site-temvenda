# 📋 Importar Plano Alimentar Atualizado

## ✅ Script SQL Gerado

O script `import_plano_csv.py` processou o arquivo CSV fornecido e gerou o SQL de importação.

**Arquivo gerado:** `supabase/import_plano_alimentar_atualizado.sql`

---

## 📋 Próximos Passos

### 1. Importar no Banco de Dados

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/import_plano_alimentar_atualizado.sql`
4. **Copie TODO o conteúdo** e cole no SQL Editor
5. **Execute** (Run)

Este script vai:
- ✅ Limpar templates existentes
- ✅ Inserir 84 refeições (14 dias × 6 refeições)
- ✅ Mapear corretamente tipos em português
- ✅ Limpar prefixos das opções

---

### 2. Gerar Refeições para o Usuário

Após importar os templates:

1. **Execute:** `supabase/gerar_refeicoes_usuario.sql` (substitua o email)
2. Isso vai gerar refeições para os próximos 30 dias

---

## 🔄 Estrutura do Plano

### Formato do CSV
- **Separador:** Ponto e vírgula (`;`)
- **Tipos de refeição:** Em português
  - `Pré-treino` → `pre`
  - `Pós-treino` → `post`
  - `Café da manhã` → `cafe`
  - `Almoço` → `almoco`
  - `Lanche da tarde` → `lanche_tarde`
  - `Jantar` → `jantar`

### Estrutura
- **14 dias** (2 semanas)
- **6 refeições por dia**
- **Total:** 84 refeições

---

## 🎯 Funcionalidades Atualizadas

### 1. Página de Gerenciamento (`/app/plan-manager`)
- ✅ **Replicar Plano:** Replica últimas 14 refeições para próximos 14 dias
- ✅ **Importar CSV:** Agora suporta:
  - Ponto e vírgula (`;`) ou vírgula (`,`) como separador
  - Tipos em português
  - Limpeza automática de prefixos ("Opção 1 (Principal):", etc.)
  - Valores vazios (`—`) tratados como NULL

### 2. Parser CSV Melhorado
- ✅ Detecta automaticamente o separador
- ✅ Remove prefixos das opções
- ✅ Trata valores vazios corretamente
- ✅ Mapeia tipos em português

---

## 📊 Verificar Importação

Execute este SQL para verificar:

```sql
-- Verificar total de refeições
SELECT COUNT(*) as total FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002';

-- Verificar por semana
SELECT week_index, COUNT(*) as total 
FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002'
GROUP BY week_index;

-- Verificar tipos de refeição
SELECT meal_type, COUNT(*) as total 
FROM public.plan_templates 
WHERE program_id = '00000000-0000-0000-0000-000000000002'
GROUP BY meal_type;
```

**Resultado esperado:**
- ✅ Total: 84 refeições
- ✅ Semana 1: 42 refeições
- ✅ Semana 2: 42 refeições
- ✅ 6 tipos diferentes (pre, post, cafe, almoco, lanche_tarde, jantar)

---

## 🔧 Arquivos Criados/Atualizados

1. ✅ `scripts/import_plano_csv.py` (NOVO)
   - Script Python para processar CSV
   - Suporta ponto e vírgula
   - Limpa prefixos automaticamente

2. ✅ `supabase/import_plano_alimentar_atualizado.sql` (GERADO)
   - SQL pronto para executar
   - 84 refeições formatadas corretamente

3. ✅ `apps/web/src/app/app/plan-manager/page.tsx` (ATUALIZADO)
   - Parser CSV melhorado
   - Suporta formato com ponto e vírgula
   - Limpeza automática de prefixos

---

## 🧪 Teste Agora

1. **Execute o SQL:** `import_plano_alimentar_atualizado.sql` no Supabase
2. **Gere refeições:** Execute `gerar_refeicoes_usuario.sql` (substitua email)
3. **Teste importação:** Acesse `/app/plan-manager` e teste importar o CSV
4. **Verifique:** Veja as refeições no calendário (`/app/today`)

---

## 📝 Formato CSV Suportado

O sistema agora suporta ambos os formatos:

### Formato 1: Ponto e vírgula (novo)
```csv
date;day_label;meal_type;option_selected;opt1;opt2;opt3;avoid
;Segunda;Pré-treino;;Opção 1 (Principal): Venom + água;...
```

### Formato 2: Vírgula (antigo)
```csv
date,day_label,meal_type,option_selected,opt1,opt2,opt3,avoid
,Segunda,pre,,Venom + água,...
```

---

Execute o SQL `import_plano_alimentar_atualizado.sql` no Supabase para atualizar o banco com o plano correto! 🚀







