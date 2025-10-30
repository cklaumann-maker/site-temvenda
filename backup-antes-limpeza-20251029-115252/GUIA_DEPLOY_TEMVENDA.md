# 🚀 DEPLOY PARA TEMVENDA.COM.BR - GUIA PASSO A PASSO

## 📋 PASSO 1: ACESSAR A HOSPEDAGEM

### **Opção A: cPanel**
1. Acesse o cPanel do temvenda.com.br
2. Vá em "Gerenciador de Arquivos"
3. Navegue até a pasta `public_html` (raiz do WordPress)

### **Opção B: FTP**
1. Use um cliente FTP (FileZilla, WinSCP, etc.)
2. Conecte com as credenciais do temvenda.com.br
3. Navegue até a pasta raiz do WordPress

## 📁 PASSO 2: UPLOAD DOS ARQUIVOS

### **Arquivos para Upload (da pasta deploy-temvenda/):**

**📄 Páginas HTML (11 arquivos):**
- admin-panel.html
- admin-stats.html  
- admin-users.html
- consultoria.html
- diagnostico.html
- formacao-lideres.html
- home-corporativo.html
- login-admin.html
- noticias.html
- palestras.html
- treinamento-incompany.html

**🔧 Arquivos de Configuração:**
- auth-manager.js
- logo-temvenda.png
- .htaccess (⚠️ IMPORTANTE - ver passo 3)

### **⚠️ ATENÇÃO:**
- Faça upload de TODOS os arquivos para a **RAIZ** do WordPress
- Mesmo diretório onde está o `wp-config.php`
- Mantenha os nomes dos arquivos exatamente como estão

## ⚙️ PASSO 3: CONFIGURAR .HTACCESS

### **IMPORTANTE:** 
O arquivo `.htaccess` é CRÍTICO para o funcionamento das URLs!

### **Opção A: Substituir .htaccess existente**
1. Faça **BACKUP** do .htaccess atual
2. Substitua pelo novo .htaccess do deploy-temvenda/

### **Opção B: Adicionar regras ao .htaccess existente**
Adicione estas linhas no INÍCIO do .htaccess atual:

```apache
# Redirecionamentos personalizados TEM VENDA
RewriteEngine On

# Páginas principais
RewriteRule ^diagnostico/?$ /diagnostico.html [L,QSA]
RewriteRule ^home-moderna/?$ /home-corporativo.html [L,QSA]
RewriteRule ^formacao-lideres/?$ /formacao-lideres.html [L,QSA]
RewriteRule ^consultoria/?$ /consultoria.html [L,QSA]
RewriteRule ^palestras/?$ /palestras.html [L,QSA]
RewriteRule ^treinamento-incompany/?$ /treinamento-incompany.html [L,QSA]

# Área administrativa
RewriteRule ^login-admin/?$ /login-admin.html [L,QSA]
RewriteRule ^admin-panel/?$ /admin-panel.html [L,QSA]
RewriteRule ^admin-stats/?$ /admin-stats.html [L,QSA]
RewriteRule ^admin-users/?$ /admin-users.html [L,QSA]

# Notícias públicas
RewriteRule ^noticias/?$ /noticias.html [L,QSA]
```

## 🧪 PASSO 4: TESTAR AS URLs

### **URLs para Testar:**
1. **Página Inicial:** https://temvenda.com.br/home-moderna
2. **Diagnóstico:** https://temvenda.com.br/diagnostico
3. **Consultoria:** https://temvenda.com.br/consultoria
4. **Formação:** https://temvenda.com.br/formacao-lideres
5. **Palestras:** https://temvenda.com.br/palestras
6. **Treinamento:** https://temvenda.com.br/treinamento-incompany
7. **Login Admin:** https://temvenda.com.br/login-admin

### **✅ Se funcionar:** Você verá as páginas carregando
### **❌ Se der erro 404:** Verificar configuração do .htaccess

## 🔐 PASSO 5: TESTAR SISTEMA ADMINISTRATIVO

### **Credenciais de Login:**
- **Root:** `cesar` / `temvenda2024`
- **Admin:** `admin` / `temvenda2024`

### **URLs Administrativas:**
1. **Login:** https://temvenda.com.br/login-admin
2. **Painel Notícias:** https://temvenda.com.br/admin-panel
3. **Estatísticas:** https://temvenda.com.br/admin-stats
4. **Usuários:** https://temvenda.com.br/admin-users

### **Testes a Fazer:**
- [ ] Login funcionando
- [ ] Navegação entre páginas admin
- [ ] Upload de imagens
- [ ] Alteração de estatísticas
- [ ] Gerenciamento de usuários

## 🚨 SOLUÇÃO DE PROBLEMAS

### **Erro 404 nas URLs:**
1. Verificar se .htaccess foi aplicado
2. Verificar se mod_rewrite está habilitado
3. Verificar se arquivos estão na raiz correta

### **Erro de Login:**
1. Verificar se auth-manager.js está acessível
2. Verificar conexão com Supabase
3. Verificar credenciais no banco

### **Problemas de CSS/Imagens:**
1. Verificar se logo-temvenda.png está acessível
2. Verificar caminhos relativos
3. Verificar permissões dos arquivos

## ✅ CHECKLIST FINAL

- [ ] Todos os arquivos HTML uploadados
- [ ] auth-manager.js uploadado
- [ ] logo-temvenda.png uploadado
- [ ] .htaccess configurado
- [ ] URLs funcionando
- [ ] Login administrativo funcionando
- [ ] Sistema de permissões funcionando
- [ ] Responsividade testada

## 🎉 DEPLOY CONCLUÍDO QUANDO:
- Todas as URLs funcionando
- Sistema administrativo acessível
- Login funcionando
- Páginas carregando corretamente

**🚀 SITE TEM VENDA EM PRODUÇÃO!**
