# 🔧 Executar Correção RLS - Versão Simples

## ⚠️ IMPORTANTE: Execute esta versão mais simples

A versão anterior ainda causava recursão. Esta versão usa uma abordagem mais direta sem funções helper.

## 📋 Passo a Passo

### 1. Execute o SQL no Supabase SQL Editor

Copie e execute o conteúdo de:
```
rotina-app/supabase/migrations/20240101000007_fix_rls_simple.sql
```

**OU copie este SQL diretamente:**

```sql
-- SIMPLE FIX: Remove recursion by using direct checks instead of helper functions
-- This is the safest approach - no helper functions that could cause recursion

-- Drop ALL existing policies on org_members to start fresh
DROP POLICY IF EXISTS "Users can view org members in their orgs" ON public.org_members;
DROP POLICY IF EXISTS "Owners can manage org members" ON public.org_members;
DROP POLICY IF EXISTS "Users can view own org membership" ON public.org_members;
DROP POLICY IF EXISTS "Users can view org members via programs" ON public.org_members;

-- Drop helper function if it exists (we won't use it)
DROP FUNCTION IF EXISTS public.user_belongs_to_org(UUID, UUID);

-- Simple policy: Users can see their own org_members records
CREATE POLICY "Users can view own org membership"
  ON public.org_members FOR SELECT
  USING (user_id = auth.uid());

-- Policy: Users can see org_members of orgs they belong to
-- But we check enrollments/programs instead to avoid recursion
CREATE POLICY "Users can view org members via programs"
  ON public.org_members FOR SELECT
  USING (
    org_id IN (
      SELECT DISTINCT p.org_id 
      FROM public.programs p
      JOIN public.enrollments e ON e.program_id = p.id
      WHERE e.user_id = auth.uid() AND e.active = true
    )
  );

-- Policy: Owners can manage (but check via programs to avoid recursion)
CREATE POLICY "Owners can manage org members"
  ON public.org_members FOR ALL
  USING (
    user_id = auth.uid()
    AND role = 'OWNER'
    AND active = true
  )
  WITH CHECK (
    user_id = auth.uid()
    AND role = 'OWNER'
    AND active = true
  );

-- Fix plan_templates policies
DROP POLICY IF EXISTS "Users can view plan templates in their programs" ON public.plan_templates;
DROP POLICY IF EXISTS "Users can manage plan templates in their programs" ON public.plan_templates;
DROP POLICY IF EXISTS "Owners and coaches can manage plan templates" ON public.plan_templates;
DROP POLICY IF EXISTS "Users can view plan templates" ON public.plan_templates;
DROP POLICY IF EXISTS "Users can manage plan templates" ON public.plan_templates;

-- Simple policy: Users enrolled in program can manage templates
CREATE POLICY "Users can view plan templates"
  ON public.plan_templates FOR SELECT
  USING (
    program_id IN (
      SELECT program_id FROM public.enrollments
      WHERE user_id = auth.uid() AND active = true
    )
  );

CREATE POLICY "Users can manage plan templates"
  ON public.plan_templates FOR ALL
  USING (
    program_id IN (
      SELECT program_id FROM public.enrollments
      WHERE user_id = auth.uid() AND active = true
    )
  )
  WITH CHECK (
    program_id IN (
      SELECT program_id FROM public.enrollments
      WHERE user_id = auth.uid() AND active = true
    )
  );
```

### 2. Verificar se funcionou

Execute este SQL para verificar:

```sql
-- Verificar políticas de org_members
SELECT policyname, cmd 
FROM pg_policies 
WHERE tablename = 'org_members';

-- Verificar políticas de plan_templates
SELECT policyname, cmd 
FROM pg_policies 
WHERE tablename = 'plan_templates';

-- Verificar se você tem enrollment
SELECT * FROM enrollments 
WHERE user_id = auth.uid() 
  AND program_id = '00000000-0000-0000-0000-000000000002'
  AND active = true;
```

### 3. Se não tiver enrollment, criar:

```sql
-- Criar enrollment para o programa demo
INSERT INTO enrollments (user_id, program_id, start_date, active)
VALUES (
  auth.uid(),
  '00000000-0000-0000-0000-000000000002',
  CURRENT_DATE,
  true
)
ON CONFLICT (user_id, program_id) WHERE active = true 
DO UPDATE SET start_date = CURRENT_DATE, updated_at = NOW();
```

### 4. Testar importação

1. Recarregue a página do app
2. Vá para `/app/plan-manager`
3. Tente importar o CSV novamente

## 🔍 Diferenças desta versão

1. **Sem funções helper**: Não usa funções que podem causar recursão
2. **Checks diretos**: Usa subconsultas diretas em vez de funções
3. **Evita recursão**: As políticas não consultam a mesma tabela que estão protegendo

## ⚠️ Se ainda não funcionar

Execute este SQL para desabilitar temporariamente RLS e testar:

```sql
-- TEMPORÁRIO: Desabilitar RLS para testar
ALTER TABLE public.org_members DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.plan_templates DISABLE ROW LEVEL SECURITY;

-- Testar importação

-- Depois, reabilitar:
ALTER TABLE public.org_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.plan_templates ENABLE ROW LEVEL SECURITY;
```

**Mas isso é apenas para teste!** Depois reabilite o RLS e use as políticas corretas.

---

**Execute o SQL da versão simples primeiro!** 🚀







