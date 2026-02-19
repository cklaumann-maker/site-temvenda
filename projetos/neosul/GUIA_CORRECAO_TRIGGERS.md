# Guia de Correção - Triggers do NEOSUL

## Problema Reportado

Os triggers `update_planejamento_mensal_updated_at` e `update_planejamento_semanal_updated_at` não foram criados corretamente no Supabase.

## Causa Provável

1. As tabelas foram criadas antes da função trigger
2. Houve algum erro na execução que foi ignorado
3. A função `update_updated_at_column()` não foi criada

## Solução

### Passo 1: Verificar Status Atual

Execute no SQL Editor do Supabase:

```sql
-- Abrir e executar o arquivo:
verificar-triggers.sql
```

Isso mostrará:
- Quais triggers estão instalados
- Se a função existe

### Passo 2: Corrigir os Triggers

Execute no SQL Editor do Supabase:

```sql
-- Abrir e executar o arquivo:
corrigir-triggers.sql
```

Este script:
1. Remove triggers existentes (se houver)
2. Recria a função `update_updated_at_column()`
3. Cria os 3 triggers necessários:
   - `update_usuarios_updated_at`
   - `update_planejamento_mensal_updated_at`
   - `update_planejamento_semanal_updated_at`

### Passo 3: Verificar Correção

Execute novamente:

```sql
-- Abrir e executar o arquivo:
verificar-triggers.sql
```

Agora você deve ver **3 triggers** listados.

## O que os Triggers Fazem

Os triggers atualizam automaticamente o campo `updated_at` toda vez que um registro é modificado (UPDATE).

### Exemplo prático:

```sql
-- Sem trigger: você precisa fazer isso manualmente
UPDATE neosul_planejamento_mensal 
SET objetivo_principal = 'Novo objetivo',
    updated_at = NOW()  -- ❌ você precisa lembrar disso!
WHERE id = '...';

-- Com trigger: é automático
UPDATE neosul_planejamento_mensal 
SET objetivo_principal = 'Novo objetivo'
WHERE id = '...';
-- ✓ updated_at é atualizado automaticamente pelo trigger!
```

## Como Testar se Está Funcionando

### Teste Manual:

1. Execute no SQL Editor:

```sql
-- 1. Criar um planejamento de teste
INSERT INTO neosul_planejamento_mensal (
  mes, ano, gerente_nome, gerente_perfil,
  objetivo_principal, prioridade_1
) VALUES (
  2, 2026, 'Cesar', 'gerente',
  'Teste de trigger', 'Prioridade teste'
)
RETURNING id, created_at, updated_at;
```

2. Anote o `id` e os timestamps. Você verá que `created_at` e `updated_at` são iguais.

3. Aguarde alguns segundos e execute:

```sql
-- 2. Atualizar o registro
UPDATE neosul_planejamento_mensal
SET objetivo_principal = 'Objetivo atualizado'
WHERE mes = 2 AND ano = 2026 AND gerente_nome = 'Cesar'
RETURNING id, created_at, updated_at;
```

4. Agora `updated_at` deve ser MAIOR que `created_at` (alguns segundos depois).

5. Limpar teste:

```sql
-- 3. Remover o registro de teste
DELETE FROM neosul_planejamento_mensal
WHERE mes = 2 AND ano = 2026 AND gerente_nome = 'Cesar';
```

### Resultado Esperado:

- ✅ `created_at` permanece o mesmo
- ✅ `updated_at` é atualizado automaticamente para NOW()
- ✅ Você não precisa setar `updated_at` manualmente

## Arquivos Criados

1. **`corrigir-triggers.sql`** - Script para corrigir/recriar os triggers
2. **`verificar-triggers.sql`** - Script para verificar status dos triggers
3. **`GUIA_CORRECAO_TRIGGERS.md`** - Este guia (documentação)

## Troubleshooting

### Erro: "function update_updated_at_column() does not exist"

**Solução**: Execute `corrigir-triggers.sql` que cria a função primeiro.

### Erro: "permission denied"

**Solução**: Verifique se você está executando com usuário admin no Supabase.

### Triggers aparecem mas não funcionam

**Solução**: 
1. Execute `DROP TRIGGER nome_do_trigger ON nome_da_tabela;`
2. Execute novamente `corrigir-triggers.sql`

## Prevenção Futura

Se você precisar recriar as tabelas do zero:

1. Execute primeiro: `setup-database.sql` (cria tudo de uma vez)
2. OU execute na ordem:
   - Crie as tabelas
   - Crie a função
   - Crie os triggers

A ordem importa! A função deve existir antes dos triggers.

## Status da Correção

Após executar `corrigir-triggers.sql`:

- ✅ Função criada: `update_updated_at_column()`
- ✅ Trigger criado: `update_usuarios_updated_at`
- ✅ Trigger criado: `update_planejamento_mensal_updated_at`
- ✅ Trigger criado: `update_planejamento_semanal_updated_at`
