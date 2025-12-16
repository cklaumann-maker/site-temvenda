# Guia Completo: Deploy no Render.com

Este guia passo a passo vai te ajudar a configurar o backend do módulo financeiro no Render.com.

## 📋 Pré-requisitos

- Conta no Render.com (gratuita em https://render.com)
- Acesso às credenciais do Supabase
- Acesso ao Google Drive (Service Account JSON)
- GitHub com o código (ou fazer upload manual)

---

## 🚀 Passo 1: Preparar o Repositório

### Opção A: Se já tem no GitHub
1. Certifique-se de que o código está commitado e no GitHub
2. Anote a URL do repositório

### Opção B: Se não tem no GitHub
1. Criar repositório no GitHub
2. Fazer push do código:
   ```bash
   cd /Users/cesark/site-temvenda
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/seu-usuario/site-temvenda.git
   git push -u origin main
   ```

---

## 🎯 Passo 2: Criar Serviço no Render

1. **Acesse Render.com** e faça login
2. Clique em **"New +"** → **"Web Service"**
3. **Conecte seu repositório GitHub**:
   - Se for a primeira vez, autorize o Render a acessar seu GitHub
   - Selecione o repositório `site-temvenda`
   - Clique em **"Connect"**

---

## ⚙️ Passo 3: Configurar o Serviço

### Informações Básicas:
- **Name**: `temvenda-finance-api` (ou outro nome de sua escolha)
- **Region**: Escolha a região mais próxima (ex: `Oregon (US West)`)
- **Branch**: `main` (ou a branch que você usa)
- **Root Directory**: `backend` ⚠️ **IMPORTANTE: Deixe em branco se o backend está na raiz, ou coloque `backend` se está em subpasta**

### Build & Start:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

⚠️ **Se o backend está em subpasta `backend/`**, use:
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🔐 Passo 4: Configurar Variáveis de Ambiente

Na seção **"Environment Variables"**, adicione as seguintes variáveis:

### Variáveis Obrigatórias:

1. **APP_PASSWORD**
   - **Value**: `SuaSenhaForte123!` (escolha uma senha forte)
   - **Description**: Senha para acessar o módulo financeiro

2. **JWT_SECRET_KEY**
   - **Value**: Gere uma chave aleatória longa (ex: `openssl rand -hex 32`)
   - **Description**: Chave secreta para assinar tokens JWT
   - 💡 **Dica**: Use um gerador online ou execute: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

3. **JWT_ACCESS_EXPIRES_HOURS**
   - **Value**: `8`
   - **Description**: Horas de expiração do token

4. **SUPABASE_URL**
   - **Value**: `https://seu-projeto.supabase.co`
   - **Description**: URL do seu projeto Supabase
   - 💡 Encontre em: Supabase Dashboard → Settings → API → Project URL

5. **SUPABASE_SERVICE_ROLE_KEY**
   - **Value**: `sua-service-role-key-aqui`
   - **Description**: Service Role Key do Supabase
   - 💡 Encontre em: Supabase Dashboard → Settings → API → service_role key
   - ⚠️ **IMPORTANTE**: Use a `service_role` key, não a `anon` key

6. **DRIVE_FILE_ID**
   - **Value**: `1ABC...XYZ` (ID do arquivo Google Drive)
   - **Description**: ID do arquivo Excel no Google Drive
   - 💡 Como encontrar: Abra o arquivo no Google Drive → URL será `https://drive.google.com/file/d/ID_AQUI/view`

7. **GOOGLE_PROJECTION_FILE_ID**
   - **Value**: `1DEF...UVW` (ID do arquivo de projeção)
   - **Description**: ID do arquivo de projeção D+60 no Google Drive

8. **GOOGLE_SERVICE_ACCOUNT_JSON**
   - **Value**: `{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}`
   - **Description**: JSON completo da Service Account do Google em **UMA LINHA**
   - 💡 **Como obter**:
     1. Acesse Google Cloud Console
     2. Crie uma Service Account ou use existente
     3. Baixe o JSON
     4. Converta para uma linha (remova quebras de linha)
     5. Cole aqui

9. **FRONTEND_ORIGINS**
   - **Value**: `https://www.temvenda.com.br,https://temvenda.com.br`
   - **Description**: Origens permitidas para CORS

10. **ENVIRONMENT**
    - **Value**: `production`
    - **Description**: Ambiente de execução

---

## 📝 Passo 5: Formato do GOOGLE_SERVICE_ACCOUNT_JSON

O JSON da Service Account precisa estar em **UMA LINHA**. Exemplo:

```
{"type":"service_account","project_id":"meu-projeto","private_key_id":"abc123","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n","client_email":"service@meu-projeto.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/service%40meu-projeto.iam.gserviceaccount.com"}
```

💡 **Dica**: Use um conversor online ou execute:
```bash
cat service_account.json | jq -c .
```

---

## 🚀 Passo 6: Deploy

1. Clique em **"Create Web Service"**
2. O Render vai começar a fazer o build
3. Aguarde alguns minutos (primeira vez pode demorar 5-10 minutos)
4. Você verá os logs do build em tempo real

---

## ✅ Passo 7: Verificar se Funcionou

1. **Aguardar o deploy terminar** (status "Live")
2. **Anotar a URL** gerada (ex: `https://temvenda-finance-api.onrender.com`)
3. **Testar o endpoint de health**:
   - Acesse: `https://sua-url.onrender.com/health`
   - Deve retornar: `{"status":"ok","database":"ok"}`

---

## 🔧 Passo 8: Configurar Frontend

1. **Editar `financeiro/config-api.js`**:
   ```javascript
   window.FINANCE_API_URL = "https://sua-url.onrender.com";
   ```

2. **Fazer upload** dos arquivos:
   - `financeiro/index.html`
   - `financeiro/config-api.js`
   
   Para o servidor do site (garantindo que fiquem em `/financeiro/`)

---

## 🐛 Troubleshooting

### Erro no Build
- Verifique se o **Root Directory** está correto
- Verifique se o **requirements.txt** está no lugar certo
- Veja os logs de build no Render

### Erro 500 no Health Check
- Verifique se as variáveis de ambiente estão corretas
- Verifique os logs no Render (aba "Logs")
- Verifique se o Supabase está acessível

### Erro de CORS
- Verifique se `FRONTEND_ORIGINS` inclui `https://www.temvenda.com.br`
- Verifique se a URL no frontend está correta

### Erro ao conectar no Google Drive
- Verifique se o `GOOGLE_SERVICE_ACCOUNT_JSON` está em uma linha
- Verifique se a Service Account tem permissão no arquivo do Drive
- Verifique se o `DRIVE_FILE_ID` está correto

### Erro ao conectar no Supabase
- Verifique se `SUPABASE_URL` está correto (sem barra no final)
- Verifique se `SUPABASE_SERVICE_ROLE_KEY` é a service_role key, não anon
- Verifique se as tabelas foram criadas no Supabase

---

## 📊 Monitoramento

- **Logs**: Acesse a aba "Logs" no Render para ver logs em tempo real
- **Metrics**: A aba "Metrics" mostra CPU, memória, etc.
- **Events**: A aba "Events" mostra histórico de deploys

---

## 🔄 Atualizações Futuras

Quando fizer alterações no código:
1. Faça commit e push para o GitHub
2. O Render detecta automaticamente e faz novo deploy
3. Ou clique em "Manual Deploy" → "Deploy latest commit"

---

## 💰 Custos

- **Plano Free**: 750 horas/mês (suficiente para desenvolvimento/testes)
- **Plano Starter**: $7/mês (recomendado para produção)
- ⚠️ **Importante**: No plano free, o serviço "dorme" após 15 minutos de inatividade. O primeiro request pode demorar ~30s para "acordar".

---

## 🎉 Pronto!

Seu backend está rodando! Agora é só:
1. Configurar o frontend com a URL do Render
2. Fazer upload dos arquivos
3. Testar em `https://www.temvenda.com.br/financeiro/`

---

## 📞 Precisa de Ajuda?

- Documentação Render: https://render.com/docs
- Suporte Render: https://render.com/support

