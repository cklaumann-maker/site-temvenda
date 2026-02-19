# 🔧 Correção: Tornar cliente_id nullable na tabela neosul_treinamentos_agendamentos

## ❌ Problema

Ao tentar salvar um agendamento de treinamento, ocorre o erro:
```
null value in column "cliente_id" of relation "neosul_treinamentos_agendamentos" violates not-null constraint
```

## 🔍 Causa

A tabela `neosul_treinamentos_agendamentos` foi criada originalmente para trabalhar apenas com clientes, mas depois foi adaptada para trabalhar também com empresas. No entanto, o campo `cliente_id` ainda tem a constraint NOT NULL, impedindo que seja NULL quando estamos criando um agendamento para uma empresa.

## ✅ Solução

Execute a migração SQL para tornar `cliente_id` nullable e adicionar uma constraint que garante que pelo menos um dos dois campos (`cliente_id` ou `empresa_id`) está preenchido.

## 📋 Passo a Passo

### 1. Acessar o Supabase
1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Faça login na sua conta

### 2. Abrir o SQL Editor
1. No menu lateral, clique em **"SQL Editor"**
2. Clique em **"New query"**

### 3. Executar o Script
1. Abra o arquivo: `CORRIGIR_CLIENTE_ID_AGENDAMENTOS.sql`
2. **Copie TODO o conteúdo** do arquivo
3. Cole no SQL Editor do Supabase
4. Clique em **"Run"** ou pressione `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac)

### 4. Verificar Sucesso
Após executar, você deve ver:
- ✅ Mensagem de sucesso
- ✅ Tabela mostrando que `cliente_id` agora é nullable
- ✅ Constraint CHECK criada

## 🔍 O que a migração faz:

1. **Remove NOT NULL** do campo `cliente_id`
2. **Adiciona constraint CHECK** que garante:
   - Se `cliente_id` está preenchido, `empresa_id` deve ser NULL
   - Se `empresa_id` está preenchido, `cliente_id` deve ser NULL
   - Pelo menos um dos dois deve estar preenchido

## ✅ Após a migração

O código JavaScript já está preparado para enviar `cliente_id: null` quando criando agendamentos para empresas. Após executar a migração, o erro não deve mais ocorrer.

## 🧪 Como testar

1. Acesse o sistema NEOSUL
2. Vá em **Treinamentos** → **Agendamentos**
3. Clique em **"Novo Agendamento"**
4. Selecione: **Empresa**, **Trilha**, **Módulo**
5. Defina data/hora de início e fim
6. Adicione participantes (opcional)
7. Clique em **"Salvar Agendamento"**
8. ✅ Deve salvar sem erros

## 📝 Notas Importantes

- Esta migração é **segura** e não afeta dados existentes
- A constraint CHECK garante a integridade dos dados
- O código JavaScript já foi atualizado para funcionar com esta estrutura
