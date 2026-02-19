# NEOSUL - Características Completas do Calendário

## 📐 Estrutura Geral do Espaço do Calendário

### Container Principal (`#module-calendario`)
- **Display**: `flex`
- **Gap**: `5px` (espaço entre calendário e sidebar)
- **Position**: `relative`
- **Height**: `calc(100vh - 180px)` (altura total da viewport menos 180px)
- **Margin-left**: `5px` (deslocado 5px para a esquerda)

### Layout do Calendário (`.calendar-layout`)
- **Flex**: `1` (ocupa espaço disponível)
- **Display**: `flex`
- **Flex-direction**: `column` (vertical)
- **Gap**: `1rem` (16px) entre elementos
- **Overflow-y**: `auto` (scroll vertical se necessário)
- **Transition**: `all 0.3s ease`

#### Quando sidebar está aberta (`body:not(.sidebar-collapsed)`)
- **Margin-right**: `150px`
- **Max-width**: `calc(100% - 528.5px)`

#### Quando sidebar está recolhida (`body.sidebar-collapsed`)
- **Gap**: `1.5rem` (24px)
- **Max-width**: `100%`

---

## 📅 Calendário Principal (`.calendar-main`)

### Características Gerais
- **Background**: `var(--neosul-white)` (branco)
- **Border-radius**: `8px`
- **Padding**: `0.875rem` (14px)
- **Box-shadow**: `0 2px 8px rgba(0, 0, 0, 0.05)`
- **Flex-shrink**: `0` (não encolhe)
- **Transition**: `all 0.3s ease`
- **Max-width**: `100%`
- **Margin-left**: `5px`

#### Quando sidebar está recolhida
- **Padding**: `1.5rem` (24px)

### Header do Calendário (`.calendar-header`)
- **Display**: `flex`
- **Align-items**: `center`
- **Justify-content**: `space-between`
- **Margin-bottom**: `1rem` (16px)
- **Padding-bottom**: `0.75rem` (12px)
- **Border-bottom**: `2px solid var(--neosul-gray-light)`

### Navegação do Calendário (`.calendar-nav`)
- **Display**: `flex`
- **Align-items**: `center`
- **Gap**: `1.5rem` (24px)

#### Botões de Navegação
- **Background**: `transparent`
- **Border**: `1px solid var(--neosul-border)`
- **Border-radius**: `4px`
- **Padding**: `0.5rem 0.75rem` (8px 12px)
- **Cursor**: `pointer`
- **Color**: `var(--neosul-gray)`
- **Transition**: `all 0.3s ease`
- **Display**: `flex`
- **Align-items**: `center`
- **Gap**: `0.25rem` (4px)

#### Ícones SVG nos Botões
- **Width**: `16px`
- **Height**: `16px`

#### Hover dos Botões
- **Background**: `var(--neosul-gray-light)`
- **Border-color**: `var(--neosul-blue)`
- **Color**: `var(--neosul-blue)`

### Título do Mês/Ano (`.calendar-month-year`)
- **Font-size**: `1.5rem` (24px)
- **Font-weight**: `700` (bold)
- **Color**: `var(--neosul-gray-dark)`

---

## 🔲 Grade do Calendário (`.calendar-grid`)

### Características Gerais
- **Display**: `grid`
- **Grid-template-columns**: `repeat(7, 1fr)` (7 colunas iguais)
- **Gap**: `2px` (espaço entre quadrados)
- **Transition**: `all 0.3s ease`

#### Quando sidebar está aberta (`body:not(.sidebar-collapsed)`)
- **Gap**: `2px`

#### Quando sidebar está recolhida (`body.sidebar-collapsed`)
- **Gap**: `6px`

---

## 📆 Quadrados de Dias (`.calendar-day`)

### Características Base
- **Aspect-ratio**: `1` (sempre quadrado)
- **Border**: `1px solid var(--neosul-border)`
- **Border-radius**: `4px`
- **Padding**: `0.5rem` (8px) - padrão, mas sobrescrito
- **Cursor**: `pointer`
- **Transition**: `all 0.3s ease`
- **Position**: `relative`
- **Background**: `var(--neosul-white)`

### Quando Sidebar Está Aberta (`body:not(.sidebar-collapsed)`)
- **Min-height**: `12px`
- **Padding**: `0.09rem` (≈ 1.44px)
- **Aspect-ratio**: `1`

### Quando Sidebar Está Recolhida (`body.sidebar-collapsed`)
- **Min-height**: `32px`
- **Padding**: `0.15rem` (≈ 2.4px)
- **Aspect-ratio**: `1`

### Estados dos Quadrados

#### Hover (`.calendar-day:hover`)
- **Background**: `var(--neosul-gray-light)`
- **Border-color**: `var(--neosul-blue)`

#### Mês Anterior/Posterior (`.calendar-day.other-month`)
- **Opacity**: `0.3`
- **Pointer-events**: `none` (não clicável)

#### Semana Atual (`.calendar-day.current-week`)
- **Border**: `2px solid var(--neosul-blue)`
- **Background**: `rgba(30, 77, 139, 0.05)` (azul muito claro)

#### Hoje (`.calendar-day.today`)
- **Background**: `var(--neosul-blue)` (azul sólido)
- **Color**: `var(--neosul-white)` (texto branco)
- **Font-weight**: `700` (bold)

---

## 🔢 Número do Dia (`.day-number`)

### Características Base
- **Font-size**: `0.9375rem` (15px)
- **Font-weight**: `600` (semi-bold)

#### Quando Sidebar Está Aberta (`body:not(.sidebar-collapsed)`)
- **Font-size**: `0.875rem` (14px)

#### Quando Sidebar Está Recolhida (`body.sidebar-collapsed`)
- **Font-size**: `1rem` (16px)

---

## 📋 Cards de Atividades Dentro dos Quadrados

### Container de Atividades
- **Position**: `absolute`
- **Bottom**: `2px`
- **Left**: `2px`
- **Right**: `2px`
- **Display**: `flex`
- **Flex-direction**: `column`
- **Gap**: `3px` (entre os cards)

### Card de Atividades Normais (Verde)
- **Background**: `rgba(129, 199, 132, 0.15)` (verde claro)
- **Border**: `1px solid #81c784`
- **Border-left**: `3px solid #81c784`
- **Border-radius**: `3px`
- **Padding**: `3px 5px`
- **Box-shadow**: `0 1px 2px rgba(0, 0, 0, 0.05)`
- **Display**: `flex`
- **Justify-content**: `space-between`
- **Font-size**: `0.625rem` (10px)
- **Color**: `#81c784` (verde)

### Card de Consultoria Externa (Salmon)
- **Background**: `rgba(255, 171, 145, 0.15)` (salmon claro)
- **Border**: `1px solid #ffab91`
- **Border-left**: `3px solid #ffab91`
- **Border-radius**: `3px`
- **Padding**: `3px 5px`
- **Box-shadow**: `0 1px 2px rgba(0, 0, 0, 0.05)`
- **Display**: `flex`
- **Justify-content**: `space-between`
- **Font-size**: `0.625rem` (10px)
- **Color**: `#ffab91` (salmon)

### Conteúdo dos Cards
- **Label**: "Atividades" (para atividades normais)
- **Label**: "Consultoria Externa" (para consultoria externa)
- **Contador**: Número de atividades do tipo
- **Gap entre label e contador**: `6px`

---

## 🏷️ Badge de Semana (`.week-badge`)
- **Position**: `absolute`
- **Top**: `2px`
- **Right**: `2px`
- **Background**: `var(--neosul-blue)`
- **Color**: `var(--neosul-white)`
- **Font-size**: `0.6rem` (9.6px)
- **Padding**: `2px 4px`
- **Border-radius**: `2px`
- **Font-weight**: `700` (bold)
- **Conteúdo**: "S" + número da semana (ex: "S1", "S2")

---

## 🔵 Indicadores de Status (`.day-indicators`)
- **Display**: `flex`
- **Gap**: `2px`
- **Margin-top**: `4px`
- **Flex-wrap**: `wrap`

### Indicador Dot (`.indicator-dot`)
- **Width**: `6px`
- **Height**: `6px`
- **Border-radius**: `50%` (círculo)

#### Cores por Status
- **Planejado** (`.planned`): `#28a745` (verde)
- **Em Andamento** (`.in-progress`): `#ffc107` (amarelo)
- **Atrasado** (`.delayed`): `#dc3545` (vermelho)
- **Não Planejado** (`.not-planned`): `#6c757d` (cinza)

---

## 📊 Cabeçalho dos Dias da Semana (`.calendar-day-header`)
- **Text-align**: `center`
- **Font-size**: `0.6875rem` (11px)
- **Font-weight**: `700` (bold)
- **Color**: `var(--neosul-gray)`
- **Padding**: `0.375rem 0` (6px vertical)
- **Text-transform**: `uppercase`

---

## 📋 Tabelas de Atividades

### Container das Tabelas
- **Margin-top**: `0.75rem` (12px)
- **Display**: `grid`
- **Gap**: `1rem` (16px entre tabelas)

### Título das Tabelas
- **Font-size**: `0.6875rem` (11px)
- **Font-weight**: `500`
- **Margin-bottom**: `0.5rem` (8px)
- **Text-transform**: `uppercase`
- **Letter-spacing**: `0.5px`
- **Color**: `var(--neosul-gray)`
- **Display**: `flex`
- **Align-items**: `center`
- **Gap**: `0.375rem` (6px)

#### Ícones nos Títulos
- **Width**: `11px`
- **Height**: `11px`

### Tabela de Atividades (`.table-atividades`)

#### Características Gerais
- **Width**: `100%`
- **Border-collapse**: `collapse`
- **Font-size**: `0.75rem` (12px)
- **Border**: `none`
- **Transition**: `all 0.3s ease`

#### Quando Sidebar Está Recolhida
- **Font-size**: `0.8125rem` (13px)

#### Cabeçalho (`.table-atividades thead`)
- **Background**: `transparent`

#### Células do Cabeçalho (`.table-atividades th`)
- **Padding**: `0.375rem 0.5rem` (6px 8px)
- **Text-align**: `left`
- **Font-weight**: `500`
- **Color**: `var(--neosul-gray)`
- **Text-transform**: `uppercase`
- **Font-size**: `0.6875rem` (11px)
- **Letter-spacing**: `0.5px`

#### Células do Corpo (`.table-atividades td`)
- **Padding**: `0.5rem` (8px)
- **Border-bottom**: `1px solid rgba(0, 0, 0, 0.03)`
- **Vertical-align**: `middle`
- **Font-weight**: `400`

#### Linhas do Corpo (`.table-atividades tbody tr`)
- **Transition**: `background 0.15s ease`

#### Hover das Linhas
- **Background**: `rgba(30, 77, 139, 0.02)` (azul muito claro)
- **Cursor**: `pointer`

#### Linha de Consultoria Externa (`.table-atividades tbody tr.consultoria-externa`)
- **Background**: `rgba(250, 128, 114, 0.12)` (salmon claro)

#### Hover de Consultoria Externa
- **Background**: `rgba(250, 128, 114, 0.18)` (salmon mais escuro)

#### Última Linha
- **Border-bottom**: `none`

---

## 📊 Resumo Semanal

### Container do Resumo (`#resumoSemanalInfo`)
- **Display**: `flex`
- **Gap**: `1rem` (16px)
- **Margin-bottom**: `0.75rem` (12px)
- **Padding**: `0.5rem` (8px)
- **Background**: `rgba(30, 77, 139, 0.02)` (azul muito claro)
- **Border-radius**: `4px`

### Botão de Toggle Relatório (`#toggleRelatorioSemanal`)
- **Background**: `transparent`
- **Border**: `1px solid var(--neosul-border)`
- **Border-radius**: `4px`
- **Padding**: `0.25rem 0.5rem` (4px 8px)
- **Font-size**: `0.625rem` (10px)
- **Color**: `var(--neosul-blue)`
- **Cursor**: `pointer`
- **Display**: `flex`
- **Align-items**: `center`
- **Gap**: `0.25rem` (4px)

#### Ícone do Botão
- **Width**: `12px`
- **Height**: `12px`

### Relatório Detalhado (`#relatorioSemanalDetalhado`)
- **Display**: `none` (oculto por padrão)
- **Margin-top**: `0.75rem` (12px)

---

## 📏 Espaçamentos e Margens

### Entre Calendário e Tabelas
- **Margin-top**: `0.75rem` (12px)

### Entre Tabelas
- **Gap**: `1rem` (16px)

### Entre Calendário e Sidebar
- **Gap**: `5px`

### Padding do Calendário Principal
- **Padrão**: `0.875rem` (14px)
- **Sidebar recolhida**: `1.5rem` (24px)

---

## 🎨 Cores Utilizadas

### Cores Principais
- **Azul NEOSUL**: `#1e4d8b` (`var(--neosul-blue)`)
- **Azul Claro**: `#2563a8` (`var(--neosul-blue-light)`)
- **Azul Escuro**: `#163761` (`var(--neosul-blue-dark)`)
- **Branco**: `#ffffff` (`var(--neosul-white)`)
- **Cinza Claro**: `#f8f9fa` (`var(--neosul-gray-light)`)
- **Cinza**: `#6c757d` (`var(--neosul-gray)`)
- **Cinza Escuro**: `#343a40` (`var(--neosul-gray-dark)`)
- **Borda**: `#e0e5eb` (`var(--neosul-border)`)

### Cores de Atividades
- **Verde (Atividades Normais)**: `#81c784`
- **Salmon (Consultoria Externa)**: `#ffab91` / `#fa8072`

### Cores de Status
- **Previsto**: `#2196f3` (azul)
- **Realizado**: `#4caf50` (verde)
- **Em Andamento**: `#ff9800` (laranja)
- **Cancelado**: `#f44336` (vermelho)

---

## 📐 Resumo das Dimensões

### Quadrados de Dias

| Estado | Min-Height | Padding | Gap | Font-size (número) |
|--------|------------|---------|-----|-------------------|
| Sidebar Aberta | 12px | 0.09rem (≈1.44px) | 2px | 0.875rem (14px) |
| Sidebar Recolhida | 32px | 0.15rem (≈2.4px) | 6px | 1rem (16px) |

### Cards de Atividades nos Quadrados
- **Padding**: `3px 5px`
- **Font-size**: `0.625rem` (10px)
- **Gap entre cards**: `3px`
- **Border-left**: `3px solid`

### Tabelas
- **Font-size**: `0.75rem` (12px) / `0.8125rem` (13px quando sidebar recolhida)
- **Padding células**: `0.5rem` (8px)
- **Padding cabeçalho**: `0.375rem 0.5rem` (6px 8px)

### Espaçamentos Principais
- **Gap calendário-layout**: `1rem` (16px) / `1.5rem` (24px quando sidebar recolhida)
- **Margin-top tabelas**: `0.75rem` (12px)
- **Gap entre tabelas**: `1rem` (16px)
- **Gap calendário-sidebar**: `5px`

---

## 🔄 Transições e Animações

- **Todas as transições**: `0.3s ease`
- **Hover dos botões**: `all 0.3s ease`
- **Hover das linhas da tabela**: `background 0.15s ease`
- **Transform no hover**: `translateX(2px)` (cards de atividades)

---

## 📱 Responsividade

### Media Queries
- **Max-width 768px**: Sidebar oculta, grid de 1 coluna
- **Max-width 1024px**: Layout de 2 colunas vira 1 coluna

---

## 🎯 Funcionalidades Especiais

### Cards de Atividades nos Quadrados
- Mostram contagem separada de atividades normais (verde) e consultoria externa (salmon)
- Posicionados no bottom do quadrado
- Layout flex column com gap de 3px

### Badge de Semana
- Aparece apenas no primeiro dia da semana (domingo)
- Mostra número da semana (S1, S2, etc.)

### Indicadores de Status
- Dots coloridos baseados no status do planejamento semanal
- Posicionados abaixo do número do dia

### Tabelas Interativas
- Linhas clicáveis para editar atividades
- Destaque especial para atividades de consultoria externa (fundo salmon)
- Hover effect em todas as linhas

---

Este documento lista todas as características visuais e estruturais do calendário NEOSUL.
