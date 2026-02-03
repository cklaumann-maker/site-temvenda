# 📤 Guia Completo de Upload - Ana Cristina Cardoso

## 📋 Arquivos que você precisa subir

### 1. Arquivo HTML Principal
- **Arquivo**: `index.html`
- **Caminho no FTP**: `projetos/ana-cristina-cardoso/index.html`
- **Obrigatório**: ✅ Sim

### 2. Logo da Ana Cristina Cardoso
- **Nome do arquivo**: `logo.png`
- **Caminho no FTP**: `projetos/ana-cristina-cardoso/logo.png`
- **Obrigatório**: ⚠️ Opcional (mas recomendado)
- **Formato**: PNG (com fundo transparente, se possível)
- **Tamanho recomendado**: Altura de aproximadamente 50-100px

---

## 🎨 Como renomear a logo

### Passo a passo:

1. **Localize sua imagem de logo** (pode estar em qualquer formato: .jpg, .png, .svg, etc.)

2. **Renomeie o arquivo para**: `logo.png`
   - Se sua imagem for `.jpg` ou outro formato, você pode:
     - Renomear para `logo.png` (o navegador ainda vai carregar)
     - **OU** converter para PNG usando um editor de imagens

3. **Coloque o arquivo na mesma pasta** que o `index.html`:
   ```
   projetos/ana-cristina-cardoso/
   ├── index.html
   └── logo.png  ← Sua logo aqui
   ```

---

## 📁 Estrutura completa no servidor FTP

```
[raiz do site]/
└── projetos/
    ├── index.html  ← Página de listagem de projetos (também atualizada)
    └── ana-cristina-cardoso/
        ├── index.html  ← Landing page da Ana Cristina
        └── logo.png    ← Logo da Ana Cristina
```

---

## 🚀 Ordem de upload sugerida

### Passo 1: Criar a pasta
1. Acesse seu FTP
2. Navegue até a pasta `projetos/`
3. Crie a pasta `ana-cristina-cardoso` (se não existir)

### Passo 2: Subir o HTML
1. Faça upload do arquivo `index.html` para `projetos/ana-cristina-cardoso/index.html`

### Passo 3: Preparar e subir a logo
1. Renomeie sua imagem para `logo.png`
2. Faça upload para `projetos/ana-cristina-cardoso/logo.png`

### Passo 4: Atualizar página de projetos (se necessário)
1. Se ainda não subiu, faça upload do arquivo `projetos/index.html` atualizado

---

## ✅ Verificação após upload

Após fazer o upload, acesse:
- **Landing page**: `https://seusite.com/projetos/ana-cristina-cardoso/`
- **Página de projetos**: `https://seusite.com/projetos/`

A logo deve aparecer no header da página. Se não aparecer:
- Verifique se o nome do arquivo está exatamente como `logo.png` (minúsculas)
- Verifique se está na mesma pasta do `index.html`
- O código já tem tratamento de erro - se a logo não existir, ela será ocultada automaticamente

---

## 📝 Resumo rápido

| Item | Nome do Arquivo | Caminho no FTP |
|------|----------------|----------------|
| Landing Page | `index.html` | `projetos/ana-cristina-cardoso/index.html` |
| Logo | `logo.png` | `projetos/ana-cristina-cardoso/logo.png` |
| Listagem | `index.html` | `projetos/index.html` |

---

## 💡 Dica importante

- O código HTML está configurado para procurar `logo.png` na mesma pasta
- Se você usar outro nome ou formato, precisará editar o HTML na linha 853:
  ```html
  <img src="logo.png" alt="Ana Cristina Cardoso Logo" ...>
  ```
  E alterar `logo.png` para o nome do seu arquivo.
