# 📤 Upload Final - Módulo Financeiro (Nome: "caixa")

## ⚠️ Problema Identificado

O InfinityFree está bloqueando:
- ❌ `financeiro/` → Bloqueado
- ❌ `fluxo-caixa/` → Bloqueado

**Solução:** Usar o nome **`caixa/`** (mais simples, provavelmente não bloqueado).

---

## 📁 Estrutura no Servidor (htdocs/)

```
htdocs/
├── .htaccess              ← SUBSTITUIR (já atualizado)
└── caixa/                 ← CRIAR esta pasta
    ├── index.html         ← ENVIAR
    └── config-api.js      ← ENVIAR
```

---

## ✅ Arquivos para Upload

### 1. `.htaccess-htdocs` → Renomear para `.htaccess`

**Origem:** `.htaccess-htdocs` (no seu computador)  
**Destino:** `htdocs/.htaccess` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** o arquivo existente

**Regras incluídas:**
- `/financeiro/` → redireciona para `/caixa/`
- `/fluxo-caixa/` → redireciona para `/caixa/`
- `/caixa/` → carrega o index.html

---

### 2. `caixa/index.html`

**Origem:** `caixa/index.html` (no seu computador)  
**Destino:** `htdocs/caixa/index.html` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** se já existir

---

### 3. `caixa/config-api.js`

**Origem:** `caixa/config-api.js` (no seu computador)  
**Destino:** `htdocs/caixa/config-api.js` (no servidor)  
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

### 4. Criar Pasta caixa/

1. Dentro de `htdocs/`, crie a pasta `caixa/`
2. **NÃO** use "financeiro" ou "fluxo-caixa" (serão bloqueados)

### 5. Enviar Arquivos

1. Entre na pasta `htdocs/caixa/`
2. Envie `index.html`
3. Envie `config-api.js`

---

## ✅ URLs que Funcionarão

Após o upload, estas URLs funcionarão:

1. **URL original (redireciona):**
   ```
   https://www.temvenda.com.br/financeiro/
   ```
   → Redireciona para `/caixa/`

2. **URL alternativa (redireciona):**
   ```
   https://www.temvenda.com.br/fluxo-caixa/
   ```
   → Redireciona para `/caixa/`

3. **URL final (direta):**
   ```
   https://www.temvenda.com.br/caixa/
   ```
   → Carrega diretamente ✅

4. **URL direta ao arquivo:**
   ```
   https://www.temvenda.com.br/caixa/index.html
   ```
   → Também funciona ✅

---

## 🔍 Verificação

### 1. Estrutura no Servidor

Confirme que existe:
- `htdocs/.htaccess` (atualizado)
- `htdocs/caixa/`
- `htdocs/caixa/index.html`
- `htdocs/caixa/config-api.js`

### 2. Testar URLs

1. **Teste 1:** `https://www.temvenda.com.br/caixa/`
   - Deve carregar diretamente ✅

2. **Teste 2:** `https://www.temvenda.com.br/caixa/index.html`
   - Deve carregar diretamente ✅

3. **Teste 3:** `https://www.temvenda.com.br/financeiro/`
   - Deve redirecionar para `/caixa/` ✅

---

## 📋 Checklist

- [ ] Backup do `.htaccess` atual feito
- [ ] `.htaccess-htdocs` enviado para `htdocs/.htaccess` (renomeado)
- [ ] Pasta `htdocs/caixa/` criada
- [ ] `htdocs/caixa/index.html` enviado
- [ ] `htdocs/caixa/config-api.js` enviado
- [ ] Permissões verificadas (644 para arquivos, 755 para pasta)
- [ ] Teste `/caixa/` funciona
- [ ] Teste `/caixa/index.html` funciona

---

## 💡 Por Que "caixa"?

- ✅ Nome simples e curto
- ✅ Provavelmente não bloqueado pelo InfinityFree
- ✅ Mantém a funcionalidade
- ✅ URLs antigas ainda funcionam (redirecionam)

---

## ⚠️ Importante

**NÃO** crie estas pastas no servidor (serão bloqueadas):
- ❌ `financeiro/`
- ❌ `fluxo-caixa/`

**USE:** `caixa/` ✅

---

## 🆘 Se "caixa" Também For Bloqueado

Se mesmo "caixa" for bloqueado, tente estes nomes alternativos:

1. `gestao/`
2. `sistema/`
3. `app/`
4. `admin-caixa/`
5. `dashboard/`

Basta renomear a pasta e atualizar o `.htaccess` com o novo nome.

