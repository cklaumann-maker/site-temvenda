# Deploy Rápido - Módulo Financeiro

## Passos para Produção

### 1. Escolher onde hospedar o Backend

**Opção A: Render.com (Recomendado - Grátis)**
- Criar conta em https://render.com
- Criar novo "Web Service"
- Conectar repositório GitHub ou fazer upload do código
- Configurar variáveis de ambiente (ver abaixo)
- Anotar a URL gerada (ex: `https://temvenda-finance.onrender.com`)

**Opção B: Railway.app**
- Similar ao Render, também tem plano gratuito

**Opção C: Servidor próprio**
- Se tiver acesso SSH ao servidor do site

### 2. Configurar Backend

**Variáveis de Ambiente necessárias:**
```
ENVIRONMENT=production
APP_PASSWORD=sua-senha-forte-aqui
JWT_SECRET_KEY=chave-secreta-jwt-muito-longa-e-aleatoria
JWT_ACCESS_EXPIRES_HOURS=8
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-do-supabase
DRIVE_FILE_ID=id-do-arquivo-google-drive
GOOGLE_PROJECTION_FILE_ID=id-do-arquivo-projecao-google-drive
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}  # JSON completo em uma linha
FRONTEND_ORIGINS=https://www.temvenda.com.br,https://temvenda.com.br
```

**Comando de Start:**
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3. Configurar Frontend

1. **Editar `financeiro/config-api.js`**:
   ```javascript
   window.FINANCE_API_URL = "https://sua-api-backend.onrender.com";
   ```

2. **Fazer upload dos arquivos**:
   - `financeiro/index.html`
   - `financeiro/config-api.js`
   
   Para o servidor, garantindo que fiquem em `/financeiro/`

### 4. Testar

1. Acessar: `https://www.temvenda.com.br/financeiro/`
2. Fazer login com a senha configurada em `APP_PASSWORD`
3. Testar carregar um mês
4. Verificar console do navegador (F12) para erros

## Troubleshooting

**Erro de CORS:**
- Verificar se `FRONTEND_ORIGINS` inclui `https://www.temvenda.com.br`

**Erro 404 na API:**
- Verificar se a URL em `config-api.js` está correta
- Verificar se o backend está rodando

**Erro ao conectar no Supabase:**
- Verificar se `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` estão corretos

## Segurança

- ✅ Use senhas fortes
- ✅ Não commite arquivos `.env`
- ✅ Use HTTPS em produção
- ✅ Mantenha dependências atualizadas

