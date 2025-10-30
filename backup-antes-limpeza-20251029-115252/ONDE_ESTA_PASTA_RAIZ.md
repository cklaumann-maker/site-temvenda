# 📁 LOCALIZAÇÃO DA PASTA RAIZ DO WORDPRESS

## 🏠 ONDE ENCONTRAR A PASTA RAIZ

### **Opção 1: cPanel (Mais Comum)**
```
📂 public_html/
├── wp-config.php          ← ARQUIVO PRINCIPAL DO WORDPRESS
├── wp-content/
├── wp-admin/
├── wp-includes/
├── index.php
└── .htaccess              ← AQUI VOCÊ VAI SUBSTITUIR/EDITAR
```

### **Opção 2: Estrutura Alternativa**
```
📂 www/
├── wp-config.php          ← ARQUIVO PRINCIPAL DO WORDPRESS
├── wp-content/
├── wp-admin/
├── wp-includes/
├── index.php
└── .htaccess
```

### **Opção 3: Subdomínio**
```
📂 temvenda.com.br/
├── wp-config.php          ← ARQUIVO PRINCIPAL DO WORDPRESS
├── wp-content/
├── wp-admin/
├── wp-includes/
├── index.php
└── .htaccess
```

## 🔍 COMO IDENTIFICAR A PASTA CORRETA

### **Sinais de que você está na pasta certa:**
- ✅ Arquivo `wp-config.php` presente
- ✅ Pasta `wp-content/` presente
- ✅ Pasta `wp-admin/` presente
- ✅ Pasta `wp-includes/` presente
- ✅ Arquivo `index.php` presente
- ✅ Arquivo `.htaccess` presente (ou deveria estar)

### **❌ Se você NÃO vê esses arquivos:**
- Você está na pasta errada
- Continue navegando até encontrar

## 📋 PASSOS PARA ENCONTRAR

### **No cPanel:**
1. Acesse "Gerenciador de Arquivos"
2. Clique em `public_html`
3. Procure pelo arquivo `wp-config.php`
4. Se encontrar, você está na pasta certa!

### **No FTP:**
1. Conecte com suas credenciais
2. Navegue até a pasta principal
3. Procure pelo arquivo `wp-config.php`
4. Se encontrar, você está na pasta certa!

## 🎯 ONDE FAZER UPLOAD DOS ARQUIVOS

### **Arquivos para upload na MESMA pasta onde está:**
- `wp-config.php` ← **REFERÊNCIA PRINCIPAL**
- `wp-content/`
- `wp-admin/`
- `wp-includes/`

### **Seus arquivos TEM VENDA vão ficar junto com:**
```
📂 public_html/ (ou pasta raiz)
├── wp-config.php          ← WordPress
├── wp-content/            ← WordPress
├── wp-admin/              ← WordPress
├── wp-includes/           ← WordPress
├── index.php              ← WordPress
├── .htaccess              ← WordPress (você vai editar)
├── admin-panel.html       ← SEU ARQUIVO
├── admin-stats.html       ← SEU ARQUIVO
├── home-corporativo.html  ← SEU ARQUIVO
├── auth-manager.js        ← SEU ARQUIVO
├── logo-temvenda.png      ← SEU ARQUIVO
└── ... (todos os outros arquivos HTML)
```

## ⚠️ IMPORTANTE

### **NÃO faça upload em:**
- ❌ `wp-content/` (pasta de conteúdo)
- ❌ `wp-admin/` (pasta administrativa)
- ❌ `wp-includes/` (pasta de includes)
- ❌ Subpastas

### **FAÇA upload na:**
- ✅ **Pasta raiz** (mesmo nível do wp-config.php)
- ✅ **Mesma pasta** onde estão wp-content/, wp-admin/, etc.

## 🔧 EXEMPLO PRÁTICO

Se você está no cPanel e vê:
```
📂 public_html/
├── wp-config.php
├── wp-content/
├── wp-admin/
├── wp-includes/
├── index.php
└── .htaccess
```

**FAÇA UPLOAD DOS SEUS ARQUIVOS AQUI:**
```
📂 public_html/
├── wp-config.php          ← WordPress
├── wp-content/            ← WordPress
├── wp-admin/              ← WordPress
├── wp-includes/           ← WordPress
├── index.php              ← WordPress
├── .htaccess              ← WordPress (você vai editar)
├── admin-panel.html       ← SEU UPLOAD
├── admin-stats.html       ← SEU UPLOAD
├── home-corporativo.html  ← SEU UPLOAD
├── auth-manager.js        ← SEU UPLOAD
├── logo-temvenda.png      ← SEU UPLOAD
└── ... (todos os outros)
```

## 🎯 RESUMO

**A pasta raiz do WordPress é onde está o arquivo `wp-config.php`**

**Faça upload dos seus arquivos na MESMA pasta onde está o `wp-config.php`**
