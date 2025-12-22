# 📤 Arquivos para Enviar via FTP - Módulo Financeiro

## 📋 Arquivos Necessários

Para o módulo financeiro funcionar em `www.temvenda.com.br/financeiro`, você precisa enviar **apenas 2 arquivos**:

### ✅ Arquivos Obrigatórios

1. **`financeiro/index.html`**
   - Arquivo principal do módulo financeiro
   - Contém todo o HTML, CSS e JavaScript inline
   - Não precisa de arquivos externos (Chart.js é carregado via CDN)

2. **`financeiro/config-api.js`**
   - Arquivo de configuração da URL da API
   - **IMPORTANTE**: Atualizar antes de enviar (ver abaixo)

---

## 🔧 ANTES de Enviar - Atualizar config-api.js

**⚠️ CRÍTICO**: Você precisa atualizar o arquivo `config-api.js` com a URL do seu backend no Render.

### Passo 1: Obter URL do Backend no Render

Após fazer o deploy do backend no Render, você receberá uma URL como:
- `https://temvenda-finance-api.onrender.com`
- Ou outra URL que o Render gerar

### Passo 2: Editar config-api.js

Abra o arquivo `financeiro/config-api.js` e altere a linha 5:

**ANTES (desenvolvimento):**
```javascript
window.FINANCE_API_URL = "http://localhost:8001";
```

**DEPOIS (produção):**
```javascript
window.FINANCE_API_URL = "https://sua-api-backend.onrender.com";
```

**Exemplo real:**
```javascript
window.FINANCE_API_URL = "https://temvenda-finance-api.onrender.com";
```

---

## 📁 Estrutura no Servidor

No servidor FTP, os arquivos devem ficar assim:

```
/
├── financeiro/
│   ├── index.html          ← Enviar este arquivo
│   └── config-api.js       ← Enviar este arquivo (já atualizado)
```

**Caminho completo no servidor:**
- `/financeiro/index.html`
- `/financeiro/config-api.js`

---

## 🚀 Passo a Passo para Enviar

### 1. Preparar os Arquivos

```bash
# 1. Editar config-api.js com a URL do Render
# 2. Verificar que os arquivos estão prontos
```

### 2. Conectar via FTP

Use seu cliente FTP favorito (FileZilla, Cyberduck, etc.) e conecte ao servidor do temvenda.com.br

### 3. Navegar até a Raiz do Site

Normalmente é a pasta `public_html/` ou `www/` ou `htdocs/`

### 4. Criar/Certificar que Existe a Pasta `financeiro/`

Se não existir, crie a pasta `financeiro/` na raiz do site

### 5. Enviar os Arquivos

- Arraste `index.html` para dentro de `/financeiro/`
- Arraste `config-api.js` para dentro de `/financeiro/`

### 6. Verificar Permissões

Certifique-se de que os arquivos têm permissão de leitura:
- `index.html`: 644 (rw-r--r--)
- `config-api.js`: 644 (rw-r--r--)

---

## ✅ Verificação Pós-Deploy

Após enviar os arquivos, teste:

1. **Acessar a URL:**
   ```
   https://www.temvenda.com.br/financeiro/
   ```

2. **Verificar se carrega:**
   - Deve aparecer a tela de login
   - Não deve dar erro 404

3. **Testar login:**
   - Use a senha configurada em `APP_PASSWORD` no Render
   - Deve fazer login com sucesso

4. **Verificar Console (F12):**
   - Abrir DevTools (F12)
   - Ir na aba "Console"
   - Não deve ter erros de CORS ou 404

---

## 🔍 Troubleshooting

### Erro 404 ao acessar /financeiro/

**Causa:** Arquivos não foram enviados ou estão no lugar errado

**Solução:**
- Verificar se `index.html` está em `/financeiro/index.html`
- Verificar se o servidor suporta subpastas
- Verificar se há `.htaccess` bloqueando

### Erro de CORS no Console

**Causa:** Backend não está configurado para aceitar requisições do domínio

**Solução:**
- Verificar se `FRONTEND_ORIGINS` no Render inclui `https://www.temvenda.com.br`
- Verificar se a URL em `config-api.js` está correta

### Erro 404 nas Requisições da API

**Causa:** URL da API incorreta ou backend não está rodando

**Solução:**
- Verificar se a URL em `config-api.js` está correta
- Verificar se o backend está rodando no Render
- Testar a URL diretamente: `https://sua-api.onrender.com/health`

---

## 📝 Checklist Final

Antes de considerar o deploy completo:

- [ ] Backend deployado no Render e funcionando
- [ ] URL do backend anotada
- [ ] `config-api.js` atualizado com a URL do Render
- [ ] Pasta `financeiro/` criada no servidor FTP
- [ ] `index.html` enviado para `/financeiro/`
- [ ] `config-api.js` enviado para `/financeiro/`
- [ ] Permissões dos arquivos verificadas (644)
- [ ] Teste de acesso: `https://www.temvenda.com.br/financeiro/`
- [ ] Teste de login funcionando
- [ ] Console do navegador sem erros

---

## 🎯 Resumo Rápido

**Arquivos para enviar:**
1. `financeiro/index.html`
2. `financeiro/config-api.js` (já atualizado com URL do Render)

**Onde enviar:**
- Para `/financeiro/` na raiz do servidor FTP

**URL final:**
- `https://www.temvenda.com.br/financeiro/`

---

## 💡 Dica

Se você usar um script de deploy automatizado, pode adicionar estes arquivos à lista de arquivos para upload.

