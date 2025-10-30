# 🚀 Guia Completo: Hospedagem Gratuita com FTP

## 📋 Opções de Hospedagem Gratuita

### 1. **InfinityFree** ⭐ (Recomendado)
- ✅ **Grátis:** 100% gratuito, sem limite de tempo
- ✅ **Domínio:** Suporta domínio próprio (temvenda.com.br)
- ✅ **FTP:** Acesso completo via FTP
- ✅ **PHP:** Versão 8.1
- ✅ **SSL:** Certificado SSL gratuito
- ✅ **MySQL:** Banco de dados incluído
- ✅ **cPanel:** Painel de controle completo
- ⚠️ **Limitação:** Sem limite de tráfego, mas pode ter limitações de CPU

**URL:** https://www.infinityfree.net/

---

### 2. **000webhost**
- ✅ **Grátis:** 100% gratuito
- ✅ **FTP:** Acesso via FTP
- ✅ **PHP:** Versão 7.4 ou superior
- ✅ **MySQL:** Banco de dados incluído
- ✅ **SSL:** Certificado SSL gratuito
- ⚠️ **Limitação:** 300 MB de espaço, sem suporte técnico

**URL:** https://www.000webhost.com/

---

### 3. **Freehostia**
- ✅ **Grátis:** Plano básico gratuito
- ✅ **FTP:** Acesso via FTP
- ✅ **PHP:** Suportado
- ✅ **MySQL:** Banco de dados incluído
- ⚠️ **Limitação:** 250 MB de espaço, limitado

**URL:** https://www.freehostia.com/

---

### 4. **AwardSpace**
- ✅ **Grátis:** Plano gratuito disponível
- ✅ **FTP:** Acesso via FTP
- ✅ **PHP:** Suportado
- ✅ **MySQL:** Banco de dados incluído
- ⚠️ **Limitação:** 1 GB de espaço, limitado

**URL:** https://www.awardspace.com/

---

## 🎯 Passo a Passo: InfinityFree (Recomendado)

### **ETAPA 1: Criar Conta**

1. Acesse: https://www.infinityfree.net/
2. Clique em **"Sign Up"** (Cadastrar)
3. Preencha:
   - Email
   - Senha
   - Nome de usuário
4. Confirme o email

---

### **ETAPA 2: Criar Conta de Hospedagem**

1. Faça login no painel
2. Clique em **"Create Account"** (Criar Conta)
3. Escolha:
   - **Domain:** Seu domínio (temvenda.com.br)
   - **Username:** Escolha um nome de usuário
   - **Password:** Escolha uma senha forte
4. Clique em **"Create Account"**

---

### **ETAPA 3: Configurar Domínio**

1. No painel, encontre sua conta
2. Clique em **"Manage"**
3. Vá em **"Domain Settings"**
4. Configure:
   - **Domain:** temvenda.com.br
   - **Nameservers:** Anote os nameservers fornecidos

---

### **ETAPA 4: Configurar DNS do Domínio**

1. Acesse o painel do seu provedor de domínio (Registro.br, GoDaddy, etc.)
2. Vá em **"DNS"** ou **"Nameservers"**
3. Altere os nameservers para os fornecidos pela InfinityFree
4. Aguarde 24-48 horas para propagação

---

### **ETAPA 5: Obter Credenciais FTP**

1. No painel InfinityFree, vá em **"Manage"**
2. Clique em **"FTP Accounts"**
3. Anote:
   - **Servidor FTP:** ftp.infinityfree.net
   - **Usuário:** (seu username)
   - **Senha:** (sua senha)
   - **Porta:** 21

---

### **ETAPA 6: Conectar via FTP**

#### **Opção A: FileZilla (Recomendado)**

1. **Baixe o FileZilla:** https://filezilla-project.org/
2. **Instale** o programa
3. **Configure a conexão:**
   - Host: `ftp.infinityfree.net`
   - Username: (seu username)
   - Password: (sua senha)
   - Porta: `21`
4. Clique em **"Quickconnect"**

#### **Opção B: Terminal/CMD**

```bash
ftp ftp.infinityfree.net
# Digite seu username
# Digite sua senha
```

---

### **ETAPA 7: Fazer Upload dos Arquivos**

#### **Via FileZilla:**

1. **Lado esquerdo:** Seus arquivos locais
2. **Lado direito:** Servidor FTP
3. **Navegue até:** `htdocs/` ou `public_html/`
4. **Arraste** os arquivos da pasta `deploy-wp-content/temvenda/`
5. **Aguarde** o upload completar

#### **Via Terminal:**

```bash
# Navegue até a pasta deploy-wp-content/temvenda/
cd deploy-wp-content/temvenda/

# Conecte via FTP
ftp ftp.infinityfree.net

# Entre na pasta pública
cd htdocs

# Faça upload dos arquivos
put home-corporativo.html
put consultoria.html
put formacao-lideres.html
# ... continue para todos os arquivos
```

---

### **ETAPA 8: Verificar Arquivos**

1. Acesse: `http://temvenda.com.br/home-corporativo.html`
2. Verifique se todos os arquivos carregam
3. Teste os links entre páginas

---

## 📁 Estrutura de Arquivos Recomendada

```
htdocs/
├── home-corporativo.html
├── consultoria.html
├── formacao-lideres.html
├── palestras.html
├── treinamento-incompany.html
├── diagnostico.html
├── noticias.html
├── login-admin.html
├── admin-panel.html
├── admin-stats.html
├── admin-users.html
├── auth-manager.js
├── logo-temvenda.png
└── .htaccess (se necessário)
```

---

## 🔧 Configuração do .htaccess

Crie um arquivo `.htaccess` na raiz com:

```apache
# Configuração básica
DirectoryIndex home-corporativo.html index.html

# Redirecionamentos
RewriteEngine On
RewriteBase /

# Redirecionar raiz para home
RewriteRule ^$ home-corporativo.html [L]

# Redirecionar /diagnostico para diagnostico.html
RewriteRule ^diagnostico$ diagnostico.html [L]

# Redirecionar /consultoria para consultoria.html
RewriteRule ^consultoria$ consultoria.html [L]

# Redirecionar /formacao-lideres para formacao-lideres.html
RewriteRule ^formacao-lideres$ formacao-lideres.html [L]

# Redirecionar /treinamento-incompany para treinamento-incompany.html
RewriteRule ^treinamento-incompany$ treinamento-incompany.html [L]

# Redirecionar /palestras para palestras.html
RewriteRule ^palestras$ palestras.html [L]

# Redirecionar /noticias para noticias.html
RewriteRule ^noticias$ noticias.html [L]

# Redirecionar /login-admin para login-admin.html
RewriteRule ^login-admin$ login-admin.html [L]
```

---

## ⚠️ IMPORTANTE: Ajustar Caminhos

Quando hospedar em hospedagem gratuita, você precisará ajustar os caminhos:

### **Antes (wp-content):**
```html
href="/wp-content/temvenda/consultoria.html"
```

### **Depois (raiz):**
```html
href="/consultoria.html"
```

Ou mantenha apenas:
```html
href="consultoria.html"
```

---

## 🛠️ Script de Ajuste de Caminhos

Crie um script para ajustar automaticamente:

```bash
#!/bin/bash
# ajustar-caminhos-ftp.sh

# Remove /wp-content/temvenda/ de todos os links
find . -name "*.html" -type f -exec sed -i '' 's|/wp-content/temvenda/||g' {} \;

# Remove /wp-content/temvenda/ de todas as imagens
find . -name "*.html" -type f -exec sed -i '' 's|src="/wp-content/temvenda/|src="|g' {} \;

echo "✅ Caminhos ajustados para FTP!"
```

---

## 📊 Checklist de Upload

- [ ] Criar conta na hospedagem gratuita
- [ ] Configurar domínio e DNS
- [ ] Obter credenciais FTP
- [ ] Conectar via FileZilla
- [ ] Fazer upload de todos os arquivos HTML
- [ ] Fazer upload de imagens (logo-temvenda.png)
- [ ] Fazer upload de JavaScript (auth-manager.js)
- [ ] Criar arquivo .htaccess
- [ ] Ajustar caminhos nos arquivos HTML
- [ ] Testar todas as páginas
- [ ] Verificar links entre páginas
- [ ] Testar responsividade

---

## 🚨 Problemas Comuns e Soluções

### **Erro 403 Forbidden**
- Verifique se os arquivos estão em `htdocs/` ou `public_html/`
- Verifique permissões dos arquivos (chmod 644)

### **Erro 404 Not Found**
- Verifique os caminhos dos links
- Verifique se o arquivo existe no servidor
- Verifique o .htaccess

### **Imagens não carregam**
- Verifique caminhos das imagens
- Verifique se os arquivos de imagem foram enviados
- Verifique permissões

### **JavaScript não funciona**
- Verifique caminhos dos scripts
- Verifique se auth-manager.js foi enviado
- Verifique console do navegador (F12)

---

## 💡 Dicas Importantes

1. **Backup:** Sempre faça backup antes de fazer upload
2. **Teste local:** Teste tudo localmente antes de hospedar
3. **Organização:** Mantenha arquivos organizados
4. **SSL:** Configure SSL gratuito (Let's Encrypt)
5. **Performance:** Otimize imagens antes de fazer upload

---

## 📞 Suporte

- **InfinityFree:** https://forum.infinityfree.net/
- **000webhost:** https://www.000webhost.com/forum

---

**Última atualização:** $(date)

