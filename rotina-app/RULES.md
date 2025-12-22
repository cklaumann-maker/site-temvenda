# RULES.md - Regras de Negócio

## 1. Cálculo de Aderência

### Pseudocódigo
```
FUNÇÃO calcular_aderencia(user_id, date):
  planned_meals = CONTAR daily_meals ONDE user_id E date
  done_meals = CONTAR daily_meals ONDE user_id E date E option_selected IS NOT NULL
  
  SE planned_meals == 0:
    RETORNAR 0
  
  adherence_pct = (done_meals / planned_meals) * 100
  RETORNAR adherence_pct
```

### Validação
- **Input**: `user_id` (UUID), `date` (DATE)
- **Output**: `adherence_pct` (DECIMAL 0-100)
- **Erro**: Se `user_id` não existe → retornar erro 404

### Mensagens de Erro
- "Usuário não encontrado"
- "Erro ao calcular aderência"

---

## 2. Regra de Doces em Dias Úteis

### Pseudocódigo
```
FUNÇÃO verificar_permissao_doce(user_id, date, meal_type):
  enrollment = BUSCAR enrollment ONDE user_id E active = true
  SE enrollment NÃO EXISTE:
    RETORNAR ERRO "Usuário não está inscrito em nenhum programa"
  
  ruleset = BUSCAR ruleset ONDE program_id = enrollment.program_id
  SE ruleset NÃO EXISTE:
    RETORNAR ERRO "Regras não configuradas para este programa"
  
  dia_semana = DIA_DA_SEMANA(date) // 1=Segunda, 7=Domingo
  é_dia_útil = (dia_semana >= 1 E dia_semana <= 5)
  
  SE NÃO é_dia_útil:
    RETORNAR PERMITIDO // Finais de semana sempre permitem
  
  dias_desde_inicio = DIFERENÇA_EM_DIAS(date, enrollment.start_date)
  
  // Período de bloqueio rígido inicial
  SE dias_desde_inicio < ruleset.hard_block_days:
    REGISTRAR rule_event(
      user_id,
      'SWEET_BLOCKED',
      date,
      'Tentativa de consumo bloqueada durante período rígido'
    )
    RETORNAR BLOQUEADO
  
  // Após período inicial, seguir modo configurado
  SE ruleset.weekday_sweets_mode == 'HARD_BLOCK':
    REGISTRAR rule_event(
      user_id,
      'SWEET_BLOCKED',
      date,
      'Consumo bloqueado conforme regras do programa'
    )
    RETORNAR BLOQUEADO
  
  SE ruleset.weekday_sweets_mode == 'EXCEPTION_WITH_COST':
    exceções_semana = CONTAR rule_events ONDE 
      user_id E 
      tipo = 'SWEET_EXCEPTION_USED' E
      date >= INICIO_SEMANA(date) E
      date <= FIM_SEMANA(date)
    
    SE exceções_semana >= ruleset.weekly_exception_limit:
      REGISTRAR rule_event(
        user_id,
        'SWEET_BLOCKED',
        date,
        'Limite de exceções semanais atingido'
      )
      RETORNAR BLOQUEADO
    
    // Perguntar ao usuário se deseja usar exceção
    RETORNAR REQUER_CONFIRMAÇÃO_EXCEÇÃO
  
  SE ruleset.weekday_sweets_mode == 'ALLOW':
    RETORNAR PERMITIDO
```

### Validações
- **Input**: `user_id`, `date`, `meal_type` (deve conter "doce" ou estar em lista de itens bloqueados)
- **Output**: `{ allowed: boolean, requires_confirmation: boolean, message: string }`
- **Erros**:
  - "Usuário não está inscrito em nenhum programa"
  - "Regras não configuradas"
  - "Data inválida"

### Mensagens de Erro/Feedback
- **Bloqueado (período rígido)**: "Você está no período de bloqueio rígido. Doces não são permitidos nos primeiros X dias."
- **Bloqueado (modo HARD_BLOCK)**: "Doces não são permitidos em dias úteis conforme as regras do seu programa."
- **Limite de exceções**: "Você já usou todas as exceções desta semana. Doces serão permitidos novamente na próxima semana."
- **Requer confirmação**: "Usar uma exceção? Você tem X exceções restantes esta semana."

---

## 3. Regra de Pizza (Opcional)

### Pseudocódigo
```
FUNÇÃO verificar_permissao_pizza(user_id, date, slices):
  enrollment = BUSCAR enrollment ONDE user_id E active = true
  ruleset = BUSCAR ruleset ONDE program_id = enrollment.program_id
  
  SE ruleset.pizza_limit IS NULL:
    RETORNAR PERMITIDO // Regra não configurada
  
  dia_semana = DIA_DA_SEMANA(date)
  SE dia_semana != 7: // Não é domingo
    RETORNAR PERMITIDO // Regra só aplica no domingo
  
  SE slices > ruleset.pizza_limit:
    REGISTRAR rule_event(
      user_id,
      'PIZZA_LIMIT_EXCEEDED',
      date,
      CONCATENAR('Tentativa de consumir ', slices, ' fatias (limite: ', ruleset.pizza_limit, ')')
    )
    RETORNAR BLOQUEADO
  
  REGISTRAR rule_event(
    user_id,
    'PIZZA_CONSUMED',
    date,
    CONCATENAR('Consumidas ', slices, ' fatias de pizza')
  )
  RETORNAR PERMITIDO
```

### Validações
- **Input**: `user_id`, `date`, `slices` (INTEGER > 0)
- **Output**: `{ allowed: boolean, message: string }`
- **Erros**: "Número de fatias inválido"

### Mensagens
- **Limite excedido**: "O limite de fatias de pizza no domingo é X. Você tentou consumir Y fatias."
- **Sucesso**: "Pizza registrada: X fatias consumidas."

---

## 4. Geração de Daily Meals

### Pseudocódigo
```
FUNÇÃO gerar_daily_meals(user_id, date):
  // Verificar se já existem
  existentes = BUSCAR daily_meals ONDE user_id E date
  SE existentes.count > 0:
    RETORNAR existentes // Já gerados
  
  enrollment = BUSCAR enrollment ONDE user_id E active = true
  SE enrollment NÃO EXISTE:
    RETORNAR ERRO "Usuário não está inscrito"
  
  dias_desde_inicio = DIFERENÇA_EM_DIAS(date, enrollment.start_date)
  week_index = (dias_desde_inicio DIV 7) + 1 // Semana 1, 2, 3...
  
  templates = BUSCAR plan_templates ONDE 
    program_id = enrollment.program_id E
    week_index = week_index E
    day_of_week = DIA_DA_SEMANA(date)
  
  SE templates.count == 0:
    RETORNAR ERRO "Templates não disponíveis para esta semana"
  
  daily_meals = []
  PARA CADA template EM templates:
    daily_meal = CRIAR daily_meal({
      user_id,
      date,
      meal_type: template.meal_type,
      opt1: template.opt1,
      opt2: template.opt2,
      opt3: template.opt3,
      avoid: template.avoid,
      option_selected: NULL
    })
    daily_meals.ADICIONAR(daily_meal)
  
  SALVAR daily_meals
  RETORNAR daily_meals
```

### Validações
- **Input**: `user_id`, `date`
- **Output**: Array de `daily_meals`
- **Erros**:
  - "Usuário não está inscrito em nenhum programa"
  - "Templates não disponíveis para esta semana"
  - "Erro ao gerar refeições do dia"

### Mensagens de Erro
- "Plano não disponível para hoje. Entre em contato com seu coach."
- "Erro ao carregar seu plano. Tente novamente."

---

## 5. Check-in Diário

### Pseudocódigo
```
FUNÇÃO criar_checkin(user_id, date, dados):
  VALIDAR dados:
    - weight: DECIMAL > 0 E < 500 (opcional)
    - workout_done: BOOLEAN
    - cardio_min: INTEGER >= 0 E <= 300
    - functional: BOOLEAN
  
  checkin_existente = BUSCAR daily_checkin ONDE user_id E date
  SE checkin_existente EXISTE:
    ATUALIZAR checkin_existente COM dados
    RETORNAR checkin_existente
  SENÃO:
    checkin = CRIAR daily_checkin({
      user_id,
      date,
      weight: dados.weight,
      workout_done: dados.workout_done,
      cardio_min: dados.cardio_min,
      functional: dados.functional
    })
    SALVAR checkin
    RETORNAR checkin
```

### Validações
- **Input**: 
  - `user_id` (UUID, obrigatório)
  - `date` (DATE, obrigatório, não pode ser futuro)
  - `weight` (DECIMAL, opcional, 0 < weight < 500)
  - `workout_done` (BOOLEAN, obrigatório)
  - `cardio_min` (INTEGER, obrigatório, 0 <= cardio_min <= 300)
  - `functional` (BOOLEAN, obrigatório)
- **Output**: `daily_checkin` criado/atualizado
- **Erros**:
  - "Data não pode ser no futuro"
  - "Peso inválido (deve estar entre 0 e 500 kg)"
  - "Minutos de cardio inválidos (máximo 300 minutos)"

### Mensagens de Erro
- "Preencha todos os campos obrigatórios"
- "Data inválida"
- "Valores fora do intervalo permitido"

---

## 6. Marcar Refeição como Feita

### Pseudocódigo
```
FUNÇÃO marcar_refeicao_feita(user_id, date, meal_type, option_selected):
  VALIDAR option_selected EM ['opt1', 'opt2', 'opt3']
  
  daily_meal = BUSCAR daily_meal ONDE 
    user_id E 
    date E 
    meal_type
  
  SE daily_meal NÃO EXISTE:
    RETORNAR ERRO "Refeição não encontrada"
  
  // Verificar regras de doce se aplicável
  SE meal_type CONTÉM "doce" OU daily_meal.avoid CONTÉM "doce":
    permissao = verificar_permissao_doce(user_id, date, meal_type)
    SE permissao.allowed == false:
      RETORNAR ERRO permissao.message
  
  daily_meal.option_selected = option_selected
  SALVAR daily_meal
  
  // Recalcular aderência
  adherence = calcular_aderencia(user_id, date)
  
  RETORNAR { daily_meal, adherence }
```

### Validações
- **Input**: 
  - `user_id`, `date`, `meal_type` (obrigatórios)
  - `option_selected` (deve ser 'opt1', 'opt2' ou 'opt3')
- **Output**: `daily_meal` atualizado + `adherence_pct`
- **Erros**:
  - "Refeição não encontrada"
  - "Opção selecionada inválida"
  - Mensagens de bloqueio de regras

### Mensagens de Erro
- "Refeição não encontrada para esta data"
- "Opção inválida. Selecione uma das opções disponíveis."
- [Mensagens de bloqueio de doce conforme regra 2]

---

## 7. Validações de RBAC (Role-Based Access Control)

### Pseudocódigo
```
FUNÇÃO verificar_acesso_admin(user_id):
  profile = BUSCAR profile ONDE id = user_id
  SE profile NÃO EXISTE:
    RETORNAR false
  
  org_member = BUSCAR org_member ONDE user_id E active = true
  SE org_member NÃO EXISTE:
    RETORNAR false
  
  SE org_member.role EM ['OWNER', 'COACH']:
    RETORNAR true
  
  RETORNAR false

FUNÇÃO verificar_acesso_membro(user_id, target_user_id):
  SE user_id == target_user_id:
    RETORNAR true // Próprio usuário
  
  // Coach pode ver membros do seu programa
  org_member_coach = BUSCAR org_member ONDE user_id E role = 'COACH'
  enrollment_target = BUSCAR enrollment ONDE user_id = target_user_id E active = true
  
  SE enrollment_target.program_id EM programas_do_coach:
    RETORNAR true
  
  // Owner pode ver todos da organização
  org_member_owner = BUSCAR org_member ONDE user_id E role = 'OWNER'
  org_member_target = BUSCAR org_member ONDE user_id = target_user_id
  
  SE org_member_owner.org_id == org_member_target.org_id:
    RETORNAR true
  
  RETORNAR false
```

### Validações
- **Input**: `user_id`, `target_user_id` (opcional)
- **Output**: `boolean`
- **Erros**: Não retorna erro, apenas false

---

## 8. Regras Faseadas (Hard Block → Exception with Cost)

### Pseudocódigo
```
FUNÇÃO determinar_modo_regra(user_id, date):
  enrollment = BUSCAR enrollment ONDE user_id E active = true
  ruleset = BUSCAR ruleset ONDE program_id = enrollment.program_id
  
  dias_desde_inicio = DIFERENÇA_EM_DIAS(date, enrollment.start_date)
  
  SE dias_desde_inicio < ruleset.hard_block_days:
    RETORNAR 'HARD_BLOCK' // Sempre bloqueado
  
  RETORNAR ruleset.weekday_sweets_mode // Segue configuração
```

### Validações
- Sempre calcula baseado em `enrollment.start_date` e `ruleset.hard_block_days`
- Não permite exceções durante período rígido

---

## 9. Exportação CSV

### Pseudocódigo
```
FUNÇÃO exportar_template_plano(program_id, week_index):
  templates = BUSCAR plan_templates ONDE program_id E week_index
  programa = BUSCAR program ONDE id = program_id
  org = BUSCAR org ONDE id = programa.org_id
  
  csv_rows = []
  csv_rows.ADICIONAR([
    'org_name',
    'program_name',
    'week_index',
    'day_of_week',
    'day_label',
    'meal_type',
    'opt1',
    'opt2',
    'opt3',
    'avoid'
  ])
  
  PARA CADA template EM templates:
    day_label = NOME_DIA(template.day_of_week)
    csv_rows.ADICIONAR([
      org.name,
      programa.name,
      template.week_index,
      template.day_of_week,
      day_label,
      template.meal_type,
      template.opt1,
      template.opt2,
      template.opt3,
      template.avoid
    ])
  
  RETORNAR GERAR_CSV(csv_rows)

FUNÇÃO exportar_plano_usuario(user_id, start_date, end_date):
  enrollment = BUSCAR enrollment ONDE user_id E active = true
  
  daily_meals = BUSCAR daily_meals ONDE 
    user_id E 
    date >= start_date E 
    date <= end_date
    ORDENAR POR date, meal_type
  
  csv_rows = []
  csv_rows.ADICIONAR([
    'date',
    'day_label',
    'meal_type',
    'option_selected',
    'opt1',
    'opt2',
    'opt3',
    'avoid'
  ])
  
  PARA CADA meal EM daily_meals:
    day_label = NOME_DIA(DIA_DA_SEMANA(meal.date))
    csv_rows.ADICIONAR([
      FORMATAR_DATA(meal.date),
      day_label,
      meal.meal_type,
      meal.option_selected OU '',
      meal.opt1,
      meal.opt2,
      meal.opt3,
      meal.avoid
    ])
  
  RETORNAR GERAR_CSV(csv_rows)

FUNÇÃO exportar_aderencia(user_id, start_date, end_date):
  checkins = BUSCAR daily_checkins ONDE 
    user_id E 
    date >= start_date E 
    date <= end_date
    ORDENAR POR date
  
  csv_rows = []
  csv_rows.ADICIONAR([
    'date',
    'adherence_pct',
    'meals_done',
    'meals_planned',
    'weight_kg',
    'cardio_min',
    'workout_done',
    'functional'
  ])
  
  PARA CADA checkin EM checkins:
    adherence = calcular_aderencia(user_id, checkin.date)
    meals_done = CONTAR daily_meals ONDE user_id E date = checkin.date E option_selected IS NOT NULL
    meals_planned = CONTAR daily_meals ONDE user_id E date = checkin.date
    
    csv_rows.ADICIONAR([
      FORMATAR_DATA(checkin.date),
      adherence,
      meals_done,
      meals_planned,
      checkin.weight OU '',
      checkin.cardio_min,
      checkin.workout_done ? 'Sim' : 'Não',
      checkin.functional ? 'Sim' : 'Não'
    ])
  
  RETORNAR GERAR_CSV(csv_rows)
```

### Validações
- **Input**: IDs válidos, datas no formato correto
- **Output**: String CSV com BOM UTF-8 para Excel
- **Erros**: "Dados não encontrados", "Período inválido"

### Mensagens de Erro
- "Nenhum dado encontrado para exportar"
- "Período de datas inválido"

---

## 10. Validações de Entrada (Zod Schemas)

### Schema: Daily Check-in
```typescript
{
  weight: z.number().min(0).max(500).optional(),
  workout_done: z.boolean(),
  cardio_min: z.number().int().min(0).max(300),
  functional: z.boolean()
}
```

### Schema: Mark Meal Done
```typescript
{
  meal_type: z.string(),
  option_selected: z.enum(['opt1', 'opt2', 'opt3'])
}
```

### Schema: Ruleset
```typescript
{
  weekday_sweets_mode: z.enum(['HARD_BLOCK', 'EXCEPTION_WITH_COST', 'ALLOW']),
  hard_block_days: z.number().int().min(0).max(365),
  weekly_exception_limit: z.number().int().min(0).max(10),
  pizza_limit: z.number().int().min(0).max(10).optional()
}
```

---

## 11. Tratamento de Erros

### Categorias
1. **Validação**: 400 Bad Request
2. **Autorização**: 403 Forbidden
3. **Não encontrado**: 404 Not Found
4. **Conflito**: 409 Conflict
5. **Servidor**: 500 Internal Server Error

### Formato de Resposta de Erro
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Mensagem amigável ao usuário",
    "details": { /* detalhes opcionais */ }
  }
}
```

---

## 12. Regras de Negócio - Resumo

### Fase 1: Hard Block (Primeiros X dias)
- ✅ Doces completamente bloqueados em dias úteis
- ✅ Todas as tentativas registradas em `rule_events`
- ✅ Mensagem clara: "Período de bloqueio rígido"

### Fase 2: Modo Configurado (Após X dias)
- **HARD_BLOCK**: Continua bloqueado
- **EXCEPTION_WITH_COST**: Permite com limite semanal
- **ALLOW**: Permite livremente

### Validações Críticas
- ✅ RLS garante isolamento de dados
- ✅ Validação server-side de todas as regras
- ✅ Auditoria completa em `rule_events`
- ✅ Cálculo de aderência sempre atualizado

