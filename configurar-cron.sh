#!/bin/bash

# ⚙️ Configurador de Cron para Notícias TEM VENDA
# Configura o cron para rodar quartas e sábados às 08:00

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_SCRIPT="$SCRIPT_DIR/cron-noticias.sh"

echo "⚙️ CONFIGURANDO CRON PARA NOTÍCIAS TEM VENDA"
echo "============================================="
echo ""

# Tornar script executável
chmod +x "$CRON_SCRIPT"
echo "✅ Script tornado executável: $CRON_SCRIPT"
echo ""

# Verificar se já existe entrada no crontab
if crontab -l 2>/dev/null | grep -q "cron-noticias.sh"; then
    echo "⚠️  Cron já configurado!"
    echo ""
    echo "📋 Entradas atuais:"
    crontab -l 2>/dev/null | grep "cron-noticias.sh"
    echo ""
    read -p "Deseja reconfigurar? (s/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Configuração cancelada"
        exit 0
    fi
    
    # Remover entradas antigas
    crontab -l 2>/dev/null | grep -v "cron-noticias.sh" | crontab -
    echo "✅ Entradas antigas removidas"
fi

# Criar nova entrada
NEW_CRON="0 8 * * 3,6 cd $SCRIPT_DIR && $CRON_SCRIPT"

# Adicionar ao crontab
(crontab -l 2>/dev/null; echo "$NEW_CRON") | crontab -

echo "✅ Cron configurado com sucesso!"
echo ""
echo "📅 Agendamento:"
echo "  - Quartas-feiras às 08:00"
echo "  - Sábados às 08:00"
echo ""
echo "📋 Entrada criada:"
echo "  $NEW_CRON"
echo ""
echo "🔍 Verificar crontab:"
echo "  crontab -l"
echo ""
echo "📋 Verificar logs após execução:"
echo "  tail -f logs/news-*.log"
echo ""
echo "⚠️  IMPORTANTE: Configure OPENAI_API_KEY antes da primeira execução!"
echo "  export OPENAI_API_KEY='sk-sua-chave-aqui'"
echo "  (Adicione ao .env ou ao crontab)"


