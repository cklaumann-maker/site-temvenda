#!/bin/bash

# 🔧 Script para ajustar caminhos para hospedagem FTP gratuita
# Remove /wp-content/temvenda/ de todos os links e imagens

echo "🔧 Ajustando caminhos para hospedagem FTP..."
echo "============================================="
echo ""

# Diretório de origem
SOURCE_DIR="deploy-wp-content/temvenda"

# Diretório de destino
DEST_DIR="deploy-ftp"

# Criar diretório de destino
mkdir -p "$DEST_DIR"

# Copiar todos os arquivos
echo "📋 Copiando arquivos..."
cp -r "$SOURCE_DIR"/* "$DEST_DIR/"

echo "✅ Arquivos copiados!"
echo ""

# Ajustar caminhos nos arquivos HTML
echo "🔧 Ajustando caminhos..."
find "$DEST_DIR" -name "*.html" -type f | while read file; do
    echo "  Processando: $(basename $file)"
    
    # Remove /wp-content/temvenda/ de links
    sed -i '' 's|href="/wp-content/temvenda/|href="/|g' "$file"
    
    # Remove /wp-content/temvenda/ de imagens
    sed -i '' 's|src="/wp-content/temvenda/|src="/|g' "$file"
    
    # Remove /wp-content/temvenda/ de scripts
    sed -i '' 's|src="/wp-content/temvenda/|src="/|g' "$file"
    
    # Ajusta links relativos (remove /wp-content/temvenda/)
    sed -i '' 's|/wp-content/temvenda/||g' "$file"
done

echo ""
echo "✅ Ajustes concluídos!"
echo ""
echo "📁 Arquivos prontos para FTP em: $DEST_DIR/"
echo ""
echo "📋 Arquivos para upload:"
ls -lh "$DEST_DIR" | grep -E "\.(html|js|png)$" | awk '{print "  ✅ " $9 " (" $5 ")"}'
echo ""
echo "🚀 Pronto para fazer upload via FTP!"
echo ""
echo "📝 Próximos passos:"
echo "  1. Conecte via FTP ao seu servidor"
echo "  2. Navegue até htdocs/ ou public_html/"
echo "  3. Faça upload de todos os arquivos de $DEST_DIR/"
echo "  4. Teste em: http://seudominio.com.br/home-corporativo.html"

