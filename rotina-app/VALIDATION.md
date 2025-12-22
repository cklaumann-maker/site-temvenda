# VALIDATION.md - Pré-Validação e Self-Check

## Comandos de Build e Validação

### 1. Instalar Dependências

```bash
cd rotina-app
pnpm install
```

**Status Esperado**: Instalação completa sem erros críticos

---

### 2. Lint

```bash
pnpm lint
```

**Status Esperado**: 
- Sem erros de lint críticos
- Warnings aceitáveis (formatação, etc.)

**Nota**: Alguns warnings podem aparecer em arquivos de configuração. Isso é normal.

---

### 3. Typecheck

```bash
pnpm typecheck
```

**Status Esperado**: 
- Sem erros de tipo
- Avisos de tipos opcionais são aceitáveis

**Possíveis Problemas**:
- Tipos do Supabase podem precisar ser gerados: `npx supabase gen types typescript`
- Tipos de `@rotina/shared` podem precisar ser construídos primeiro: `pnpm --filter shared build`

---

### 4. Build Web App

```bash
pnpm --filter web build
```

**Status Esperado**: Build completo sem erros

**Possíveis Problemas**:
- Variáveis de ambiente não configuradas (usar `.env.example` como base)
- Tipos faltando (ver typecheck acima)

---

### 5. Validação de SQL Migrations

```bash
cd supabase
supabase db diff --schema public
```

**Status Esperado**: 
- Sem diferenças (se migrations já aplicadas)
- Ou mostrar apenas mudanças esperadas

**Validação Manual**:
```sql
-- Verificar se todas as tabelas existem
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Verificar se RLS está habilitado
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Verificar policies
SELECT tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'public';
```

---

### 6. Validação de RLS Policies

**Teste Manual** (requer Supabase local ou remoto):

```sql
-- Como usuário MEMBER, deve ver apenas próprios dados
SET ROLE authenticated;
SET request.jwt.claim.sub = 'user-member-id';

SELECT * FROM daily_meals; -- Deve retornar apenas do próprio usuário

-- Como COACH, deve ver membros do programa
SET request.jwt.claim.sub = 'user-coach-id';
SELECT * FROM daily_meals; -- Deve retornar membros do programa

-- Como MEMBER tentando acessar /admin, deve falhar
-- (testado no middleware do Next.js)
```

---

### 7. Validação de Export CSV

**Teste Manual**:

1. **Export Plan Template**:
   ```bash
   curl "http://localhost:3000/api/export/template?program_id=<id>&week_index=1" \
     -H "Cookie: <auth-cookie>"
   ```
   **Esperado**: CSV com headers corretos:
   ```
   org_name,program_name,week_index,day_of_week,day_label,meal_type,opt1,opt2,opt3,avoid
   ```

2. **Export User Schedule**:
   ```bash
   curl "http://localhost:3000/api/export/plan?start_date=2024-01-01&end_date=2024-01-14" \
     -H "Cookie: <auth-cookie>"
   ```
   **Esperado**: CSV com headers:
   ```
   date,day_label,meal_type,option_selected,opt1,opt2,opt3,avoid
   ```

3. **Export Adherence**:
   ```bash
   curl "http://localhost:3000/api/export/adherence?start_date=2024-01-01&end_date=2024-01-30" \
     -H "Cookie: <auth-cookie>"
   ```
   **Esperado**: CSV com headers:
   ```
   date,adherence_pct,meals_done,meals_planned,weight_kg,cardio_min,workout_done,functional
   ```

**Validação de Excel**:
- Abrir CSV no Excel
- Verificar se BOM UTF-8 está presente (caracteres especiais corretos)
- Verificar se colunas estão separadas corretamente

---

### 8. Validação de RBAC

**Teste Manual**:

1. **MEMBER não pode acessar /admin**:
   - Login como MEMBER
   - Tentar acessar `/admin/members`
   - **Esperado**: Redirecionado para `/app/today`

2. **COACH pode acessar /admin**:
   - Login como COACH
   - Acessar `/admin/members`
   - **Esperado**: Ver lista de membros do programa

3. **MEMBER não pode ver dados de outros**:
   - Login como MEMBER A
   - Tentar acessar dados do MEMBER B via API
   - **Esperado**: RLS bloqueia (403 ou vazio)

---

### 9. Validação de Regras de Negócio

**Teste Manual**:

1. **Hard Block Inicial**:
   - Criar enrollment com `start_date = hoje`
   - Tentar marcar refeição com doce em dia útil
   - **Esperado**: Bloqueado com mensagem clara

2. **Geração de Daily Meals**:
   - Abrir `/app/today` pela primeira vez
   - **Esperado**: `daily_meals` gerados automaticamente

3. **Cálculo de Aderência**:
   - Marcar algumas refeições como feitas
   - Verificar dashboard
   - **Esperado**: Aderência calculada corretamente

---

### 10. Variáveis de Ambiente

**Verificar**:

```bash
# Web App
cat apps/web/.env.local
# Deve conter:
# NEXT_PUBLIC_SUPABASE_URL
# NEXT_PUBLIC_SUPABASE_ANON_KEY
# SUPABASE_SERVICE_ROLE_KEY

# Mobile App
cat apps/mobile/.env
# Deve conter:
# EXPO_PUBLIC_SUPABASE_URL
# EXPO_PUBLIC_SUPABASE_ANON_KEY
```

---

## Checklist Pré-Deploy

### Código
- [ ] `pnpm install` executa sem erros
- [ ] `pnpm lint` passa (warnings aceitáveis)
- [ ] `pnpm typecheck` passa
- [ ] `pnpm --filter web build` passa

### Database
- [ ] Migrations aplicadas sem erros
- [ ] RLS habilitado em todas as tabelas
- [ ] Policies criadas e testadas
- [ ] Funções database criadas

### Segurança
- [ ] RLS policies testadas manualmente
- [ ] RBAC middleware funcionando
- [ ] Service Role Key não exposta no cliente
- [ ] CORS configurado

### Funcionalidades
- [ ] Login funciona
- [ ] Geração de daily_meals funciona
- [ ] Check-in funciona
- [ ] Export CSV funciona (3 tipos)
- [ ] Regras de doce funcionam

### Variáveis de Ambiente
- [ ] Todas configuradas no Vercel
- [ ] Todas configuradas no EAS (mobile)

---

## Problemas Conhecidos e Mitigações

### 1. Tipos do Supabase Não Gerados

**Problema**: `database.types.ts` é placeholder  
**Mitigação**: 
```bash
npx supabase gen types typescript --project-id <project-id> > apps/web/src/lib/supabase/database.types.ts
```

### 2. Build Falha por Dependências

**Problema**: Workspace packages não construídos  
**Mitigação**:
```bash
pnpm --filter shared build
pnpm --filter ui build
pnpm --filter web build
```

### 3. RLS Policies Não Funcionam

**Problema**: Policies não aplicadas  
**Mitigação**:
```bash
cd supabase
supabase db push
# Verificar logs para erros
```

### 4. Export CSV com Encoding Errado

**Problema**: Excel não abre corretamente  
**Mitigação**: Verificar se BOM UTF-8 está presente (`\uFEFF`)

---

## Testes Recomendados (Pós-Deploy)

1. **Smoke Tests**:
   - Login
   - Navegação básica
   - Check-in
   - Export

2. **Security Tests**:
   - Tentar acessar /admin como MEMBER
   - Tentar acessar dados de outros usuários
   - Verificar logs de RLS

3. **Performance Tests**:
   - Tempo de carregamento de páginas
   - Tempo de geração de daily_meals
   - Tempo de export CSV

---

## Comandos Rápidos de Validação

```bash
# Validação completa
cd rotina-app
pnpm install && pnpm lint && pnpm typecheck && pnpm --filter web build

# Apenas typecheck
pnpm typecheck

# Apenas build
pnpm --filter web build

# Verificar estrutura
tree -L 3 -I node_modules
```

---

## Notas Finais

- **Alguns arquivos podem precisar de ajustes** após primeira execução (ex: tipos do Supabase)
- **Seed data** pode precisar ser ajustado para dados reais
- **Mobile app** requer configuração adicional do Expo
- **Deploy** requer configuração de DNS e variáveis de ambiente

Este documento deve ser atualizado conforme problemas são encontrados e resolvidos.

