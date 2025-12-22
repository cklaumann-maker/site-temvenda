# 📤 Guia Completo de Upload - Módulo Financeiro

## 📋 Arquivos para Upload

### ✅ Arquivos Obrigatórios (Atualizados em 16/12/2024)

Estes arquivos foram atualizados hoje e **DEVEM** ser enviados:

1. **`financeiro/index.html`** (83 KB)
   - Data: 16/12/2024 09:10
   - ✅ **ENVIAR** - Versão atualizada

2. **`financeiro/config-api.js`** (521 bytes)
   - Data: 16/12/2024 10:23
   - ✅ **ENVIAR** - Já configurado com URL do Render

3. **`.htaccess`** (atualizado)
   - ✅ **ENVIAR** - Contém regra para `/financeiro/`

---

## 📁 Estrutura no Servidor FTP

### Pasta de Destino: **RAIZ do site**

Normalmente é uma destas pastas:
- `public_html/`
- `htdocs/`
- `www/`
- Ou a pasta raiz que o seu FTP mostra

### Estrutura Final:

```
/ (raiz do site)
├── .htaccess                    ← SUBSTITUIR (arquivo atualizado)
├── financeiro/                  ← CRIAR esta pasta (se não existir)
│   ├── index.html               ← ENVIAR
│   └── config-api.js            ← ENVIAR
└── (outros arquivos do site...)
```

---

## 🚀 Passo a Passo de Upload

### 1. Preparar os Arquivos

Você tem 3 arquivos para enviar:

**Arquivo 1:** `.htaccess-financeiro` → renomear para `.htaccess`
**Arquivo 2:** `financeiro/index.html`
**Arquivo 3:** `financeiro/config-api.js`

---

### 2. Conectar via FTP

1. Abra seu cliente FTP (FileZilla, Cyberduck, etc.)
2. Conecte ao servidor do temvenda.com.br
3. Navegue até a **raiz do site** (geralmente `public_html/` ou `htdocs/`)

---

### 3. Upload do .htaccess

**⚠️ IMPORTANTE:** Este arquivo já existe no servidor. Você vai **SUBSTITUIR** ele.

1. **Fazer backup primeiro** (opcional, mas recomendado):
   - Baixe o `.htaccess` atual do servidor
   - Salve como backup (ex: `.htaccess.backup`)

2. **Enviar o novo .htaccess:**
   - Local: `.htaccess-financeiro` (no seu computador)
   - Servidor: `.htaccess` (na raiz)
   - ⚠️ **SUBSTITUIR** o arquivo existente

---

### 4. Criar/Certificar Pasta financeiro/

1. Na raiz do servidor, verifique se existe a pasta `financeiro/`
2. **Se não existir:** crie a pasta `financeiro/`
3. **Se já existir:** verifique o conteúdo

---

### 5. Upload dos Arquivos do Financeiro

**Dentro da pasta `financeiro/`**, envie:

1. **`index.html`**
   - Origem: `financeiro/index.html` (seu computador)
   - Destino: `/financeiro/index.html` (servidor)
   - ⚠️ Se já existir, **SUBSTITUIR**

2. **`config-api.js`**
   - Origem: `financeiro/config-api.js` (seu computador)
   - Destino: `/financeiro/config-api.js` (servidor)
   - ⚠️ Se já existir, **SUBSTITUIR**

---

## ✅ Verificação Pós-Upload

### 1. Verificar Estrutura

Via FTP, confirme que existe:
```
/
├── .htaccess
└── financeiro/
    ├── index.html
    └── config-api.js
```

### 2. Verificar Permissões

- `.htaccess`: **644** (rw-r--r--)
- `financeiro/index.html`: **644** (rw-r--r--)
- `financeiro/config-api.js`: **644** (rw-r--r--)
- Pasta `financeiro/`: **755** (rwxr-xr-x)

### 3. Testar Acesso

1. **Teste direto:**
   ```
   https://www.temvenda.com.br/financeiro/index.html
   ```
   - Deve carregar a página de login

2. **Teste URL amigável:**
   ```
   https://www.temvenda.com.br/financeiro/
   ```
   - Deve carregar a mesma página

---

## 📝 Resumo dos Arquivos

| Arquivo | Origem | Destino | Ação |
|---------|--------|---------|------|
| `.htaccess-financeiro` | Seu PC | `/` (raiz) → renomear para `.htaccess` | **SUBSTITUIR** |
| `financeiro/index.html` | Seu PC | `/financeiro/index.html` | **SUBSTITUIR** |
| `financeiro/config-api.js` | Seu PC | `/financeiro/config-api.js` | **SUBSTITUIR** |

---

## ⚠️ Importante

### Arquivos Atualizados em 15/12

Se você viu arquivos com data de 15/12, verifique:

- **Se são arquivos do financeiro:** ✅ **SIM, envie** (são as versões atualizadas)
- **Se são outros arquivos do site:** Verifique se são atualizações importantes antes de enviar

### Backup Recomendado

Antes de substituir o `.htaccess`:
1. Baixe o `.htaccess` atual do servidor
2. Salve como backup
3. Depois envie o novo

---

## 🎯 Checklist Final

- [ ] Backup do `.htaccess` atual feito
- [ ] `.htaccess-financeiro` enviado e renomeado para `.htaccess` na raiz
- [ ] Pasta `financeiro/` criada/verificada na raiz
- [ ] `financeiro/index.html` enviado
- [ ] `financeiro/config-api.js` enviado
- [ ] Permissões verificadas (644 para arquivos, 755 para pasta)
- [ ] Teste direto funcionando: `/financeiro/index.html`
- [ ] Teste URL amigável funcionando: `/financeiro/`

---

## 🆘 Se Algo Der Errado

1. **Restaurar .htaccess:**
   - Use o backup que você fez
   - Ou use o `.htaccess-root` original

2. **Verificar logs do servidor** (se tiver acesso)

3. **Testar arquivo por arquivo:**
   - Envie um de cada vez
   - Teste após cada upload

---

## 💡 Dica

Se você não tem certeza sobre qual é a raiz do site:
1. Procure por arquivos como `index.html` ou `index.php`
2. Esses arquivos geralmente estão na raiz
3. É nessa mesma pasta que você deve colocar o `.htaccess` e criar a pasta `financeiro/`

