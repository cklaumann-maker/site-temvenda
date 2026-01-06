#!/bin/bash

# 🚀 Script para fazer push do rotina-app para GitHub
# Execute este script na pasta rotina-app

echo "🚀 Preparando push do rotina-app para GitHub..."
echo ""

# Verificar se está na pasta correta
if [ ! -f "package.json" ]; then
    echo "❌ Erro: Execute este script dentro da pasta rotina-app"
    exit 1
fi

# Voltar para a raiz do repositório Git
cd ..

# Verificar status
echo "📊 Verificando status do Git..."
git status rotina-app/ --short | head -20

echo ""
echo "📦 Adicionando arquivos do rotina-app..."
git add rotina-app/

echo ""
echo "💾 Fazendo commit..."
git commit -m "feat: adicionar aplicação Rotina App completa

- Sistema de controle de dieta e calorias
- Integração com Supabase
- Dashboard de calorias e aderência
- Sistema de check-in diário
- Gerenciamento de plano alimentar
- Perfil de usuário com IMC
- Deploy configurado para Vercel
- Migrations do banco de dados
- Scripts de importação de dados"

echo ""
echo "📤 Fazendo push para GitHub..."
git push origin main

echo ""
echo "✅ Push concluído!"
echo ""
echo "🔗 Verifique em: https://github.com/cklaumann-maker/site-temvenda"
echo "📁 A pasta rotina-app/ deve aparecer no repositório"







