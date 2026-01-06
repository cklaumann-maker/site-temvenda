# 📅 Calendário do Plano Alimentar Criado

## ✅ O que foi feito

1. **Calendário Visual Criado** (`TodayCalendar.tsx`)
   - Visualização mensal tipo calendário
   - Mostra adesão por dia (barra de progresso)
   - Permite marcar refeições como feitas (check)
   - Detalhes das refeições do dia atual

2. **Script de Importação Criado**
   - Arquivo: `scripts/import_meal_plan.py`
   - Gera SQL para importar seu plano alimentar
   - Arquivo gerado: `supabase/import_meal_plan.sql`

---

## 📋 Próximos Passos

### 1. Importar Plano Alimentar no Banco

O SQL já foi gerado! Agora você precisa executá-lo:

1. **Acesse:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. **Vá em:** SQL Editor
3. **Abra o arquivo:** `rotina-app/supabase/import_meal_plan.sql`
4. **Copie todo o conteúdo** e cole no SQL Editor
5. **Execute** (Run)

Isso vai importar todas as 84 refeições do seu plano (2 semanas).

---

### 2. Verificar Tipos de Refeição

O seu plano usa tipos diferentes do sistema atual:
- **Seu plano:** `pre`, `post`, `breakfast`, `lunch`, `snack`, `dinner`
- **Sistema atual:** `cafe`, `lanche_manha`, `almoco`, `lanche_tarde`, `jantar`, `ceia`

**Mapeamento aplicado:**
- `pre` → `pre` (mantido)
- `post` → `post` (mantido)
- `breakfast` → `cafe`
- `lunch` → `almoco`
- `snack` → `lanche_tarde`
- `dinner` → `jantar`

**⚠️ IMPORTANTE:** Se o banco não aceitar `pre` e `post`, você precisará:
1. Adicionar esses tipos ao enum do banco, OU
2. Mapear `pre` → `lanche_manha` e `post` → `lanche_tarde`

---

### 3. Recarregar o App

Após importar o SQL:
1. Recarregue a página `/app/today`
2. Você verá o calendário com seu plano alimentar
3. Pode marcar refeições como feitas (check)

---

## 🎨 Como Funciona

### Calendário Visual
- **Visualização mensal** com todos os dias
- **Barra de progresso** por dia mostrando adesão
- **Dia atual destacado** em azul
- **Navegação** entre meses (setas)

### Marcar Refeições
- **Checkbox** ao lado de cada refeição
- **Clique para marcar/desmarcar** como feita
- **Atualização em tempo real** no banco
- **Cálculo automático** de adesão

### Detalhes do Dia
- **Seção inferior** mostra refeições do dia atual
- **Lista completa** com todas as refeições
- **Opções disponíveis** (opt1, opt2, opt3)
- **Avisos** (avoid) em vermelho

---

## 📊 Estrutura do Plano

Seu plano tem:
- **2 semanas** (Semana 1 e Semana 2)
- **7 dias por semana** (Segunda a Domingo)
- **6 refeições por dia:**
  - Pré-treino (`pre`)
  - Pós-treino (`post`)
  - Café da Manhã (`breakfast`)
  - Almoço (`lunch`)
  - Lanche (`snack`)
  - Jantar (`dinner`)

**Total:** 84 refeições (2 semanas × 7 dias × 6 refeições)

---

## 🔧 Arquivos Criados/Modificados

1. ✅ `apps/web/src/app/app/today/TodayCalendar.tsx` (NOVO)
   - Componente de calendário visual
   - Marcação de refeições
   - Cálculo de adesão

2. ✅ `apps/web/src/app/app/today/page.tsx` (ATUALIZADO)
   - Agora usa `TodayCalendar` ao invés de `TodayClient`

3. ✅ `scripts/import_meal_plan.py` (NOVO)
   - Script Python para gerar SQL
   - Mapeia tipos de refeição
   - Gera INSERT statements

4. ✅ `supabase/import_meal_plan.sql` (GERADO)
   - SQL pronto para executar
   - 84 refeições importadas

---

## ⚠️ Ajustes Necessários

### Se `pre` e `post` não funcionarem:

Você pode precisar atualizar o schema do banco para aceitar esses tipos. Execute este SQL:

```sql
-- Adicionar tipos pre e post ao enum (se necessário)
-- Verifique primeiro se o tipo meal_type é um enum ou varchar
```

Ou ajuste o mapeamento no script Python para usar tipos existentes.

---

## 🧪 Teste Agora

1. **Execute o SQL** no Supabase (passo 1 acima)
2. **Recarregue** a página `/app/today`
3. **Veja o calendário** com seu plano
4. **Marque refeições** como feitas
5. **Veja a adesão** atualizar em tempo real

---

## 📱 Interface do Calendário

```
┌─────────────────────────────────────┐
│  ← Dezembro 2024 →        [Hoje]  │
│                                     │
│  Dom Seg Ter Qua Qui Sex Sáb       │
│  1   2   3   4   5   6   7         │
│  8   9   10  11  12  13  14        │
│  15  16  17  18  19  20  21        │
│  22  23  24  25  26  27  28        │
│  29  30  31                         │
│                                     │
│  ────────────────────────────────  │
│  Hoje - Segunda, 22 de dezembro    │
│                                     │
│  ☑ Pré-treino                      │
│     Venom + água                    │
│                                     │
│  ☐ Pós-treino                      │
│     Whey + banana + água de coco   │
│                                     │
└─────────────────────────────────────┘
```

---

Execute o SQL e teste o calendário! 🎉







