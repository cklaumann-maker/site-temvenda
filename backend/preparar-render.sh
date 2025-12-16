#!/bin/bash

# Script para preparar variáveis de ambiente para Render.com
# Execute: bash preparar-render.sh

echo "=========================================="
echo "Preparação de Variáveis para Render.com"
echo "=========================================="
echo ""

# Gerar JWT_SECRET_KEY
echo "1. Gerando JWT_SECRET_KEY..."
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
echo "   JWT_SECRET_KEY=$JWT_SECRET"
echo ""

# Verificar se existe service_account.json
if [ -f "../service_account.json" ]; then
    echo "2. Convertendo service_account.json para uma linha..."
    GOOGLE_JSON=$(cat ../service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))")
    echo "   ✅ Arquivo encontrado e convertido"
    echo "   (Cole o valor abaixo no Render)"
    echo ""
    echo "$GOOGLE_JSON"
    echo ""
elif [ -f "service_account.json" ]; then
    echo "2. Convertendo service_account.json para uma linha..."
    GOOGLE_JSON=$(cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))")
    echo "   ✅ Arquivo encontrado e convertido"
    echo "   (Cole o valor abaixo no Render)"
    echo ""
    echo "$GOOGLE_JSON"
    echo ""
else
    echo "2. ⚠️  service_account.json não encontrado"
    echo "   Procurando em: ../service_account.json e ./service_account.json"
    echo "   Você precisará converter manualmente"
    echo ""
fi

echo "=========================================="
echo "Variáveis para adicionar no Render:"
echo "=========================================="
echo ""
echo "ENVIRONMENT=production"
echo "APP_PASSWORD=<SUA_SENHA_FORTE>"
echo "JWT_SECRET_KEY=$JWT_SECRET"
echo "JWT_ACCESS_EXPIRES_HOURS=8"
echo "SUPABASE_URL=<https://seu-projeto.supabase.co>"
echo "SUPABASE_SERVICE_ROLE_KEY=<sua-service-role-key>"
echo "DRIVE_FILE_ID=<id-do-arquivo-google-drive>"
echo "GOOGLE_PROJECTION_FILE_ID=<id-do-arquivo-projecao>"
echo "GOOGLE_SERVICE_ACCOUNT_JSON=<json-em-uma-linha>"
echo "FRONTEND_ORIGINS=https://www.temvenda.com.br,https://temvenda.com.br"
echo ""
echo "=========================================="
echo "Próximos passos:"
echo "=========================================="
echo "1. Acesse https://render.com"
echo "2. Crie um novo Web Service"
echo "3. Conecte seu repositório GitHub"
echo "4. Configure as variáveis acima"
echo "5. Build Command: pip install -r requirements.txt"
echo "6. Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo ""

