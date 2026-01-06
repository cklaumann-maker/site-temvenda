# 🔍 Diagnóstico: Rota `/api/food-items` não aparece

## ✅ Verificações Realizadas

### 1. Arquivo Existe e Está Correto
- ✅ `rotina-app/apps/web/src/app/api/food-items/route.ts` existe
- ✅ Exporta `GET` e `POST` corretamente
- ✅ Usa `NextResponse` corretamente
- ✅ Estrutura de diretórios está correta

### 2. Componente Usa a Rota
- ✅ `FoodItemSelector.tsx` faz fetch para `/api/food-items`
- ✅ Tratamento de erro está implementado

### 3. Build Concluído
- ✅ Build foi bem-sucedido
- ⚠️ Rota não aparece na lista de rotas geradas (mas isso é normal para rotas dinâmicas)

## 🎯 Por que a rota não aparece na lista?

No Next.js App Router, rotas de API que são **dinâmicas** (usam cookies, autenticação, etc.) podem não aparecer na lista de rotas estáticas durante o build, mas **funcionam normalmente em runtime**.

A rota `/api/food-items`:
- Usa `createClient()` do Supabase (que usa cookies)
- É uma rota dinâmica (λ no build output)
- Deve funcionar mesmo não aparecendo na lista

## 🧪 Como Testar

### 1. Testar a Rota Diretamente

Após o deploy, teste diretamente no navegador:

```
https://rotina-five.vercel.app/api/food-items
```

**Resultado esperado:**
- ✅ Se retornar `{"items": []}` → Rota funciona! (tabela pode estar vazia)
- ❌ Se retornar 404 → Problema real

### 2. Verificar Console do Navegador

1. Abra a aplicação: `https://rotina-five.vercel.app/app/today`
2. Abra DevTools (F12)
3. Vá na aba Network
4. Clique em "+ Selecionar alimentos da lista"
5. Procure por requisição para `/api/food-items`
6. Verifique o status da resposta

### 3. Verificar Logs do Vercel

No Vercel Dashboard:
1. Vá em "Deployments"
2. Clique no último deploy
3. Vá em "Functions" ou "Logs"
4. Procure por erros relacionados a `/api/food-items`

## 🐛 Possíveis Problemas e Soluções

### Problema 1: Rota retorna 404

**Causa:** Next.js não detectou a rota durante o build

**Solução:**
1. Verificar se o arquivo está em `src/app/api/food-items/route.ts`
2. Verificar se não há erros de sintaxe
3. Forçar novo deploy

### Problema 2: Rota retorna 500

**Causa:** Erro ao acessar o banco de dados

**Possíveis causas:**
- Tabela `food_items` não existe
- Problema de RLS (Row Level Security)
- Erro na conexão com Supabase

**Solução:**
1. Executar migration: `20240101000012_create_food_items_table.sql`
2. Verificar políticas RLS
3. Verificar variáveis de ambiente do Supabase no Vercel

### Problema 3: Componente não aparece

**Causa:** Erro JavaScript ou componente não está sendo importado

**Solução:**
1. Verificar console do navegador para erros
2. Verificar se `FoodItemSelector` está sendo importado em `TodayCalendar.tsx`
3. Limpar cache do navegador (Ctrl+F5)

## ✅ Checklist de Verificação

- [ ] Deploy foi concluído com sucesso
- [ ] Rota `/api/food-items` retorna JSON (não 404)
- [ ] Tabela `food_items` existe no Supabase
- [ ] Políticas RLS estão configuradas corretamente
- [ ] Variáveis de ambiente do Supabase estão configuradas no Vercel
- [ ] Componente `FoodItemSelector` aparece na página
- [ ] Console do navegador não mostra erros

## 📝 Próximos Passos

1. **Teste a rota diretamente:**
   ```
   https://rotina-five.vercel.app/api/food-items
   ```

2. **Se retornar 404:**
   - Verificar estrutura de diretórios
   - Forçar novo deploy
   - Verificar logs do Vercel

3. **Se retornar 500:**
   - Executar migrations no Supabase
   - Verificar políticas RLS
   - Verificar variáveis de ambiente

4. **Se retornar JSON vazio:**
   - ✅ Rota funciona!
   - Apenas precisa popular a tabela com dados

## 🔧 Comandos Úteis

### Verificar se a rota existe no build:
```bash
# No diretório do projeto
cd rotina-app/apps/web
ls -la .next/server/app/api/food-items/
```

### Testar localmente:
```bash
cd rotina-app
pnpm install
pnpm run build
pnpm run start
# Acesse: http://localhost:3000/api/food-items
```

