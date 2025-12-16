# Guia de Deploy do Módulo Financeiro

Este guia explica como colocar o módulo financeiro em produção em `www.temvenda.com.br/financeiro`.

## Estrutura do Sistema

- **Frontend**: `financeiro/index.html` (arquivo estático)
- **Backend**: FastAPI em `backend/` (precisa rodar em servidor Python)

## Opções de Deploy

### Opção 1: Backend em Serviço de Hospedagem Python (Recomendado)

Use serviços como **Render**, **Railway**, **Fly.io** ou **PythonAnywhere** para hospedar o backend.

#### Passo 1: Deploy do Backend

1. **Criar conta em um serviço de hospedagem Python** (ex: Render.com)

2. **Criar novo serviço Web Service**:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     ENVIRONMENT=production
     APP_PASSWORD=sua-senha-segura-aqui
     JWT_SECRET_KEY=chave-secreta-jwt-muito-segura
     JWT_ACCESS_EXPIRES_HOURS=8
     SUPABASE_URL=https://seu-projeto.supabase.co
     SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key
     DRIVE_FILE_ID=id-do-arquivo-google-drive
     GOOGLE_PROJECTION_FILE_ID=id-do-arquivo-projecao
     GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}  # JSON completo em uma linha
     FRONTEND_ORIGINS=https://www.temvenda.com.br,https://temvenda.com.br
     ```

3. **Anotar a URL do backend** (ex: `https://temvenda-finance-api.onrender.com`)

#### Passo 2: Configurar Frontend

1. **Editar `financeiro/index.html`**:
   - Localizar a linha: `const API_URL = window.FINANCE_API_URL || "http://localhost:8001";`
   - Alterar para: `const API_URL = window.FINANCE_API_URL || "https://sua-api-backend.onrender.com";`

2. **Ou criar um script de configuração** (recomendado):
   - Adicionar antes do `</head>`:
   ```html
   <script>
     window.FINANCE_API_URL = "https://sua-api-backend.onrender.com";
   </script>
   ```

#### Passo 3: Fazer Upload do Frontend

- Fazer upload do arquivo `financeiro/index.html` para o servidor do site
- Garantir que está acessível em `www.temvenda.com.br/financeiro/`

---

### Opção 2: Backend no Mesmo Servidor (com Proxy Reverso)

Se você tiver acesso SSH ao servidor e puder rodar Python, pode usar um proxy reverso.

#### Passo 1: Configurar Backend no Servidor

1. **Fazer upload do backend**:
   ```bash
   scp -r backend/ usuario@servidor:/caminho/para/backend/
   ```

2. **Instalar dependências**:
   ```bash
   cd /caminho/para/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Criar arquivo `.env`**:
   ```bash
   nano .env
   ```
   Adicionar as mesmas variáveis de ambiente da Opção 1.

4. **Rodar com systemd** (criar `/etc/systemd/system/temvenda-finance.service`):
   ```ini
   [Unit]
   Description=Tem Venda Finance API
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/caminho/para/backend
   Environment="PATH=/caminho/para/backend/venv/bin"
   ExecStart=/caminho/para/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Iniciar serviço**:
   ```bash
   sudo systemctl enable temvenda-finance
   sudo systemctl start temvenda-finance
   ```

#### Passo 2: Configurar Proxy Reverso no .htaccess

Adicionar ao `.htaccess` na raiz:

```apache
<IfModule mod_rewrite.c>
RewriteEngine On

# Proxy para API do financeiro
RewriteCond %{REQUEST_URI} ^/api/finance/(.*)$
RewriteRule ^api/finance/(.*)$ http://127.0.0.1:8001/api/$1 [P,L]
</IfModule>
```

**Nota**: Isso requer `mod_proxy` e `mod_proxy_http` habilitados no Apache. Se não estiverem disponíveis, use a Opção 1.

#### Passo 3: Configurar Frontend

No `financeiro/index.html`, alterar:
```javascript
const API_URL = window.FINANCE_API_URL || "/api/finance";
```

---

### Opção 3: Backend como Subdomínio

Criar subdomínio `api.temvenda.com.br` apontando para o backend.

1. **Configurar DNS**: Criar registro A ou CNAME para `api.temvenda.com.br`
2. **Configurar backend** para aceitar requisições de `https://www.temvenda.com.br`
3. **No frontend**: `const API_URL = "https://api.temvenda.com.br";`

---

## Checklist de Deploy

- [ ] Backend rodando e acessível
- [ ] Variáveis de ambiente configuradas no backend
- [ ] CORS configurado para aceitar `https://www.temvenda.com.br`
- [ ] Frontend atualizado com URL correta da API
- [ ] Arquivo `financeiro/index.html` no servidor
- [ ] Testar login no módulo financeiro
- [ ] Testar carregamento de mês
- [ ] Testar salvamento de entradas
- [ ] Testar salvamento de compras

## Testes Pós-Deploy

1. Acessar `https://www.temvenda.com.br/financeiro/`
2. Fazer login com a senha configurada
3. Carregar um mês (ex: `12-25`)
4. Testar salvar entradas do dia
5. Testar salvar compras do dia
6. Verificar console do navegador para erros

## Troubleshooting

### Erro de CORS
- Verificar se `FRONTEND_ORIGINS` inclui `https://www.temvenda.com.br`
- Verificar se o backend está retornando headers CORS corretos

### Erro 404 na API
- Verificar se a URL da API está correta no frontend
- Verificar se o backend está rodando
- Verificar logs do backend

### Erro de autenticação
- Verificar se `APP_PASSWORD` está configurado corretamente
- Verificar se `JWT_SECRET_KEY` está configurado

### Erro ao carregar dados do Supabase
- Verificar se `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` estão corretos
- Verificar se as tabelas foram criadas no Supabase

## Segurança

- ✅ Use senhas fortes para `APP_PASSWORD`
- ✅ Use chave JWT segura e única
- ✅ Não commite arquivos `.env` no Git
- ✅ Use HTTPS em produção
- ✅ Configure CORS apenas para domínios necessários
- ✅ Mantenha dependências atualizadas

