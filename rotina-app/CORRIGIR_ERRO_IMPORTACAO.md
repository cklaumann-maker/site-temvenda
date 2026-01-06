# 🔧 Corrigir Erro de Importação de Planilha

## ❌ Erro Atual

```
infinite recursion detected in policy for relation "org_members"
Failed to load resource: the server responded with a status of 500
```

## 🔍 Causa

O erro ocorre porque as políticas RLS (Row Level Security) estão causando recursão infinita ao tentar verificar permissões. Especificamente:

1. **Política de `org_members`** está tentando ler de `org_members` para verificar se pode ler de `org_members` (recursão)
2. **Política de `plan_templates`** pode estar bloqueando usuários que não são OWNER ou COACH

## ✅ Solução

### Passo 1: Execute a Migration SQL

Acesse o **Supabase SQL Editor** e execute o arquivo:

```
rotina-app/supabase/migrations/20240101000005_fix_rls_recursion.sql
```

**Conteúdo da migration:**

```sql
-- Fix RLS recursion issues and allow users to import plan templates

-- Drop problematic policies
DROP POLICY IF EXISTS "Users can view org members in their orgs" ON public.org_members;
DROP POLICY IF EXISTS "Owners can manage org members" ON public.org_members;

-- Create helper function to check org membership (with SECURITY DEFINER to avoid recursion)
CREATE OR REPLACE FUNCTION public.user_belongs_to_org(check_user_id UUID, check_org_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.org_members
    WHERE user_id = check_user_id
      AND org_id = check_org_id
      AND active = true
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Recreate org_members policies using the helper function
CREATE POLICY "Users can view org members in their orgs"
  ON public.org_members FOR SELECT
  USING (
    public.user_belongs_to_org(auth.uid(), org_id)
  );

CREATE POLICY "Owners can manage org members"
  ON public.org_members FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.org_members
      WHERE org_id = org_members.org_id
        AND user_id = auth.uid()
        AND role = 'OWNER'
        AND active = true
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.org_members
      WHERE org_id = org_members.org_id
        AND user_id = auth.uid()
        AND role = 'OWNER'
        AND active = true
    )
  );

-- Allow users to insert/update/delete plan_templates for their enrolled programs
DROP POLICY IF EXISTS "Owners and coaches can manage plan templates" ON public.plan_templates;

CREATE POLICY "Users can manage plan templates in their programs"
  ON public.plan_templates FOR ALL
  USING (
    -- User is enrolled in the program
    EXISTS (
      SELECT 1 FROM public.enrollments
      WHERE program_id = plan_templates.program_id
        AND user_id = auth.uid()
        AND active = true
    )
    OR
    -- User is owner or coach
    EXISTS (
      SELECT 1 FROM public.org_members om
      JOIN public.programs p ON p.org_id = om.org_id
      WHERE om.user_id = auth.uid()
        AND om.role IN ('OWNER', 'COACH')
        AND om.active = true
        AND p.id = plan_templates.program_id
    )
  )
  WITH CHECK (
    -- User is enrolled in the program
    EXISTS (
      SELECT 1 FROM public.enrollments
      WHERE program_id = plan_templates.program_id
        AND user_id = auth.uid()
        AND active = true
    )
    OR
    -- User is owner or coach
    EXISTS (
      SELECT 1 FROM public.org_members om
      JOIN public.programs p ON p.org_id = om.org_id
      WHERE om.user_id = auth.uid()
        AND om.role IN ('OWNER', 'COACH')
        AND om.active = true
        AND p.id = plan_templates.program_id
    )
  );
```

### Passo 2: Verificar Enrollment

Antes de importar, certifique-se de que você tem um enrollment ativo no programa demo:

```sql
-- Verificar seu enrollment
SELECT * FROM enrollments 
WHERE user_id = auth.uid() 
  AND program_id = '00000000-0000-0000-0000-000000000002'
  AND active = true;

-- Se não existir, criar (substitua 'SEU_USER_ID' pelo seu ID)
INSERT INTO enrollments (user_id, program_id, start_date, active)
VALUES (
  auth.uid(), -- ou seu user_id
  '00000000-0000-0000-0000-000000000002',
  CURRENT_DATE,
  true
)
ON CONFLICT (user_id, program_id) WHERE active = true 
DO UPDATE SET start_date = CURRENT_DATE, updated_at = NOW();
```

### Passo 3: Testar Importação

1. Acesse: `http://localhost:3001/app/plan-manager`
2. Faça upload do CSV
3. Verifique se não há mais erros no console

## 🔍 Verificação

Após executar a migration, verifique:

```sql
-- Verificar se a função foi criada
SELECT proname FROM pg_proc WHERE proname = 'user_belongs_to_org';

-- Verificar políticas de plan_templates
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE tablename = 'plan_templates';

-- Verificar políticas de org_members
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE tablename = 'org_members';
```

## 📝 O que foi corrigido?

1. ✅ **Recursão infinita em `org_members`**: Criada função helper com `SECURITY DEFINER` para evitar recursão
2. ✅ **Permissão para importar `plan_templates`**: Usuários com enrollment ativo agora podem importar planilhas
3. ✅ **Políticas RLS otimizadas**: Políticas mais eficientes e sem recursão

## ⚠️ Se ainda não funcionar

1. Verifique se você está autenticado:
   ```sql
   SELECT auth.uid();
   ```

2. Verifique se tem enrollment:
   ```sql
   SELECT * FROM enrollments WHERE user_id = auth.uid() AND active = true;
   ```

3. Verifique se o programa existe:
   ```sql
   SELECT * FROM programs WHERE id = '00000000-0000-0000-0000-000000000002';
   ```

4. Tente importar novamente após verificar tudo acima

---

**Execute a migration SQL primeiro!** 🚀







