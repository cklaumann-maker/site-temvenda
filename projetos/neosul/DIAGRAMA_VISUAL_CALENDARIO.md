# 📐 Diagrama Visual do Calendário NEOSUL

## 🎨 Visão Geral da Estrutura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONTAINER PRINCIPAL                                 │
│                      (#module-calendario)                                   │
│  Height: calc(100vh - 180px) | Gap: 5px | Margin-left: 5px                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    CALENDÁRIO (calendar-layout)                     │  │
│  │  Margin-right: 150px | Max-width: calc(100% - 528.5px)             │  │
│  │  Gap: 1rem (16px) quando sidebar aberta                              │  │
│  │  Gap: 1.5rem (24px) quando sidebar recolhida                        │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │              HEADER DO CALENDÁRIO                             │  │  │
│  │  │  Height: ~60px | Padding-bottom: 0.75rem (12px)             │  │  │
│  │  │  ┌──────┐  ┌──────────────────┐  ┌──────┐  ┌──────┐         │  │  │
│  │  │  │  ←   │  │  Fevereiro 2026  │  │ Novo │  │  →   │         │  │  │
│  │  │  │      │  │                  │  │ Mês  │  │      │         │  │  │
│  │  │  └──────┘  └──────────────────┘  └──────┘  └──────┘         │  │  │
│  │  │  Gap: 1.5rem (24px)                                          │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │              CABEÇALHO DOS DIAS DA SEMANA                    │  │  │
│  │  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │  │  │
│  │  │  │ DOM │ │ SEG │ │ TER │ │ QUA │ │ QUI │ │ SEX │ │ SÁB │    │  │  │
│  │  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘    │  │  │
│  │  │  Font-size: 0.6875rem (11px) | Padding: 0.375rem (6px)     │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │              GRADE DO CALENDÁRIO (calendar-grid)             │  │  │
│  │  │  Grid: 7 colunas (repeat(7, 1fr))                           │  │  │
│  │  │  Gap: 2px (sidebar aberta) | 6px (sidebar recolhida)         │  │  │
│  │  │                                                              │  │  │
│  │  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │  │  │
│  │  │  │  1  │ │  2  │ │  3  │ │  4  │ │  5  │ │  6  │ │  7  │    │  │  │
│  │  │  │ S1  │ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  │     │ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  │[G:2]│ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  │[S:1]│ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘    │  │  │
│  │  │                                                              │  │  │
│  │  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │  │  │
│  │  │  │  8  │ │  9  │ │ 10  │ │ 11  │ │ 12  │ │ 13  │ │ 14  │    │  │  │
│  │  │  │     │ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  │     │ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  │     │ │     │ │     │ │     │ │     │ │     │ │     │    │  │  │
│  │  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘    │  │  │
│  │  │  ... (continua para todas as semanas do mês)                │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  Margin-top: 0.75rem (12px)                                        │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │              TABELA: ATIVIDADES DO DIA                       │  │  │
│  │  │  Font-size: 0.75rem (12px)                                   │  │  │
│  │  │  Padding células: 0.5rem (8px)                              │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  Gap: 1rem (16px)                                                   │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │              TABELA: RESUMO SEMANAL                          │  │  │
│  │  │  Font-size: 0.75rem (12px)                                   │  │  │
│  │  │  Padding células: 0.5rem (8px)                              │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Gap: 5px                                                                  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    SIDEBAR (details-sidebar)                        │  │
│  │  Width: 580px | Position: fixed | Right: 0                         │  │
│  │  Top: 120px | Padding: 1rem (16px)                                  │  │
│  │  Gap entre cards: 1rem (16px)                                       │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │  Card: Contador de Horas                                      │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │  Card: Planejamento Mensal                                   │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │  Card: Planejamento Semanal                                  │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │  Card: Resumo Semanal                                       │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔲 DETALHAMENTO DO QUADRADO DE DIA

### Quando Sidebar Está ABERTA (`body:not(.sidebar-collapsed)`)

```
┌─────────────────────────────────────────┐
│  ┌───────────────────────────────────┐   │
│  │  [S1] ← Badge Semana             │   │  Top: 2px, Right: 2px
│  │  8px × 8px                        │   │  Font-size: 0.6rem (9.6px)
│  │                                   │   │
│  │  1                                │   │  Número do Dia
│  │  ← day-number                     │   │  Font-size: 0.875rem (14px)
│  │                                   │   │  Font-weight: 600
│  │                                   │   │
│  │                                   │   │
│  │                                   │   │
│  │  ┌─────────────────────────────┐  │   │
│  │  │ Atividades: 3               │  │   │  Card Verde (normal)
│  │  └─────────────────────────────┘  │   │  Bottom: 2px, Left: 2px, Right: 2px
│  │  ┌─────────────────────────────┐  │   │  Padding: 3px 5px
│  │  │ Consultoria Externa: 1       │  │   │  Font-size: 0.625rem (10px)
│  │  └─────────────────────────────┘  │   │  Gap entre cards: 3px
│  └───────────────────────────────────┘   │
│                                           │
│  QUADRADO TOTAL:                         │
│  Min-height: 12px                        │
│  Padding: 0.09rem (≈1.44px)              │
│  Border: 1px solid                      │
│  Border-radius: 4px                      │
│  Aspect-ratio: 1 (quadrado)              │
└─────────────────────────────────────────┘
```

### Quando Sidebar Está RECOLHIDA (`body.sidebar-collapsed`)

```
┌─────────────────────────────────────────┐
│  ┌───────────────────────────────────┐   │
│  │  [S1] ← Badge Semana             │   │  Top: 2px, Right: 2px
│  │  8px × 8px                        │   │  Font-size: 0.6rem (9.6px)
│  │                                   │   │
│  │                                   │   │
│  │  1                                │   │  Número do Dia
│  │  ← day-number                     │   │  Font-size: 1rem (16px)
│  │                                   │   │  Font-weight: 600
│  │                                   │   │
│  │                                   │   │
│  │                                   │   │
│  │                                   │   │
│  │                                   │   │
│  │                                   │   │
│  │  ┌─────────────────────────────┐  │   │
│  │  │ Atividades: 3               │  │   │  Card Verde (normal)
│  │  └─────────────────────────────┘  │   │  Bottom: 2px, Left: 2px, Right: 2px
│  │  ┌─────────────────────────────┐  │   │  Padding: 3px 5px
│  │  │ Consultoria Externa: 1       │  │   │  Font-size: 0.625rem (10px)
│  │  └─────────────────────────────┘  │   │  Gap entre cards: 3px
│  └───────────────────────────────────┘   │
│                                           │
│  QUADRADO TOTAL:                         │
│  Min-height: 32px                        │
│  Padding: 0.15rem (≈2.4px)               │
│  Border: 1px solid                      │
│  Border-radius: 4px                      │
│  Aspect-ratio: 1 (quadrado)              │
└─────────────────────────────────────────┘
```

---

## 📊 TABELA DE MEDIDAS COMPLETA

### Container Principal
| Elemento | Propriedade | Valor (Sidebar Aberta) | Valor (Sidebar Recolhida) |
|----------|-------------|------------------------|---------------------------|
| `#module-calendario` | Height | `calc(100vh - 180px)` | `calc(100vh - 180px)` |
| `#module-calendario` | Gap | `5px` | `5px` |
| `#module-calendario` | Margin-left | `5px` | `5px` |

### Calendário Layout
| Elemento | Propriedade | Valor (Sidebar Aberta) | Valor (Sidebar Recolhida) |
|----------|-------------|------------------------|---------------------------|
| `.calendar-layout` | Margin-right | `150px` | `0px` |
| `.calendar-layout` | Max-width | `calc(100% - 528.5px)` | `100%` |
| `.calendar-layout` | Gap | `1rem` (16px) | `1.5rem` (24px) |

### Calendário Principal
| Elemento | Propriedade | Valor (Sidebar Aberta) | Valor (Sidebar Recolhida) |
|----------|-------------|------------------------|---------------------------|
| `.calendar-main` | Padding | `0.875rem` (14px) | `1.5rem` (24px) |
| `.calendar-main` | Margin-left | `5px` | `5px` |
| `.calendar-header` | Margin-bottom | `1rem` (16px) | `1rem` (16px) |
| `.calendar-header` | Padding-bottom | `0.75rem` (12px) | `0.75rem` (12px) |
| `.calendar-month-year` | Font-size | `1.5rem` (24px) | `1.5rem` (24px) |

### Grade do Calendário
| Elemento | Propriedade | Valor (Sidebar Aberta) | Valor (Sidebar Recolhida) |
|----------|-------------|------------------------|---------------------------|
| `.calendar-grid` | Grid-columns | `repeat(7, 1fr)` | `repeat(7, 1fr)` |
| `.calendar-grid` | Gap | `2px` | `6px` |

### Quadrados de Dias
| Elemento | Propriedade | Valor (Sidebar Aberta) | Valor (Sidebar Recolhida) |
|----------|-------------|------------------------|---------------------------|
| `.calendar-day` | Min-height | `12px` | `32px` |
| `.calendar-day` | Padding | `0.09rem` (≈1.44px) | `0.15rem` (≈2.4px) |
| `.calendar-day` | Border | `1px solid` | `1px solid` |
| `.calendar-day` | Border-radius | `4px` | `4px` |
| `.calendar-day` | Aspect-ratio | `1` | `1` |
| `.day-number` | Font-size | `0.875rem` (14px) | `1rem` (16px) |
| `.day-number` | Font-weight | `600` | `600` |

### Cards de Atividades nos Quadrados
| Elemento | Propriedade | Valor |
|----------|-------------|-------|
| Container | Position | `absolute` |
| Container | Bottom | `2px` |
| Container | Left | `2px` |
| Container | Right | `2px` |
| Container | Gap | `3px` |
| Card Verde | Padding | `3px 5px` |
| Card Verde | Font-size | `0.625rem` (10px) |
| Card Salmon | Padding | `3px 5px` |
| Card Salmon | Font-size | `0.625rem` (10px) |

### Badge de Semana
| Elemento | Propriedade | Valor |
|----------|-------------|-------|
| `.week-badge` | Position | `absolute` |
| `.week-badge` | Top | `2px` |
| `.week-badge` | Right | `2px` |
| `.week-badge` | Font-size | `0.6rem` (9.6px) |
| `.week-badge` | Padding | `2px 4px` |

### Tabelas
| Elemento | Propriedade | Valor (Sidebar Aberta) | Valor (Sidebar Recolhida) |
|----------|-------------|------------------------|---------------------------|
| Container | Margin-top | `0.75rem` (12px) | `0.75rem` (12px) |
| Container | Gap | `1rem` (16px) | `1rem` (16px) |
| `.table-atividades` | Font-size | `0.75rem` (12px) | `0.8125rem` (13px) |
| `.table-atividades th` | Padding | `0.375rem 0.5rem` (6px 8px) | `0.375rem 0.5rem` (6px 8px) |
| `.table-atividades td` | Padding | `0.5rem` (8px) | `0.5rem` (8px) |

### Sidebar
| Elemento | Propriedade | Valor |
|----------|-------------|-------|
| `.details-sidebar` | Width | `580px` |
| `.details-sidebar` | Position | `fixed` |
| `.details-sidebar` | Right | `0px` |
| `.details-sidebar` | Top | `120px` |
| `.details-sidebar` | Padding | `1rem` (16px) |
| `.details-sidebar` | Gap | `1rem` (16px) |

---

## 🎯 PONTOS DE REFERÊNCIA PARA MUDANÇAS

### Para Ajustar Tamanho dos Quadrados:
- **Altura**: `.calendar-day` → `min-height`
- **Padding**: `.calendar-day` → `padding`
- **Gap entre quadrados**: `.calendar-grid` → `gap`

### Para Ajustar Tamanho do Calendário:
- **Altura total**: `#module-calendario` → `height`
- **Largura máxima**: `.calendar-layout` → `max-width`
- **Padding interno**: `.calendar-main` → `padding`

### Para Ajustar Espaçamento:
- **Entre calendário e sidebar**: `#module-calendario` → `gap`
- **Entre calendário e tabelas**: Container das tabelas → `margin-top`
- **Entre tabelas**: Container das tabelas → `gap`

### Para Ajustar Sidebar:
- **Largura**: `.details-sidebar` → `width`
- **Espaço reservado**: `.calendar-layout` → `margin-right` e `max-width`

### Para Ajustar Cards de Atividades:
- **Tamanho do texto**: Cards → `font-size`
- **Padding**: Cards → `padding`
- **Gap entre cards**: Container → `gap`
- **Posição**: Container → `bottom`, `left`, `right`

---

## 📐 CONVERSÃO DE UNIDADES

| Unidade | Valor em Pixels (assumindo 16px base) |
|---------|--------------------------------------|
| `0.09rem` | ≈ 1.44px |
| `0.15rem` | ≈ 2.4px |
| `0.375rem` | 6px |
| `0.5rem` | 8px |
| `0.625rem` | 10px |
| `0.6875rem` | 11px |
| `0.75rem` | 12px |
| `0.8125rem` | 13px |
| `0.875rem` | 14px |
| `1rem` | 16px |
| `1.5rem` | 24px |

---

## 🖼️ Diagrama Visual Gerado

Uma imagem visual detalhada foi gerada em:
`/Users/cesark/site-temvenda/projetos/neosul/diagrama-calendario-neosul.png`

Esta imagem mostra a estrutura completa do calendário com todas as medidas e elementos visuais.

---

**Última atualização**: 2026-02-01
**Versão**: 1.0
