#!/bin/bash

# 🚀 Script de Deploy para TEM VENDA
# Este script prepara os arquivos para upload no WordPress

echo "🚀 Preparando deploy para temvenda.com.br..."

# Criar diretório de deploy
mkdir -p deploy-temvenda
cd deploy-temvenda

# Copiar arquivos principais
echo "📁 Copiando arquivos principais..."
cp ../wordpress/admin-panel.html .
cp ../wordpress/admin-stats.html .
cp ../wordpress/admin-users.html .
cp ../wordpress/login-admin.html .
cp ../wordpress/home-corporativo.html .
cp ../wordpress/diagnostico.html .
cp ../wordpress/consultoria.html .
cp ../wordpress/formacao-lideres.html .
cp ../wordpress/palestras.html .
cp ../wordpress/treinamento-incompany.html .
cp ../wordpress/noticias.html .
cp ../auth-manager.js .

# Copiar logo
cp ../logo-temvenda.png .

# Criar arquivo .htaccess
echo "⚙️ Criando .htaccess..."
cat > .htaccess << 'EOF'
# Redirecionamentos personalizados TEM VENDA
RewriteEngine On

# Páginas principais
RewriteRule ^diagnostico/?$ /diagnostico.html [L,QSA]
RewriteRule ^home-moderna/?$ /home-corporativo.html [L,QSA]
RewriteRule ^formacao-lideres/?$ /formacao-lideres.html [L,QSA]
RewriteRule ^consultoria/?$ /consultoria.html [L,QSA]
RewriteRule ^palestras/?$ /palestras.html [L,QSA]
RewriteRule ^treinamento-incompany/?$ /treinamento-incompany.html [L,QSA]

# Área administrativa
RewriteRule ^login-admin/?$ /login-admin.html [L,QSA]
RewriteRule ^admin-panel/?$ /admin-panel.html [L,QSA]
RewriteRule ^admin-stats/?$ /admin-stats.html [L,QSA]
RewriteRule ^admin-users/?$ /admin-users.html [L,QSA]

# Notícias públicas
RewriteRule ^noticias/?$ /noticias.html [L,QSA]

# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
EOF

# Criar arquivo de instruções
echo "📋 Criando instruções de deploy..."
cat > INSTRUCOES_DEPLOY.txt << 'EOF'
🚀 INSTRUÇÕES DE DEPLOY PARA TEMVENDA.COM.BR

1. UPLOAD DOS ARQUIVOS:
   - Faça upload de todos os arquivos .html para a raiz do WordPress
   - Faça upload do auth-manager.js para a raiz do WordPress
   - Faça upload do logo-temvenda.png para a raiz do WordPress

2. CONFIGURAR .HTACCESS:
   - Substitua o conteúdo do .htaccess atual pelo conteúdo do arquivo .htaccess incluído
   - OU adicione as regras de redirecionamento ao .htaccess existente

3. TESTAR URLs:
   - https://temvenda.com.br/home-moderna
   - https://temvenda.com.br/diagnostico
   - https://temvenda.com.br/login-admin
   - https://temvenda.com.br/admin-panel

4. CREDENCIAIS:
   - Root: cesar / temvenda2024
   - Admin: admin / temvenda2024

5. SISTEMA DE NOTÍCIAS:
   - Configure cron job para executar news_collector.py
   - Verifique configurações do Supabase
   - Teste coleta automática de notícias

✅ DEPLOY COMPLETO!
EOF

echo "✅ Arquivos preparados para deploy!"
echo "📁 Diretório: deploy-temvenda/"
echo "📋 Instruções: deploy-temvenda/INSTRUCOES_DEPLOY.txt"
echo ""
echo "🚀 Próximos passos:"
echo "1. Fazer upload dos arquivos para temvenda.com.br"
echo "2. Configurar .htaccess"
echo "3. Testar todas as URLs"
echo "4. Configurar cron job para notícias"
