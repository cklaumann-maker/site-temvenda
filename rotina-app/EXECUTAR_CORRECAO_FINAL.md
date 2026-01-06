# 🔧 Correção Final RLS - Sem Recursão

## ⚠️ IMPORTANTE: Execute esta versão FINAL

Esta versão remove completamente a recursão ao simplificar todas as políticas e evitar consultas a `org_members` dentro de políticas que protegem outras tabelas.

## 📋 Passo a Passo

### 1. Execute o SQL no Supabase SQL Editor

Copie e execute o conteúdo de:
```
rotina-app/supabase/migrations/20240101000008_fix_rls_final.sql
```

**OU copie este SQL diretamente:**

```sql
-- FINAL FIX: Remove all recursion by simplifying policies
-- This version completely avoids org_members checks in enrollments and plan_templates

-- ============================================
-- STEP 1: Fix enrollments policies
-- ============================================

-- Drop existing enrollments policies
DROP POLICY IF EXISTS "Users can view own enrollments" ON public.enrollments;
DROP POLICY IF EXISTS "Coaches can view enrollments in their programs" ON public.enrollments;
DROP POLICY IF EXISTS "Users can create own enrollments" ON public.enrollments;
DROP POLICY IF EXISTS "Coaches can create enrollments" ON public.enrollments;

-- Simple policy: Users can manage their own enrollments (no org_members check)
CREATE POLICY "Users can manage own enrollments"
  ON public.enrollments FOR ALL
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- ============================================
-- STEP 2: Fix plan_templates policies  
-- ============================================

-- Drop ALL existing plan_templates policies
DROP POLICY IF EXISTS "Users can view plan templates in their programs" ON public.plan_templates;
DROP POLICY IF EXISTS "Users can manage plan templates in their programs" ON public.plan_templates;
DROP POLICY IF EXISTS "Owners and coaches can manage plan templates" ON public.plan_templates;
DROP POLICY IF EXISTS "Users can view plan templates" ON public.plan_templates;
DROP POLICY IF EXISTS "Users can manage plan templates" ON public.plan_templates;

-- Simple policy: Users can manage templates for programs they're enrolled in
-- This checks ONLY enrollments, NOT org_members (avoids recursion)
CREATE POLICY "Users can view plan templates"
  ON public.plan_templates FOR SELECT
  USING (
    program_id IN (
      SELECT program_id 
      FROM public.enrollments
      WHERE user_id = auth.uid() 
        AND active = true
    )
  );

CREATE POLICY "Users can manage plan templates"
  ON public.plan_templates FOR ALL
  USING (
    program_id IN (
      SELECT program_id 
      FROM public.enrollments
      WHERE user_id = auth.uid() 
        AND active = true
    )
  )
  WITH CHECK (
    program_id IN (
      SELECT program_id 
      FROM public.enrollments
      WHERE user_id = auth.uid() 
        AND active = true
    )
  );

-- ============================================
-- STEP 3: Fix org_members policies (simplified)
-- ============================================

-- Drop ALL existing org_members policies
DROP POLICY IF EXISTS "Users can view org members in their orgs" ON public.org_members;
DROP POLICY IF EXISTS "Owners can manage org members" ON public.org_members;
DROP POLICY IF EXISTS "Users can view own org membership" ON public.org_members;
DROP POLICY IF EXISTS "Users can view org members via programs" ON public.org_members;

-- Drop helper function
DROP FUNCTION IF EXISTS public.user_belongs_to_org(UUID, UUID);

-- Very simple policies that don't cause recursion
CREATE POLICY "Users can view own org membership"
  ON public.org_members FOR SELECT
  USING (user_id = auth.uid());

-- Policy for viewing org members - but only check via direct org_id match
-- We'll use a simpler approach: users can see org_members if they have an enrollment
-- in a program from that org (but check enrollments, not org_members recursively)
CREATE POLICY "Users can view org members via enrollments"
  ON public.org_members FOR SELECT
  USING (
    org_id IN (
      SELECT DISTINCT p.org_id
      FROM public.programs p
      JOIN public.enrollments e ON e.program_id = p.id
      WHERE e.user_id = auth.uid() 
        AND e.active = true
    )
  );

-- Owners can manage (simple check - no recursion)
CREATE POLICY "Owners can manage org members"
  ON public.org_members FOR ALL
  USING (
    user_id = auth.uid()
    AND role = 'OWNER'
  )
  WITH CHECK (
    user_id = auth.uid()
    AND role = 'OWNER'
  );
```

### 2. Criar Enrollment (se não existir)

Após executar o SQL acima, crie o enrollment:

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

### 3. Verificar

```sql
-- Verificar enrollment
SELECT * FROM enrollments 
WHERE user_id = auth.uid() 
  AND program_id = '00000000-0000-0000-0000-000000000002'
  AND active = true;

-- Verificar políticas
SELECT tablename, policyname, cmd 
FROM pg_policies 
WHERE tablename IN ('enrollments', 'plan_templates', 'org_members')
ORDER BY tablename, policyname;
```

### 4. Testar Importação

1. Recarregue a página do app (Ctrl+Shift+R ou Cmd+Shift+R)
2. Vá para `/app/plan-manager`
3. Tente importar o CSV novamente

## 🔍 O que esta versão faz diferente?

1. **`enrollments`**: Política muito simples - usuários só podem gerenciar seus próprios enrollments
2. **`plan_templates`**: Verifica apenas `enrollments`, nunca consulta `org_members`
3. **`org_members`**: Políticas simplificadas que não causam recursão

## ⚠️ Se ainda não funcionar

Como último recurso, podemos temporariamente desabilitar RLS apenas para `plan_templates` durante a importação:

```sql
-- TEMPORÁRIO: Desabilitar RLS para plan_templates
ALTER TABLE public.plan_templates DISABLE ROW LEVEL SECURITY;

-- Testar importação

-- Depois reabilitar:
ALTER TABLE public.plan_templates ENABLE ROW LEVEL SECURITY;
-- E executar as políticas acima novamente
```

**Mas tente a solução acima primeiro!** Ela deve funcionar porque não há mais recursão.

---

**Execute o SQL da versão FINAL primeiro!** 🚀







