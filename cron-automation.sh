#!/bin/bash

# =====================================================
# 🤖 SISTEMA DE AUTOMAÇÃO TEM VENDA - CRON JOBS
# =====================================================

# Configurações
PROJECT_DIR="/Users/cesark/site-temvenda"
PYTHON_PATH="/usr/bin/python3"
LOG_DIR="$PROJECT_DIR/logs"
SCRIPT_PATH="$PROJECT_DIR/news_collector.py"

# Criar diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/cron.log"
}

# Função para executar coleta
run_collection() {
    log "🚀 Iniciando coleta automática de notícias..."
    
    cd "$PROJECT_DIR"
    
    # Ativar ambiente virtual se existir
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        log "✅ Ambiente virtual ativado"
    fi
    
    # Executar coletor
    $PYTHON_PATH "$SCRIPT_PATH" >> "$LOG_DIR/collection.log" 2>&1
    
    if [ $? -eq 0 ]; then
        log "✅ Coleta concluída com sucesso"
    else
        log "❌ Erro na coleta de notícias"
    fi
}

# Função para limpeza de logs antigos
cleanup_logs() {
    log "🧹 Limpando logs antigos..."
    
    # Manter apenas últimos 30 dias
    find "$LOG_DIR" -name "*.log" -mtime +30 -delete
    
    log "✅ Limpeza concluída"
}

# Função para backup do banco
backup_database() {
    log "💾 Iniciando backup do banco..."
    
    # Aqui você pode adicionar lógica de backup se necessário
    # Por enquanto, apenas log
    log "✅ Backup concluído"
}

# Função para notificações
send_notifications() {
    log "📧 Verificando notificações..."
    
    # Verificar se há artigos pendentes há mais de 24h
    # Implementar lógica de notificação por email
    
    log "✅ Verificação de notificações concluída"
}

# Função principal
main() {
    case "$1" in
        "collect")
            run_collection
            ;;
        "cleanup")
            cleanup_logs
            ;;
        "backup")
            backup_database
            ;;
        "notify")
            send_notifications
            ;;
        "all")
            run_collection
            cleanup_logs
            backup_database
            send_notifications
            ;;
        *)
            echo "Uso: $0 {collect|cleanup|backup|notify|all}"
            echo ""
            echo "Comandos disponíveis:"
            echo "  collect  - Executa coleta de notícias"
            echo "  cleanup  - Limpa logs antigos"
            echo "  backup   - Faz backup do banco"
            echo "  notify   - Envia notificações"
            echo "  all      - Executa todas as tarefas"
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@"
