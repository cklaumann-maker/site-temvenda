# Racional da contagem de horas – NEOSUL

Este documento descreve **exatamente** como são calculadas as horas no sistema: contador geral e consultoria externa, e a relação entre eles.

---

## 1. Fonte dos dados

- **Tabela:** `neosul_atividades_diarias`
- **Filtro de dono:** todas as contagens usam `gerente_nome` = pessoa em visualização (usuário logado ou colaborador selecionado no filtro).
- **Campos usados:** `data`, `hora_inicio`, `hora_fim`, `tipo`, `status`.

**Cálculo de duração de uma atividade (em minutos):**

```text
duração = (hora_fim em minutos desde 0h) − (hora_inicio em minutos desde 0h)
         (se fim ≤ inicio, retorna 0)
```

Ou seja: cada atividade contribui com a diferença entre `hora_fim` e `hora_inicio` (em minutos).

---

## 2. Contador de horas (geral) – Dia / Semana / Mês

### Regra

- **Não soma** atividades do tipo **consultoria_externa**.
- Soma **apenas** atividades cujo `tipo` é **diferente** de `consultoria_externa` (reunião, visita, treinamento, planejamento, operacional, outro).

### Fórmula (conceitual)

```text
Total geral (dia/semana/mês) = Σ duração(atividade)
                                 para cada atividade onde tipo ≠ 'consultoria_externa'
```

### Onde aparece

- **Top bar:** Dia, Semana, Mês (horas).
- **Sidebar do calendário:** Total do dia, da semana e do mês (mesmos valores).
- **Resumo da tabela da semana:** total de horas da semana (também **exclui** consultoria externa).
- **Resumo por dia** (tabela da semana): minutos por dia **excluindo** consultoria externa.

### Resumo por tipo (mês)

- O bloco “Por tipo” (reunião, visita, etc.) usa **só** atividades do mês com `tipo !== 'consultoria_externa'`.
- Ou seja: consultoria externa **não** entra no contador geral nem no resumo por tipo.

---

## 3. Contador de consultoria externa

### Regra

- Soma **apenas** atividades do tipo **consultoria_externa**.
- Usa a **mesma** duração (hora_fim − hora_inicio) por atividade.

### Fórmula (conceitual)

```text
Consultoria (dia/semana/mês) = Σ duração(atividade)
                               para cada atividade onde tipo === 'consultoria_externa'
```

### Métricas exibidas (quando o card é visível)

| Métrica              | Cálculo                                                                 |
|----------------------|-------------------------------------------------------------------------|
| **Dia**              | Soma das durações das atividades `consultoria_externa` do dia.          |
| **Semana**           | Soma das durações das atividades `consultoria_externa` da semana.      |
| **Mês**              | Soma das durações das atividades `consultoria_externa` do mês.        |
| **Sessões (mês)**    | Número de atividades (registros) com `tipo === 'consultoria_externa'` no mês. |
| **Percentual**       | `consultoriaMes / minutosMes * 100` (arredondado).                     |

Onde:

- `consultoriaMes` = total de **minutos** de consultoria externa no mês.
- `minutosMes` = total de minutos do **contador geral** no mês (já **excluindo** consultoria externa).

Ou seja: o percentual é “horas de consultoria no mês” em relação às “horas do contador geral no mês” (que não incluem consultoria). **Não** é percentual sobre um total que já inclua consultoria.

### Visibilidade do card

- O **card** de consultoria externa (e os números acima) só é exibido para:
  - perfil **diretor**, ou
  - usuário **Cesar** (nome + username).

---

## 4. Relação entre os dois: um soma no outro?

**Não.** Eles são **isolados**:

| Contador              | O que entra na soma                                      |
|-----------------------|----------------------------------------------------------|
| **Contador geral**    | Todas as atividades **exceto** `consultoria_externa`.   |
| **Consultoria externa** | **Apenas** atividades com `tipo === 'consultoria_externa'`. |

- Uma atividade é **ou** “geral” **ou** “consultoria externa”, nunca os dois ao mesmo tempo.
- Nenhuma hora é somada nos dois contadores.
- O **total “geral”** (Dia/Semana/Mês) **nunca** inclui consultoria externa.
- Para ter um “total que inclua tudo” (geral + consultoria), seria preciso somar os dois números manualmente; o sistema não exibe esse total único.

---

## 5. Resumo por status (mês)

- O bloco “Por status” (previsto, realizado, em andamento, cancelado) usa apenas atividades com `tipo !== 'consultoria_externa'`.
- Consultoria externa **não** entra no contador geral, no resumo por tipo nem no resumo por status.

---

## 6. Tabela resumo da semana (por dia)

- **Total de atividades:** conta **todas** as atividades (inclui consultoria externa).
- **Minutos por dia** no resumo: soma apenas atividades com `tipo !== 'consultoria_externa'` (igual ao contador geral).

---

## 7. Referência rápida no código

- **Contador geral (excluindo consultoria):**  
  `calcularTotal(atividades)` → `filter(a => a.tipo !== 'consultoria_externa')` + `calcularDuracaoAtividade`.
- **Consultoria externa:**  
  `calcularConsultoria(atividades)` → `filter(a => a.tipo === 'consultoria_externa')` + `calcularDuracaoAtividade`.
- **Percentual consultoria:**  
  `consultoriaPercentual = minutosMes > 0 ? Math.round((consultoriaMes / minutosMes) * 100) : 0`  
  (com `minutosMes` já sem consultoria).

Documento gerado com base no `index.html` do projeto NEOSUL (função `atualizarContadorHoras` e funções relacionadas).
