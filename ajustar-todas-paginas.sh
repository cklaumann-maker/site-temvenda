#!/bin/bash

# 🔧 Script para ajustar caminhos em todas as páginas
echo "🔧 Ajustando caminhos em todas as páginas..."

# Função para ajustar um arquivo
adjust_file() {
    local file="$1"
    echo "Ajustando: $file"
    
    # Ajustar logo-temvenda.png
    sed -i '' 's|src="logo-temvenda.png"|src="/wp-content/temvenda/logo-temvenda.png"|g' "$file"
    
    # Ajustar auth-manager.js
    sed -i '' 's|src="auth-manager.js"|src="/wp-content/temvenda/auth-manager.js"|g' "$file"
    
    # Ajustar links internos para usar caminhos wp-content
    sed -i '' 's|href="/diagnostico"|href="/wp-content/temvenda/diagnostico.html"|g' "$file"
    sed -i '' 's|href="/consultoria"|href="/wp-content/temvenda/consultoria.html"|g' "$file"
    sed -i '' 's|href="/formacao-lideres"|href="/wp-content/temvenda/formacao-lideres.html"|g' "$file"
    sed -i '' 's|href="/palestras"|href="/wp-content/temvenda/palestras.html"|g' "$file"
    sed -i '' 's|href="/treinamento-incompany"|href="/wp-content/temvenda/treinamento-incompany.html"|g' "$file"
    sed -i '' 's|href="/login-admin"|href="/wp-content/temvenda/login-admin.html"|g' "$file"
    sed -i '' 's|href="/admin-panel"|href="/wp-content/temvenda/admin-panel.html"|g' "$file"
    sed -i '' 's|href="/admin-stats"|href="/wp-content/temvenda/admin-stats.html"|g' "$file"
    sed -i '' 's|href="/admin-users"|href="/wp-content/temvenda/admin-users.html"|g' "$file"
    sed -i '' 's|href="/noticias"|href="/wp-content/temvenda/noticias.html"|g' "$file"
    sed -i '' 's|href="/home-moderna"|href="/wp-content/temvenda/home-corporativo.html"|g' "$file"
}

# Ajustar todas as páginas HTML (exceto home-corporativo que já foi ajustado)
for file in deploy-wp-content/temvenda/*.html; do
    if [ -f "$file" ] && [ "$(basename "$file")" != "home-corporativo.html" ]; then
        adjust_file "$file"
    fi
done

echo "✅ Ajustes concluídos!"
echo ""
echo "📁 Arquivos ajustados em: deploy-wp-content/temvenda/"
echo "🌐 URLs finais:"
echo "  - https://temvenda.com.br/wp-content/temvenda/home-corporativo.html"
echo "  - https://temvenda.com.br/wp-content/temvenda/consultoria.html"
echo "  - https://temvenda.com.br/wp-content/temvenda/formacao-lideres.html"
echo "  - https://temvenda.com.br/wp-content/temvenda/palestras.html"
echo "  - https://temvenda.com.br/wp-content/temvenda/treinamento-incompany.html"
echo ""
echo "🚀 Pronto para upload no wp-content!"

