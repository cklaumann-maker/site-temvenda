# 🔍 Verificação de TypeScript Antes do Deploy

## ✅ Checklist de Verificação

### 1. Verificar Erros de TypeScript Localmente

Antes de fazer push, sempre execute:

```bash
cd rotina-app/apps/web
pnpm exec tsc --noEmit
```

### 2. Padrões que Causam Erros no Vercel

#### ❌ Problema: Inferência de Tipo do Supabase

O Supabase TypeScript pode não inferir corretamente tipos de:
- `.insert()` - inserção de dados
- `.select()` - seleção de dados
- `.map()` - transformação de arrays retornados

#### ✅ Solução: Type Assertions

Sempre adicione `as any` quando necessário:

```typescript
// ❌ ERRADO
const { data } = await supabase.from('table').select('*');
const items = (data || []).map(item => item.field);

// ✅ CORRETO
const { data } = await supabase.from('table').select('*');
const items = ((data as any[]) || []).map((item: any) => item.field);
```

```typescript
// ❌ ERRADO
await supabase.from('table').insert({ field: value });

// ✅ CORRETO
await supabase.from('table').insert({ field: value } as any);
```

### 3. Arquivos que Precisam de Atenção

- ✅ `src/app/api/food-items/route.ts` - Corrigido
- ✅ `src/app/api/admin/users/route.ts` - Corrigido
- ✅ `src/app/app/admin/food-items/import/page.tsx` - Corrigido
- ⚠️ `src/app/app/plan-manager/page.tsx` - Já tem type assertions

### 4. Comando de Verificação Completa

**Opção 1: Usar o script automatizado (Recomendado)**

```bash
cd rotina-app
./scripts/verificar-typescript.sh
```

**Opção 2: Verificação manual**

```bash
# 1. Verificar TypeScript
cd rotina-app/apps/web
pnpm exec tsc --noEmit

# 2. Verificar build local
cd rotina-app
pnpm run build

# 3. Se tudo passar, fazer commit e push
git add -A
git commit -m "fix: descrição do fix"
git push origin main
```

### 5. Padrões a Procurar

Use grep para encontrar padrões problemáticos:

```bash
# Procurar por .insert() sem type assertion
grep -r "\.insert({" rotina-app/apps/web/src --include="*.ts" --include="*.tsx"

# Procurar por .map() sem type assertion em arrays do Supabase
grep -r "\.map((.*) =>" rotina-app/apps/web/src --include="*.ts" --include="*.tsx"
```

## 📝 Notas

- O Vercel usa TypeScript strict mode durante o build
- Erros que não aparecem localmente podem aparecer no Vercel
- Sempre teste o build localmente antes de fazer push
- Use `as any` quando necessário, mas documente o motivo

