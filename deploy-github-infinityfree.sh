#!/bin/bash

echo "🚀 Deploy TEM VENDA - GitHub + InfinityFree"
echo "============================================="

# Verificar se estamos no diretório correto
if [ ! -f "index.html" ]; then
    echo "❌ Execute este script no diretório raiz do projeto"
    exit 1
fi

# 1. Verificar se Git está inicializado
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
fi

# 2. Configurar remote para o repositório existente
echo "🔗 Configurando repositório remoto..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/cesark/site-temvenda.git

# 3. Fazer backup do repositório atual
echo "💾 Fazendo backup do repositório atual..."
git fetch origin
git checkout -b backup-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true
git checkout main 2>/dev/null || git checkout -b main

# 4. Criar .gitignore se não existir
if [ ! -f ".gitignore" ]; then
    echo "📝 Criando .gitignore..."
    cat > .gitignore << EOF
# Arquivos de configuração sensíveis
.env
supabase-config.js
email-config.js

# Logs
*.log
logs/

# Arquivos temporários
.DS_Store
Thumbs.db
*.tmp
*.temp

# Node modules (se houver)
node_modules/

# Arquivos de backup
*.bak
*.backup
EOF
fi

# 5. Adicionar todos os arquivos
echo "📦 Adicionando arquivos ao Git..."
git add .

# 6. Commit das mudanças
echo "💾 Fazendo commit das atualizações..."
git commit -m "🚀 Deploy Completo: Sistema de captura de leads Instagram

✅ Funcionalidades implementadas:
- Página de captura /instagram com design responsivo
- Admin completo para gerenciar textos e PDF
- Integração total com Supabase (leads + configurações)
- Envio automático de e-mail via EmailJS
- Funil de vendas integrado com drag & drop
- Upload de PDF para Storage público
- Sistema de permissões granular
- Histórico de atividades dos leads
- WhatsApp integrado nos cards
- Diagnóstico automático cria lead no funil

🔧 Arquivos principais:
- instagram.html (página de captura)
- admin-stats.html (gerenciamento Instagram)
- admin-funil.html (funil de vendas)
- supabase-config.js (configurações)
- email-config.js (EmailJS)

📊 Banco de dados:
- leads_funnel (leads do funil)
- lead_activities (histórico)
- instagram_capture_config (textos e PDF)
- diagnostics (resultados do diagnóstico)

🌐 URLs:
- /instagram (captura de leads)
- /admin (painel administrativo)
- /diagnostico (ferramenta de diagnóstico)"

# 7. Push para GitHub
echo "📤 Enviando para GitHub..."
git push origin main

echo ""
echo "✅ Deploy concluído com sucesso!"
echo ""
echo "📋 Resumo do que foi enviado:"
echo "- Sistema completo de captura de leads"
echo "- Admin para gerenciar conteúdo"
echo "- Integração com Supabase e EmailJS"
echo "- Funil de vendas com drag & drop"
echo "- Upload de PDF e imagens"
echo ""
echo "🔗 Repositório: https://github.com/cesark/site-temvenda"
echo ""
echo "📋 Próximos passos para InfinityFree:"
echo "1. Acesse o painel do InfinityFree"
echo "2. Vá em File Manager"
echo "3. Faça upload dos arquivos atualizados"
echo "4. Configure supabase-config.js e email-config.js"
echo ""
echo "🌐 URLs do site:"
echo "- Página principal: https://temvenda.com.br"
echo "- Captura Instagram: https://temvenda.com.br/instagram"
echo "- Admin: https://temvenda.com.br/admin"

echo ""
echo "✅ Deploy para GitHub concluído!"
echo ""
echo "📋 Próximos passos para InfinityFree:"
echo "1. Acesse o painel do InfinityFree"
echo "2. Vá em File Manager"
echo "3. Faça upload dos arquivos (ou use FTP)"
echo "4. Configure o domínio temvenda.com.br"
echo ""
echo "🔧 Arquivos importantes para configurar:"
echo "- supabase-config.js (credenciais do Supabase)"
echo "- email-config.js (credenciais do EmailJS)"
echo ""
echo "🌐 URLs do site:"
echo "- Página principal: https://temvenda.com.br"
echo "- Captura Instagram: https://temvenda.com.br/instagram"
echo "- Admin: https://temvenda.com.br/admin"
