# 🔄 Sincronizar Variáveis: Local ↔ Render

## ✅ O Problema

O erro `invalid_grant: Invalid JWT Signature` do Google indica que o `GOOGLE_SERVICE_ACCOUNT_JSON` local está diferente ou incorreto comparado ao Render.

---

## 🔍 Passo 1: Verificar Variáveis no Render

1. Acesse: Render Dashboard → Seu serviço → **Environment**
2. Copie os valores de:
   - `GOOGLE_SERVICE_ACCOUNT_JSON`
   - `DRIVE_FILE_ID`
   - `JWT_SECRET_KEY` (se quiser sincronizar também)

---

## 🔍 Passo 2: Verificar Arquivo Local

```bash
cd backend
cat .env
```

Verifique se as variáveis estão configuradas.

---

## ✅ Passo 3: Atualizar `.env` Local

Edite `backend/.env` e atualize com os valores do Render:

```env
# Google Drive
DRIVE_FILE_ID=mesmo-valor-do-render
GOOGLE_SERVICE_ACCOUNT_JSON=mesmo-json-do-render-em-uma-linha

# JWT (opcional, mas recomendado sincronizar)
JWT_SECRET_KEY=mesmo-valor-do-render

# Outras variáveis
APP_PASSWORD=sua-senha-local
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua-key
```

---

## ⚠️ Importante: Formato do GOOGLE_SERVICE_ACCOUNT_JSON

O `GOOGLE_SERVICE_ACCOUNT_JSON` deve estar em **uma única linha**, sem quebras.

**❌ ERRADO:**
```env
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",
"project_id":"...",
...}
```

**✅ CORRETO:**
```env
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"...","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
```

---

## 🔧 Passo 4: Converter JSON para Uma Linha (se necessário)

Se você tem o arquivo `service_account.json` original:

```bash
cd backend
cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))"
```

Copie o resultado e cole no `.env`:

```env
GOOGLE_SERVICE_ACCOUNT_JSON={resultado-do-comando-acima}
```

---

## ✅ Passo 5: Reiniciar Backend

Após atualizar o `.env`:

```bash
cd backend
# Pare o backend (Ctrl+C se estiver rodando)
# Inicie novamente
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🧪 Passo 6: Testar

1. Acesse `http://localhost:8000/caixa/`
2. Faça login
3. Clique em "🔄 Atualizar Fluxo"
4. Verifique se funciona

---

## 📋 Checklist de Sincronização

- [ ] `DRIVE_FILE_ID` local = `DRIVE_FILE_ID` Render
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` local = `GOOGLE_SERVICE_ACCOUNT_JSON` Render
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` está em uma linha (sem quebras)
- [ ] `JWT_SECRET_KEY` local = `JWT_SECRET_KEY` Render (opcional)
- [ ] Backend reiniciado após atualizar `.env`
- [ ] Teste funcionando

---

## 🆘 Ainda Não Funciona?

Se após sincronizar ainda der erro:

1. **Verificar logs do backend:**
   - Terminal onde o backend está rodando
   - Procurar por erros específicos

2. **Verificar formato do JSON:**
   - Certifique-se de que está em uma linha
   - Sem aspas extras
   - Sem caracteres especiais quebrados

3. **Verificar permissões do Service Account:**
   - O Service Account precisa ter acesso ao arquivo do Google Drive
   - Verificar no Google Cloud Console

---

## 💡 Dica: Script de Sincronização

Você pode criar um script para facilitar:

```bash
#!/bin/bash
# sync-env-from-render.sh

echo "Copie os valores do Render e cole aqui:"
echo ""
read -p "DRIVE_FILE_ID: " DRIVE_FILE_ID
read -p "GOOGLE_SERVICE_ACCOUNT_JSON (cole o JSON completo): " GOOGLE_JSON
read -p "JWT_SECRET_KEY: " JWT_SECRET

cat > backend/.env <<EOF
# Google Drive
DRIVE_FILE_ID=$DRIVE_FILE_ID
GOOGLE_SERVICE_ACCOUNT_JSON=$GOOGLE_JSON

# JWT
JWT_SECRET_KEY=$JWT_SECRET

# Outras (ajuste conforme necessário)
APP_PASSWORD=sua-senha
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua-key
EOF

echo "✅ Arquivo .env atualizado!"
```

