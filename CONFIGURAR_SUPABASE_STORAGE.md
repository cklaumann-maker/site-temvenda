# 📦 Configurar Supabase Storage para Imagens

## 🎯 Objetivo

Configurar o bucket `client-logos` no Supabase Storage para que as imagens dos clientes parceiros apareçam no site.

---

## 📋 Passo a Passo

### **1. Criar o Bucket no Supabase**

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto: **TEM VENDA**
3. No menu lateral, clique em **Storage**
4. Clique em **"New bucket"** ou **"Criar bucket"**
5. Configure:
   - **Name:** `client-logos`
   - **Public bucket:** ✅ **MARQUE ESTA OPÇÃO** (importante!)
   - **File size limit:** 5 MB (ou o que preferir)
   - **Allowed MIME types:** `image/*` (ou deixe vazio para permitir todos)
6. Clique em **"Create bucket"**

### **2. Configurar Permissões (RLS Policies)**

Após criar o bucket, configure as políticas:

1. Clique no bucket `client-logos`
2. Vá em **"Policies"** ou **"Políticas"**
3. Clique em **"New Policy"**
4. Selecione **"For full customization"**
5. Configure:

**Policy Name:** `Public read access`

**Policy Definition:**
```sql
CREATE POLICY "Public read access"
ON storage.objects
FOR SELECT
USING (bucket_id = 'client-logos');
```

6. Salve a política

### **3. Configurar CORS (Opcional mas Recomendado)**

1. No Supabase Dashboard, vá em **Settings** → **API**
2. Role até **"CORS Configuration"**
3. Adicione seu domínio:
   ```
   https://www.temvenda.com.br
   https://temvenda.com.br
   http://localhost:8000
   ```
4. Salve

---

## 📤 Fazer Upload das Imagens

### **Opção 1: Via Interface do Supabase (Mais Fácil)**

1. No Supabase Dashboard, vá em **Storage**
2. Clique no bucket `client-logos`
3. Clique em **"Upload file"** ou **"Upload arquivo"**
4. Selecione as imagens dos logos dos clientes
5. Aguarde o upload completar

**Formatos suportados:**
- `.png`
- `.jpg` / `.jpeg`
- `.svg`
- `.webp`
- `.gif`

### **Opção 2: Via Script Python (Automático)**

Use o script `upload_logos_to_supabase.py` (será criado abaixo)

---

## 🔍 Verificar se Está Funcionando

### **1. Teste no Console do Navegador**

1. Abra o site: `www.temvenda.com.br`
2. Abra o Console (F12)
3. Procure por:
   - `✅ Imagem carregada: [URL]` → Funcionando!
   - `⚠️ Imagem não carregou: [URL]` → Problema
   - `❌ Erro ao carregar logos do Supabase` → Erro de conexão

### **2. Teste Direto da URL**

1. No Supabase Dashboard, vá em **Storage** → `client-logos`
2. Clique em uma imagem
3. Copie a URL pública
4. Cole no navegador
5. Deve abrir a imagem diretamente

---

## 🚨 Problemas Comuns

### **Problema: "Bucket not found"**

**Causa:** Bucket não foi criado ou nome está errado

**Solução:**
- Verifique se o bucket se chama exatamente `client-logos`
- Verifique se está no projeto correto do Supabase

### **Problema: "Access denied" ou "Forbidden"**

**Causa:** Bucket não está público ou políticas RLS não estão configuradas

**Solução:**
1. Verifique se marcou "Public bucket" ao criar
2. Verifique se a política RLS está ativa
3. Verifique se a política permite SELECT

### **Problema: "CORS error"**

**Causa:** CORS não configurado para seu domínio

**Solução:**
1. Configure CORS no Supabase (passo 3 acima)
2. Adicione seu domínio na lista de origens permitidas

### **Problema: Imagens não aparecem**

**Causa:** Bucket vazio ou imagens não foram enviadas

**Solução:**
1. Verifique se há imagens no bucket
2. Verifique se os nomes dos arquivos estão corretos
3. Verifique o console do navegador para erros

---

## 📝 Checklist

- [ ] Bucket `client-logos` criado
- [ ] Bucket marcado como **público**
- [ ] Política RLS configurada para leitura pública
- [ ] CORS configurado (opcional mas recomendado)
- [ ] Imagens enviadas para o bucket
- [ ] Testado no console do navegador
- [ ] Imagens aparecem no site

---

## 💡 Dicas

1. **Nomes de arquivos:**
   - Use nomes descritivos: `cliente-empresa.png`
   - Evite espaços: use `-` ou `_`
   - Use letras minúsculas

2. **Tamanho das imagens:**
   - Otimize antes de enviar
   - Recomendado: máximo 200KB por logo
   - Formato: PNG com transparência ou JPG

3. **Organização:**
   - Todas as imagens na raiz do bucket
   - Não use subpastas (por enquanto)

---

**Última atualização:** 2025-11-18

