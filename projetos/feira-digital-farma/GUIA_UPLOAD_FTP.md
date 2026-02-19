# 📤 Guia de Upload FTP - Feira Digital Farma

## 🎯 Estrutura de Diretórios no FTP

A estrutura no servidor deve ser exatamente igual à estrutura local:

```
/htdocs/projetos/feira-digital-farma/
├── index.html
├── cadastro.html
├── contato.html
├── confirmar-email.html
├── login-participante.html
├── industrias.html
├── distribuidoras.html
├── parceiros-corporativos.html
├── admin/
│   ├── login.html
│   ├── dashboard.html
│   ├── auth-fdf.js
│   └── assets/
│       ├── css/
│       │   └── admin.css
│       └── js/
│           ├── dashboard.js
│           ├── crud-manager.js
│           ├── logo-upload.js
│           └── cnpj-upload.js
└── assets/
    ├── css/
    │   └── style.css
    └── js/
        ├── main.js
        ├── cadastro-participante.js
        ├── login-participante.js
        └── confirmar-email.js
```

---

## 📋 Lista Completa de Arquivos para Upload

### ✅ **Páginas Principais (Raiz)**
- `index.html` - Página inicial
- `cadastro.html` - Cadastro de participantes
- `contato.html` - Página de contato
- `confirmar-email.html` - Confirmação de email
- `login-participante.html` - Login de participantes
- `industrias.html` - Página para indústrias
- `distribuidoras.html` - Página para distribuidoras
- `parceiros-corporativos.html` - Página para parceiros corporativos

### ✅ **Área Administrativa**
- `admin/login.html` - Login administrativo
- `admin/dashboard.html` - Dashboard administrativo
- `admin/auth-fdf.js` - Autenticação administrativa
- `admin/assets/css/admin.css` - Estilos administrativos
- `admin/assets/js/dashboard.js` - Lógica do dashboard
- `admin/assets/js/crud-manager.js` - Gerenciador CRUD
- `admin/assets/js/logo-upload.js` - Upload de logos
- `admin/assets/js/cnpj-upload.js` - Upload de CNPJs

### ✅ **Assets (CSS e JS)**
- `assets/css/style.css` - Estilos principais
- `assets/js/main.js` - JavaScript principal
- `assets/js/cadastro-participante.js` - Lógica de cadastro
- `assets/js/login-participante.js` - Lógica de login
- `assets/js/confirmar-email.js` - Confirmação de email

---

## 🚫 **Arquivos que NÃO devem ser enviados**

### Arquivos de Documentação (apenas para referência local):
- `README.md`
- `COMO_GERAR_HASHES.md`
- `SOLUCAO_LOGIN_ADMIN.md`
- `DEBUG_DASHBOARD.md`
- `DEBUG_LOGIN.md`
- `INSTRUCOES_*.md`
- `RESUMO_*.md`
- `DIAGNOSTICO_*.md`
- `LOGINS_E_SENHAS.md`

### Arquivos de Teste/Desenvolvimento:
- `test-bcrypt.html`
- `gerar-hashes-admin.html`

### Arquivos SQL (executar no Supabase, não no FTP):
- `*.sql` - Todos os arquivos SQL devem ser executados no Supabase SQL Editor

---

## 📦 **Passo a Passo do Upload**

### **Opção 1: Upload Manual via FTP Client**

1. **Conectar ao FTP:**
   - Host: `ftp.temvenda.com.br` (ou seu servidor)
   - Usuário: seu usuário FTP
   - Senha: sua senha FTP
   - Porta: 21 (ou a porta configurada)

2. **Navegar até o diretório:**
   ```
   cd htdocs/projetos/
   ```

3. **Criar diretório (se não existir):**
   ```
   mkdir feira-digital-farma
   cd feira-digital-farma
   ```

4. **Criar subdiretórios:**
   ```
   mkdir admin
   mkdir admin/assets
   mkdir admin/assets/css
   mkdir admin/assets/js
   mkdir assets
   mkdir assets/css
   mkdir assets/js
   ```

5. **Upload dos arquivos (manter estrutura):**
   - Upload das páginas HTML na raiz
   - Upload dos arquivos da pasta `admin/`
   - Upload dos arquivos da pasta `assets/`

### **Opção 2: Upload via File Manager (cPanel)**

1. Acessar cPanel → File Manager
2. Navegar até `/htdocs/projetos/`
3. Criar pasta `feira-digital-farma` (se não existir)
4. Entrar na pasta e criar subpastas:
   - `admin/assets/css`
   - `admin/assets/js`
   - `assets/css`
   - `assets/js`
5. Upload dos arquivos mantendo a estrutura

### **Opção 3: Upload via Terminal (rsync/scp)**

```bash
# Exemplo com rsync (ajuste o caminho do servidor)
rsync -avz --exclude='*.md' --exclude='*.sql' --exclude='test-*.html' --exclude='gerar-*.html' \
  projetos/feira-digital-farma/ \
  usuario@servidor:/htdocs/projetos/feira-digital-farma/
```

---

## ✅ **Checklist de Upload**

### Antes do Upload:
- [ ] Verificar se todas as páginas HTML estão completas
- [ ] Verificar se todos os arquivos CSS e JS estão presentes
- [ ] Confirmar que as configurações do Supabase estão corretas nos arquivos HTML
- [ ] Testar localmente se possível

### Durante o Upload:
- [ ] Criar estrutura de pastas correta
- [ ] Upload de todos os arquivos HTML
- [ ] Upload de todos os arquivos CSS
- [ ] Upload de todos os arquivos JS
- [ ] Manter a estrutura de diretórios idêntica

### Após o Upload:
- [ ] Testar URL: `https://temvenda.com.br/projetos/feira-digital-farma/`
- [ ] Verificar se a página inicial carrega
- [ ] Testar navegação entre páginas
- [ ] Testar cadastro de participante
- [ ] Testar login administrativo: `https://temvenda.com.br/projetos/feira-digital-farma/admin/login.html`
- [ ] Verificar se os estilos estão carregando
- [ ] Verificar se os scripts estão funcionando
- [ ] Testar responsividade (mobile)

---

## 🔧 **Configurações Importantes**

### **Supabase**
Os arquivos HTML já contêm as configurações do Supabase inline:
- URL: `https://mgcoyeohqelystqmytah.supabase.co`
- Anon Key: (já configurada nos arquivos)

### **Google Fonts**
As fontes são carregadas via CDN:
- Poppins
- Playfair Display
- Montserrat

### **Bibliotecas Externas (CDN)**
- Supabase JS: `@supabase/supabase-js@2`
- Bcrypt.js: `bcryptjs@2.4.3`

---

## 🌐 **URLs Após Upload**

- **Página Inicial:** `https://temvenda.com.br/projetos/feira-digital-farma/`
- **Cadastro:** `https://temvenda.com.br/projetos/feira-digital-farma/cadastro.html`
- **Login Admin:** `https://temvenda.com.br/projetos/feira-digital-farma/admin/login.html`
- **Dashboard Admin:** `https://temvenda.com.br/projetos/feira-digital-farma/admin/dashboard.html`

---

## ⚠️ **Observações Importantes**

1. **Permissões de Arquivos:**
   - HTML, CSS, JS: `644` (leitura para todos, escrita para dono)
   - Diretórios: `755` (execução para todos)

2. **Banco de Dados:**
   - Execute todos os arquivos `.sql` no Supabase SQL Editor ANTES de testar o site
   - Principal: `CRIAR_BANCO_DADOS_COMPLETO.sql`
   - Storage: `CRIAR_STORAGE_LOGOS.sql`
   - Usuários: `CRIAR_USUARIO_ROOT_CEASR.sql`

3. **Segurança:**
   - Não faça upload de arquivos `.md` ou `.sql` para o servidor
   - Mantenha as configurações do Supabase seguras

4. **Cache:**
   - Após upload, limpe o cache do navegador (Ctrl+F5)
   - Se usar CDN, faça purge do cache

---

## 📞 **Suporte**

Se encontrar problemas após o upload:
1. Verifique o console do navegador (F12) para erros
2. Verifique se todos os arquivos foram enviados
3. Verifique se a estrutura de pastas está correta
4. Verifique se o banco de dados foi configurado no Supabase
