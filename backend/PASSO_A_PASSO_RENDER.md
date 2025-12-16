# 🚀 Passo a Passo: Deploy no Render.com

## 📝 Passo 1: Criar Conta e Conectar GitHub

1. Acesse https://render.com
2. Clique em **"Get Started for Free"**
3. Faça login com GitHub
4. Autorize o Render a acessar seus repositórios

---

## 📦 Passo 2: Criar Novo Web Service

1. No Dashboard, clique em **"New +"**
2. Selecione **"Web Service"**
3. Selecione seu repositório `site-temvenda`
4. Clique em **"Connect"**

---

## ⚙️ Passo 3: Configurar o Serviço

### Informações Básicas:
- **Name**: `temvenda-finance-api`
- **Region**: `Oregon (US West)` ou mais próxima
- **Branch**: `main`
- **Root Directory**: `backend` ⚠️ **IMPORTANTE**

### Runtime:
- **Runtime**: `Python 3`

### Build & Start Commands:
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

---

## 🔐 Passo 4: Adicionar Variáveis de Ambiente

Clique em **"Advanced"** → **"Add Environment Variable"** e adicione:

### 1. ENVIRONMENT
```
ENVIRONMENT=production
```

### 2. APP_PASSWORD
```
APP_PASSWORD=SuaSenhaForte123!
```
⚠️ Escolha uma senha forte - será usada para fazer login no módulo financeiro

### 3. JWT_SECRET_KEY
Execute no terminal:
```bash
cd backend
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```
Cole o resultado aqui.

### 4. JWT_ACCESS_EXPIRES_HOURS
```
JWT_ACCESS_EXPIRES_HOURS=8
```

### 5. SUPABASE_URL
```
SUPABASE_URL=https://seu-projeto.supabase.co
```
💡 Encontre em: Supabase Dashboard → Settings → API → Project URL

### 6. SUPABASE_SERVICE_ROLE_KEY
```
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-aqui
```
💡 Encontre em: Supabase Dashboard → Settings → API → service_role key
⚠️ Use a **service_role** key, não a anon key!

### 7. DRIVE_FILE_ID
```
DRIVE_FILE_ID=1ABC...XYZ
```
💡 Como encontrar:
1. Abra o arquivo Excel no Google Drive
2. A URL será: `https://drive.google.com/file/d/ID_AQUI/view`
3. Copie o `ID_AQUI`

### 8. GOOGLE_PROJECTION_FILE_ID
```
GOOGLE_PROJECTION_FILE_ID=1DEF...UVW
```
💡 Mesmo processo do DRIVE_FILE_ID, mas para o arquivo de projeção

### 9. GOOGLE_SERVICE_ACCOUNT_JSON
Este é o mais complicado. O JSON precisa estar em **UMA LINHA**.

**Opção A - Se você tem o arquivo `service_account.json` na raiz:**
```bash
cd /Users/cesark/site-temvenda
cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))"
```
Cole o resultado completo (tudo em uma linha) no Render.

**Opção B - Manualmente:**
1. Abra o arquivo `service_account.json`
2. Remova todas as quebras de linha
3. Cole no Render

Exemplo de formato:
```
{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",...}
```

### 10. FRONTEND_ORIGINS
```
FRONTEND_ORIGINS=https://www.temvenda.com.br,https://temvenda.com.br
```

---

## 🚀 Passo 5: Fazer Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o build (pode demorar 5-10 minutos na primeira vez)
3. Você verá os logs em tempo real

---

## ✅ Passo 6: Verificar se Funcionou

1. Aguarde o status ficar **"Live"** (verde)
2. Anote a URL gerada (ex: `https://temvenda-finance-api.onrender.com`)
3. Teste o endpoint de health:
   - Acesse: `https://sua-url.onrender.com/health`
   - Deve retornar: `{"status":"ok","database":"ok"}`

---

## 🔧 Passo 7: Configurar Frontend

1. **Edite `financeiro/config-api.js`**:
   ```javascript
   window.FINANCE_API_URL = "https://sua-url.onrender.com";
   ```

2. **Faça upload** para o servidor:
   - `financeiro/index.html`
   - `financeiro/config-api.js`

---

## 🐛 Problemas Comuns

### ❌ Build falha
- Verifique se o **Root Directory** está como `backend`
- Verifique se o `requirements.txt` existe

### ❌ Health check retorna erro
- Verifique os logs no Render (aba "Logs")
- Verifique se todas as variáveis de ambiente estão corretas
- Verifique se o Supabase está acessível

### ❌ Erro de CORS
- Verifique se `FRONTEND_ORIGINS` inclui `https://www.temvenda.com.br`
- Verifique se a URL no frontend está correta

### ❌ Erro ao conectar no Google Drive
- Verifique se `GOOGLE_SERVICE_ACCOUNT_JSON` está em uma linha
- Verifique se a Service Account tem permissão no arquivo
- Verifique se o `DRIVE_FILE_ID` está correto

---

## 📊 Monitorar

- **Logs**: Dashboard → Seu Serviço → Aba "Logs"
- **Metrics**: Dashboard → Seu Serviço → Aba "Metrics"
- **Events**: Dashboard → Seu Serviço → Aba "Events"

---

## 💡 Dicas

- No plano free, o serviço "dorme" após 15 min de inatividade
- O primeiro request após dormir pode demorar ~30s
- Para produção, considere o plano Starter ($7/mês)

---

## ✅ Checklist Final

- [ ] Serviço criado no Render
- [ ] Todas as variáveis de ambiente configuradas
- [ ] Health check funcionando
- [ ] Frontend configurado com URL do Render
- [ ] Testado login no módulo financeiro
- [ ] Testado carregamento de mês

---

## 🎉 Pronto!

Seu backend está rodando! Agora é só testar em `https://www.temvenda.com.br/financeiro/`

