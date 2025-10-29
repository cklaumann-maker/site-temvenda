#!/bin/bash

# Script de migração WordPress para GitHub
# Execute este script após baixar os arquivos do servidor

echo "🚀 Iniciando migração do WordPress para GitHub..."

# Criar diretório wordpress se não existir
if [ ! -d "wordpress" ]; then
    mkdir wordpress
    echo "✅ Diretório wordpress criado"
fi

# Verificar se os arquivos foram baixados
if [ ! -f "wordpress/wp-config.php" ]; then
    echo "❌ Arquivo wp-config.php não encontrado!"
    echo "📋 Instruções:"
    echo "1. Baixe todos os arquivos do servidor via FTP para a pasta 'wordpress/'"
    echo "2. Execute este script novamente"
    exit 1
fi

echo "✅ Arquivos WordPress encontrados"

# Criar wp-config-local.php baseado no wp-config.php original
if [ -f "wordpress/wp-config.php" ]; then
    cp wordpress/wp-config.php wordpress/wp-config-production.php
    echo "✅ Backup do wp-config.php criado como wp-config-production.php"
fi

# Criar wp-config.php para ambiente local
cat > wordpress/wp-config.php << 'EOF'
<?php
/**
 * Configuração WordPress para ambiente local
 */

// Configurações do banco de dados
define('DB_NAME', 'temvenda_db');
define('DB_USER', 'wordpress');
define('DB_PASSWORD', 'wordpress_password');
define('DB_HOST', 'db:3306');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

// Chaves de segurança (gerar novas em: https://api.wordpress.org/secret-key/1.1/salt/)
define('AUTH_KEY',         'coloque-sua-chave-aqui');
define('SECURE_AUTH_KEY',  'coloque-sua-chave-aqui');
define('LOGGED_IN_KEY',    'coloque-sua-chave-aqui');
define('NONCE_KEY',        'coloque-sua-chave-aqui');
define('AUTH_SALT',        'coloque-sua-chave-aqui');
define('SECURE_AUTH_SALT', 'coloque-sua-chave-aqui');
define('LOGGED_IN_SALT',   'coloque-sua-chave-aqui');
define('NONCE_SALT',       'coloque-sua-chave-aqui');

// Prefixo das tabelas do banco
$table_prefix = 'wp_';

// Configurações de debug
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);

// URLs do site
define('WP_HOME', 'http://localhost:8080');
define('WP_SITEURL', 'http://localhost:8080');

// Configurações de memória
ini_set('memory_limit', '256M');

// Configurações de upload
define('WP_MEMORY_LIMIT', '256M');

// Desabilitar edição de arquivos via admin
define('DISALLOW_FILE_EDIT', true);

// Configurações de cache (se usar)
// define('WP_CACHE', true);

if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}

require_once ABSPATH . 'wp-settings.php';
EOF

echo "✅ wp-config.php para ambiente local criado"

# Criar diretório para uploads se não existir
if [ ! -d "wordpress/wp-content/uploads" ]; then
    mkdir -p wordpress/wp-content/uploads
    echo "✅ Diretório de uploads criado"
fi

# Criar arquivo .htaccess básico
cat > wordpress/.htaccess << 'EOF'
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

echo "✅ Arquivo .htaccess criado"

echo ""
echo "🎉 Migração concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: docker-compose up -d"
echo "2. Acesse: http://localhost:8080"
echo "3. Importe o banco de dados via phpMyAdmin (http://localhost:8081)"
echo "4. Configure o WordPress com as credenciais do banco local"
echo ""
echo "⚠️  Lembre-se de:"
echo "- Gerar novas chaves de segurança em: https://api.wordpress.org/secret-key/1.1/salt/"
echo "- Atualizar as URLs no banco de dados após importar"
echo "- Fazer backup antes de qualquer alteração"
