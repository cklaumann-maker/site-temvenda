# Configuração Rápida para Render.com

## Checklist de Deploy

### 1. Preparação
- [ ] Código commitado no GitHub
- [ ] Arquivo `requirements.txt` existe
- [ ] Arquivo `Procfile` existe (ou usar Start Command manual)

### 2. Criar Serviço no Render
- [ ] Novo Web Service criado
- [ ] Repositório conectado
- [ ] Root Directory: `backend` (se backend está em subpasta) ou vazio (se está na raiz)

### 3. Build & Start Commands

**Se backend está na raiz do repositório:**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Se backend está em subpasta `backend/`:**
- Build: `cd backend && pip install -r requirements.txt`
- Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Variáveis de Ambiente (TODAS obrigatórias)

```bash
ENVIRONMENT=production
APP_PASSWORD=sua-senha-forte-aqui
JWT_SECRET_KEY=chave-secreta-jwt-aleatoria-longa
JWT_ACCESS_EXPIRES_HOURS=8
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key
DRIVE_FILE_ID=id-do-arquivo-google-drive
GOOGLE_PROJECTION_FILE_ID=id-do-arquivo-projecao
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}  # EM UMA LINHA
FRONTEND_ORIGINS=https://www.temvenda.com.br,https://temvenda.com.br
```

### 5. Testar
- [ ] Health check: `https://sua-url.onrender.com/health`
- [ ] Deve retornar: `{"status":"ok","database":"ok"}`

### 6. Configurar Frontend
- [ ] Editar `financeiro/config-api.js` com URL do Render
- [ ] Fazer upload dos arquivos

## Comandos Úteis

### Gerar JWT_SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Converter Service Account JSON para uma linha:
```bash
cat service_account.json | jq -c .
```

### Verificar variáveis no Render:
- Dashboard → Seu Serviço → Environment → Ver todas as variáveis

## URLs Importantes

- **Render Dashboard**: https://dashboard.render.com
- **Seu Serviço**: https://dashboard.render.com/web/seu-servico-id
- **Logs**: https://dashboard.render.com/web/seu-servico-id/logs

