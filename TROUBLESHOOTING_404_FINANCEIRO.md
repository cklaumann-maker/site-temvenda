# 🔍 Troubleshooting: Erro 404 em /financeiro/

## ❌ Problema

Ao acessar `https://www.temvenda.com.br/financeiro/`, aparece erro 404:
```
Failed to load resource: the server responded with a status of 404 (Not Found)
```

---

## ✅ Soluções Possíveis

### 1. Verificar se os Arquivos Foram Enviados

**Via FTP, verifique se existem:**
- `/financeiro/index.html`
- `/financeiro/config-api.js`

**Como verificar:**
1. Conecte via FTP ao servidor
2. Navegue até a raiz do site (geralmente `public_html/` ou `htdocs/`)
3. Verifique se existe a pasta `financeiro/`
4. Dentro dela, devem estar os 2 arquivos

**Se não existirem:**
- Envie os arquivos novamente
- Certifique-se de que a pasta `financeiro/` foi criada na raiz

---

### 2. Verificar Caminho Correto no Servidor

**Estrutura correta no servidor:**
```
/
├── index.html (página principal)
├── financeiro/
│   ├── index.html      ← Deve estar aqui
│   └── config-api.js   ← Deve estar aqui
└── .htaccess
```

**Caminhos incorretos comuns:**
- ❌ `/public_html/financeiro/index.html` (se a raiz já é public_html)
- ❌ `/www/financeiro/index.html` (se a raiz já é www)
- ✅ `/financeiro/index.html` (na raiz do site)

---

### 3. Adicionar Regra no .htaccess (se necessário)

Se o servidor usa WordPress ou tem regras de rewrite, pode ser necessário adicionar uma regra.

**Edite o arquivo `.htaccess` na raiz do servidor e adicione:**

```apache
# Permitir acesso direto à pasta financeiro
RewriteRule ^financeiro/?$ /financeiro/index.html [L]
```

**OU, se já houver regras do WordPress, adicione ANTES das regras do WordPress:**

```apache
# Regras personalizadas (ANTES do WordPress)
RewriteEngine On

# Módulo Financeiro
RewriteRule ^financeiro/?$ /financeiro/index.html [L]

# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
```

---

### 4. Testar Acesso Direto ao Arquivo

Tente acessar diretamente:
```
https://www.temvenda.com.br/financeiro/index.html
```

**Se funcionar:**
- O arquivo existe, mas precisa de regra no .htaccess

**Se não funcionar:**
- O arquivo não foi enviado ou está no lugar errado

---

### 5. Verificar Permissões dos Arquivos

Via FTP, verifique as permissões:
- `index.html`: **644** (rw-r--r--)
- `config-api.js`: **644** (rw-r--r--)
- Pasta `financeiro/`: **755** (rwxr-xr-x)

**Como alterar (se necessário):**
- Clique com botão direito no arquivo → Properties/Permissions
- Defina: Owner: Read+Write, Group: Read, Others: Read

---

### 6. Verificar se o Servidor Suporta Subpastas

Alguns servidores podem ter restrições. Teste:

1. **Criar arquivo de teste:**
   - Crie `financeiro/teste.html` com conteúdo: `<h1>Teste</h1>`
   - Envie via FTP
   - Acesse: `https://www.temvenda.com.br/financeiro/teste.html`

2. **Se funcionar:**
   - O servidor suporta subpastas
   - O problema é específico do `index.html`

3. **Se não funcionar:**
   - Pode haver restrição no servidor
   - Considere colocar os arquivos na raiz com nomes diferentes

---

## 🔧 Solução Alternativa: Arquivos na Raiz

Se a subpasta não funcionar, você pode colocar os arquivos na raiz:

**Renomear:**
- `financeiro/index.html` → `financeiro.html` (na raiz)
- `financeiro/config-api.js` → `financeiro-config.js` (na raiz)

**E atualizar o HTML:**
- No `financeiro.html`, altere: `<script src="config-api.js">` para `<script src="financeiro-config.js">`

**Adicionar regra no .htaccess:**
```apache
RewriteRule ^financeiro/?$ /financeiro.html [L]
```

---

## 📋 Checklist de Verificação

- [ ] Arquivos enviados via FTP
- [ ] Pasta `financeiro/` existe na raiz
- [ ] `index.html` está dentro de `financeiro/`
- [ ] `config-api.js` está dentro de `financeiro/`
- [ ] Permissões corretas (644 para arquivos, 755 para pasta)
- [ ] Teste direto: `/financeiro/index.html` funciona?
- [ ] Regra no `.htaccess` adicionada (se necessário)

---

## 🆘 Ainda com Problemas?

1. **Verificar logs do servidor** (se tiver acesso)
2. **Contatar suporte da hospedagem** sobre acesso a subpastas
3. **Testar com arquivo simples** primeiro (teste.html)
4. **Verificar se há firewall ou bloqueios** no servidor

---

## 💡 Dica Rápida

A forma mais simples de testar:
1. Acesse diretamente: `https://www.temvenda.com.br/financeiro/index.html`
2. Se funcionar → adicione regra no .htaccess
3. Se não funcionar → arquivo não foi enviado ou está no lugar errado

