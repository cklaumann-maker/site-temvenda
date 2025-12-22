#!/bin/bash

echo "🧪 Testando Backend Local"
echo "========================="
echo ""

# Verificar se o backend está rodando
echo "1. Verificando se o backend está rodando na porta 8001..."
if lsof -i :8001 > /dev/null 2>&1; then
    echo "✅ Backend está rodando na porta 8001"
else
    echo "❌ Backend NÃO está rodando na porta 8001"
    echo "   Execute: cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"
    exit 1
fi

echo ""

# Testar endpoint de health
echo "2. Testando endpoint /health..."
HEALTH_RESPONSE=$(curl -s http://localhost:8001/health)
if [ $? -eq 0 ]; then
    echo "✅ Resposta do /health:"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo "❌ Erro ao acessar /health"
    exit 1
fi

echo ""

# Verificar variáveis de ambiente
echo "3. Verificando arquivo .env..."
if [ -f "backend/.env" ]; then
    echo "✅ Arquivo .env encontrado"
    echo "   Variáveis configuradas:"
    grep -E "^(APP_PASSWORD|SUPABASE_URL|DRIVE_FILE_ID|GOOGLE_SERVICE_ACCOUNT_JSON)=" backend/.env | sed 's/=.*/=***/' || echo "   Nenhuma variável encontrada"
else
    echo "⚠️  Arquivo .env NÃO encontrado em backend/.env"
    echo "   Crie o arquivo com as variáveis necessárias"
fi

echo ""

# Testar login (se APP_PASSWORD estiver configurado)
if [ -f "backend/.env" ]; then
    APP_PASSWORD=$(grep "^APP_PASSWORD=" backend/.env | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    if [ -n "$APP_PASSWORD" ]; then
        echo "4. Testando login..."
        LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8001/api/auth/login \
            -H "Content-Type: application/json" \
            -d "{\"password\":\"$APP_PASSWORD\"}")
        
        if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
            echo "✅ Login funcionando!"
            TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
            if [ -n "$TOKEN" ]; then
                echo "   Token obtido: ${TOKEN:0:20}..."
            fi
        else
            echo "❌ Erro no login:"
            echo "$LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"
        fi
    else
        echo "⚠️  APP_PASSWORD não configurado no .env"
    fi
fi

echo ""
echo "========================="
echo "✅ Teste concluído!"

