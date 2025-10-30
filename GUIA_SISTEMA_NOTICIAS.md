# 📰 SISTEMA DE NOTÍCIAS TEM VENDA - GUIA COMPLETO

## 🎯 COMO FUNCIONA O SISTEMA

### **📊 VISÃO GERAL**

O sistema de notícias funciona de forma **semi-automática**:

1. **🤖 Coleta Automática** → Script Python coleta notícias de sites farmacêuticos
2. **🧠 Análise com IA** → ChatGPT analisa cada notícia e gera insights comerciais
3. **💾 Armazenamento** → Notícias são salvas no Supabase com status "pending"
4. **👤 Aprovação Manual** → Você aprova/rejeita notícias no painel admin
5. **📰 Publicação** → Notícias aprovadas aparecem na página pública

---

## 🔄 FLUXO COMPLETO

```
┌─────────────────┐
│  Sites RSS      │
│  (Fontes)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  news_collector │────▶│  OpenAI API     │
│  .py            │     │  (ChatGPT)      │
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Supabase       │
│  (status:       │
│   pending)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Admin Panel    │
│  (Aprovação)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Página Pública │
│  (status:       │
│   approved)     │
└─────────────────┘
```

---

## 🤖 CONEXÃO COM CHATGPT - JÁ ESTÁ PRONTO!

### **✅ Status Atual:**
- ✅ **Código pronto:** `news_collector.py` já usa OpenAI
- ✅ **Análise comercial:** ChatGPT gera insights automaticamente
- ⚠️ **Falta configurar:** Apenas a chave da API (OPENAI_API_KEY)

### **🔑 O QUE VOCÊ PRECISA FAZER:**

1. **Obter chave da OpenAI:**
   - Acesse: https://platform.openai.com/api-keys
   - Crie uma conta (se não tiver)
   - Gere uma nova chave de API

2. **Configurar variável de ambiente:**
   ```bash
   export OPENAI_API_KEY="sk-sua-chave-aqui"
   ```

3. **Ou criar arquivo `.env`:**
   ```bash
   echo "OPENAI_API_KEY=sk-sua-chave-aqui" > .env
   ```

---

## 📅 CONFIGURAÇÃO PARA RODAR 2X POR SEMANA

### **🎯 Objetivo:**
- **Quartas-feiras:** Coleta de notícias
- **Sábados:** Coleta de notícias
- **Você aprova:** Nas quartas e sábados, após a coleta

### **⚙️ Configuração do Cron:**

```bash
# Editar crontab
crontab -e

# Adicionar estas linhas:
# Quartas-feiras às 08:00
0 8 * * 3 cd /caminho/para/site-temvenda && /usr/bin/python3 news_collector.py >> logs/news-wednesday.log 2>&1

# Sábados às 08:00
0 8 * * 6 cd /caminho/para/site-temvenda && /usr/bin/python3 news_collector.py >> logs/news-saturday.log 2>&1
```

---

## 🧠 O QUE O CHATGPT FAZ AUTOMATICAMENTE

### **📊 Análise Comercial Completa:**

Para cada notícia, o ChatGPT gera:

1. **🎯 Impacto no Negócio** (Alta/Média/Baixa)
   - Como a notícia afeta o mercado farmacêutico

2. **💰 Oportunidades de Vendas**
   - Identifica chances de crescimento de receita

3. **⚡ Vantagem Competitiva**
   - Como usar a informação para se destacar

4. **📋 Ações Práticas**
   - O que o gestor pode fazer imediatamente

5. **⚠️ Fatores de Risco**
   - Desafios e riscos identificados

6. **📈 Tendências de Mercado**
   - Movimentos do setor

7. **📋 Resumo Executivo**
   - Para tomada de decisão rápida

### **💡 Exemplo de Análise:**

**Notícia:** "Anvisa aprova novo genérico para hipertensão"

**Análise ChatGPT:**
- **Impacto:** Alta
- **Oportunidade:** Aumentar mix de genéricos pode elevar margem
- **Ação:** Treinar equipe sobre novo medicamento
- **Vantagem:** Posicionar-se como especialista em genéricos

---

## 🚀 COMO USAR

### **1. Configuração Inicial (Uma vez apenas):**

```bash
# Instalar dependências Python
pip3 install -r requirements.txt

# Configurar OpenAI API Key
export OPENAI_API_KEY="sk-sua-chave-aqui"

# Testar coleta manual
python3 news_collector.py
```

### **2. Configurar Cron (Quartas e Sábados):**

```bash
# Criar script de cron
cat > cron-noticias.sh << 'EOF'
#!/bin/bash
cd /caminho/para/site-temvenda
export OPENAI_API_KEY="sk-sua-chave-aqui"
/usr/bin/python3 news_collector.py >> logs/news-$(date +\%Y\%m\%d).log 2>&1
EOF

chmod +x cron-noticias.sh

# Adicionar ao crontab
crontab -e
# Adicionar:
0 8 * * 3,6 /caminho/para/cron-noticias.sh
```

### **3. Após Cada Coleta:**

1. Acesse: `http://localhost:8000/admin-panel.html`
2. Revise as notícias coletadas
3. Aprove as relevantes
4. Rejeite as não relevantes

---

## 📋 REQUISITOS DO SISTEMA

### **✅ Já Configurado:**
- ✅ Supabase conectado
- ✅ Código Python pronto
- ✅ Análise com IA implementada
- ✅ Painel admin funcionando

### **⚠️ Você Precisa:**
- ⚠️ Chave da OpenAI API (gratuita até certo limite)
- ⚠️ Servidor para rodar cron (ou usar serviço de cron online)

---

## 💰 CUSTOS

### **OpenAI API:**
- **Modelo usado:** GPT-3.5-turbo (mais barato)
- **Custo aproximado:** ~$0.001-0.002 por notícia
- **2x por semana:** ~$0.50-1.00 por mês
- **Plano gratuito:** $5 créditos grátis (suficiente para vários meses)

### **Alternativas Gratuitas:**
- Se quiser economizar, o sistema funciona sem IA (análise básica)
- Mas os insights não serão tão poderosos

---

## 🔧 TROUBLESHOOTING

### **Erro: OpenAI não configurada**
```bash
export OPENAI_API_KEY="sk-sua-chave"
```

### **Erro: Módulos Python não encontrados**
```bash
pip3 install supabase openai beautifulsoup4 feedparser requests
```

### **Erro: Cron não roda**
```bash
# Verificar logs
tail -f logs/news-*.log

# Testar manualmente
python3 news_collector.py
```

---

## 📊 MONITORAMENTO

### **Verificar Coletas:**
```bash
# Ver últimas coletas
tail -f logs/news_collector.log

# Ver notícias pendentes no Supabase
# Acesse admin-panel.html
```

### **Estatísticas:**
- Painel admin mostra estatísticas em tempo real
- Total de notícias coletadas
- Taxa de aprovação
- Notícias por categoria

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

- [ ] Criar conta OpenAI
- [ ] Obter chave da API
- [ ] Configurar OPENAI_API_KEY
- [ ] Instalar dependências Python
- [ ] Testar coleta manual
- [ ] Configurar cron para quartas e sábados
- [ ] Verificar logs após primeira execução
- [ ] Aprovar notícias no painel admin

---

**Última atualização:** $(date)


