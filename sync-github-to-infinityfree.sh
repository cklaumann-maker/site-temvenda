#!/bin/bash

echo "🔄 Sincronização GitHub → InfinityFree"
echo "======================================"

# Verificar se estamos no diretório correto
if [ ! -f "index.html" ]; then
    echo "❌ Execute este script no diretório raiz do projeto"
    exit 1
fi

# Configurações do InfinityFree
FTP_HOST="ftpupload.net"
FTP_USER="if0_40283323"
FTP_PASS="bqfvYPo802HiA1"
FTP_DIR="htdocs"  # diretório principal do site

echo "🔧 Configurações FTP configuradas:"
echo "   - Host: $FTP_HOST"
echo "   - Usuário: $FTP_USER"
echo "   - Diretório: $FTP_DIR"
echo ""

# Verificar se lftp está instalado
if ! command -v lftp &> /dev/null; then
    echo "📦 Instalando lftp..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install lftp
        else
            echo "❌ Instale o Homebrew primeiro: https://brew.sh"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y lftp
    else
        echo "❌ Sistema operacional não suportado. Instale lftp manualmente."
        exit 1
    fi
fi

# Credenciais já configuradas ✅

echo "🔄 Sincronizando arquivos..."

# Criar script de sincronização
cat > sync_ftp.lftp << EOF
open $FTP_HOST
user $FTP_USER $FTP_PASS
cd $FTP_DIR
lcd $(pwd)

# Upload de arquivos HTML principais
put index.html
put home-corporativo.html
put instagram.html
put diagnostico.html
put noticias.html
put consultoria.html
put formacao-lideres.html
put treinamento-incompany.html
put palestras.html

# Upload de páginas admin
put admin.html
put admin-panel.html
put admin-stats.html
put admin-users.html
put admin-funil.html
put admin-leads.html
put login-admin.html

# Upload de arquivos JavaScript
put auth-manager.js
put supabase-config.js
put email-config.js

# Upload de favicons
put favicon.ico
put favicon-32.png

# Upload de configuração
put .htaccess

# Upload de arquivos de deploy
put deploy-github-infinityfree.sh
put sync-github-to-infinityfree.sh
put GUIA_DEPLOY_COMPLETO.md

quit
EOF

# Executar sincronização
lftp -f sync_ftp.lftp

# Limpar arquivo temporário
rm sync_ftp.lftp

echo ""
echo "✅ Sincronização concluída!"
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
echo "3. Execute: ./sync-github-to-infinityfree.sh"
