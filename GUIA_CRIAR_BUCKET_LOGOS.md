# 📦 Guia: Criar Bucket "client-logos" no Supabase Storage

## Passo a Passo

### 1. Acesse o Painel do Supabase
- Acesse: https://supabase.com/dashboard
- Faça login na sua conta
- Selecione o projeto do site TEM VENDA

### 2. Navegue até Storage
- No menu lateral esquerdo, clique em **Storage**
- Você verá a lista de buckets existentes

### 3. Criar Novo Bucket
- Clique no botão **"New bucket"** ou **"Create bucket"**
- Preencha os campos:
  - **Name**: `client-logos` (exatamente esse nome, sem espaços)
  - **Public bucket**: ✅ **MARQUE ESTA OPÇÃO** (muito importante!)
  - **File size limit**: 5242880 (5MB) - opcional
  - **Allowed MIME types**: opcional (pode deixar vazio ou adicionar: `image/jpeg, image/png, image/gif, image/webp, image/svg+xml`)

### 4. Salvar
- Clique em **"Create bucket"** ou **"Save"**

### 5. Verificar
- O bucket `client-logos` deve aparecer na lista
- Deve estar marcado como **Public** (ícone de olho ou indicador público)

## ⚠️ Importante

- O bucket **DEVE** ser público para que as logos apareçam no site
- O nome deve ser exatamente `client-logos` (sem aspas)
- Após criar, aguarde alguns segundos antes de tentar fazer upload

## 🔧 Verificar Políticas (Opcional)

Se mesmo após criar o bucket ainda der erro, verifique as políticas:

1. No bucket `client-logos`, clique em **"Policies"**
2. Certifique-se de que há uma política para leitura pública
3. Se não houver, você pode criar uma política básica de leitura pública

## ✅ Testar

Após criar o bucket:
1. Recarregue a página `/stats.html`
2. Tente fazer upload de uma logo novamente
3. Se funcionar, você verá o preview da logo após o upload

