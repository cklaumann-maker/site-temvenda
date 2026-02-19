# 🔍 Análise Completa: Redução de 40% na Altura dos Quadrados

## Problemas Identificados que Impactam a Altura

### 1. **Conteúdo Interno Forçando Expansão**
   - `min-height: 9px` é muito pequeno, mas o conteúdo interno está expandindo os quadrados
   - `aspect-ratio: 1` força quadrados, mas não limita altura quando há conteúdo

### 2. **Elementos que Contribuem para a Altura:**

#### A. Número do Dia (`.day-number`)
   - Font-size: `0.875rem` (14px) quando sidebar aberta
   - Sem `line-height` definido (usa padrão ~1.2-1.5)
   - **Impacto**: ~16-20px de altura

#### B. Cards de Atividades (criados via JavaScript)
   - Padding: `3px 5px` (vertical: 3px × 2 = 6px)
   - Font-size: `0.625rem` (10px)
   - Border-left: `3px`
   - Gap entre cards: `3px`
   - **Impacto**: Cada card ~12-15px, com gap ~18-21px para 2 cards

#### C. Badge de Semana (`.week-badge`)
   - Padding: `2px 4px` (vertical: 2px × 2 = 4px)
   - Font-size: `0.6rem` (9.6px)
   - **Impacto**: ~8-10px

#### D. Padding do Quadrado
   - Padding: `0.09rem` (≈1.44px) × 2 = ~2.88px total vertical

#### E. Gap do Grid
   - Gap: `2px` entre quadrados (não afeta altura individual)

### 3. **Altura Total Estimada Atual:**
   - Quadrado vazio: ~9px (min-height) + ~3px (padding) = ~12px
   - Quadrado com número: ~20px
   - Quadrado com 1 card: ~35px
   - Quadrado com 2 cards: ~50px

## Soluções para Reduzir 40% da Altura

### Estratégia: Reduzir TODOS os elementos proporcionalmente

1. **Reduzir min-height**: 9px → 5.4px (40% menos)
2. **Reduzir padding do quadrado**: 0.09rem → 0.054rem (40% menos)
3. **Reduzir font-size do número**: 0.875rem → 0.525rem (40% menos, ~8.4px)
4. **Reduzir padding dos cards**: 3px → 1.8px (40% menos)
5. **Reduzir gap entre cards**: 3px → 1.8px (40% menos)
6. **Reduzir font-size dos cards**: 0.625rem → 0.375rem (40% menos, ~6px)
7. **Reduzir border-left dos cards**: 3px → 1.8px (40% menos)
8. **Reduzir padding do badge**: 2px → 1.2px (40% menos)
9. **Adicionar line-height reduzido** nos elementos de texto

### Cálculo Final:
- Quadrado vazio: ~5.4px + ~1px (padding) = ~6.4px
- Quadrado com número: ~12px
- Quadrado com 1 card: ~20px
- Quadrado com 2 cards: ~28px

**Redução aproximada de 40-45% em todos os cenários**
