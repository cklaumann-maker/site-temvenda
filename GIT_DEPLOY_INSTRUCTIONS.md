# Configuração do Git para o projeto TEM VENDA
# Execute estes comandos manualmente no terminal:

# 1. Configurar Git (se ainda não configurado)
git config --global user.name "Cesar Klaumann"
git config --global user.email "cklaumann@gmail.com"

# 2. Inicializar repositório (se ainda não inicializado)
git init

# 3. Conectar ao repositório GitHub
git remote add origin https://github.com/cklaumann-maker/site-temvenda.git

# 4. Adicionar todos os arquivos
git add .

# 5. Fazer commit inicial
git commit -m "Initial commit: Site TEM VENDA com sistema completo de administração"

# 6. Fazer push para o GitHub
git branch -M main
git push -u origin main

# Arquivos principais incluídos:
# - admin-panel-corporativo.html (página de liberação de notícias)
# - admin-stats-corporativo.html (página de estatísticas)
# - admin-users-complete.html (página de usuários)
# - home-corporativo.html (página inicial)
# - login-admin-new.html (página de login)
# - auth-manager.js (sistema de autenticação)
# - Todas as páginas de serviços (consultoria, formação, palestras, etc.)
# - Sistema completo de notícias com Supabase
# - Docker configuration
# - Documentação completa
