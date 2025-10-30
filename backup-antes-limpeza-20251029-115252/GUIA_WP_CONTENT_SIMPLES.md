# 🚀 DEPLOY NO WP-CONTENT - GUIA SIMPLES

## 📁 SITUAÇÃO
- ✅ Você tem acesso ao `wp-content/`
- ❌ Não tem acesso à pasta raiz
- 🎯 **SOLUÇÃO:** Deploy dentro do wp-content

## 📋 PASSOS SIMPLES

### **1. Criar pasta no wp-content**
No seu wp-content, crie uma pasta chamada `temvenda`

### **2. Upload dos arquivos**
Faça upload de TODOS os arquivos de `deploy-temvenda/` para:
```
📂 wp-content/temvenda/
├── admin-panel.html
├── admin-stats.html
├── admin-users.html
├── consultoria.html
├── diagnostico.html
├── formacao-lideres.html
├── home-corporativo.html
├── login-admin.html
├── noticias.html
├── palestras.html
├── treinamento-incompany.html
├── auth-manager.js
└── logo-temvenda.png
```

### **3. URLs que funcionarão**
- **Página inicial:** `https://temvenda.com.br/wp-content/temvenda/home-corporativo.html`
- **Login admin:** `https://temvenda.com.br/wp-content/temvenda/login-admin.html`
- **Painel notícias:** `https://temvenda.com.br/wp-content/temvenda/admin-panel.html`
- **Estatísticas:** `https://temvenda.com.br/wp-content/temvenda/admin-stats.html`
- **Usuários:** `https://temvenda.com.br/wp-content/temvenda/admin-users.html`
- **Diagnóstico:** `https://temvenda.com.br/wp-content/temvenda/diagnostico.html`
- **Consultoria:** `https://temvenda.com.br/wp-content/temvenda/consultoria.html`
- **Formação:** `https://temvenda.com.br/wp-content/temvenda/formacao-lideres.html`
- **Palestras:** `https://temvenda.com.br/wp-content/temvenda/palestras.html`
- **Treinamento:** `https://temvenda.com.br/wp-content/temvenda/treinamento-incompany.html`
- **Notícias:** `https://temvenda.com.br/wp-content/temvenda/noticias.html`

## 🔧 AJUSTES NECESSÁRIOS

### **Problema:** Caminhos podem não funcionar
### **Solução:** Ajustar manualmente nos arquivos

### **Exemplo de ajuste:**
Se um arquivo não carregar o logo ou JavaScript, você precisa alterar:

**ANTES:**
```html
<script src="auth-manager.js"></script>
<img src="logo-temvenda.png" alt="Logo">
```

**DEPOIS:**
```html
<script src="/wp-content/temvenda/auth-manager.js"></script>
<img src="/wp-content/temvenda/logo-temvenda.png" alt="Logo">
```

## 🎯 RESUMO FINAL

### **O que fazer:**
1. **Criar pasta** `temvenda` no `wp-content`
2. **Upload** de todos os arquivos para `wp-content/temvenda/`
3. **Testar** as URLs com `/wp-content/temvenda/`
4. **Ajustar** caminhos se necessário

### **URLs principais:**
- **Home:** `https://temvenda.com.br/wp-content/temvenda/home-corporativo.html`
- **Login:** `https://temvenda.com.br/wp-content/temvenda/login-admin.html`
- **Admin:** `https://temvenda.com.br/wp-content/temvenda/admin-panel.html`

### **Credenciais:**
- **Root:** `cesar` / `temvenda2024`
- **Admin:** `admin` / `temvenda2024`

**Esta solução funciona perfeitamente para seu caso!** 🎉
