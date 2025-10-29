# 🚀 INSTRUÇÕES COMPLETAS PARA GITHUB E DEPLOY

## 📋 COMANDOS PARA EXECUTAR NO TERMINAL

### **1. Configurar Git (se ainda não configurado)**
```bash
git config --global user.name "Cesar Klaumann"
git config --global user.email "cklaumann@gmail.com"
```

### **2. Inicializar e conectar ao GitHub**
```bash
# Inicializar repositório
git init

# Conectar ao seu repositório GitHub
git remote add origin https://github.com/cklaumann-maker/site-temvenda.git

# Verificar conexão
git remote -v
```

### **3. Fazer commit e push**
```bash
# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "🚀 Site TEM VENDA - Sistema completo de administração

✨ Funcionalidades implementadas:
- Sistema de autenticação completo
- Página de liberação de notícias (admin-panel)
- Página de estatísticas (admin-stats) 
- Página de usuários (admin-users)
- Página inicial corporativa (home-corporativo)
- Páginas de serviços (consultoria, formação, palestras, treinamento)
- Sistema de diagnóstico interativo
- Integração com Supabase para notícias
- Sistema de permissões granular
- Design responsivo e profissional
- Deploy preparado para temvenda.com.br"

# Definir branch principal
git branch -M main

# Fazer push para o GitHub
git push -u origin main
```

## 🌐 DEPLOY PARA TEMVENDA.COM.BR

### **Arquivos Preparados em `/deploy-temvenda/`:**
- ✅ `admin-panel.html` - Liberação de notícias
- ✅ `admin-stats.html` - Estatísticas
- ✅ `admin-users.html` - Usuários
- ✅ `login-admin.html` - Login
- ✅ `home-corporativo.html` - Página inicial
- ✅ `diagnostico.html` - Diagnóstico
- ✅ `consultoria.html` - Consultoria
- ✅ `formacao-lideres.html` - Formação
- ✅ `palestras.html` - Palestras
- ✅ `treinamento-incompany.html` - Treinamento
- ✅ `noticias.html` - Notícias públicas
- ✅ `auth-manager.js` - Sistema de autenticação
- ✅ `logo-temvenda.png` - Logo
- ✅ `.htaccess` - Configuração de redirecionamentos

### **Passos para Deploy:**

1. **Acesse o cPanel/FTP do temvenda.com.br**

2. **Faça upload dos arquivos:**
   - Upload todos os arquivos `.html` para a raiz do WordPress
   - Upload `auth-manager.js` para a raiz
   - Upload `logo-temvenda.png` para a raiz

3. **Configurar .htaccess:**
   - Substitua o conteúdo do `.htaccess` atual pelo arquivo `.htaccess` incluído
   - OU adicione as regras de redirecionamento ao `.htaccess` existente

4. **Testar URLs:**
   - `https://temvenda.com.br/home-moderna`
   - `https://temvenda.com.br/diagnostico`
   - `https://temvenda.com.br/login-admin`
   - `https://temvenda.com.br/admin-panel`

5. **Credenciais de Acesso:**
   - **Root:** `cesar` / `temvenda2024`
   - **Admin:** `admin` / `temvenda2024`

## 🔧 CONFIGURAÇÕES ADICIONAIS

### **Sistema de Notícias (Opcional):**
- Configure cron job para executar `news_collector.py`
- Verifique configurações do Supabase
- Teste coleta automática de notícias

### **SSL e Performance:**
- Verifique se SSL está funcionando
- Teste responsividade em dispositivos móveis
- Otimize performance se necessário

## ✅ CHECKLIST FINAL
- [ ] Repositório GitHub atualizado
- [ ] Arquivos HTML uploadados
- [ ] .htaccess configurado
- [ ] URLs funcionando
- [ ] Login administrativo funcionando
- [ ] Sistema de notícias funcionando (se aplicável)
- [ ] Responsividade testada
- [ ] SSL funcionando

## 🎉 RESULTADO FINAL
Site TEM VENDA completamente funcional em:
- **GitHub:** https://github.com/cklaumann-maker/site-temvenda
- **Produção:** https://temvenda.com.br

**Sistema completo de administração implementado!** 🚀
