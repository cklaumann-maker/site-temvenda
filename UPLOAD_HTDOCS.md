# 📤 Upload para htdocs/ - Módulo Financeiro

## 📍 Estrutura do Servidor

Seu servidor usa a pasta `htdocs/` como raiz do site.

**Estrutura:**
```
htdocs/
├── .htaccess              ← SUBSTITUIR aqui
├── index.html (ou index.php)
└── financeiro/            ← CRIAR aqui
    ├── index.html         ← ENVIAR aqui
    └── config-api.js      ← ENVIAR aqui
```

---

## ✅ Arquivos para Upload

### 1. `.htaccess-htdocs` → Renomear para `.htaccess`

**Origem:** `.htaccess-htdocs` (no seu computador)  
**Destino:** `htdocs/.htaccess` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** o arquivo existente

**⚠️ IMPORTANTE:**
- Fazer **BACKUP** do `.htaccess` atual antes de substituir
- O arquivo já está configurado para funcionar em `htdocs/`
- Não precisa alterar nada, só substituir

---

### 2. `financeiro/index.html`

**Origem:** `financeiro/index.html` (no seu computador)  
**Destino:** `htdocs/financeiro/index.html` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** se já existir

**Passos:**
1. Via FTP, navegue até `htdocs/`
2. Crie a pasta `financeiro/` (se não existir)
3. Envie o arquivo `index.html` para dentro de `financeiro/`

---

### 3. `financeiro/config-api.js`

**Origem:** `financeiro/config-api.js` (no seu computador)  
**Destino:** `htdocs/financeiro/config-api.js` (no servidor)  
**Ação:** ⚠️ **SUBSTITUIR** se já existir

**Passos:**
1. Via FTP, navegue até `htdocs/financeiro/`
2. Envie o arquivo `config-api.js`

---

## 🎯 Passo a Passo Completo

### 1. Conectar via FTP

1. Abra seu cliente FTP
2. Conecte ao servidor
3. Navegue até a pasta `htdocs/`

### 2. Fazer Backup do .htaccess

1. Baixe o arquivo `htdocs/.htaccess` atual
2. Salve como backup (ex: `.htaccess.backup-2024-12-16`)

### 3. Enviar Novo .htaccess

1. Envie o arquivo `.htaccess-htdocs` do seu computador
2. Para `htdocs/.htaccess` no servidor
3. ⚠️ **SUBSTITUIR** o arquivo existente

### 4. Criar Pasta financeiro/

1. Dentro de `htdocs/`, verifique se existe `financeiro/`
2. **Se não existir:** crie a pasta `financeiro/`
3. **Se já existir:** verifique o conteúdo

### 5. Enviar Arquivos do Financeiro

1. Entre na pasta `htdocs/financeiro/`
2. Envie `index.html`
3. Envie `config-api.js`

---

## ✅ Estrutura Final em htdocs/

```
htdocs/
├── .htaccess                    ← SUBSTITUÍDO
├── index.html (ou index.php)
├── (outros arquivos do site...)
└── financeiro/                  ← CRIADO
    ├── index.html               ← ENVIADO
    └── config-api.js            ← ENVIADO
```

---

## 🔍 Verificação

### 1. Verificar Estrutura via FTP

Confirme que existe:
- `htdocs/.htaccess`
- `htdocs/financeiro/`
- `htdocs/financeiro/index.html`
- `htdocs/financeiro/config-api.js`

### 2. Verificar Permissões

- `.htaccess`: **644**
- `financeiro/index.html`: **644**
- `financeiro/config-api.js`: **644**
- Pasta `financeiro/`: **755**

### 3. Testar

1. **Teste direto:**
   ```
   https://www.temvenda.com.br/financeiro/index.html
   ```

2. **Teste URL amigável:**
   ```
   https://www.temvenda.com.br/financeiro/
   ```

Ambos devem funcionar!

---

## ⚠️ Importante

### Não Precisa Alterar Nada no .htaccess

O arquivo `.htaccess-htdocs` que criei **já está configurado** para funcionar em `htdocs/`. As regras de rewrite funcionam relativas à raiz do site, então não precisa ajustar caminhos.

### A Regra do Financeiro

A linha adicionada:
```apache
RewriteRule ^financeiro/?$ /financeiro/index.html [L]
```

Funciona perfeitamente em `htdocs/` porque:
- `^financeiro/?$` = detecta a URL `/financeiro/`
- `/financeiro/index.html` = caminho relativo à raiz do site (htdocs/)
- `[L]` = última regra (para aqui)

---

## 📋 Checklist Final

- [ ] Backup do `.htaccess` atual feito
- [ ] `.htaccess-htdocs` enviado para `htdocs/.htaccess` (renomeado)
- [ ] Pasta `htdocs/financeiro/` criada/verificada
- [ ] `htdocs/financeiro/index.html` enviado
- [ ] `htdocs/financeiro/config-api.js` enviado
- [ ] Permissões verificadas
- [ ] Teste funcionando: `https://www.temvenda.com.br/financeiro/`

---

## 💡 Resumo

**Pasta de destino:** `htdocs/`  
**Arquivos:** 3 arquivos (`.htaccess` + 2 do financeiro)  
**Ação:** Substituir `.htaccess`, criar `financeiro/` e enviar os 2 arquivos

**Não precisa alterar nada** - o `.htaccess-htdocs` já está pronto para usar em `htdocs/`!

