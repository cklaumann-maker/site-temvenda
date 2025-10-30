#!/bin/bash

# 🧹 Script de Limpeza Automatizado (sem perguntas)
# Move arquivos do deploy-wp-content/temvenda/ para a raiz e ajusta links

set -e

echo "🧹 LIMPEZA E ORGANIZAÇÃO DO DIRETÓRIO RAIZ"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Backup
echo -e "${BLUE}📦 Passo 1: Criando backup...${NC}"
BACKUP_DIR="backup-antes-limpeza-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r deploy-wp-content "$BACKUP_DIR/" 2>/dev/null || true
cp *.html "$BACKUP_DIR/" 2>/dev/null || true
cp *.md "$BACKUP_DIR/" 2>/dev/null || true
cp *.sh "$BACKUP_DIR/" 2>/dev/null || true
cp *.js "$BACKUP_DIR/" 2>/dev/null || true
cp *.png "$BACKUP_DIR/" 2>/dev/null || true
echo -e "${GREEN}✅ Backup criado em: $BACKUP_DIR/${NC}"
echo ""

# 2. Copiar arquivos
echo -e "${BLUE}📋 Passo 2: Copiando arquivos para a raiz...${NC}"
if [ ! -d "deploy-wp-content/temvenda" ]; then
    echo "❌ Erro: Pasta deploy-wp-content/temvenda não encontrada!"
    exit 1
fi

cp deploy-wp-content/temvenda/*.html . 2>/dev/null || true
cp deploy-wp-content/temvenda/*.js . 2>/dev/null || true
cp deploy-wp-content/temvenda/*.png . 2>/dev/null || true
echo -e "${GREEN}✅ Arquivos copiados!${NC}"
echo ""

# 3. Criar index.html também
if [ -f "home-corporativo.html" ]; then
    cp home-corporativo.html index.html
    echo -e "${GREEN}✅ index.html criado!${NC}"
fi
echo ""

# 4. Ajustar links
echo -e "${BLUE}🔧 Passo 3: Ajustando links...${NC}"
for file in *.html; do
    if [ -f "$file" ]; then
        echo "  Processando: $file"
        sed -i '' 's|href="/wp-content/temvenda/|href="/|g' "$file"
        sed -i '' 's|src="/wp-content/temvenda/|src="/|g' "$file"
        sed -i '' 's|/wp-content/temvenda/||g' "$file"
    fi
done

if [ -f "auth-manager.js" ]; then
    echo "  Processando: auth-manager.js"
    sed -i '' 's|/wp-content/temvenda/||g' auth-manager.js
fi
echo -e "${GREEN}✅ Links ajustados!${NC}"
echo ""

# 5. Criar .htaccess
echo -e "${BLUE}📄 Passo 4: Criando .htaccess...${NC}"
cat > .htaccess << 'EOF'
DirectoryIndex index.html home-corporativo.html
RewriteEngine On
RewriteBase /
RewriteRule ^$ index.html [L]
RewriteRule ^diagnostico$ diagnostico.html [L]
RewriteRule ^consultoria$ consultoria.html [L]
RewriteRule ^formacao-lideres$ formacao-lideres.html [L]
RewriteRule ^treinamento-incompany$ treinamento-incompany.html [L]
RewriteRule ^palestras$ palestras.html [L]
RewriteRule ^noticias$ noticias.html [L]
RewriteRule ^login-admin$ login-admin.html [L]
RewriteRule ^admin-panel$ admin-panel.html [L]
RewriteRule ^admin-stats$ admin-stats.html [L]
RewriteRule ^admin-users$ admin-users.html [L]
EOF
echo -e "${GREEN}✅ .htaccess criado!${NC}"
echo ""

# 6. Remover pastas desnecessárias
echo -e "${BLUE}🗑️  Passo 5: Removendo pastas desnecessárias...${NC}"
rm -rf deploy-temvenda elementor html-pages html-standalone logs 2>/dev/null || true
echo -e "${GREEN}✅ Pastas removidas!${NC}"
echo ""

# 7. Limpar documentação redundante
echo -e "${BLUE}📚 Passo 6: Limpando documentação redundante...${NC}"
rm -f ANALISE_COMERCIAL_IA.md CHECKLIST_DEPLOY.md CRON_SETUP.md \
    DEPLOY_TEMVENDA.md DEPLOY_WP_CONTENT.md GIT_DEPLOY_INSTRUCTIONS.md \
    GUIA_DEPLOY_TEMVENDA.md GUIA_WP_CONTENT_SIMPLES.md \
    INSTRUCOES_COMPLETAS.md MIGRATION_GUIDE.md \
    ONDE_ESTA_PASTA_RAIZ.md SISTEMA_COMPLETO.md \
    SISTEMA_FINAL_COMPLETO.md SUPABASE_SETUP.md 2>/dev/null || true
echo -e "${GREEN}✅ Documentação limpa!${NC}"
echo ""

# 8. Resumo
echo -e "${GREEN}✅ LIMPEZA CONCLUÍDA!${NC}"
echo ""
echo "📁 Arquivos na raiz:"
ls -lh *.html *.js *.png 2>/dev/null | awk '{print "  ✅ " $9}' | head -15
echo ""
echo "📋 Resumo:"
echo "  ✅ Backup em: $BACKUP_DIR"
echo "  ✅ Links ajustados"
echo "  ✅ .htaccess criado"
echo "  ✅ Pastas desnecessárias removidas"
echo ""
echo "🧪 PRÓXIMOS PASSOS:"
echo "  1. Teste: python3 -m http.server 8000"
echo "  2. Acesse: http://localhost:8000"
echo "  3. Teste todos os links"
echo ""
echo -e "${GREEN}🎉 Diretório organizado!${NC}"

