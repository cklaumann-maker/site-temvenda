#!/bin/bash

# 🚀 Script para atualizar home-corporativo.html no WordPress
echo "🚀 ATUALIZANDO HOME-CORPORATIVO NO WORDPRESS"
echo "============================================="
echo ""

# Verificar se o arquivo existe
if [ ! -f "deploy-wp-content/temvenda/home-corporativo.html" ]; then
    echo "❌ Erro: Arquivo home-corporativo.html não encontrado!"
    exit 1
fi

echo "📄 Arquivo encontrado:"
echo "  📁 Local: deploy-wp-content/temvenda/home-corporativo.html"
echo "  📊 Tamanho: $(ls -lh deploy-wp-content/temvenda/home-corporativo.html | awk '{print $5}')"
echo "  📅 Modificado: $(ls -l deploy-wp-content/temvenda/home-corporativo.html | awk '{print $6, $7, $8}')"
echo ""

echo "🎯 INSTRUÇÕES PARA UPLOAD:"
echo "=========================="
echo ""
echo "1️⃣ Acesse seu painel WordPress (cPanel ou FTP)"
echo "2️⃣ Navegue até: wp-content/temvenda/"
echo "3️⃣ Faça upload do arquivo: deploy-wp-content/temvenda/home-corporativo.html"
echo "4️⃣ Substitua o arquivo existente"
echo ""
echo "🌐 URL para testar:"
echo "https://temvenda.com.br/wp-content/temvenda/home-corporativo.html"
echo ""
echo "✅ CARACTERÍSTICAS DO ARQUIVO ATUALIZADO:"
echo "  🎨 Design: Home moderna com fundo preto"
echo "  🔗 Links: Todos ajustados para wp-content/temvenda/"
echo "  📱 Responsivo: Funciona em mobile e desktop"
echo "  🚀 Performance: Otimizado para carregamento rápido"
echo ""
echo "📋 CHECKLIST PÓS-UPLOAD:"
echo "  ☐ Arquivo carregou sem erros"
echo "  ☐ Logo aparece corretamente"
echo "  ☐ Links de navegação funcionam"
echo "  ☐ Botões 'Saiba mais' redirecionam"
echo "  ☐ Footer com links corretos"
echo "  ☐ Design responsivo funcionando"
echo ""
echo "🎉 Pronto para upload!"
