# 📋 Gerenciar Plano Alimentar

## ✅ Funcionalidades Criadas

### 1. Página de Gerenciamento (`/app/plan-manager`)
- **Replicar Plano:** Replica as últimas 14 refeições para os próximos 14 dias
- **Importar Novo Plano:** Importa um novo plano alimentar via arquivo CSV

### 2. Botão na Tela Inicial
- Novo card "Gerenciar Plano" na página inicial
- Link na navegação superior

---

## 🎯 Como Usar

### Replicar Plano (14 dias)

1. **Acesse:** `/app/plan-manager`
2. **Clique em:** "Replicar Plano (14 dias)"
3. **Aguarde:** O sistema vai:
   - Buscar as últimas 14 refeições
   - Replicar para os próximos 14 dias
   - Mostrar mensagem de sucesso

**O que acontece:**
- Pega as refeições dos últimos 14 dias
- Replica para os próximos 14 dias (a partir do dia seguinte ao último)
- Mantém a mesma estrutura (6 refeições por dia)

---

### Importar Novo Plano

1. **Acesse:** `/app/plan-manager`
2. **Clique em:** "Escolher arquivo CSV"
3. **Selecione:** Um arquivo CSV com o formato:
   ```
   date,day_label,meal_type,option_selected,opt1,opt2,opt3,avoid
   ,Segunda,pre,,Venom + água,,,"Comer sólido"
   ,Segunda,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
   ...
   ```
4. **Aguarde:** O sistema vai:
   - Processar o arquivo CSV
   - Atualizar `plan_templates`
   - Regenerar `daily_meals` para os próximos 14 dias

**Formato esperado:**
- Colunas: `date,day_label,meal_type,option_selected,opt1,opt2,opt3,avoid`
- `day_label`: Segunda, Terça, Quarta, etc. (pode ter "(S2)" para semana 2)
- `meal_type`: pre, post, breakfast, lunch, snack, dinner
- `opt1`, `opt2`, `opt3`: Opções de refeição
- `avoid`: Alimentos a evitar

---

## 📋 Estrutura do Plano

O plano tem **14 dias** (2 semanas):
- **Semana 1:** Segunda a Domingo (7 dias)
- **Semana 2:** Segunda (S2) a Domingo (S2) (7 dias)
- **Total:** 84 refeições (14 dias × 6 refeições/dia)

**Tipos de refeição:**
- `pre` - Pré-treino
- `post` - Pós-treino
- `breakfast` - Café da Manhã
- `lunch` - Almoço
- `snack` - Lanche
- `dinner` - Jantar

---

## 🔄 Fluxo de Replicação

```
1. Usuário clica em "Replicar Plano"
   ↓
2. Sistema busca últimas 14 refeições de daily_meals
   ↓
3. Agrupa refeições por data
   ↓
4. Replica para os próximos 14 dias
   ↓
5. Insere no banco (daily_meals)
   ↓
6. Mostra mensagem de sucesso
```

---

## 📤 Fluxo de Importação

```
1. Usuário seleciona arquivo CSV
   ↓
2. Sistema lê e processa CSV
   ↓
3. Mapeia tipos de refeição e dias
   ↓
4. Atualiza plan_templates
   ↓
5. Regenera daily_meals para próximos 14 dias
   ↓
6. Mostra mensagem de sucesso
```

---

## 🎨 Interface

### Página de Gerenciamento

```
┌─────────────────────────────────────┐
│  Gerenciar Plano Alimentar          │
│  ─────────────────────────────────  │
│                                     │
│  ┌─────────────────────────────┐  │
│  │ Replicar Plano              │  │
│  │ Replique as últimas 14      │  │
│  │ refeições para os próximos   │  │
│  │ 14 dias.                    │  │
│  │ [Replicar Plano (14 dias)]  │  │
│  └─────────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐  │
│  │ Importar Novo Plano         │  │
│  │ Importe um novo plano        │  │
│  │ alimentar a partir de um    │  │
│  │ arquivo CSV.                │  │
│  │ [Escolher arquivo CSV]      │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## ⚠️ Observações

### Replicação
- **Requer:** Pelo menos 14 dias de refeições existentes
- **Cria:** Refeições para os próximos 14 dias
- **Não sobrescreve:** Refeições já existentes (usa INSERT, não UPDATE)

### Importação
- **Formato:** CSV com cabeçalho específico
- **Atualiza:** `plan_templates` (template geral)
- **Regenera:** `daily_meals` para os próximos 14 dias
- **Validação:** Verifica formato antes de processar

---

## 🔧 Arquivos Criados/Modificados

1. ✅ `apps/web/src/app/app/plan-manager/page.tsx` (NOVO)
   - Página completa de gerenciamento
   - Função de replicação
   - Função de importação CSV

2. ✅ `apps/web/src/app/app/page.tsx` (ATUALIZADO)
   - Adicionado card "Gerenciar Plano"

3. ✅ `apps/web/src/app/app/layout.tsx` (ATUALIZADO)
   - Adicionado link na navegação

4. ✅ `supabase/atualizar_plan_templates.sql` (NOVO)
   - Script para limpar e atualizar templates

---

## 🧪 Teste Agora

1. **Acesse:** http://localhost:3001/app/plan-manager
2. **Teste replicação:** Clique em "Replicar Plano"
3. **Teste importação:** Selecione um arquivo CSV
4. **Verifique:** Veja as refeições no calendário (`/app/today`)

---

## 📝 Próximos Passos

- [ ] Testar replicação com dados reais
- [ ] Validar formato CSV na importação
- [ ] Adicionar preview antes de importar
- [ ] Adicionar confirmação antes de replicar

---

Agora você pode replicar o plano de 14 dias ou importar um novo plano alimentar! 🎉

