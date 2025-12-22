#!/bin/bash
echo "🧪 TESTANDO ACESSO À PÁGINA LOGIN-ADMIN..."
echo ""

# Verificar se o arquivo existe
if [ -f "login-admin.html" ]; then
    echo "✅ Arquivo login-admin.html existe"
else
    echo "❌ Arquivo login-admin.html NÃO encontrado"
    exit 1
fi

# Verificar se o servidor está rodando
if curl -s http://localhost:8000/login-admin.html > /dev/null 2>&1; then
    echo "✅ Servidor respondeu"
    echo "📄 URL correta: http://localhost:8000/login-admin.html"
else
    echo "⚠️  Servidor não está respondendo"
    echo "💡 Inicie o servidor: python3 -m http.server 8000"
fi
