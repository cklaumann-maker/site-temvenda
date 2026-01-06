# Correções Aplicadas

## ✅ Problemas Resolvidos

### 1. Erro de Recursão Infinita nas Políticas RLS

**Problema:** `infinite recursion detected in policy for relation "user_profiles"`

**Solução:**
- Criada migration `20240101000013_fix_user_profiles_rls_recursion.sql`
- Políticas RLS agora usam a função `is_root_user()` que é `SECURITY DEFINER`
- Isso evita a recursão porque a função não precisa verificar RLS

**Execute no Supabase:**
```sql
-- Arquivo: rotina-app/supabase/migrations/20240101000013_fix_user_profiles_rls_recursion.sql
```

### 2. Carregar Dados do Perfil na Tela

**Problema:** Perfil não carregava dados existentes

**Solução:**
- Alterado `.single()` para `.maybeSingle()` para não dar erro se perfil não existir
- Adicionado tratamento de erro adequado
- Dados agora são carregados corretamente se já existirem

**Arquivo modificado:** `apps/web/src/app/app/profile/page.tsx`

### 3. Importação de Alimentos na Aba Plano

**Problema:** Importação estava apenas em `/app/admin/food-items/import`

**Solução:**
- Adicionado link para importação na página `/app/plan-manager`
- Agora aparece como uma seção: "Importar Alimentos"
- Link direto para `/app/admin/food-items/import`

**Arquivo modificado:** `apps/web/src/app/app/plan-manager/page.tsx`

### 4. Componente FoodItemSelector Não Aparece

**Status:** O componente está implementado e sendo usado em `TodayCalendar.tsx`

**Verificar:**
- O componente `FoodItemSelector` está importado
- Está sendo usado no lugar de `OtherMealOption`
- Se não aparecer, pode ser que:
  1. O deploy ainda não foi concluído
  2. A tabela `food_items` não foi criada
  3. Precisa executar as migrations

## 📋 Próximos Passos

### 1. Executar Migration de Correção RLS

```sql
-- Execute no Supabase SQL Editor:
-- rotina-app/supabase/migrations/20240101000013_fix_user_profiles_rls_recursion.sql
```

### 2. Executar Migration da Tabela de Alimentos

```sql
-- Execute no Supabase SQL Editor:
-- rotina-app/supabase/migrations/20240101000012_create_food_items_table.sql
```

### 3. Popular Tabela de Alimentos (Opcional)

```sql
-- Execute no Supabase SQL Editor:
-- rotina-app/supabase/popular_food_items.sql
```

### 4. Verificar Deploy

- Acesse o Vercel Dashboard
- Verifique se o último deployment foi concluído
- Se houver erros, veja os logs

### 5. Testar Funcionalidades

- **Perfil:** Tente salvar o perfil (não deve mais dar erro de recursão)
- **Alimentos:** Acesse `/app/plan-manager` e veja o link "Importar Alimentos"
- **Seleção de Alimentos:** Na página "Hoje", deve aparecer "+ Selecionar alimentos da lista"

## 🔍 Verificar se Está Funcionando

### Perfil:
1. Acesse `/app/profile`
2. Preencha os dados
3. Clique em "Salvar Alterações"
4. Não deve dar erro de recursão

### Importação na Aba Plano:
1. Acesse `/app/plan-manager`
2. Role até o final
3. Deve ver a seção "Importar Alimentos"
4. Clique no botão verde

### Seleção de Alimentos:
1. Acesse `/app/today`
2. Para cada refeição, deve aparecer "+ Selecionar alimentos da lista"
3. Se não aparecer, verifique se:
   - A migration foi executada
   - A tabela `food_items` existe
   - O deploy foi concluído

## 🐛 Troubleshooting

### Se o componente FoodItemSelector não aparecer:

1. **Verificar se a migration foi executada:**
   ```sql
   SELECT COUNT(*) FROM public.food_items;
   ```

2. **Verificar se o componente está sendo usado:**
   - Abra DevTools (F12)
   - Veja se há erros no console
   - Procure por erros relacionados a `FoodItemSelector`

3. **Limpar cache do navegador:**
   - Ctrl+F5 (Windows/Linux)
   - Cmd+Shift+R (Mac)

### Se ainda der erro de recursão:

1. Verifique se a migration `20240101000013_fix_user_profiles_rls_recursion.sql` foi executada
2. Verifique se a função `is_root_user()` existe:
   ```sql
   SELECT proname FROM pg_proc WHERE proname = 'is_root_user';
   ```
3. Se não existir, execute a migration novamente

## 📝 Arquivos Modificados

- `rotina-app/supabase/migrations/20240101000013_fix_user_profiles_rls_recursion.sql` (novo)
- `rotina-app/apps/web/src/app/app/profile/page.tsx` (modificado)
- `rotina-app/apps/web/src/app/app/plan-manager/page.tsx` (modificado)

## 🚀 Deploy

O código foi commitado e enviado para o GitHub. O Vercel deve fazer o deploy automaticamente em alguns minutos.

**Não precisa de FTP!** Tudo é automático via Git + Vercel.

