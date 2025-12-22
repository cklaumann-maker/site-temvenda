# 🔍 Diagnóstico: Automação de Coleta de Notícias

## ❌ Problemas Identificados

### 1. **Workflows do GitHub Actions NÃO foram commitados**

**Status:**
- ✅ Arquivos existem localmente: `.github/workflows/news-automation.yml` e `.github/workflows/news-automation-daily.yml`
- ❌ **NÃO foram commitados no Git**
- ❌ **NÃO foram enviados para o GitHub**

**Evidência:**
```bash
git status .github/workflows/
# Mostra:
# - modified: .github/workflows/news-automation.yml
# - untracked: .github/workflows/news-automation-daily.yml
```

**Impacto:** Os workflows não existem no GitHub, então não podem rodar automaticamente.

---

### 2. **Cron Jobs Locais estão FALHANDO**

**Status:**
- ✅ Cron jobs configurados (rodam a cada 6 horas)
- ❌ **Últimas execuções falharam**

**Evidência dos logs:**
```
[2025-11-17 12:00:03] 🚀 Iniciando coleta automática de notícias...
[2025-11-17 12:00:08] ❌ Erro na coleta de notícias
```

**Última execução bem-sucedida:** Não encontrada nos logs recentes

**Impacto:** A automação local não está funcionando.

---

## ✅ Soluções

### **Solução 1: Ativar GitHub Actions (Recomendado - Cloud)**

#### **Passo 1: Commit e Push dos Workflows**

```bash
cd /Users/cesark/site-temvenda

# Adicionar workflows ao Git
git add .github/workflows/news-automation.yml
git add .github/workflows/news-automation-daily.yml

# Commit
git commit -m "feat: adicionar workflows de automação de notícias"

# Push para o GitHub
git push origin main
```

#### **Passo 2: Configurar Secrets no GitHub**

1. Acesse: `https://github.com/SEU_USUARIO/SEU_REPO/settings/secrets/actions`
2. Adicione os 3 secrets:
   - `OPENAI_API_KEY` → Sua chave da OpenAI
   - `SUPABASE_URL` → URL do seu Supabase
   - `SUPABASE_KEY` → Chave do Supabase

#### **Passo 3: Verificar se Actions está Habilitado**

1. Acesse: `https://github.com/SEU_USUARIO/SEU_REPO/settings/actions`
2. Verifique se está: ✅ "Allow all actions and reusable workflows"

#### **Passo 4: Testar Manualmente**

1. Vá em: `Actions` (aba no topo do repositório)
2. Selecione: "🤖 Coleta Automática de Notícias"
3. Clique em: "Run workflow"
4. Aguarde e veja os logs

#### **Agendamento Configurado:**

- **news-automation.yml:** Quartas e sábados às 8h BRT (11h UTC)
- **news-automation-daily.yml:** A cada 6 horas (00:00, 06:00, 12:00, 18:00 UTC)

---

### **Solução 2: Corrigir Cron Jobs Locais**

#### **Passo 1: Verificar Erro Específico**

```bash
cd /Users/cesark/site-temvenda
tail -100 logs/collection.log
```

#### **Passo 2: Testar Manualmente**

```bash
cd /Users/cesark/site-temvenda
./cron-automation.sh collect
```

#### **Passo 3: Verificar Dependências**

```bash
# Verificar se Python está correto
which python3

# Verificar se o script existe
ls -lah news_collector.py

# Testar execução direta
python3 news_collector.py
```

#### **Passo 4: Verificar Variáveis de Ambiente**

O script precisa das variáveis:
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`

Verifique se estão configuradas no ambiente do cron.

---

## 🎯 Recomendação

**Use GitHub Actions (Solução 1)** porque:
- ✅ Roda na nuvem (não depende do seu computador)
- ✅ Mais confiável
- ✅ Logs fáceis de ver
- ✅ Não precisa manter computador ligado

**Cron local** só como backup ou para desenvolvimento.

---

## 📋 Checklist de Correção

### Para GitHub Actions:
- [ ] Fazer commit dos workflows
- [ ] Fazer push para o GitHub
- [ ] Configurar os 3 secrets no GitHub
- [ ] Verificar se Actions está habilitado
- [ ] Testar execução manual
- [ ] Verificar logs da primeira execução automática

### Para Cron Local:
- [ ] Verificar logs de erro específicos
- [ ] Testar execução manual do script
- [ ] Verificar variáveis de ambiente
- [ ] Corrigir problema identificado
- [ ] Testar novamente

---

## 🔍 Próximos Passos

1. **Decida:** GitHub Actions (cloud) ou Cron local?
2. **Execute** os passos da solução escolhida
3. **Teste** manualmente primeiro
4. **Monitore** as próximas execuções automáticas

