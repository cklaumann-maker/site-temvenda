# 🔧 Corrigir Tabela de Perfil

## ⚠️ Problema

A tabela `user_profiles` foi criada com uma estrutura incorreta que causava erro ao salvar.

## ✅ Solução

Execute o SQL abaixo no Supabase SQL Editor para corrigir a tabela:

### **OPÇÃO 1: Se a tabela ainda não foi criada**

Execute apenas a migration normal:
- `supabase/migrations/20240101000006_create_user_profiles.sql`

### **OPÇÃO 2: Se a tabela já foi criada (com erro)**

Execute o script de correção:
- `supabase/corrigir_user_profiles.sql`

Este script vai:
1. Deletar a tabela antiga (se existir)
2. Recriar com a estrutura correta
3. Configurar RLS corretamente
4. Criar triggers necessários

## 📋 Estrutura Correta

A tabela agora usa apenas `user_id` como PRIMARY KEY (sem campo `id` duplicado):

```sql
CREATE TABLE public.user_profiles (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT,
  phone TEXT,
  cpf TEXT,
  city TEXT,
  state TEXT,
  height_cm INTEGER,
  weight_kg NUMERIC(5,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🚀 Após executar

1. Acesse `/app/profile`
2. Preencha seus dados
3. Salve o perfil
4. Deve funcionar sem erros!







