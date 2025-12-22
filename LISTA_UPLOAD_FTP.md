# 📤 Lista de Arquivos para Upload no FTP

## ✅ Arquivos Modificados (Obrigatório)

### **1. admin-stats.html**
- **Localização:** Raiz do projeto
- **O que mudou:** Upload de imagens para Supabase Storage
- **Tamanho:** ~125 KB
- **✅ OBRIGATÓRIO**

### **2. index.html**
- **Localização:** Raiz do projeto
- **O que mudou:** 
  - Melhorias no carregamento de logos
  - Inclusão do script `image-error-handler.js`
- **Tamanho:** ~270 KB
- **✅ OBRIGATÓRIO**

### **3. .htaccess**
- **Localização:** Raiz do projeto
- **O que mudou:**
  - Página 404 customizada
  - Remoção de parâmetro `?i=1`
  - Redirecionamento www
- **Tamanho:** ~2 KB
- **✅ OBRIGATÓRIO**

### **4. entrar.html**
- **Localização:** Raiz do projeto
- **O que mudou:** Verificado e confirmado correto
- **Tamanho:** ~11 KB
- **⚠️ Verificar se já existe no servidor**

---

## 🆕 Arquivos Novos (Obrigatório)

### **5. 404.html**
- **Localização:** Raiz do projeto
- **O que é:** Página de erro 404 customizada
- **Tamanho:** ~4.4 KB
- **✅ OBRIGATÓRIO**

### **6. scripts/image-error-handler.js**
- **Localização:** `scripts/image-error-handler.js`
- **O que é:** Script para tratamento de erros de imagens
- **Tamanho:** ~4.5 KB
- **✅ OBRIGATÓRIO**
- **⚠️ Criar pasta `scripts/` se não existir no servidor**

### **7. scripts/diagnostico-upload.js**
- **Localização:** `scripts/diagnostico-upload.js`
- **O que é:** Script de diagnóstico para upload de imagens
- **Tamanho:** ~6 KB
- **✅ RECOMENDADO** (ajuda a identificar problemas)
- **⚠️ Criar pasta `scripts/` se não existir no servidor**

---

## 📋 Checklist de Upload

### **Arquivos na Raiz:**
- [ ] `admin-stats.html` (modificado)
- [ ] `index.html` (modificado)
- [ ] `.htaccess` (modificado)
- [ ] `entrar.html` (verificar se já existe)
- [ ] `404.html` (novo)

### **Arquivos em Subpastas:**
- [ ] `scripts/image-error-handler.js` (novo)
- [ ] `scripts/diagnostico-upload.js` (novo)
- [ ] `scripts/load-page-images.js` (novo)
  - ⚠️ Criar pasta `scripts/` se não existir

### **Páginas com Imagens (Modificadas):**
- [ ] `formacao-lideranca.html` (modificado)
- [ ] `palestras.html` (modificado)
- [ ] `treinamento-empresa.html` (modificado)

---

## 🗂️ Estrutura no Servidor FTP

```
htdocs/
├── admin-stats.html          ← MODIFICADO
├── index.html                ← MODIFICADO
├── .htaccess                 ← MODIFICADO
├── entrar.html               ← VERIFICAR
├── 404.html                  ← NOVO
├── formacao-lideranca.html   ← MODIFICADO
├── palestras.html            ← MODIFICADO
├── treinamento-empresa.html  ← MODIFICADO
└── scripts/                  ← CRIAR SE NÃO EXISTIR
    ├── image-error-handler.js ← NOVO
    ├── diagnostico-upload.js   ← NOVO
    └── load-page-images.js     ← NOVO
```

---

## 📝 Ordem Recomendada de Upload

1. **Primeiro:** Criar pasta `scripts/` (se não existir)
2. **Segundo:** Upload de `scripts/image-error-handler.js`
3. **Terceiro:** Upload de `404.html`
4. **Quarto:** Upload de `.htaccess`
5. **Quinto:** Upload de `admin-stats.html`
6. **Sexto:** Upload de `index.html`
7. **Sétimo:** Verificar `entrar.html` (se não existir, fazer upload)

---

## ⚠️ Importante

### **Antes de Fazer Upload:**

1. **Backup:**
   - Faça backup dos arquivos atuais no servidor
   - Especialmente `.htaccess` e `index.html`

2. **Permissões:**
   - `.htaccess` deve ter permissão `644`
   - Arquivos HTML devem ter permissão `644`
   - Pasta `scripts/` deve ter permissão `755`

3. **Teste:**
   - Após upload, teste:
     - Página 404: `www.temvenda.com.br/pagina-teste`
     - Admin: `www.temvenda.com.br/admin-stats.html`
     - Home: `www.temvenda.com.br`

---

## 🔍 Verificações Pós-Upload

### **1. Página 404:**
```
Acesse: www.temvenda.com.br/pagina-inexistente
Esperado: Deve mostrar página 404 customizada
```

### **2. Remoção de ?i=1:**
```
Acesse: www.temvenda.com.br/?i=1
Esperado: Deve redirecionar para www.temvenda.com.br/index.html
```

### **3. Upload de Imagens:**
```
Acesse: www.temvenda.com.br/admin-stats.html
Teste: Selecionar imagem → Salvar imagem
Esperado: Mensagem "✅ Imagem salva com sucesso no Supabase Storage!"
```

### **4. Script de Imagens:**
```
Acesse: www.temvenda.com.br
Console (F12): Verificar se não há erros de carregamento
```

---

## 📊 Resumo

**Total de arquivos:** 10
- **Modificados:** 7
- **Novos:** 3

**Tamanho total aproximado:** ~330 KB

---

**Última atualização:** 2025-11-18

