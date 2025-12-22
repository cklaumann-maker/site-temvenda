# 🔧 Ajuste: Upload de Imagens para Supabase Storage

## ✅ O Que Foi Ajustado

A página `admin-stats.html` foi atualizada para fazer upload de imagens diretamente para o **Supabase Storage** ao invés de salvar apenas no `localStorage`.

---

## 🎯 Mudanças Aplicadas

### **1. Função `saveImage()` Atualizada**

**Antes:**
- ❌ Salvava apenas no `localStorage` (base64)
- ❌ Limitado a ~5MB
- ❌ Não acessível de outros dispositivos

**Agora:**
- ✅ Faz upload para Supabase Storage (bucket `page-images`)
- ✅ Salva URL pública no `localStorage` como fallback
- ✅ Sem limite de tamanho (limitado pelo Supabase)
- ✅ Acessível de qualquer lugar
- ✅ Fallback para localStorage se upload falhar

### **2. Função `confirmSave()` Atualizada**

- ✅ Agora é `async` (aguarda upload)
- ✅ Mostra mensagem de progresso
- ✅ Feedback visual durante upload

### **3. Função `removeImage()` Atualizada**

- ✅ Remove do Supabase Storage quando aplicável
- ✅ Remove do localStorage
- ✅ Feedback visual

---

## 📦 Bucket Necessário

O código cria automaticamente o bucket `page-images` se não existir, mas é recomendado criar manualmente:

### **Criar Bucket no Supabase:**

1. Acesse: https://supabase.com/dashboard
2. Vá em **Storage** → **New bucket**
3. Configure:
   - **Name:** `page-images`
   - **Public bucket:** ✅ **MARQUE ESTA OPÇÃO**
   - **File size limit:** 10 MB (ou o que preferir)
   - **Allowed MIME types:** `image/*`
4. Clique em **Create bucket**

### **Configurar Política RLS:**

1. No bucket `page-images`, vá em **Policies**
2. Crie política de leitura pública:
   ```sql
   CREATE POLICY "Public read access"
   ON storage.objects
   FOR SELECT
   USING (bucket_id = 'page-images');
   ```

---

## 🔍 Como Funciona Agora

### **Fluxo de Upload:**

1. Usuário seleciona imagem
2. Imagem é comprimida (máx 1600x1200px)
3. **Upload para Supabase Storage** (bucket `page-images`)
4. URL pública é obtida
5. URL é salva no `localStorage` como fallback
6. Preview atualizado com URL do Supabase

### **Fluxo de Remoção:**

1. Usuário clica em "Remover"
2. Remove do `localStorage`
3. Remove do Supabase Storage (se aplicável)
4. Preview limpo

---

## 🚨 Importante: Service Key

O código usa `serviceKey` para fazer upload (precisa de permissões de escrita).

**Verifique se está configurado:**

No `admin-stats.html`, procure por:
```javascript
window.SUPABASE_CONFIG = {
    url: '...',
    anonKey: '...',
    serviceKey: '...'  // ← DEVE ESTAR PRESENTE!
};
```

**Se não estiver:**
- Adicione a `serviceKey` na configuração
- Ou o upload falhará e usará fallback para localStorage

---

## 📋 Checklist

- [ ] Bucket `page-images` criado no Supabase
- [ ] Bucket marcado como **público**
- [ ] Política RLS configurada (leitura pública)
- [ ] `serviceKey` configurada no `admin-stats.html`
- [ ] Testar upload de imagem
- [ ] Verificar se imagem aparece no Supabase Storage
- [ ] Testar remoção de imagem

---

## 🧪 Como Testar

1. Acesse: `/admin-stats.html`
2. Vá na seção "🖼️ Gerenciar Imagens das Páginas"
3. Selecione uma imagem
4. Clique em "Salvar imagem"
5. Verifique:
   - ✅ Mensagem de sucesso aparece
   - ✅ Preview mostra a imagem
   - ✅ No Supabase Dashboard → Storage → `page-images` → deve ter a imagem

---

## 🔄 Fallback

Se o upload para Supabase falhar:
- ✅ Imagem é salva no `localStorage` (base64)
- ✅ Funciona normalmente, mas limitado a ~5MB
- ✅ Mensagem de aviso é exibida

---

## 📝 Notas Técnicas

### **Estrutura no Storage:**
```
page-images/
  └── images/
      ├── formacao-lider.jpg
      ├── formacao-cesar.jpg
      ├── palestras-hero.jpg
      ├── palestras-cesar.jpg
      └── treinamento-hero.jpg
```

### **Formato de URLs:**
```
https://[PROJECT].supabase.co/storage/v1/object/public/page-images/images/[nome].jpg
```

---

**Última atualização:** 2025-11-18

