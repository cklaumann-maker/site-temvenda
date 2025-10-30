#!/bin/bash

# Script para extrair HTML de todas as páginas WordPress
echo "🚀 Extraindo HTML das páginas WordPress..."

# Lista de páginas para extrair
pages=(
    "diagnostico:DIAGNOSTICO"
    "home:TEM VENDA - home"
    "consultoria:Consultoria - bio"
    "formacao:Formação Líderes de Farmácia"
    "incompany:INCOMPANY - bio"
    "palestras:PALESTRAS"
    "bio:TEM VENDA - bio"
)

# Extrair cada página
for page_info in "${pages[@]}"; do
    IFS=':' read -r slug title <<< "$page_info"
    
    echo "📄 Extraindo: $title"
    
    # Extrair HTML do banco
    docker exec temvenda_db mysql -u wordpress -pwordpress_password temvenda_db \
        -e "SELECT post_content FROM wp_posts WHERE post_name = '$slug' AND post_type = 'page';" \
        > "html-pages/${slug}.html"
    
    # Remover cabeçalho do MySQL
    sed -i '' '1d' "html-pages/${slug}.html"
    
    echo "✅ $title extraído para html-pages/${slug}.html"
done

echo ""
echo "🎉 Extração concluída!"
echo "📁 Arquivos criados em: html-pages/"
echo ""
echo "📋 Próximos passos:"
echo "1. Instale o tema 'Hello Elementor'"
echo "2. Edite cada página com Elementor"
echo "3. Cole o HTML correspondente no Widget HTML"
echo "4. Atualize as páginas"

