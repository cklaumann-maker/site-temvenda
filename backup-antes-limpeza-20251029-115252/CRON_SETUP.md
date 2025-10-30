# 🤖 CONFIGURAÇÃO DE CRON JOBS - TEM VENDA

## 📅 **CRON JOBS RECOMENDADOS**

### 1. **Coleta de Notícias (A cada 6 horas)**
```bash
# Adicionar ao crontab (crontab -e)
0 */6 * * * /Users/cesark/site-temvenda/cron-automation.sh collect
```

### 2. **Limpeza de Logs (Diário às 2h)**
```bash
0 2 * * * /Users/cesark/site-temvenda/cron-automation.sh cleanup
```

### 3. **Backup do Banco (Semanal aos domingos às 3h)**
```bash
0 3 * * 0 /Users/cesark/site-temvenda/cron-automation.sh backup
```

### 4. **Notificações (Diário às 9h)**
```bash
0 9 * * * /Users/cesark/site-temvenda/cron-automation.sh notify
```

### 5. **Execução Completa (Diário às 6h)**
```bash
0 6 * * * /Users/cesark/site-temvenda/cron-automation.sh all
```

## 🔧 **CONFIGURAÇÃO**

### 1. **Instalar Dependências**
```bash
cd /Users/cesark/site-temvenda
pip install -r requirements.txt
```

### 2. **Configurar Variáveis de Ambiente**
```bash
cp env.example .env
# Editar .env com suas configurações
```

### 3. **Configurar Crontab**
```bash
# Abrir editor de crontab
crontab -e

# Adicionar as linhas dos cron jobs acima
```

### 4. **Testar Execução**
```bash
# Testar coleta manual
./cron-automation.sh collect

# Testar todas as funções
./cron-automation.sh all
```

## 📊 **MONITORAMENTO**

### Logs Disponíveis:
- `logs/cron.log` - Log geral do sistema
- `logs/collection.log` - Log específico da coleta
- `logs/backup.log` - Log de backups
- `logs/notifications.log` - Log de notificações

### Verificar Status:
```bash
# Ver logs em tempo real
tail -f logs/cron.log

# Verificar últimos cron jobs
grep CRON /var/log/syslog | tail -10
```

## ⚙️ **CONFIGURAÇÕES AVANÇADAS**

### Frequência Personalizada:
- **Muito Ativa**: A cada 2 horas (`0 */2 * * *`)
- **Moderada**: A cada 6 horas (`0 */6 * * *`)
- **Conservadora**: A cada 12 horas (`0 */12 * * *`)

### Horários Personalizados:
- **Horário Comercial**: `0 8-18 * * 1-5`
- **Finais de Semana**: `0 10,14,18 * * 0,6`
- **Noturno**: `0 2,6,10 * * *`

## 🚨 **TROUBLESHOOTING**

### Problemas Comuns:

1. **Permissões**: `chmod +x cron-automation.sh`
2. **Python Path**: Verificar `which python3`
3. **Dependências**: `pip install -r requirements.txt`
4. **Variáveis**: Verificar arquivo `.env`

### Comandos de Diagnóstico:
```bash
# Verificar se cron está rodando
sudo systemctl status cron

# Ver logs de erro
journalctl -u cron

# Testar script manualmente
./cron-automation.sh collect
```

## 📈 **OTIMIZAÇÕES**

### Performance:
- Limitar artigos por execução
- Usar cache para fontes
- Otimizar queries do banco

### Recursos:
- Monitorar uso de CPU/memória
- Configurar limites de tempo
- Implementar retry automático

---

**🎯 Sistema configurado para funcionar automaticamente!**
