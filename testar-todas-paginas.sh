#!/bin/bash

# 🧪 Script de Teste Completo - Todas as Páginas
# Testa todas as páginas e verifica links funcionando

echo "🧪 TESTE COMPLETO DE TODAS AS PÁGINAS"
echo "======================================"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BASE_URL="http://localhost:8000"
PAGES=(
    "index.html"
    "home-corporativo.html"
    "consultoria.html"
    "formacao-lideres.html"
    "treinamento-incompany.html"
    "palestras.html"
    "diagnostico.html"
    "noticias.html"
    "login-admin.html"
)

# Contadores
TOTAL=0
SUCCESS=0
FAILED=0

echo -e "${BLUE}📄 TESTANDO PÁGINAS PRINCIPAIS...${NC}"
echo ""

for page in "${PAGES[@]}"; do
    TOTAL=$((TOTAL + 1))
    echo -n "  Testando: $page ... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$page" 2>/dev/null)
    
    if [ "$status" = "200" ]; then
        echo -e "${GREEN}✅ OK (200)${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}❌ FALHOU ($status)${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo -e "${BLUE}🔗 TESTANDO LINKS INTERNOS...${NC}"
echo ""

# Testar links na home-corporativo
echo "  Links em home-corporativo.html:"
for link in consultoria formacao-lideres treinamento-incompany palestras diagnostico noticias; do
    echo -n "    /$link ... "
    # Verificar se o link existe no HTML
    if curl -s "$BASE_URL/home-corporativo.html" | grep -q "href=\"/$link"; then
        # Testar se a página existe
        status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$link.html" 2>/dev/null)
        if [ "$status" = "200" ]; then
            echo -e "${GREEN}✅${NC}"
        else
            echo -e "${YELLOW}⚠️  Link existe mas página retorna $status${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Link não encontrado no HTML${NC}"
    fi
done

echo ""
echo -e "${BLUE}🖼️  TESTANDO ASSETS...${NC}"
echo ""

# Testar logo
echo -n "  logo-temvenda.png ... "
logo_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/logo-temvenda.png" 2>/dev/null)
if [ "$logo_status" = "200" ]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ Não encontrado ($logo_status)${NC}"
fi

# Testar auth-manager.js
echo -n "  auth-manager.js ... "
js_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/auth-manager.js" 2>/dev/null)
if [ "$js_status" = "200" ]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${YELLOW}⚠️  Não encontrado ($js_status)${NC}"
fi

echo ""
echo -e "${BLUE}🔐 TESTANDO ÁREA ADMINISTRATIVA...${NC}"
echo ""

ADMIN_PAGES=("login-admin.html" "admin-panel.html" "admin-stats.html" "admin-users.html")
for admin_page in "${ADMIN_PAGES[@]}"; do
    echo -n "  $admin_page ... "
    status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$admin_page" 2>/dev/null)
    if [ "$status" = "200" ]; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ FALHOU ($status)${NC}"
    fi
done

echo ""
echo -e "${BLUE}📊 TESTANDO FOOTERS...${NC}"
echo ""

FOOTER_PAGES=("consultoria.html" "formacao-lideres.html" "treinamento-incompany.html" "palestras.html")
for footer_page in "${FOOTER_PAGES[@]}"; do
    echo -n "  Footer em $footer_page ... "
    # Verificar se tem botão admin
    admin_btn=$(curl -s "$BASE_URL/$footer_page" | grep -c 'class="admin-btn"')
    footer_section=$(curl -s "$BASE_URL/$footer_page" | grep -c '<h3>Admin</h3>')
    
    if [ "$admin_btn" -gt 0 ] && [ "$footer_section" -gt 0 ]; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ Footer incompleto${NC}"
    fi
done

echo ""
echo "=========================================="
echo -e "${GREEN}✅ TESTE CONCLUÍDO!${NC}"
echo ""
echo "📊 Resumo:"
echo "  Total de páginas testadas: $TOTAL"
echo "  Sucesso: $SUCCESS"
echo "  Falhas: $FAILED"
echo ""
echo "🌐 Acesse: $BASE_URL"
echo ""
echo "📋 Páginas para testar manualmente:"
for page in "${PAGES[@]}"; do
    echo "  • $BASE_URL/$page"
done


