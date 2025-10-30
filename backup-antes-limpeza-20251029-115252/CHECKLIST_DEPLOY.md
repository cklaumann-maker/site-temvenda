# 🚀 CHECKLIST DE DEPLOY - TEMVENDA.COM.BR

## ✅ ARQUIVOS PRONTOS PARA UPLOAD
- [x] admin-panel.html (31KB) - Liberação de notícias
- [x] admin-stats.html (33KB) - Estatísticas e imagens  
- [x] admin-users.html (36KB) - Gerenciamento de usuários
- [x] login-admin.html (10KB) - Sistema de login
- [x] home-corporativo.html (49KB) - Página inicial moderna
- [x] diagnostico.html (61KB) - Diagnóstico interativo
- [x] consultoria.html (28KB) - Página de consultoria
- [x] formacao-lideres.html (39KB) - Formação de líderes
- [x] palestras.html (33KB) - Palestras
- [x] treinamento-incompany.html (33KB) - Treinamento in-company
- [x] noticias.html (25KB) - Notícias públicas
- [x] auth-manager.js (7KB) - Sistema de autenticação
- [x] logo-temvenda.png (1.3MB) - Logo da empresa
- [x] .htaccess - Configuração de redirecionamentos

## 📋 PASSOS PARA DEPLOY

### **1. ACESSO AO HOSPEDAGEM**
- [ ] Acessar cPanel/FTP do temvenda.com.br
- [ ] Fazer backup do .htaccess atual (caso necessário)
- [ ] Verificar espaço em disco disponível

### **2. UPLOAD DOS ARQUIVOS**
- [ ] Upload de todos os arquivos .html para a raiz do WordPress
- [ ] Upload do auth-manager.js para a raiz
- [ ] Upload do logo-temvenda.png para a raiz
- [ ] Verificar permissões dos arquivos (644 para arquivos, 755 para diretórios)

### **3. CONFIGURAÇÃO DO .HTACCESS**
- [ ] Fazer backup do .htaccess atual
- [ ] Substituir pelo novo .htaccess OU adicionar as regras ao existente
- [ ] Verificar se mod_rewrite está habilitado

### **4. TESTE DAS URLs**
- [ ] https://temvenda.com.br/home-moderna
- [ ] https://temvenda.com.br/diagnostico  
- [ ] https://temvenda.com.br/consultoria
- [ ] https://temvenda.com.br/formacao-lideres
- [ ] https://temvenda.com.br/palestras
- [ ] https://temvenda.com.br/treinamento-incompany
- [ ] https://temvenda.com.br/login-admin
- [ ] https://temvenda.com.br/admin-panel
- [ ] https://temvenda.com.br/admin-stats
- [ ] https://temvenda.com.br/admin-users
- [ ] https://temvenda.com.br/noticias

### **5. TESTE DO SISTEMA ADMINISTRATIVO**
- [ ] Login com cesar / temvenda2024
- [ ] Login com admin / temvenda2024
- [ ] Verificar permissões de usuários
- [ ] Testar upload de imagens
- [ ] Testar alteração de estatísticas

### **6. VERIFICAÇÕES FINAIS**
- [ ] SSL funcionando (https://)
- [ ] Responsividade em mobile
- [ ] Performance adequada
- [ ] Logo carregando corretamente
- [ ] Links internos funcionando

## 🔧 CONFIGURAÇÕES ADICIONAIS (OPCIONAL)

### **Sistema de Notícias**
- [ ] Configurar cron job para news_collector.py
- [ ] Verificar conexão com Supabase
- [ ] Testar coleta automática de notícias

### **Otimizações**
- [ ] Configurar cache do navegador
- [ ] Otimizar imagens se necessário
- [ ] Configurar CDN se disponível

## 🚨 POSSÍVEIS PROBLEMAS E SOLUÇÕES

### **Erro 404 nas URLs**
- Verificar se .htaccess foi aplicado corretamente
- Verificar se mod_rewrite está habilitado
- Verificar se os arquivos estão na raiz correta

### **Erro de permissões**
- Verificar permissões dos arquivos (644)
- Verificar permissões do diretório (755)

### **Problemas de CSS/JS**
- Verificar se auth-manager.js está acessível
- Verificar caminhos relativos dos recursos

### **Problemas de login**
- Verificar se Supabase está configurado
- Verificar credenciais no banco de dados

## 📞 SUPORTE
Se encontrar problemas durante o deploy, verifique:
1. Logs de erro do servidor
2. Console do navegador (F12)
3. Configurações do .htaccess
4. Permissões dos arquivos

## ✅ DEPLOY CONCLUÍDO QUANDO:
- [ ] Todas as URLs funcionando
- [ ] Sistema de login funcionando
- [ ] Área administrativa acessível
- [ ] Responsividade testada
- [ ] SSL funcionando
- [ ] Performance adequada

**🎉 SITE TEM VENDA EM PRODUÇÃO!**
