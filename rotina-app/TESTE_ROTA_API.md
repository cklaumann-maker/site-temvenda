# 🧪 Teste da Rota `/api/food-items`

## ✅ Passo a Passo para Verificar

### 1. Teste Direto da Rota (Mais Importante!)

Após o deploy, teste diretamente no navegador:

```
https://rotina-five.vercel.app/api/food-items
```

**Resultados possíveis:**

#### ✅ Sucesso - Retorna JSON:
```json
{"items": []}
```
**Significa:** Rota funciona! Apenas precisa popular a tabela.

#### ❌ Erro 404:
**Significa:** Rota não foi detectada pelo Next.js
**Solução:** Verificar estrutura de diretórios e forçar novo deploy

#### ❌ Erro 500:
**Significa:** Erro ao acessar banco de dados
**Solução:** 
- Executar migration `20240101000012_create_food_items_table.sql`
- Verificar variáveis de ambiente do Supabase no Vercel

### 2. Verificar no Console do Navegador

1. Acesse: `https://rotina-five.vercel.app/app/today`
2. Abra DevTools (F12)
3. Vá na aba **Console**
4. Procure por erros relacionados a:
   - `FoodItemSelector`
   - `food-items`
   - `fetch`

### 3. Verificar Requisições de Rede

1. Acesse: `https://rotina-five.vercel.app/app/today`
2. Abra DevTools (F12)
3. Vá na aba **Network**
4. Clique em **"+ Selecionar alimentos da lista"**
5. Procure por requisição para `/api/food-items`
6. Verifique:
   - Status: 200 (sucesso) ou 404/500 (erro)
   - Response: Deve ser JSON com `{"items": [...]}`

### 4. Verificar se Componente Aparece

1. Acesse: `https://rotina-five.vercel.app/app/today`
2. Role até uma refeição
3. Procure por botão **"+ Selecionar alimentos da lista"**
4. Se não aparecer:
   - Verifique console para erros JavaScript
   - Limpe cache do navegador (Ctrl+F5)
   - Teste em modo anônimo

### 5. Verificar Logs do Vercel

1. Acesse Vercel Dashboard
2. Vá em **Deployments**
3. Clique no último deploy
4. Vá em **Functions** ou **Logs**
5. Procure por:
   - Erros relacionados a `/api/food-items`
   - Erros de conexão com Supabase
   - Erros de RLS (Row Level Security)

## 🔧 Soluções por Problema

### Problema: Rota retorna 404

**Verificar:**
1. Arquivo existe em `src/app/api/food-items/route.ts`?
2. Exporta `GET` e `POST`?
3. Estrutura de diretórios está correta?

**Solução:**
```bash
# Verificar estrutura
ls -la rotina-app/apps/web/src/app/api/food-items/

# Deve mostrar:
# route.ts
```

### Problema: Rota retorna 500

**Verificar:**
1. Tabela `food_items` existe no Supabase?
2. Políticas RLS estão configuradas?
3. Variáveis de ambiente estão corretas no Vercel?

**Solução:**
```sql
-- Executar no Supabase SQL Editor
SELECT COUNT(*) FROM public.food_items;
-- Se der erro, executar migration:
-- rotina-app/supabase/migrations/20240101000012_create_food_items_table.sql
```

### Problema: Componente não aparece

**Verificar:**
1. Console do navegador mostra erros?
2. Componente está sendo importado?
3. Cache do navegador limpo?

**Solução:**
1. Limpar cache (Ctrl+F5)
2. Verificar console para erros
3. Verificar se `FoodItemSelector` está em `TodayCalendar.tsx`

## 📋 Checklist Completo

- [ ] Deploy concluído com sucesso
- [ ] Rota `/api/food-items` retorna JSON (não 404)
- [ ] Tabela `food_items` existe no Supabase
- [ ] Políticas RLS configuradas corretamente
- [ ] Variáveis de ambiente do Supabase no Vercel
- [ ] Componente `FoodItemSelector` aparece na página
- [ ] Console do navegador sem erros
- [ ] Requisição para `/api/food-items` funciona

## 🎯 Próxima Ação

**TESTE AGORA:**
1. Acesse: `https://rotina-five.vercel.app/api/food-items`
2. Me informe o resultado:
   - ✅ Retorna JSON → Rota funciona!
   - ❌ Retorna 404 → Problema de estrutura
   - ❌ Retorna 500 → Problema de banco/configuração

