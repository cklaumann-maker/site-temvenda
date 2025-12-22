#!/bin/bash

# 🚀 Script de Deploy: GitHub → InfinityFree
# Automatiza o processo de preparação e upload

echo "🚀 Deploy do GitHub para InfinityFree"
echo "======================================"
echo ""

# Configurações (AJUSTE AQUI)
GITHUB_REPO="https://github.com/cklaumann-maker/site-temvenda.git"
REPO_DIR="temp-site-clone"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Clonar ou atualizar repositório
echo -e "${BLUE}📥 Passo 1: Clonando/Atualizando repositório do GitHub...${NC}"
if [ -d "$REPO_DIR" ]; then
    echo "Repositório já existe, atualizando..."
    cd "$REPO_DIR"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
    cd ..
else
    echo "Clonando repositório..."
    git clone "$GITHUB_REPO" "$REPO_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao clonar repositório. Verifique a URL do GitHub."
        exit 1
    fi
fi

echo -e "${GREEN}✅ Repositório atualizado!${NC}"
echo ""

# 2. Preparar arquivos para FTP
echo -e "${BLUE}🔧 Passo 2: Preparando arquivos para FTP...${NC}"
cd "$REPO_DIR"

# Verificar se o script existe
if [ ! -f "preparar-ftp.sh" ]; then
    echo "⚠️ Script preparar-ftp.sh não encontrado."
    echo "Criando estrutura manualmente..."
    
    # Criar diretório de deploy
    mkdir -p deploy-ftp
    
    # Copiar arquivos de deploy-wp-content/temvenda
    if [ -d "deploy-wp-content/temvenda" ]; then
        cp -r deploy-wp-content/temvenda/* deploy-ftp/
    else
        echo "❌ Pasta deploy-wp-content/temvenda não encontrada!"
        exit 1
    fi
    
    # Ajustar caminhos
    find deploy-ftp -name "*.html" -type f | while read file; do
        sed -i '' 's|href="/wp-content/temvenda/|href="/|g' "$file"
        sed -i '' 's|src="/wp-content/temvenda/|src="/|g' "$file"
        sed -i '' 's|/wp-content/temvenda/||g' "$file"
    done
else
    # Executar script existente
    chmod +x preparar-ftp.sh
    ./preparar-ftp.sh
fi

echo -e "${GREEN}✅ Arquivos preparados!${NC}"
echo ""

# 3. Mostrar arquivos prontos
echo -e "${BLUE}📋 Arquivos prontos para upload:${NC}"
ls -lh deploy-ftp/ | grep -E "\.(html|js|png)$" | awk '{print "  ✅ " $9 " (" $5 ")"}'
echo ""

# 4. Instruções para FTP
echo -e "${YELLOW}📤 Próximos passos para fazer upload via FTP:${NC}"
echo ""
echo "1. Abra o FileZilla (ou outro cliente FTP)"
echo "2. Conecte ao servidor:"
echo "   - Host: ftp.infinityfree.net"
echo "   - Usuário: (seu usuário InfinityFree)"
echo "   - Senha: (sua senha InfinityFree)"
echo "   - Porta: 21"
echo ""
echo "3. Navegue até: htdocs/ ou public_html/"
echo ""
echo "4. Faça upload dos arquivos de:"
echo "   $REPO_DIR/deploy-ftp/"
echo ""
echo "5. Teste em: http://seudominio.com.br/home-corporativo.html"
echo ""

# 5. Opção de upload automático (se curl estiver disponível)
read -p "Deseja fazer upload automático via FTP? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}📤 Configurando upload automático...${NC}"
    echo ""
    read -p "FTP Host (ex: ftp.infinityfree.net): " FTP_HOST
    read -p "FTP Usuário: " FTP_USER
    read -sp "FTP Senha: " FTP_PASS
    echo ""
    read -p "FTP Diretório (ex: htdocs): " FTP_DIR
    
    echo ""
    echo "📤 Fazendo upload..."
    
    cd deploy-ftp
    for file in *; do
        if [ -f "$file" ]; then
            echo "  Enviando: $file"
            curl -T "$file" "ftp://$FTP_USER:$FTP_PASS@$FTP_HOST/$FTP_DIR/" 2>/dev/null
            if [ $? -eq 0 ]; then
                echo -e "  ${GREEN}✅ $file enviado!${NC}"
            else
                echo -e "  ${YELLOW}⚠️ Erro ao enviar $file${NC}"
            fi
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ Upload concluído!${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Processo concluído!${NC}"
echo ""
echo "📁 Arquivos prontos em: $REPO_DIR/deploy-ftp/"
echo "🌐 Acesse seu site após o upload!"


