# 🔄 Atualizar Service Account no Render

## ✅ Status Local

A nova chave do Service Account está funcionando localmente! ✅

Agora você precisa atualizar também no **Render** para funcionar em produção.

---

## 📋 Passo a Passo

### 1. Copiar o JSON em Uma Linha

O JSON já está no seu `.env` local. Para copiar para o Render, você pode:

**Opção A: Usar o comando:**
```bash
cd backend
cat .env | grep GOOGLE_SERVICE_ACCOUNT_JSON
```

**Opção B: Ler diretamente do arquivo:**
```bash
cd backend
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
"
```

---

### 2. Atualizar no Render

1. Acesse: Render Dashboard → Seu serviço (`temvenda-finance-api`)
2. Vá em: **Environment**
3. Encontre: `GOOGLE_SERVICE_ACCOUNT_JSON`
4. Clique em **"Edit"** (ou **"Add"** se não existir)
5. Cole o JSON completo (a linha muito longa)
6. Clique em **"Save Changes"**
7. O Render vai fazer deploy automaticamente

---

### 3. Aguardar Deploy

- Render Dashboard → **Deployments**
- Aguarde o deploy concluir (geralmente 2-5 minutos)

---

### 4. Testar em Produção

1. Acesse `https://www.temvenda.com.br/caixa/`
2. Faça login
3. Clique em "🔄 Atualizar Fluxo"
4. Deve funcionar agora! ✅

---

## 🧪 Testar Localmente Primeiro

Antes de atualizar no Render, teste localmente:

1. **Reinicie o backend** (se estiver rodando):
   ```bash
   cd backend
   # Pare (Ctrl+C) e reinicie:
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

2. **Teste no frontend:**
   - Acesse `http://localhost:8000/caixa/`
   - Faça login
   - Clique em "🔄 Atualizar Fluxo"
   - Deve funcionar! ✅

---

## 📋 Checklist

- [ ] Nova chave funcionando localmente ✅
- [ ] Backend local reiniciado
- [ ] Teste local passou
- [ ] JSON copiado para Render
- [ ] Render atualizado
- [ ] Deploy concluído
- [ ] Teste em produção passou

---

## 🆘 Se Der Erro no Render

Se após atualizar no Render ainda der erro:

1. **Verificar logs do Render:**
   - Render Dashboard → Logs
   - Procurar por erros relacionados a Google Drive

2. **Verificar formato:**
   - Certifique-se de que o JSON está em **uma única linha**
   - Sem quebras de linha
   - Sem aspas extras

3. **Verificar permissões:**
   - O Service Account precisa ter acesso ao arquivo do Google Drive
   - Email: `id-drive-reader@noticias-site-476917.iam.gserviceaccount.com`
   - Permissão: "Visualizador"

