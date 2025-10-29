# 🚀 DEPLOY PARA TEMVENDA.COM.BR

## 📋 ARQUIVOS PARA UPLOAD NO WORDPRESS

### **1. Páginas Principais (Upload via FTP/cPanel)**
```
/wordpress/
├── admin-panel.html          # Página de liberação de notícias
├── admin-stats.html          # Página de estatísticas
├── admin-users.html          # Página de usuários
├── login-admin.html          # Página de login
├── home-corporativo.html     # Página inicial moderna
├── diagnostico.html          # Página de diagnóstico
├── consultoria.html          # Página de consultoria
├── formacao-lideres.html     # Página de formação
├── palestras.html            # Página de palestras
├── treinamento-incompany.html # Página de treinamento
├── noticias.html             # Página pública de notícias
└── auth-manager.js           # Sistema de autenticação
```

### **2. Configuração do .htaccess**
Adicionar estas regras no `.htaccess` do WordPress:

```apache
# Redirecionamentos personalizados TEM VENDA
RewriteRule ^diagnostico/?$ /diagnostico.html [L,QSA]
RewriteRule ^home-moderna/?$ /home-corporativo.html [L,QSA]
RewriteRule ^formacao-lideres/?$ /formacao-lideres.html [L,QSA]
RewriteRule ^consultoria/?$ /consultoria.html [L,QSA]
RewriteRule ^palestras/?$ /palestras.html [L,QSA]
RewriteRule ^treinamento-incompany/?$ /treinamento-incompany.html [L,QSA]
RewriteRule ^login-admin/?$ /login-admin.html [L,QSA]
RewriteRule ^admin-panel/?$ /admin-panel.html [L,QSA]
RewriteRule ^admin-stats/?$ /admin-stats.html [L,QSA]
RewriteRule ^admin-users/?$ /admin-users.html [L,QSA]
RewriteRule ^noticias/?$ /noticias.html [L,QSA]
```

### **3. Configuração do Supabase**
Atualizar as URLs da API no arquivo `auth-manager.js`:
```javascript
const SUPABASE_URL = 'https://mgcoyeohqelystqmytah.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4';
```

### **4. URLs de Acesso**
Após o deploy, as páginas estarão disponíveis em:
- `https://temvenda.com.br/home-moderna` - Página inicial
- `https://temvenda.com.br/diagnostico` - Diagnóstico
- `https://temvenda.com.br/consultoria` - Consultoria
- `https://temvenda.com.br/formacao-lideres` - Formação
- `https://temvenda.com.br/palestras` - Palestras
- `https://temvenda.com.br/treinamento-incompany` - Treinamento
- `https://temvenda.com.br/login-admin` - Login administrativo
- `https://temvenda.com.br/admin-panel` - Liberação de notícias
- `https://temvenda.com.br/admin-stats` - Estatísticas
- `https://temvenda.com.br/admin-users` - Usuários
- `https://temvenda.com.br/noticias` - Notícias públicas

### **5. Credenciais de Acesso**
- **Root:** `cesar` / `temvenda2024`
- **Admin:** `admin` / `temvenda2024`

### **6. Sistema de Notícias**
- **Coletor:** `news_collector.py` (executar via cron)
- **Análise IA:** OpenAI API configurada
- **Banco:** Supabase configurado

## 🔧 PASSOS PARA DEPLOY

1. **Fazer upload dos arquivos HTML** para a raiz do WordPress
2. **Configurar .htaccess** com as regras de redirecionamento
3. **Testar todas as URLs** para verificar funcionamento
4. **Configurar cron job** para coleta automática de notícias
5. **Testar sistema de login** e permissões
6. **Verificar responsividade** em dispositivos móveis

## ✅ CHECKLIST DE DEPLOY
- [ ] Arquivos HTML uploadados
- [ ] .htaccess configurado
- [ ] URLs funcionando
- [ ] Login administrativo funcionando
- [ ] Sistema de notícias funcionando
- [ ] Responsividade testada
- [ ] SSL funcionando
- [ ] Performance otimizada
