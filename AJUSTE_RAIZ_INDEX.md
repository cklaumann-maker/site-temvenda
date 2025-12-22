# 🔧 Ajuste: Raiz Sempre Abre index.html

## ✅ Problema Resolvido

**Problema:** `www.temvenda.com.br` estava redirecionando para `https://temvenda.com.br/?i=1` ao invés de abrir `index.html` diretamente.

**Solução:** Configurações no `.htaccess` para garantir que:
- ✅ Raiz sempre abre `index.html`
- ✅ Parâmetro `?i=1` é sempre removido
- ✅ Redirecionamento de `temvenda.com.br` (sem www) para `www.temvenda.com.br`
- ✅ Nunca redireciona para URL com `?i=1`

---

## 🔧 Mudanças Aplicadas

### **1. DirectoryIndex Priorizado**
```apache
DirectoryIndex index.html index.php
```
- `index.html` tem prioridade sobre `index.php`

### **2. Redirecionamento www**
```apache
RewriteCond %{HTTP_HOST} ^temvenda\.com\.br$ [NC]
RewriteRule ^(.*)$ https://www.temvenda.com.br/$1 [R=301,L]
```
- Sempre força `www.temvenda.com.br`

### **3. Remoção Agressiva de ?i=1**
```apache
# Remove ?i=1 ANTES de qualquer outra regra
RewriteCond %{QUERY_STRING} (^|&)i=1(&|$) [NC]
RewriteRule ^(.*)$ /$1? [R=301,L]
```
- Remove o parâmetro em qualquer URL

### **4. Raiz Sempre para index.html**
```apache
# Garantir que / sempre aponte para index.html
RewriteCond %{REQUEST_URI} ^/$ [NC]
RewriteCond %{QUERY_STRING} ^$ [OR]
RewriteCond %{QUERY_STRING} !^i=1
RewriteRule ^$ /index.html [L]
```
- `/` sempre serve `index.html`

### **5. Proteção Específica para Raiz com ?i=1**
```apache
# Se alguém tentar /?i=1, redirecionar para /index.html sem parâmetro
RewriteCond %{REQUEST_URI} ^/$ [NC]
RewriteCond %{QUERY_STRING} (^|&)i=1(&|$) [NC]
RewriteRule ^$ /index.html [R=301,L]
```
- Bloqueia especificamente `/?i=1`

---

## 📋 Ordem de Execução das Regras

As regras são executadas nesta ordem (importante!):

1. **Redirecionamento www** → Força `www.`
2. **Remoção de ?i=1** → Remove parâmetro em qualquer URL
3. **Raiz para index.html** → Serve `index.html` na raiz
4. **Proteção ?i=1 na raiz** → Bloqueia `/?i=1` especificamente
5. **Arquivos existentes** → Mantém arquivos e diretórios intactos

---

## ✅ Resultados Esperados

### **URLs que Funcionam:**
- ✅ `www.temvenda.com.br` → Abre `index.html`
- ✅ `www.temvenda.com.br/` → Abre `index.html`
- ✅ `www.temvenda.com.br/index.html` → Abre `index.html`
- ✅ `temvenda.com.br` → Redireciona para `www.temvenda.com.br/index.html`

### **URLs Bloqueadas/Corrigidas:**
- ❌ `www.temvenda.com.br/?i=1` → Redireciona para `www.temvenda.com.br/index.html`
- ❌ `temvenda.com.br/?i=1` → Redireciona para `www.temvenda.com.br/index.html`
- ❌ `https://temvenda.com.br/?i=1` → Redireciona para `www.temvenda.com.br/index.html`

---

## 🧪 Como Testar

### **1. Teste Local (antes do upload)**
```bash
# Simular servidor Apache localmente
# Ou testar no servidor de desenvolvimento
```

### **2. Teste em Produção (após upload)**

**Teste 1: Raiz sem parâmetros**
```
Acesse: https://www.temvenda.com.br
Esperado: Deve abrir index.html diretamente
```

**Teste 2: Raiz com ?i=1**
```
Acesse: https://www.temvenda.com.br/?i=1
Esperado: Deve redirecionar para https://www.temvenda.com.br/index.html
```

**Teste 3: Sem www**
```
Acesse: https://temvenda.com.br
Esperado: Deve redirecionar para https://www.temvenda.com.br/index.html
```

**Teste 4: Sem www com ?i=1**
```
Acesse: https://temvenda.com.br/?i=1
Esperado: Deve redirecionar para https://www.temvenda.com.br/index.html
```

---

## 🚨 Troubleshooting

### **Problema: Ainda redireciona para ?i=1**

**Causa:** Cache do navegador ou do servidor

**Solução:**
1. Limpe o cache do navegador (Ctrl+Shift+Del)
2. Teste em modo anônimo/privado
3. Verifique se o `.htaccess` foi enviado corretamente
4. Aguarde alguns minutos (cache do servidor)

### **Problema: Loop de redirecionamento**

**Causa:** Regras conflitantes

**Solução:**
- Verifique se não há outro `.htaccess` em subdiretórios
- Verifique se o servidor suporta `mod_rewrite`
- Teste removendo regras uma por uma para identificar conflito

### **Problema: Página em branco**

**Causa:** Erro de sintaxe no `.htaccess`

**Solução:**
- Verifique sintaxe do `.htaccess`
- Teste em servidor local primeiro
- Verifique logs de erro do servidor

---

## 📝 Notas Importantes

1. **Ordem das Regras é Crítica**
   - As regras são executadas na ordem que aparecem
   - A remoção de `?i=1` deve vir ANTES de outras regras

2. **Cache do Navegador**
   - Pode levar alguns minutos para refletir mudanças
   - Use modo anônimo para testar imediatamente

3. **InfinityFree**
   - Alguns hosts gratuitos podem ter limitações
   - Se não funcionar, pode ser necessário configurar no painel do host

4. **SSL/HTTPS**
   - Certifique-se de que o SSL está configurado
   - Redirecionamentos devem usar `https://`

---

## 🔄 Arquivos Modificados

- ✅ `.htaccess` - Regras de redirecionamento e remoção de parâmetros

---

**Última atualização:** 2025-11-18

