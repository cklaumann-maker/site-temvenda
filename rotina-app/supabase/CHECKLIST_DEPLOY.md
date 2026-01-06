# ✅ Checklist: Verificar se Tudo Está Funcionando

## 🔍 Problemas Relatados

1. ❌ Componente FoodItemSelector não aparece (ainda mostra "+ Outros (inserir calorias)")
2. ❌ Não aparece opção de cadastro
3. ❌ Importação precisa estar na aba Plano
4. ✅ Deploy foi concluído com sucesso

## 📋 Checklist de Verificação

### 1. Verificar se a Tabela `food_items` Existe

Execute no Supabase SQL Editor:

```sql
SELECT COUNT(*) FROM public.food_items;
```

**Se der erro "relation does not exist":**
- Execute: `rotina-app/supabase/migrations/20240101000012_create_food_items_table.sql`

### 2. Verificar se o Componente Está Sendo Usado

O componente `FoodItemSelector` está sendo usado em:
- `apps/web/src/app/app/today/TodayCalendar.tsx` (linha 720)

**Verificar no código:**
- Deve ter: `import { FoodItemSelector } from '@/components/FoodItemSelector';`
- Deve ter: `<FoodItemSelector ... />` ao invés de `<OtherMealOption ... />`

### 3. Limpar Cache do Navegador

**IMPORTANTE:** O navegador pode estar usando versão antiga em cache!

1. **Hard Refresh:**
   - Windows/Linux: `Ctrl + F5` ou `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

2. **Ou abra em modo anônimo:**
   - `Ctrl + Shift + N` (Chrome) ou `Ctrl + Shift + P` (Firefox)

3. **Ou limpe o cache:**
   - DevTools (F12) > Application > Clear Storage > Clear site data

### 4. Verificar Console do Navegador

Abra DevTools (F12) e verifique:

1. **Erros JavaScript:**
   - Procure por erros vermelhos
   - Especialmente relacionados a `FoodItemSelector` ou `food_items`

2. **Erros de Rede:**
   - Aba Network
   - Procure por requisições para `/api/food-items`
   - Se der 404, a API não está funcionando
   - Se der 500, pode ser problema de RLS ou tabela não existe

### 5. Verificar se a API Está Funcionando

Teste diretamente no navegador:

```
https://seu-dominio.vercel.app/api/food-items
```

**Deve retornar:**
```json
{
  "items": [...]
}
```

**Se der erro 404:**
- A rota não foi criada (verificar se o arquivo existe)

**Se der erro 500:**
- Pode ser problema de RLS ou tabela não existe

### 6. Verificar Importação na Aba Plano

Acesse: `/app/plan-manager`

**Deve aparecer:**
- Seção "Importar Alimentos" (botão verde)
- Link para `/app/admin/food-items/import`

**Se não aparecer:**
- Verificar se o código foi commitado
- Verificar se o deploy foi concluído
- Limpar cache do navegador

## 🐛 Troubleshooting Específico

### Problema: Ainda aparece "+ Outros (inserir calorias)"

**Possíveis causas:**
1. Cache do navegador (mais provável)
2. Componente não foi incluído no build
3. Erro JavaScript silencioso

**Solução:**
1. Limpar cache (Ctrl+F5)
2. Verificar console do navegador
3. Verificar se o componente existe: `apps/web/src/components/FoodItemSelector.tsx`
4. Verificar se está sendo importado corretamente

### Problema: Não aparece opção de cadastro

**Verificar:**
1. A tabela `food_items` existe?
2. A API `/api/food-items` está funcionando?
3. O componente está carregando os alimentos?

**Solução:**
1. Execute a migration da tabela
2. Teste a API diretamente
3. Verifique o console do navegador

### Problema: Importação não aparece na aba Plano

**Verificar:**
1. O código foi commitado?
2. O deploy foi concluído?
3. Cache do navegador limpo?

**Solução:**
1. Verificar commit no GitHub
2. Verificar deploy no Vercel
3. Limpar cache e testar novamente

## 🔧 Ações Imediatas

### 1. Execute as Migrations (se ainda não executou)

```sql
-- 1. Criar tabela food_items
-- Arquivo: rotina-app/supabase/migrations/20240101000012_create_food_items_table.sql

-- 2. Corrigir recursão RLS
-- Arquivo: rotina-app/supabase/migrations/20240101000013_fix_user_profiles_rls_recursion.sql
```

### 2. Limpar Cache e Testar

1. Abra o navegador em modo anônimo
2. Acesse a aplicação
3. Vá para `/app/today`
4. Verifique se aparece "+ Selecionar alimentos da lista"

### 3. Verificar Console

1. Abra DevTools (F12)
2. Vá na aba Console
3. Procure por erros
4. Filtre por `[ROTINA APP]` para ver logs do app

### 4. Testar API Diretamente

No navegador, acesse:
```
https://seu-dominio.vercel.app/api/food-items
```

Deve retornar JSON com `items: []` (mesmo que vazio)

## 📝 Notas

- O deploy foi concluído com sucesso
- O código está correto no repositório
- O problema mais provável é **cache do navegador**
- Se ainda não funcionar após limpar cache, verificar se as migrations foram executadas

