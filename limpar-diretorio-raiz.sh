#!/bin/bash

# 🧹 Script de Limpeza e Organização do Diretório Raiz
# Move arquivos do deploy-wp-content/temvenda/ para a raiz e ajusta links

set -e  # Para em caso de erro

echo "🧹 LIMPEZA E ORGANIZAÇÃO DO DIRETÓRIO RAIZ"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Backup
echo -e "${BLUE}📦 Passo 1: Criando backup...${NC}"
BACKUP_DIR="backup-antes-limpeza-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Fazer backup dos arquivos importantes
echo "  Fazendo backup dos arquivos..."
cp -r deploy-wp-content "$BACKUP_DIR/" 2>/dev/null || true
cp *.html "$BACKUP_DIR/" 2>/dev/null || true
cp *.md "$BACKUP_DIR/" 2>/dev/null || true
cp *.sh "$BACKUP_DIR/" 2>/dev/null || true
cp *.js "$BACKUP_DIR/" 2>/dev/null || true
cp *.png "$BACKUP_DIR/" 2>/dev/null || true

echo -e "${GREEN}✅ Backup criado em: $BACKUP_DIR/${NC}"
echo ""

# 2. Copiar arquivos de deploy-wp-content/temvenda/ para a raiz
echo -e "${BLUE}📋 Passo 2: Copiando arquivos para a raiz...${NC}"

if [ ! -d "deploy-wp-content/temvenda" ]; then
    echo -e "${RED}❌ Erro: Pasta deploy-wp-content/temvenda não encontrada!${NC}"
    exit 1
fi

# Copiar todos os arquivos HTML, JS e PNG
cp deploy-wp-content/temvenda/*.html . 2>/dev/null || true
cp deploy-wp-content/temvenda/*.js . 2>/dev/null || true
cp deploy-wp-content/temvenda/*.png . 2>/dev/null || true

echo -e "${GREEN}✅ Arquivos copiados!${NC}"
echo ""

# 3. Renomear home-corporativo.html para index.html (opcional)
read -p "Deseja renomear home-corporativo.html para index.html? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    if [ -f "home-corporativo.html" ]; then
        cp home-corporativo.html index.html
        echo -e "${GREEN}✅ index.html criado!${NC}"
    fi
fi
echo ""

# 4. Ajustar links em todos os arquivos HTML
echo -e "${BLUE}🔧 Passo 3: Ajustando links (removendo /wp-content/temvenda/)...${NC}"

for file in *.html; do
    if [ -f "$file" ]; then
        echo "  Processando: $file"
        
        # Remover /wp-content/temvenda/ de links href
        sed -i '' 's|href="/wp-content/temvenda/|href="/|g' "$file"
        
        # Remover /wp-content/temvenda/ de imagens src
        sed -i '' 's|src="/wp-content/temvenda/|src="/|g' "$file"
        
        # Remover /wp-content/temvenda/ de scripts src
        sed -i '' 's|src="/wp-content/temvenda/|src="/|g' "$file"
        
        # Ajustar links relativos que ainda tenham /wp-content/temvenda/
        sed -i '' 's|/wp-content/temvenda/||g' "$file"
        
        # Ajustar links que apontam para home-corporativo
        sed -i '' 's|href="/home-corporativo.html|href="/index.html|g' "$file" 2>/dev/null || true
        sed -i '' 's|href="/home-corporativo|href="/index.html|g' "$file" 2>/dev/null || true
    fi
done

# Ajustar auth-manager.js se existir
if [ -f "auth-manager.js" ]; then
    echo "  Processando: auth-manager.js"
    sed -i '' 's|/wp-content/temvenda/||g' auth-manager.js
fi

echo -e "${GREEN}✅ Links ajustados!${NC}"
echo ""

# 5. Criar .htaccess com redirecionamentos
echo -e "${BLUE}📄 Passo 4: Criando .htaccess...${NC}"

cat > .htaccess << 'EOF'
# Configuração TEM VENDA
DirectoryIndex index.html home-corporativo.html

# Ativar RewriteEngine
RewriteEngine On
RewriteBase /

# Redirecionar raiz para index/home
RewriteRule ^$ index.html [L]
RewriteRule ^$ home-corporativo.html [L]

# Redirecionamentos de URLs sem .html
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

# Bloquear acesso a arquivos sensíveis
<FilesMatch "^\.">
    Order allow,deny
    Deny from all
</FilesMatch>
EOF

echo -e "${GREEN}✅ .htaccess criado!${NC}"
echo ""

# 6. Remover pastas desnecessárias (OPCIONAL - com confirmação)
echo -e "${YELLOW}🗑️  Passo 5: Remoção de pastas desnecessárias${NC}"
echo ""
echo "Pastas que podem ser removidas:"
echo "  - deploy-temvenda/"
echo "  - elementor/"
echo "  - html-pages/"
echo "  - html-standalone/"
echo "  - logs/"
echo ""
read -p "Deseja remover essas pastas? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "  Removendo pastas..."
    rm -rf deploy-temvenda elementor html-pages html-standalone logs
    echo -e "${GREEN}✅ Pastas removidas!${NC}"
else
    echo -e "${YELLOW}⚠️  Pastas mantidas.${NC}"
fi
echo ""

# 7. Limpar documentação redundante (OPCIONAL)
echo -e "${YELLOW}📚 Passo 6: Limpeza de documentação redundante${NC}"
echo ""
read -p "Deseja remover documentação redundante? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "  Removendo arquivos de documentação redundantes..."
    rm -f ANALISE_COMERCIAL_IA.md CHECKLIST_DEPLOY.md CRON_SETUP.md \
        DEPLOY_TEMVENDA.md DEPLOY_WP_CONTENT.md GIT_DEPLOY_INSTRUCTIONS.md \
        GUIA_DEPLOY_TEMVENDA.md GUIA_WP_CONTENT_SIMPLES.md \
        INSTRUCOES_COMPLETAS.md MIGRATION_GUIDE.md \
        ONDE_ESTA_PASTA_RAIZ.md SISTEMA_COMPLETO.md \
        SISTEMA_FINAL_COMPLETO.md SUPABASE_SETUP.md
    echo -e "${GREEN}✅ Documentação limpa!${NC}"
else
    echo -e "${YELLOW}⚠️  Documentação mantida.${NC}"
fi
echo ""

# 8. Resumo final
echo -e "${GREEN}✅ LIMPEZA CONCLUÍDA!${NC}"
echo ""
echo "📁 Estrutura final na raiz:"
ls -lh *.html *.js *.png 2>/dev/null | awk '{print "  ✅ " $9}'
echo ""
echo "📋 Arquivos importantes:"
echo "  ✅ .htaccess criado"
echo "  ✅ Links ajustados"
echo "  ✅ Backup em: $BACKUP_DIR"
echo ""
echo "🧪 PRÓXIMOS PASSOS:"
echo "  1. Teste localmente: python3 -m http.server 8000"
echo "  2. Acesse: http://localhost:8000"
echo "  3. Teste todos os links"
echo "  4. Se tudo estiver OK, faça commit no Git"
echo ""
echo -e "${GREEN}🎉 Diretório organizado e pronto!${NC}"


