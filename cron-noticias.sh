#!/bin/bash

# 📰 Script de Coleta de Notícias - TEM VENDA
# Executa o coletor de notícias com análise de IA
# Roda automaticamente às quartas e sábados

# Configurações
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/news-$(date +%Y%m%d-%H%M%S).log"
ENV_FILE="$SCRIPT_DIR/.env"

# Criar diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Carregar variáveis de ambiente do arquivo .env se existir
if [ -f "$ENV_FILE" ]; then
    echo "📄 Carregando variáveis de ambiente de .env..." >> "$LOG_FILE"
    set -a
    source "$ENV_FILE"
    set +a
    echo "✅ Variáveis de ambiente carregadas" >> "$LOG_FILE"
fi

# Verificar se OpenAI API Key está configurada
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY não configurada!" >> "$LOG_FILE"
    echo "Configure: export OPENAI_API_KEY='sk-sua-chave-aqui'" >> "$LOG_FILE"
    echo "Ou adicione OPENAI_API_KEY=... ao arquivo .env" >> "$LOG_FILE"
    exit 1
fi

echo "🚀 Iniciando coleta de notícias..." >> "$LOG_FILE"
echo "📅 Data: $(date)" >> "$LOG_FILE"
echo "📁 Diretório: $SCRIPT_DIR" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Navegar para o diretório do script
cd "$SCRIPT_DIR"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!" >> "$LOG_FILE"
    exit 1
fi

# Verificar se news_collector.py existe
if [ ! -f "news_collector.py" ]; then
    echo "❌ news_collector.py não encontrado!" >> "$LOG_FILE"
    exit 1
fi

# Executar coletor
echo "📡 Executando coletor de notícias..." >> "$LOG_FILE"
python3 news_collector.py >> "$LOG_FILE" 2>&1

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "" >> "$LOG_FILE"
    echo "✅ Coleta concluída com sucesso!" >> "$LOG_FILE"
    echo "📊 Verifique o painel admin para aprovar notícias" >> "$LOG_FILE"
else
    echo "" >> "$LOG_FILE"
    echo "❌ Erro na coleta de notícias!" >> "$LOG_FILE"
    echo "📋 Verifique o log completo em: $LOG_FILE" >> "$LOG_FILE"
    exit 1
fi

# Limpar logs antigos (manter últimos 30 dias)
find "$LOG_DIR" -name "news-*.log" -mtime +30 -delete

echo "✅ Script executado com sucesso!"
echo "📋 Log completo em: $LOG_FILE"

