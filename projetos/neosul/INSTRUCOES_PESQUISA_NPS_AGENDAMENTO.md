# 🔧 Modificação: Vincular Pesquisa NPS ao Agendamento

## 📋 Objetivo

Modificar a estrutura para que cada pesquisa NPS seja vinculada a um agendamento específico (cliente/trilha/módulo), em vez de ser uma pesquisa global.

## 🔍 Mudanças Necessárias

### 1. Banco de Dados
- Adicionar coluna `agendamento_id` na tabela `neosul_pesquisa_nps`
- Criar índice para melhorar performance
- Manter compatibilidade com pesquisas antigas (campo `ativo` continua funcionando)

### 2. Código JavaScript
- Modificar `salvarPesquisaNPS()` para salvar pesquisa vinculada ao agendamento selecionado
- Modificar `carregarPesquisaNPS()` para carregar pesquisa do agendamento
- Modificar página `pesquisa-nps.html` para buscar pesquisa pelo agendamento (via QR Code)

## 📋 Passo a Passo

### 1. Executar Migração SQL
1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Abra o **SQL Editor**
3. Execute o arquivo: `MODIFICAR_PESQUISA_NPS_VINCULAR_AGENDAMENTO.sql`

### 2. Verificar Migração
Após executar, verifique se a coluna foi adicionada:
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'neosul_pesquisa_nps' 
AND column_name = 'agendamento_id';
```

## 🔄 Novo Fluxo

### Antes (Pesquisa Global):
1. Criar pesquisa NPS (uma para todos)
2. Agendamento usa QR Code para acessar pesquisa global

### Depois (Pesquisa por Agendamento):
1. Ao criar/editar agendamento, criar pesquisa NPS específica
2. Pesquisa vinculada ao agendamento via `agendamento_id`
3. QR Code continua funcionando, mas busca pesquisa do agendamento específico

## ⚠️ Compatibilidade

- Pesquisas antigas (sem `agendamento_id`) continuarão funcionando
- Campo `ativo` continua sendo usado para pesquisas globais (compatibilidade)
- Novos agendamentos terão pesquisas específicas vinculadas

## 📝 Observações

- Cada agendamento pode ter sua própria pesquisa personalizada
- Permite perguntas diferentes para diferentes módulos/trilhas
- Histórico de pesquisas é mantido por agendamento
