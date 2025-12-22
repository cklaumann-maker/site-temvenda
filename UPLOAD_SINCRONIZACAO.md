# 📤 Upload FTP - Atualização de Sincronização

## ✅ Arquivos que Precisam ser Enviados

### 1. `caixa/index.html` ⚠️ **IMPORTANTE**

**O que mudou:**
- ✅ Nova aba "🔄 Sincronização"
- ✅ Função `loadSyncInfo()` para mostrar status de sincronização
- ✅ Integração com novo endpoint `/api/months/{monthCode}/sync-info`

**Ação:**
- **Origem:** `caixa/index.html` (no seu computador)
- **Destino:** `htdocs/caixa/index.html` (no servidor InfinityFree)
- **Ação:** ⚠️ **SUBSTITUIR** o arquivo existente

---

### 2. `caixa/config-api.js` (Opcional - se mudou)

**Verificar se precisa atualizar:**
- Se você mudou a URL da API, precisa atualizar
- Se está usando produção (`https://temvenda-finance-api.onrender.com`), está OK

**Ação:**
- **Origem:** `caixa/config-api.js` (no seu computador)
- **Destino:** `htdocs/caixa/config-api.js` (no servidor)
- **Ação:** ⚠️ **SUBSTITUIR** apenas se mudou

---

## 📋 Passo a Passo

### 1. Conectar via FTP

Use seu cliente FTP favorito (FileZilla, Cyberduck, etc.) e conecte ao servidor InfinityFree.

### 2. Navegar até `htdocs/`

Certifique-se de estar no diretório correto: `htdocs/`

### 3. Navegar até `htdocs/caixa/`

Se a pasta `caixa/` não existir, crie-a.

### 4. Fazer Upload

**Arquivo 1: `index.html`**
- Arraste `caixa/index.html` do seu computador
- Solte em `htdocs/caixa/`
- Confirme substituição se solicitado

**Arquivo 2: `config-api.js` (se necessário)**
- Arraste `caixa/config-api.js` do seu computador
- Solte em `htdocs/caixa/`
- Confirme substituição se solicitado

---

## ✅ Verificação

Após o upload:

1. Acesse: `https://www.temvenda.com.br/caixa/`
2. Faça login
3. Verifique se aparece a nova aba **"🔄 Sincronização"**
4. Selecione um mês e clique em "🔄 Atualizar Fluxo"
5. Vá na aba "🔄 Sincronização"
6. Deve mostrar:
   - Status da sincronização
   - Data/hora da última atualização
   - Estatísticas de importação

---

## ⚠️ Importante

### Backend (Render) - NÃO precisa de FTP

O backend está no Render e será atualizado automaticamente via Git. Você só precisa:
- ✅ Executar a migration no Supabase (SQL)
- ✅ Aguardar o deploy no Render (automático)

### Frontend (InfinityFree) - Precisa de FTP

O frontend precisa ser enviado manualmente via FTP porque:
- O InfinityFree não tem integração com Git
- Os arquivos HTML/JS precisam estar no servidor

---

## 🆘 Se Algo Não Funcionar

### Problema: Aba "Sincronização" não aparece

**Solução:**
1. Verifique se o arquivo foi enviado corretamente
2. Limpe o cache do navegador (Ctrl+Shift+R ou Cmd+Shift+R)
3. Verifique o console do navegador (F12) para erros

### Problema: Erro ao carregar informações de sincronização

**Solução:**
1. Verifique se a migration foi executada no Supabase
2. Verifique se o backend no Render foi atualizado
3. Verifique os logs do backend no Render

---

## 📋 Checklist

- [ ] Conectado via FTP ao servidor InfinityFree
- [ ] Navegou até `htdocs/caixa/`
- [ ] Fez upload de `caixa/index.html`
- [ ] (Opcional) Fez upload de `caixa/config-api.js` se mudou
- [ ] Testou acessando `https://www.temvenda.com.br/caixa/`
- [ ] Verificou se a aba "🔄 Sincronização" aparece
- [ ] Testou atualizar fluxo e verificar status na aba

---

## 💡 Dica

Se você usar FileZilla, pode criar um "Site" salvo com as credenciais do InfinityFree para facilitar uploads futuros.

