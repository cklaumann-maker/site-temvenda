#!/bin/bash

echo "🚀 Preparando deploy para servidor TemVenda..."

# Variáveis
BUILD_DIR="build-deploy"
APP_DIR="apps/web"

# Limpar build anterior
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Copiar código fonte
echo "📁 Copiando arquivos..."
cp -r $APP_DIR $BUILD_DIR/web
cp -r packages $BUILD_DIR/
cp package.json $BUILD_DIR/
cp pnpm-lock.yaml $BUILD_DIR/
cp pnpm-workspace.yaml $BUILD_DIR/

# Copiar arquivos de configuração
cp -r scripts $BUILD_DIR/ 2>/dev/null || true

# Remover node_modules (será instalado no servidor)
find $BUILD_DIR -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find $BUILD_DIR -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true

# Criar arquivo de instruções
cat > $BUILD_DIR/DEPLOY_INSTRUCTIONS.md << 'EOF'
# Instruções de Deploy

1. Faça upload desta pasta para o servidor
2. Execute os comandos em DEPLOY_STEPS.sh
EOF

# Criar script de deploy para o servidor
cat > $BUILD_DIR/DEPLOY_STEPS.sh << 'EOF'
#!/bin/bash

echo "🚀 Iniciando deploy no servidor..."

# Instalar dependências
pnpm install --frozen-lockfile --prod

# Build da aplicação
cd apps/web
pnpm build

# Criar diretório de produção
mkdir -p /var/www/rotina-app
cp -r .next /var/www/rotina-app/
cp -r public /var/www/rotina-app/ 2>/dev/null || true
cp package.json /var/www/rotina-app/
cp next.config.js /var/www/rotina-app/
cp .env.production /var/www/rotina-app/.env

# Instalar apenas dependências de produção
cd /var/www/rotina-app
pnpm install --frozen-lockfile --prod

echo "✅ Deploy concluído!"
EOF

chmod +x $BUILD_DIR/DEPLOY_STEPS.sh

echo "✅ Arquivos preparados em: $BUILD_DIR/"
echo ""
echo "📤 Próximo passo: Faça upload da pasta $BUILD_DIR para o servidor"

