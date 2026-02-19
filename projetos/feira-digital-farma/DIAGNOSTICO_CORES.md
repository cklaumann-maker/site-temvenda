# 🎨 Diagnóstico de Cores - Feira Digital Farma

## 📊 Análise Atual

### Cores Principais Identificadas:

1. **Fundo Preto** ✅
   - `--fdf-black: #000000` (preto puro)
   - `--fdf-black-soft: #0a0a0a` (preto suave)
   - `--fdf-gray-dark: #1a1a1a` (cinza escuro)

2. **Verde Principal** ✅
   - `--fdf-green: #5ee100` (verde neon brilhante)
   - `--fdf-green-dark: #4bc800` (verde escuro)
   - Uso: CTAs, destaques, bordas

3. **Azul** ⚠️
   - `--fdf-blue: #0066CC` (azul médio)
   - `--fdf-blue-dark: #0052A3` (azul escuro)
   - **Problema**: Pouco usado, pode competir com verde

4. **Laranja** ⚠️
   - `--fdf-orange: #FFB84D` (laranja claro)
   - **Problema**: Muito claro, baixo contraste no fundo preto

5. **Glassmorphism** ✅
   - `--fdf-glass-bg: rgba(255, 255, 255, 0.05)` (muito transparente)
   - `--fdf-glass-border: rgba(255, 255, 255, 0.1)` (borda sutil)

## 🔍 Problemas Identificados:

### 1. **Contraste e Legibilidade**
   - ❌ Laranja (#FFB84D) muito claro no preto - baixa legibilidade
   - ❌ Alguns textos brancos podem estar muito claros em alguns backgrounds
   - ⚠️ Glassmorphism muito sutil (0.05) - cards podem parecer "vazios"

### 2. **Hierarquia Visual**
   - ⚠️ Verde e azul competindo por atenção
   - ⚠️ Falta de cor secundária consistente
   - ✅ Verde funciona bem como cor primária

### 3. **Consistência**
   - ⚠️ Azul pouco utilizado (apenas em alguns gradientes)
   - ⚠️ Laranja usado apenas para status/badges
   - ✅ Verde bem aplicado como cor principal

### 4. **Acessibilidade**
   - ⚠️ Contraste verde/preto pode ser melhorado em alguns casos
   - ⚠️ Laranja precisa de ajuste para melhor contraste

## 💡 Sugestões de Melhoria:

### Opção 1: Refinamento Sutil (Recomendado)
**Mantém identidade, melhora contraste**

- ✅ Manter verde #5ee100 como primária
- ✅ Ajustar laranja para tom mais escuro: `#FF9500` (melhor contraste)
- ✅ Usar azul apenas em acentos sutis (não competir com verde)
- ✅ Aumentar opacidade do glassmorphism: `rgba(255, 255, 255, 0.08)`
- ✅ Adicionar tom de cinza intermediário para textos secundários

### Opção 2: Paleta Mais Restrita
**Foco total no verde, minimalista**

- ✅ Verde #5ee100 como única cor de destaque
- ✅ Remover azul completamente
- ✅ Usar apenas tons de cinza + branco + verde
- ✅ Laranja apenas para alertas/status críticos

### Opção 3: Paleta Expandida (Mais Corporativa)
**Adiciona cor terciária para mais profundidade**

- ✅ Verde #5ee100 (primária)
- ✅ Azul #0066CC (secundária - para links e informações)
- ✅ Roxo/Violeta suave para elementos especiais
- ✅ Laranja ajustado para status

## 🎯 Recomendação Final:

**Opção 1 com ajustes específicos:**

1. **Verde**: Manter #5ee100 ✅
2. **Laranja**: Mudar para `#FF9500` (mais escuro, melhor contraste)
3. **Azul**: Usar apenas em gradientes sutis ou remover
4. **Glassmorphism**: Aumentar para `rgba(255, 255, 255, 0.08)`
5. **Textos**: 
   - Primário: `rgba(255, 255, 255, 0.95)`
   - Secundário: `rgba(255, 255, 255, 0.7)`
   - Terciário: `rgba(255, 255, 255, 0.5)`

## 📐 Tamanhos dos Cards:

**Atual:**
- Padding: 48px
- Min-width grid: 320px

**Sugestão:**
- Padding: 32px (reduzir 33%)
- Min-width grid: 280px (mais compacto)
- Border-radius: 12px (mais sutil)
