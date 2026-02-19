# 🔍 Diagnóstico CSS - Quadrados do Calendário

## Mudanças Aplicadas

1. ✅ Removido `padding: 0.5rem` da regra geral `.calendar-day`
2. ✅ Adicionado `!important` nas regras específicas de `min-height` e `padding`
3. ✅ Altura ajustada: 9px (aberta) / 20px (recolhida)

## Scripts de Diagnóstico para o Console

### 1. Verificar estilos aplicados nos quadrados:

```javascript
// Pegar um quadrado de dia como exemplo
const primeiroDia = document.querySelector('.calendar-day:not(.other-month)');
if (primeiroDia) {
    const styles = window.getComputedStyle(primeiroDia);
    console.log('=== ESTILOS DO QUADRADO ===');
    console.log('Min-height:', styles.minHeight);
    console.log('Height:', styles.height);
    console.log('Width:', styles.width);
    console.log('Padding:', styles.padding);
    console.log('Aspect-ratio:', styles.aspectRatio);
    console.log('Body class:', document.body.className);
    console.log('Sidebar collapsed?', document.body.classList.contains('sidebar-collapsed'));
}
```

### 2. Verificar todas as regras CSS aplicadas:

```javascript
const primeiroDia = document.querySelector('.calendar-day:not(.other-month)');
if (primeiroDia) {
    console.log('=== TODAS AS REGRAS CSS ===');
    const sheets = Array.from(document.styleSheets);
    sheets.forEach((sheet, index) => {
        try {
            const rules = Array.from(sheet.cssRules || sheet.rules || []);
            rules.forEach(rule => {
                if (rule.selectorText && rule.selectorText.includes('calendar-day')) {
                    console.log(`Sheet ${index}:`, rule.selectorText, rule.style.cssText);
                }
            });
        } catch (e) {
            console.log(`Sheet ${index}: Não acessível (CORS ou inline)`);
        }
    });
}
```

### 3. Forçar aplicação dos estilos (teste):

```javascript
// Forçar aplicação dos novos estilos
const todosDias = document.querySelectorAll('.calendar-day:not(.other-month)');
const isCollapsed = document.body.classList.contains('sidebar-collapsed');

todosDias.forEach(dia => {
    if (isCollapsed) {
        dia.style.minHeight = '20px';
        dia.style.padding = '0.15rem';
    } else {
        dia.style.minHeight = '9px';
        dia.style.padding = '0.09rem';
    }
});

console.log(`Aplicados estilos forçados em ${todosDias.length} quadrados`);
console.log('Sidebar collapsed?', isCollapsed);
```

### 4. Verificar cache do navegador:

```javascript
// Verificar se o arquivo CSS está sendo carregado
console.log('=== VERIFICAÇÃO DE CACHE ===');
console.log('Timestamp:', new Date().toISOString());
console.log('URL atual:', window.location.href);

// Forçar reload sem cache
// Pressione Ctrl+Shift+R (Windows/Linux) ou Cmd+Shift+R (Mac)
```

## Possíveis Problemas e Soluções

### Problema 1: Cache do Navegador
**Sintoma**: Mudanças não aparecem mesmo após atualizar
**Solução**: 
- Pressione `Ctrl+Shift+R` (Windows/Linux) ou `Cmd+Shift+R` (Mac)
- Ou abra DevTools (F12) → Network → Marque "Disable cache" → Recarregue

### Problema 2: Especificidade CSS
**Sintoma**: Estilos não são aplicados mesmo com `!important`
**Solução**: Execute o script 3 acima para forçar aplicação

### Problema 3: Aspect-ratio interferindo
**Sintoma**: Quadrados muito pequenos ou distorcidos
**Solução**: O `aspect-ratio: 1` força quadrados perfeitos. Com `min-height: 9px`, a largura também será 9px.

### Problema 4: JavaScript sobrescrevendo estilos
**Sintoma**: Estilos mudam após carregar o calendário
**Solução**: Verifique se há JavaScript aplicando estilos inline (execute script 1)

## Verificação Rápida

Execute no console:

```javascript
// Verificação rápida
const dia = document.querySelector('.calendar-day:not(.other-month)');
const collapsed = document.body.classList.contains('sidebar-collapsed');
console.log('Esperado:', collapsed ? '20px' : '9px');
console.log('Atual:', window.getComputedStyle(dia).minHeight);
console.log('Match?', window.getComputedStyle(dia).minHeight === (collapsed ? '20px' : '9px'));
```

## Próximos Passos

1. Abra o DevTools (F12)
2. Vá para a aba Console
3. Execute o script 1 para verificar estilos
4. Execute o script 3 se os estilos não estiverem corretos
5. Limpe o cache e recarregue a página
