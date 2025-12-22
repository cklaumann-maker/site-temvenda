# 📤 Upload FTP - Produção (Correção Projeção)

## ✅ Arquivo que Precisa ser Enviado

### `caixa/index.html` ⚠️ **OBRIGATÓRIO**

**O que mudou:**
- ✅ Melhorias no tratamento de erros da projeção
- ✅ Mensagens de erro mais claras e específicas
- ✅ Nova aba "🔄 Sincronização" (já estava na versão anterior)

**Ação:**
- **Origem:** `caixa/index.html` (no seu computador)
- **Destino:** `htdocs/caixa/index.html` (no servidor InfinityFree)
- **Ação:** ⚠️ **SUBSTITUIR** o arquivo existente

---

## 📋 Passo a Passo Rápido

### 1. Conectar via FTP

Use seu cliente FTP (FileZilla, Cyberduck, etc.) e conecte ao servidor InfinityFree.

### 2. Navegar até `htdocs/caixa/`

Certifique-se de estar no diretório: `htdocs/caixa/`

### 3. Fazer Upload

**Arquivo:** `index.html`
- Arraste `caixa/index.html` do seu computador
- Solte em `htdocs/caixa/`
- Confirme substituição se solicitado

---

## ✅ Verificação

Após o upload:

1. Acesse: `https://www.temvenda.com.br/caixa/`
2. Faça login
3. Vá na aba "📈 Projeção D+60"
4. Clique em "📊 Atualizar Projeção"
5. Deve funcionar agora! ✅

---

## ⚠️ Importante

### Backend (Render) - NÃO precisa de FTP

O backend será atualizado automaticamente via Git quando você fizer commit e push. Você só precisa:

1. ✅ Fazer commit das mudanças:
   ```bash
   git add backend/app/main.py backend/app/finance_service.py caixa/index.html
   git commit -m "fix: melhorar tratamento de erros na projeção"
   git push
   ```

2. ✅ Aguardar deploy no Render (automático, ~2-5 minutos)

### Frontend (InfinityFree) - Precisa de FTP

O frontend precisa ser enviado manualmente via FTP.

---

## 📋 Checklist Completo

### Backend (Render):
- [ ] Fazer commit das mudanças
- [ ] Fazer push para GitHub
- [ ] Aguardar deploy no Render
- [ ] Verificar se `/health` retorna OK

### Frontend (InfinityFree):
- [ ] Conectado via FTP
- [ ] Navegou até `htdocs/caixa/`
- [ ] Fez upload de `caixa/index.html`
- [ ] Testou em produção

---

## 🧪 Teste Final

Após fazer upload e aguardar deploy do backend:

1. ✅ Acesse `https://www.temvenda.com.br/caixa/`
2. ✅ Faça login
3. ✅ Teste "🔄 Atualizar Fluxo" - deve funcionar
4. ✅ Teste "📊 Atualizar Projeção" - deve funcionar agora
5. ✅ Verifique aba "🔄 Sincronização" - deve mostrar status

---

## 💡 Dica

Se você usar FileZilla, pode salvar as credenciais do InfinityFree como um "Site" para facilitar uploads futuros.

