# 🚀 Guia de Deploy - Servidor TemVenda

Este guia explica como fazer o deploy da aplicação Rotina App no servidor do TemVenda para uso em produção.

---

## 📋 Pré-requisitos

### 1. Acesso ao Servidor
- [ ] Acesso SSH ao servidor
- [ ] Acesso root ou sudo
- [ ] Domínio configurado (ex: `rotina.temvenda.com.br`)

### 2. Software Necessário no Servidor
- Node.js 18+ (`node --version`)
- pnpm 8+ (`pnpm --version`)
- PM2 ou similar para gerenciar processos (`npm install -g pm2`)
- Nginx ou Apache como proxy reverso

### 3. Credenciais
- [ ] URL do Supabase em produção
- [ ] Chaves do Supabase (anon key e service role key)

---

## 🔧 Passo 1: Preparar o Código Localmente

### 1.1. Verificar Build

```bash
cd rotina-app

# Instalar dependências
pnpm install

# Fazer build para testar
pnpm --filter web build

# Verificar se build foi bem-sucedido
ls -la apps/web/.next
```

### 1.2. Criar Arquivo de Variáveis de Ambiente

Crie o arquivo `apps/web/.env.production`:

```bash
cd apps/web
cp env.example .env.production
```

Edite `.env.production` com suas credenciais:

```env
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-aqui
```

**⚠️ IMPORTANTE**: Não commite este arquivo no Git! Adicione ao `.gitignore`.

---

## 📦 Passo 2: Preparar Arquivos para Deploy

### 2.1. Criar Script de Deploy

Crie o arquivo `deploy-to-server.sh` na raiz do projeto:

```bash
#!/bin/bash

echo "🚀 Preparando deploy para servidor TemVenda..."

# Variáveis
BUILD_DIR="build-deploy"
APP_DIR="apps/web"

# Limpar build anterior
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Copiar código fonte
echo "📁 Copiando arquivos..."
cp -r $APP_DIR $BUILD_DIR/web
cp -r packages $BUILD_DIR/
cp package.json $BUILD_DIR/
cp pnpm-lock.yaml $BUILD_DIR/
cp pnpm-workspace.yaml $BUILD_DIR/

# Copiar arquivos de configuração
cp -r scripts $BUILD_DIR/ 2>/dev/null || true

# Remover node_modules (será instalado no servidor)
find $BUILD_DIR -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find $BUILD_DIR -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true

# Criar arquivo de instruções
cat > $BUILD_DIR/DEPLOY_INSTRUCTIONS.md << 'EOF'
# Instruções de Deploy

1. Faça upload desta pasta para o servidor
2. Execute os comandos em DEPLOY_STEPS.sh
EOF

# Criar script de deploy para o servidor
cat > $BUILD_DIR/DEPLOY_STEPS.sh << 'EOF'
#!/bin/bash

echo "🚀 Iniciando deploy no servidor..."

# Instalar dependências
pnpm install --frozen-lockfile --prod

# Build da aplicação
cd apps/web
pnpm build

# Criar diretório de produção
mkdir -p /var/www/rotina-app
cp -r .next /var/www/rotina-app/
cp -r public /var/www/rotina-app/ 2>/dev/null || true
cp package.json /var/www/rotina-app/
cp next.config.js /var/www/rotina-app/
cp .env.production /var/www/rotina-app/.env

# Instalar apenas dependências de produção
cd /var/www/rotina-app
pnpm install --frozen-lockfile --prod

echo "✅ Deploy concluído!"
EOF

chmod +x $BUILD_DIR/DEPLOY_STEPS.sh

echo "✅ Arquivos preparados em: $BUILD_DIR/"
echo ""
echo "📤 Próximo passo: Faça upload da pasta $BUILD_DIR para o servidor"
```

Torne o script executável:

```bash
chmod +x deploy-to-server.sh
```

---

## 🖥️ Passo 3: Configurar o Servidor

### 3.1. Conectar ao Servidor

```bash
ssh usuario@servidor.temvenda.com.br
```

### 3.2. Instalar Node.js e pnpm

```bash
# Instalar Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar pnpm
npm install -g pnpm

# Verificar instalação
node --version
pnpm --version
```

### 3.3. Instalar PM2 (Gerenciador de Processos)

```bash
npm install -g pm2
```

### 3.4. Criar Diretório da Aplicação

```bash
sudo mkdir -p /var/www/rotina-app
sudo chown -R $USER:$USER /var/www/rotina-app
```

---

## 📤 Passo 4: Fazer Upload dos Arquivos

### Opção A: Via SCP

```bash
# No seu computador local
cd rotina-app
./deploy-to-server.sh

# Fazer upload
scp -r build-deploy/* usuario@servidor.temvenda.com.br:/var/www/rotina-app/
```

### Opção B: Via Git (Recomendado)

```bash
# No servidor
cd /var/www
git clone https://github.com/seu-usuario/rotina-app.git rotina-app
cd rotina-app

# Instalar dependências
pnpm install --frozen-lockfile

# Copiar variáveis de ambiente
cp apps/web/env.example apps/web/.env.production
# Edite .env.production com suas credenciais

# Build
pnpm --filter web build
```

---

## ⚙️ Passo 5: Configurar Variáveis de Ambiente

No servidor, edite o arquivo `.env.production`:

```bash
cd /var/www/rotina-app/apps/web
nano .env.production
```

Adicione suas credenciais do Supabase:

```env
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-anon-key
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key
```

---

## 🚀 Passo 6: Iniciar a Aplicação

### 6.1. Usando PM2 (Recomendado)

Crie o arquivo `ecosystem.config.js` na raiz do projeto:

```javascript
module.exports = {
  apps: [{
    name: 'rotina-app',
    script: 'node_modules/next/dist/bin/next',
    args: 'start -p 3001',
    cwd: '/var/www/rotina-app/apps/web',
    instances: 1,
    exec_mode: 'fork',
    env: {
      NODE_ENV: 'production',
      PORT: 3001
    },
    error_file: '/var/log/rotina-app/error.log',
    out_file: '/var/log/rotina-app/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
```

Iniciar com PM2:

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/rotina-app
sudo chown -R $USER:$USER /var/log/rotina-app

# Iniciar aplicação
pm2 start ecosystem.config.js

# Salvar configuração do PM2
pm2 save

# Configurar PM2 para iniciar no boot
pm2 startup
# Execute o comando que aparecer (será algo como: sudo env PATH=...)

# Verificar status
pm2 status
pm2 logs rotina-app
```

### 6.2. Usando systemd (Alternativa)

Crie o arquivo `/etc/systemd/system/rotina-app.service`:

```ini
[Unit]
Description=Rotina App Next.js
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/rotina-app/apps/web
Environment=NODE_ENV=production
Environment=PORT=3001
ExecStart=/usr/bin/node node_modules/next/dist/bin/next start -p 3001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable rotina-app
sudo systemctl start rotina-app
sudo systemctl status rotina-app
```

---

## 🌐 Passo 7: Configurar Nginx como Proxy Reverso

### 7.1. Instalar Nginx

```bash
sudo apt update
sudo apt install nginx
```

### 7.2. Configurar Site

Crie o arquivo `/etc/nginx/sites-available/rotina-app`:

```nginx
server {
    listen 80;
    server_name rotina.temvenda.com.br;

    # Redirecionar HTTP para HTTPS (se tiver SSL)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Otimizações
    client_max_body_size 10M;
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
}
```

### 7.3. Ativar Site

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/rotina-app /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

---

## 🔒 Passo 8: Configurar SSL (HTTPS)

### 8.1. Usando Certbot (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d rotina.temvenda.com.br

# Renovação automática (já configurado automaticamente)
sudo certbot renew --dry-run
```

### 8.2. Atualizar Configuração Nginx

Após obter o certificado, atualize `/etc/nginx/sites-available/rotina-app`:

```nginx
server {
    listen 80;
    server_name rotina.temvenda.com.br;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name rotina.temvenda.com.br;

    ssl_certificate /etc/letsencrypt/live/rotina.temvenda.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/rotina.temvenda.com.br/privkey.pem;

    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Recarregar Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## ✅ Passo 9: Verificar Deploy

### 9.1. Testes Locais no Servidor

```bash
# Verificar se aplicação está rodando
curl http://localhost:3001

# Verificar logs
pm2 logs rotina-app
# ou
sudo journalctl -u rotina-app -f
```

### 9.2. Testes Externos

- [ ] Acesse `http://rotina.temvenda.com.br` (ou HTTPS)
- [ ] Teste login
- [ ] Teste rotas `/app/*`
- [ ] Verifique se dados estão sendo salvos no Supabase

---

## 🔄 Passo 10: Atualizações Futuras

### 10.1. Processo de Atualização

```bash
# No servidor
cd /var/www/rotina-app

# Atualizar código
git pull origin main

# Instalar novas dependências
pnpm install --frozen-lockfile

# Rebuild
pnpm --filter web build

# Reiniciar aplicação
pm2 restart rotina-app
# ou
sudo systemctl restart rotina-app
```

### 10.2. Script de Atualização Automática

Crie `update.sh`:

```bash
#!/bin/bash
cd /var/www/rotina-app
git pull origin main
pnpm install --frozen-lockfile
pnpm --filter web build
pm2 restart rotina-app
echo "✅ Aplicação atualizada!"
```

---

## 🐛 Troubleshooting

### Problema: Aplicação não inicia

```bash
# Verificar logs
pm2 logs rotina-app
# ou
sudo journalctl -u rotina-app -n 50

# Verificar se porta está em uso
sudo netstat -tulpn | grep 3001

# Verificar variáveis de ambiente
cat /var/www/rotina-app/apps/web/.env.production
```

### Problema: Erro 502 Bad Gateway

- Verificar se aplicação está rodando: `pm2 status`
- Verificar logs do Nginx: `sudo tail -f /var/log/nginx/error.log`
- Verificar configuração do Nginx: `sudo nginx -t`

### Problema: Erro de conexão com Supabase

- Verificar variáveis de ambiente
- Verificar URLs permitidas no Supabase Dashboard
- Verificar firewall do servidor

---

## 📋 Checklist Final

- [ ] Node.js e pnpm instalados
- [ ] Código enviado para servidor
- [ ] Variáveis de ambiente configuradas
- [ ] Build executado com sucesso
- [ ] Aplicação rodando (PM2 ou systemd)
- [ ] Nginx configurado
- [ ] SSL configurado (HTTPS)
- [ ] DNS apontando para servidor
- [ ] Testes realizados
- [ ] Logs monitorados

---

## 🎯 Resumo Rápido

1. **Preparar código**: `./deploy-to-server.sh`
2. **Upload para servidor**: `scp` ou `git clone`
3. **Instalar dependências**: `pnpm install`
4. **Build**: `pnpm --filter web build`
5. **Configurar variáveis**: Editar `.env.production`
6. **Iniciar**: `pm2 start ecosystem.config.js`
7. **Configurar Nginx**: Criar arquivo de configuração
8. **Configurar SSL**: `certbot --nginx`
9. **Testar**: Acessar URL em produção

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs: `pm2 logs` ou `journalctl`
2. Verifique configuração do Nginx: `sudo nginx -t`
3. Verifique variáveis de ambiente
4. Verifique conectividade com Supabase

---

**✅ Pronto! Sua aplicação está no ar!**







