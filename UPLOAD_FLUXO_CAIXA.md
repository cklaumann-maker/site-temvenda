# 📤 Upload - Módulo Financeiro (Renomeado para fluxo-caixa)

## ⚠️ Problema Identificado

O InfinityFree está **bloqueando a palavra "financeiro"** e redirecionando para página de erro.

**Solução:** Renomear a pasta para `fluxo-caixa/` (não é bloqueado).

---

## 📁 Estrutura no Servidor (htdocs/)

```
htdocs/
├── .htaccess              ← SUBSTITUIR (já atualizado)
└── fluxo-caixa/           ← CRIAR esta pasta (NÃO usar "financeiro")
    ├── index.html         ← ENVIAR
    └── config-api.js      ← ENVIAR
```

---

## ✅ Arquivos para Upload

### 1. `.htaccess-htdocs` → Renomear para `.htaccess`

**Origem:** `.htaccess-htdocs` (no seu computador)  
**Destino:** `htdocs/.htaccess` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** o arquivo existente

**O que foi alterado:**
- Adicionada regra para `/financeiro/` → redireciona para `/fluxo-caixa/`
- Adicionada regra para `/fluxo-caixa/` → carrega o index.html

---

### 2. `fluxo-caixa/index.html`

**Origem:** `fluxo-caixa/index.html` (no seu computador)  
**Destino:** `htdocs/fluxo-caixa/index.html` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** se já existir

---

### 3. `fluxo-caixa/config-api.js`

**Origem:** `fluxo-caixa/config-api.js` (no seu computador)  
**Destino:** `htdocs/fluxo-caixa/config-api.js` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** se já existir

---

## 🚀 Passo a Passo

### 1. Via FTP, navegue até `htdocs/`

### 2. Fazer Backup do .htaccess

1. Baixe o `htdocs/.htaccess` atual
2. Salve como backup

### 3. Enviar Novo .htaccess

1. Envie `.htaccess-htdocs` do seu computador
2. Para `htdocs/.htaccess` no servidor
3. ⚠️ **SUBSTITUIR** o arquivo existente

### 4. Criar Pasta fluxo-caixa/

1. Dentro de `htdocs/`, crie a pasta `fluxo-caixa/`
2. **NÃO** use o nome "financeiro" (será bloqueado)

### 5. Enviar Arquivos

1. Entre na pasta `htdocs/fluxo-caixa/`
2. Envie `index.html`
3. Envie `config-api.js`

---

## ✅ URLs que Funcionarão

Após o upload, estas URLs funcionarão:

1. **URL original (redireciona):**
   ```
   https://www.temvenda.com.br/financeiro/
   ```
   → Redireciona automaticamente para `/fluxo-caixa/`

2. **URL nova (direta):**
   ```
   https://www.temvenda.com.br/fluxo-caixa/
   ```
   → Carrega diretamente

3. **URL direta ao arquivo:**
   ```
   https://www.temvenda.com.br/fluxo-caixa/index.html
   ```
   → Também funciona

---

## 🔍 Verificação

### 1. Estrutura no Servidor

Confirme que existe:
- `htdocs/.htaccess` (atualizado)
- `htdocs/fluxo-caixa/`
- `htdocs/fluxo-caixa/index.html`
- `htdocs/fluxo-caixa/config-api.js`

### 2. Testar URLs

1. **Teste 1:** `https://www.temvenda.com.br/financeiro/`
   - Deve redirecionar para `/fluxo-caixa/` e carregar

2. **Teste 2:** `https://www.temvenda.com.br/fluxo-caixa/`
   - Deve carregar diretamente

3. **Teste 3:** `https://www.temvenda.com.br/fluxo-caixa/index.html`
   - Deve carregar diretamente

---

## 📋 Checklist

- [ ] Backup do `.htaccess` atual feito
- [ ] `.htaccess-htdocs` enviado para `htdocs/.htaccess` (renomeado)
- [ ] Pasta `htdocs/fluxo-caixa/` criada (NÃO usar "financeiro")
- [ ] `htdocs/fluxo-caixa/index.html` enviado
- [ ] `htdocs/fluxo-caixa/config-api.js` enviado
- [ ] Permissões verificadas (644 para arquivos, 755 para pasta)
- [ ] Teste `/financeiro/` redireciona para `/fluxo-caixa/`
- [ ] Teste `/fluxo-caixa/` funciona

---

## 💡 Por Que "fluxo-caixa"?

- ✅ Não é bloqueado pelo InfinityFree
- ✅ Nome descritivo e claro
- ✅ Mantém a funcionalidade
- ✅ URL `/financeiro/` ainda funciona (redireciona)

---

## ⚠️ Importante

**NÃO** crie a pasta `financeiro/` no servidor - ela será bloqueada pelo InfinityFree.

Use **`fluxo-caixa/`** em vez disso.

