# 🔧 CONFIGURAÇÃO SUPABASE PARA PRODUÇÃO

## 📋 VERIFICAÇÕES NECESSÁRIAS

### **1. Configurações do Supabase**
```javascript
// Verificar se estas configurações estão corretas em auth-manager.js
const SUPABASE_URL = 'https://mgcoyeohqelystqmytah.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4';
```

### **2. Tabelas Necessárias no Supabase**
- [ ] `admin_users` - Usuários do sistema administrativo
- [ ] `news_articles` - Artigos de notícias
- [ ] `news_sources` - Fontes de notícias
- [ ] `news_categories` - Categorias de notícias
- [ ] `news_tags` - Tags das notícias
- [ ] `news_approvals` - Aprovações de notícias

### **3. Usuários Padrão**
```sql
-- Verificar se estes usuários existem no Supabase
SELECT username, role, is_active FROM admin_users;

-- Usuários esperados:
-- cesar (root) - temvenda2024
-- admin (admin) - temvenda2024
```

### **4. Permissões dos Usuários**
```sql
-- Verificar permissões do usuário admin
SELECT username, permissions FROM admin_users WHERE username = 'admin';

-- Deve ter:
-- {
--   "manage_users": true,
--   "manage_news": true, 
--   "manage_stats": true,
--   "manage_images": true
-- }
```

## 🔐 CREDENCIAIS DE ACESSO

### **Sistema Administrativo**
- **Root:** `cesar` / `temvenda2024`
- **Admin:** `admin` / `temvenda2024`

### **Supabase Dashboard**
- **URL:** https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
- **Usar suas credenciais do Supabase**

## 📰 SISTEMA DE NOTÍCIAS (OPCIONAL)

### **Configuração do Coletor**
```python
# Arquivo: news_collector.py
# Configurar cron job para executar a cada 6 horas
# 0 */6 * * * /usr/bin/python3 /path/to/news_collector.py
```

### **Fontes de Notícias Configuradas**
- Panorama Farmacêutico
- Sincofarma
- Outras fontes farmacêuticas

### **Análise com IA**
- OpenAI API configurada
- Análise comercial automática
- Insights para gestores

## 🚨 TROUBLESHOOTING

### **Erro de Conexão com Supabase**
1. Verificar se a URL está correta
2. Verificar se a API key está válida
3. Verificar se o projeto está ativo
4. Verificar logs do navegador (F12)

### **Erro de Login**
1. Verificar se usuário existe no banco
2. Verificar se senha está correta
3. Verificar se usuário está ativo
4. Verificar hash da senha (SHA-256)

### **Erro de Permissões**
1. Verificar JSON de permissões no banco
2. Verificar se usuário tem role correto
3. Verificar se permissão específica está true

## ✅ TESTE FINAL
Após o deploy, testar:
1. Login administrativo
2. Navegação entre páginas admin
3. Upload de imagens
4. Alteração de estatísticas
5. Gerenciamento de usuários
6. Sistema de notícias (se configurado)

**🎯 Sistema pronto para produção!**
