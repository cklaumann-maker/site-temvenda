# 🔍 Verificação Manual dos Estilos (Sem Colar Código)

## Método 1: Inspecionar Elemento (Mais Fácil)

1. **Abra o DevTools**: Pressione `F12` ou `Ctrl+Shift+I` (Windows/Linux) ou `Cmd+Option+I` (Mac)

2. **Clique no ícone de inspeção** (canto superior esquerdo do DevTools) ou pressione `Ctrl+Shift+C`

3. **Clique em um quadrado do calendário** (qualquer dia do mês atual)

4. **No painel direito (Styles)**, procure por:
   - `body:not(.sidebar-collapsed) .calendar-day` ou
   - `body.sidebar-collapsed .calendar-day`

5. **Verifique os valores**:
   - `min-height` deve ser `9px` (sidebar aberta) ou `20px` (sidebar recolhida)
   - `padding` deve ser `0.09rem` (sidebar aberta) ou `0.15rem` (sidebar recolhida)

6. **Se os valores estiverem diferentes**:
   - Procure por `.calendar-day` (sem o `body:not(...)`)
   - Veja se há um `padding: 0.5rem` ou `min-height` diferente
   - Se houver, clique no ícone de "desabilitar" (linha riscada) ao lado dessa regra

## Método 2: Verificar no Computed (Valores Finais)

1. **Inspecione um quadrado** (passos 1-3 acima)

2. **Clique na aba "Computed"** no painel direito

3. **Procure por**:
   - `min-height` → deve mostrar `9px` ou `20px`
   - `height` → deve mostrar o valor calculado
   - `padding` → deve mostrar valores pequenos

## Método 3: Verificar se o Body tem a Classe Correta

1. **No DevTools**, vá para a aba "Elements" (ou "Inspector")

2. **Expanda o `<body>`** no HTML

3. **Verifique a classe**:
   - Se a sidebar estiver **aberta**: `body` não deve ter a classe `sidebar-collapsed`
   - Se a sidebar estiver **recolhida**: `body` deve ter a classe `sidebar-collapsed`

4. **Se a classe estiver errada**:
   - Clique no botão de toggle da sidebar no calendário
   - Ou adicione/remova manualmente a classe `sidebar-collapsed` no `<body>`

## Método 4: Limpar Cache e Recarregar

1. **Com o DevTools aberto**, vá para a aba "Network"

2. **Marque a opção "Disable cache"** (no topo)

3. **Mantenha o DevTools aberto** e pressione `F5` para recarregar

4. **Ou feche e reabra o navegador completamente**

## O Que Procurar

### ✅ CORRETO (Sidebar Aberta):
```
body:not(.sidebar-collapsed) .calendar-day {
    min-height: 9px !important;
    padding: 0.09rem !important;
}
```

### ✅ CORRETO (Sidebar Recolhida):
```
body.sidebar-collapsed .calendar-day {
    min-height: 20px !important;
    padding: 0.15rem !important;
}
```

### ❌ INCORRETO (Se aparecer):
```
.calendar-day {
    padding: 0.5rem;  ← Este não deve aparecer ou deve estar riscado
}
```

## Se Ainda Não Funcionar

1. **Verifique se o arquivo foi salvo**: O arquivo `index.html` deve ter as mudanças

2. **Verifique se está no arquivo correto**: Certifique-se de estar acessando `http://localhost:3000/projetos/neosul/index.html`

3. **Tente em modo anônimo**: Abra uma janela anônima/privada e acesse a URL

4. **Verifique o servidor**: Certifique-se de que o servidor local está rodando na porta 3000
