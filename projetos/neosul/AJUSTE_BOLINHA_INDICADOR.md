# 🔵 Ajuste da Bolinha Indicadora e Altura dos Retângulos

## 🎯 O Que É a Bolinha?

A bolinha cinza (ou colorida) é um **indicador de status do planejamento semanal**. Ela mostra o status da semana à qual o dia pertence:
- **Verde** (`planned`): Semana concluída
- **Amarelo** (`in-progress`): Semana em andamento
- **Vermelho** (`delayed`): Semana atrasada
- **Cinza** (`not-planned`): Semana não planejada

## ✅ Mudanças Aplicadas

### 1. Bolinha Movida para o Lado Direito do Número

**Antes**: A bolinha aparecia abaixo do número do dia, dentro de um container `.day-indicators` com `margin-top: 4px`.

**Depois**: A bolinha agora aparece **ao lado direito do número**, dentro do mesmo container do número do dia.

**Código JavaScript**:
```javascript
// Número do dia agora é um container flex
const dayNumber = document.createElement('div');
dayNumber.style.cssText = `
    display: flex;
    align-items: center;
    justify-content: space-between; /* Número à esquerda, bolinha à direita */
`;

// Bolinha adicionada diretamente ao container do número
dot.style.cssText = `
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-left: auto; /* Empurra para a direita */
`;
dayNumber.appendChild(dot);
```

**CSS**:
```css
.day-indicators {
    /* Removido - não é mais necessário */
}

/* A bolinha agora é posicionada via flexbox no day-number */
.day-number {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
```

### 2. Altura dos Retângulos Aumentada em 5%

**Antes**:
- Sidebar aberta: `min-height: 70px`
- Sidebar recolhida: `min-height: 80px`

**Depois**:
- Sidebar aberta: `min-height: 73.5px` (70px × 1.05 = 73.5px)
- Sidebar recolhida: `min-height: 84px` (80px × 1.05 = 84px)

**Código CSS**:
```css
body:not(.sidebar-collapsed) .calendar-day {
    min-height: 73.5px !important; /* +5% */
}

body.sidebar-collapsed .calendar-day {
    min-height: 84px !important; /* +5% */
}
```

## 📊 Resultado Esperado

- ✅ **Bolinha ao lado direito**: A bolinha aparece à direita do número do dia
- ✅ **Altura aumentada**: Retângulos têm 5% mais altura
- ✅ **Melhor organização**: Número e indicador ficam na mesma linha
- ✅ **Mais espaço**: Altura adicional permite melhor visualização dos cards

## 🧪 Como Testar

1. **Limpe o cache**: `Ctrl+Shift+R` ou `Cmd+Shift+R`
2. **Recarregue a página**
3. **Verifique**:
   - A bolinha aparece ao lado direito do número (não abaixo)
   - Os retângulos têm altura ligeiramente maior
   - O layout está mais organizado

## 📝 Notas Técnicas

- A bolinha é criada dinamicamente apenas quando há planejamento semanal associado ao dia
- O uso de `flexbox` com `justify-content: space-between` garante que o número fique à esquerda e a bolinha à direita
- `margin-left: auto` na bolinha garante que ela seja empurrada para a direita
- A altura de 73.5px e 84px mantém o formato retangular (mais largo que alto)
