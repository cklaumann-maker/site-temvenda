# 📐 Redução de 40% na Altura dos Quadrados do Calendário

## 🎯 Objetivo
Reduzir a altura dos quadrados de dias em 40% quando a sidebar está aberta (configuração normal), para que a tabela apareça mais acima e o calendário ocupe menos espaço vertical.

## 🔍 Problemas Identificados

### 1. **Aspect-Ratio Forçando Altura Igual à Largura**
- O `aspect-ratio: 1` estava forçando os quadrados a serem quadrados perfeitos
- Se a largura fosse 80px, a altura também seria 80px, ignorando `min-height`
- **Solução**: Remover `aspect-ratio` quando sidebar está aberta

### 2. **Conteúdo Interno Ocupando Espaço**
- Números dos dias, badges de semana e cards de atividades ocupavam espaço vertical
- **Solução**: Reduzir tamanhos de fonte e padding dos elementos internos

### 3. **Gap do Grid Aumentando Espaço Vertical**
- Gap de 2px entre linhas somava espaço desnecessário
- **Solução**: Reduzir gap para 1px quando sidebar está aberta

## ✅ Mudanças Aplicadas

### CSS - Quadrados de Dias

```css
body:not(.sidebar-collapsed) .calendar-day {
    height: auto !important;
    max-height: 35px !important; /* Altura máxima reduzida */
    min-height: 0 !important;
    padding: 0.25rem 0.15rem !important; /* Padding reduzido */
    aspect-ratio: unset !important; /* Remove aspect-ratio */
    width: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
```

### CSS - Números dos Dias

```css
body:not(.sidebar-collapsed) .day-number {
    font-size: 0.6875rem !important; /* Reduzido de 0.875rem para 0.6875rem */
    line-height: 1;
    margin-bottom: 2px;
}
```

### CSS - Badge de Semana

```css
body:not(.sidebar-collapsed) .week-badge {
    font-size: 0.5rem !important; /* Reduzido de 0.6rem */
    padding: 1px 3px !important;
    top: 1px !important;
    right: 1px !important;
}
```

### CSS - Gap do Grid

```css
body:not(.sidebar-collapsed) .calendar-grid {
    gap: 1px !important; /* Reduzido de 2px para 1px */
    row-gap: 1px !important; /* Gap vertical reduzido */
}
```

### JavaScript - Cards de Atividades

- **Padding reduzido**: `3px 5px` → `2px 3px` quando sidebar aberta
- **Font-size reduzido**: `0.625rem` → `0.5rem` quando sidebar aberta
- **Gap entre cards**: `3px` → `1px` quando sidebar aberta
- **Posicionamento**: `bottom/left/right: 2px` → `1px` quando sidebar aberta
- **Border-left**: `3px` → `2px` quando sidebar aberta

## 📊 Resultado Esperado

### Antes (Estimado)
- Altura dos quadrados: ~60-80px (baseado na largura devido ao aspect-ratio)
- Espaço vertical total do calendário: ~400-500px

### Depois
- Altura máxima dos quadrados: **35px** (redução de ~40-50%)
- Espaço vertical total do calendário: **~250-300px** (redução de ~40%)
- Tabela aparece **mais acima** na página

## 🧪 Como Testar

1. **Limpe o cache**: `Ctrl+Shift+R` ou `Cmd+Shift+R`
2. **Abra o DevTools**: `F12`
3. **Inspecione um quadrado**: Clique em um dia do calendário
4. **Verifique**:
   - `max-height` deve ser `35px`
   - `aspect-ratio` deve estar como `unset` ou não aparecer
   - `padding` deve ser `0.25rem 0.15rem`
   - `gap` do grid deve ser `1px`

## 🔧 Ajustes Adicionais Possíveis

Se ainda precisar reduzir mais:

1. **Reduzir `max-height`**: De `35px` para `30px` ou `25px`
2. **Reduzir padding**: De `0.25rem 0.15rem` para `0.2rem 0.1rem`
3. **Reduzir font-size dos números**: De `0.6875rem` para `0.625rem`
4. **Ocultar cards de atividades**: Quando sidebar aberta, mostrar apenas números

## 📝 Notas

- As mudanças **só afetam quando a sidebar está aberta**
- Quando a sidebar está recolhida, mantém-se o comportamento original (20px min-height)
- O `aspect-ratio: unset` permite que os quadrados sejam mais baixos que largos
- O `overflow: hidden` garante que conteúdo não ultrapasse os limites
