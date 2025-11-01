# 🤖 Automação TEM VENDA

Esta pasta contém todos os scripts de automação que rodam na nuvem (GitHub Actions, Railway, etc.).

## 📁 Estrutura

```
automation/
├── scripts/          # Scripts Python de automação
│   ├── news_collector.py      # Coleta notícias RSS
│   └── drive_pdf_collector.py # Coleta PDFs do Google Drive
├── logs/             # Logs de execução (gerados automaticamente)
├── config/           # Arquivos de configuração (service_account.json, etc.)
└── README.md         # Este arquivo
```

## 🚀 Como funciona

### GitHub Actions
Os scripts são executados automaticamente via GitHub Actions:
- **Frequência:** Quartas e sábados às 8h (horário de Brasília)
- **Workflow:** `.github/workflows/news-automation.yml`
- **Configuração:** Secrets no GitHub (Settings → Secrets)

### Execução Local
Para testar localmente:

```bash
cd automation/scripts
python3 news_collector.py
python3 drive_pdf_collector.py
```

## 🔐 Variáveis de Ambiente Necessárias

- `SUPABASE_URL` - URL do projeto Supabase
- `SUPABASE_KEY` - Service Key do Supabase
- `OPENAI_API_KEY` - Chave da API OpenAI
- `GOOGLE_CREDENTIALS` - JSON da service account do Google (opcional)

## 📊 Logs

Os logs são gerados automaticamente:
- `news_collector.log` - Logs da coleta de notícias
- `drive_pdf_collector.log` - Logs da coleta de PDFs

## 🔧 Manutenção

- Scripts podem ser atualizados normalmente
- Workflows do GitHub Actions são executados automaticamente
- Logs são mantidos por 30 dias (configurável)
