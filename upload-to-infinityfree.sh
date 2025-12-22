#!/bin/bash

echo "🚀 Upload para InfinityFree via curl"
echo "===================================="

# Configurações do InfinityFree
FTP_HOST="ftpupload.net"
FTP_USER="if0_40283323"
FTP_PASS="bqfvYPo802HiA1"
FTP_DIR="htdocs"

echo "🔧 Configurações:"
echo "   - Host: $FTP_HOST"
echo "   - Usuário: $FTP_USER"
echo "   - Diretório: $FTP_DIR"
echo ""

# Função para upload de arquivo
upload_file() {
    local file="$1"
    local remote_path="$2"
    
    if [ -f "$file" ]; then
        echo "📤 Enviando $file..."
        curl -T "$file" "ftp://$FTP_USER:$FTP_PASS@$FTP_HOST/$FTP_DIR/$remote_path" --silent --show-error
        if [ $? -eq 0 ]; then
            echo "✅ $file enviado com sucesso"
        else
            echo "❌ Erro ao enviar $file"
        fi
    else
        echo "⚠️  Arquivo $file não encontrado"
    fi
}

echo "🔄 Iniciando upload dos arquivos..."

# Upload de arquivos HTML principais
upload_file "index.html" "index.html"
upload_file "home-corporativo.html" "home-corporativo.html"
upload_file "instagram.html" "instagram.html"
upload_file "diagnostico.html" "diagnostico.html"
upload_file "noticias.html" "noticias.html"
upload_file "consultoria.html" "consultoria.html"
upload_file "formacao-lideres.html" "formacao-lideres.html"
upload_file "treinamento-incompany.html" "treinamento-incompany.html"
upload_file "palestras.html" "palestras.html"

# Upload de páginas admin
upload_file "admin.html" "admin.html"
upload_file "admin-panel.html" "admin-panel.html"
upload_file "admin-stats.html" "admin-stats.html"
upload_file "admin-users.html" "admin-users.html"
upload_file "admin-funil.html" "admin-funil.html"
upload_file "admin-leads.html" "admin-leads.html"
upload_file "login-admin.html" "login-admin.html"

# Upload de arquivos JavaScript
upload_file "auth-manager.js" "auth-manager.js"
upload_file "supabase-config.js" "supabase-config.js"
upload_file "email-config.js" "email-config.js"

# Upload de favicons
upload_file "favicon.ico" "favicon.ico"
upload_file "favicon-32.png" "favicon-32.png"

# Upload de configuração
upload_file ".htaccess" ".htaccess"

echo ""
echo "✅ Upload concluído!"
echo ""
echo "🌐 Teste seu site:"
echo "- https://temvenda.com.br"
echo "- https://temvenda.com.br/instagram"
echo "- https://temvenda.com.br/admin"
echo ""
echo "📋 Próximos passos:"
echo "1. Teste todas as páginas"
echo "2. Verifique se o e-mail envia"
echo "3. Teste o admin"
echo ""
echo "🔄 Para futuras atualizações:"
echo "1. Faça suas alterações localmente"
echo "2. Execute: git add . && git commit -m 'Descrição' && git push"
echo "3. Execute: ./upload-to-infinityfree.sh"

