# 🧹 Plano de Limpeza do Diretório Raiz

## 📋 Objetivo
Organizar o diretório raiz deixando apenas os arquivos essenciais para o site, com todos os links funcionando a partir da raiz (sem `/wp-content/temvenda/`).

---

## ✅ O QUE MANTER NA RAIZ

### **📄 Arquivos HTML do Site**
- `home-corporativo.html` (ou `index.html`)
- `consultoria.html`
- `formacao-lideres.html`
- `treinamento-incompany.html`
- `palestras.html`
- `diagnostico.html`
- `noticias.html`

### **🔐 Arquivos Administrativos**
- `login-admin.html`
- `admin-panel.html`
- `admin-stats.html`
- `admin-users.html`
- `auth-manager.js`

### **🖼️ Assets**
- `logo-temvenda.png`

### **📄 Arquivos de Configuração**
- `.htaccess` (para redirecionamentos)
- `.gitignore`
- `README.md` (atualizado)

### **🛠️ Scripts Úteis**
- `preparar-ftp.sh`
- `deploy-github-to-infinityfree.sh`

### **📚 Documentação Essencial**
- `GUIA_HOSPEDAGEM_GRATUITA.md`
- `GUIA_GITHUB_TO_INFINITYFREE.md`
- `GUIA_TESTE_LOCAL.md`

---

## 🗑️ O QUE REMOVER

### **📁 Pastas para Remover**
1. **`deploy-temvenda/`** - Arquivos de deploy antigo (conteúdo já em deploy-wp-content)
2. **`elementor/`** - Arquivos do Elementor (não usados mais)
3. **`html-pages/`** - Versões antigas das páginas HTML
4. **`html-standalone/`** - Versões standalone antigas
5. **`logs/`** - Logs não necessários
6. **`wordpress/`** - Toda a instalação WordPress local (manter apenas para desenvolvimento, ou remover se não usar mais)

### **📄 Arquivos de Documentação Redundantes**
Remover documentação duplicada ou desatualizada:
- `ANALISE_COMERCIAL_IA.md` (se não for necessário)
- `CHECKLIST_DEPLOY.md` (informações já em outros guias)
- `CRON_SETUP.md` (se não usar cron)
- `DEPLOY_TEMVENDA.md` (substituído por outros guias)
- `DEPLOY_WP_CONTENT.md` (informações já consolidadas)
- `GIT_DEPLOY_INSTRUCTIONS.md` (redundante)
- `GUIA_DEPLOY_TEMVENDA.md` (redundante)
- `GUIA_WP_CONTENT_SIMPLES.md` (redundante)
- `INSTRUCOES_COMPLETAS.md` (redundante)
- `MIGRATION_GUIDE.md` (não necessário mais)
- `ONDE_ESTA_PASTA_RAIZ.md` (redundante)
- `SISTEMA_COMPLETO.md` (redundante)
- `SISTEMA_FINAL_COMPLETO.md` (redundante)
- `SUPABASE_SETUP.md` (redundante - informações em SUPABASE_CONFIG.md)

### **Manter apenas:**
- `README.md`
- `SUPABASE_CONFIG.md`
- `GUIA_HOSPEDAGEM_GRATUITA.md`
- `GUIA_GITHUB_TO_INFINITYFREE.md`
- `GUIA_TESTE_LOCAL.md`
- `PLANO_LIMPEZA_RAIZ.md` (este arquivo)

---

## 🔧 AJUSTES NECESSÁRIOS NOS LINKS

### **De:**
```html
href="/wp-content/temvenda/consultoria.html"
src="/wp-content/temvenda/logo-temvenda.png"
```

### **Para:**
```html
href="/consultoria.html"
src="/logo-temvenda.png"
```

### **Arquivos que Precisam de Ajuste:**
- Todos os arquivos `.html` na raiz
- `auth-manager.js` (se tiver links)

---

## 📝 ESTRUTURA FINAL

```
site-temvenda/
├── index.html (ou home-corporativo.html)
├── consultoria.html
├── formacao-lideres.html
├── treinamento-incompany.html
├── palestras.html
├── diagnostico.html
├── noticias.html
├── login-admin.html
├── admin-panel.html
├── admin-stats.html
├── admin-users.html
├── auth-manager.js
├── logo-temvenda.png
├── .htaccess
├── .gitignore
├── README.md
├── SUPABASE_CONFIG.md
├── GUIA_HOSPEDAGEM_GRATUITA.md
├── GUIA_GITHUB_TO_INFINITYFREE.md
├── GUIA_TESTE_LOCAL.md
├── preparar-ftp.sh
├── deploy-github-to-infinityfree.sh
└── .git/
```

---

## 🚀 SCRIPT DE LIMPEZA

O script `limpar-diretorio-raiz.sh` será criado para:
1. Fazer backup dos arquivos importantes
2. Remover pastas desnecessárias
3. Copiar arquivos de `deploy-wp-content/temvenda/` para a raiz
4. Ajustar todos os links automaticamente
5. Criar `.htaccess` com redirecionamentos

---

## ⚠️ AVISOS IMPORTANTES

1. **BACKUP ANTES DE LIMPAR!**
2. **Git:** Os arquivos removidos ainda estarão no histórico do Git
3. **WordPress Local:** Se ainda usa para desenvolvimento, considere manter a pasta `wordpress/`
4. **Teste:** Após limpeza, teste todos os links localmente

---

## ✅ CHECKLIST DE EXECUÇÃO

- [ ] Fazer backup completo
- [ ] Executar script de limpeza
- [ ] Verificar arquivos na raiz
- [ ] Ajustar links (se necessário)
- [ ] Testar todas as páginas localmente
- [ ] Testar todos os links
- [ ] Verificar responsividade
- [ ] Commit no Git

---

**Última atualização:** $(date)


