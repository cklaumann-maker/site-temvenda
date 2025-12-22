# 🔧 Corrigir Service Account - Invalid JWT Signature

## ✅ Problema Identificado

O erro `invalid_grant: Invalid JWT Signature` significa que a **chave privada do Service Account está inválida ou foi revogada**.

Isso pode acontecer se:
- A chave foi revogada no Google Cloud Console
- O JSON foi copiado incorretamente (caracteres quebrados)
- A chave expirou (raro)

---

## 🔧 Solução: Criar Nova Chave

### Passo 1: Acessar Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Selecione o projeto: `noticias-site-476917`
3. Vá em: **IAM & Admin** → **Service Accounts**

### Passo 2: Encontrar o Service Account

Procure por: `id-drive-reader@noticias-site-476917.iam.gserviceaccount.com`

### Passo 3: Criar Nova Chave

1. Clique no Service Account
2. Vá na aba **"Keys"**
3. Clique em **"Add Key"** → **"Create new key"**
4. Selecione **JSON**
5. Clique em **"Create"**
6. O arquivo JSON será baixado automaticamente

### Passo 4: Converter JSON para Uma Linha

```bash
# No diretório onde o arquivo foi baixado
cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))"
```

**⚠️ IMPORTANTE:** Copie **TODO** o resultado (é uma linha muito longa).

### Passo 5: Atualizar `.env` Local

Edite `backend/.env`:

```env
GOOGLE_SERVICE_ACCOUNT_JSON={cole-aqui-o-json-em-uma-linha}
```

**⚠️ IMPORTANTE:**
- Sem aspas ao redor
- Sem quebras de linha
- Tudo em uma única linha

### Passo 6: Atualizar no Render

1. Render Dashboard → Seu serviço → **Environment**
2. Encontre `GOOGLE_SERVICE_ACCOUNT_JSON`
3. Clique em **"Edit"**
4. Cole o mesmo JSON em uma linha
5. Clique em **"Save Changes"**
6. O Render vai fazer deploy automaticamente

### Passo 7: Reiniciar Backend Local

```bash
cd backend
# Pare o backend (Ctrl+C)
# Inicie novamente
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Passo 8: Testar

1. Acesse `http://localhost:8000/caixa/`
2. Faça login
3. Clique em "🔄 Atualizar Fluxo"
4. Deve funcionar agora!

---

## 🧪 Testar Localmente (Antes de Atualizar no Render)

Após atualizar o `.env` local, teste:

```bash
cd backend
python3 -c "
import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', '')
drive_file_id = os.getenv('DRIVE_FILE_ID', '')

try:
    info = json.loads(json_str)
    credentials = service_account.Credentials.from_service_account_info(
        info,
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = service.files().get(fileId=drive_file_id, fields='id,name').execute()
    print('✅ SUCESSO! Arquivo acessível:', file_metadata.get('name'))
except Exception as e:
    print('❌ ERRO:', e)
"
```

Se aparecer "✅ SUCESSO!", está funcionando!

---

## 📋 Checklist

- [ ] Nova chave criada no Google Cloud Console
- [ ] JSON baixado
- [ ] JSON convertido para uma linha
- [ ] `.env` local atualizado
- [ ] Teste local passou
- [ ] Render atualizado com novo JSON
- [ ] Teste em produção passou

---

## 🆘 Ainda Não Funciona?

### Problema: "Service Account não tem permissão"

**Solução:**
1. No Google Drive, compartilhe o arquivo com o email do Service Account:
   - Email: `id-drive-reader@noticias-site-476917.iam.gserviceaccount.com`
   - Permissão: **"Visualizador"**

### Problema: "JSON ainda inválido"

**Solução:**
1. Verifique se copiou **tudo** (a linha é muito longa)
2. Verifique se não há espaços extras no início/fim
3. Tente converter novamente:
   ```bash
   cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))" | pbcopy
   ```
   (Isso copia direto para a área de transferência no Mac)

---

## 💡 Dica: Script de Atualização Automática

Você pode criar um script para facilitar:

```bash
#!/bin/bash
# update-service-account.sh

echo "Cole o caminho do arquivo service_account.json:"
read JSON_FILE

if [ ! -f "$JSON_FILE" ]; then
    echo "❌ Arquivo não encontrado: $JSON_FILE"
    exit 1
fi

echo "Convertendo JSON para uma linha..."
JSON_ONE_LINE=$(cat "$JSON_FILE" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))")

echo ""
echo "✅ JSON convertido!"
echo ""
echo "Atualizando backend/.env..."
sed -i.bak "s|GOOGLE_SERVICE_ACCOUNT_JSON=.*|GOOGLE_SERVICE_ACCOUNT_JSON=$JSON_ONE_LINE|" backend/.env

echo "✅ Arquivo .env atualizado!"
echo ""
echo "⚠️  Lembre-se de atualizar também no Render!"
```

