# Instruções para Alocação de Colaboradores aos Módulos

## 📋 Passo a Passo

### 1. Execute o Script SQL
- Acesse: https://mgcoyeohqelystqmytah.supabase.co
- Vá em **SQL Editor** no menu lateral
- Abra o arquivo `ADICIONAR_COLUNA_ALOCACAO_COLABORADORES.sql`
- Copie todo o conteúdo
- Cole no SQL Editor do Supabase
- Clique em **RUN** ou pressione `Ctrl+Enter`

### 2. O Script Criará:
- ✅ Coluna `alocacao_colaboradores` na tabela `neosul_cliente_trilhas`
- ✅ Índice GIN para buscas eficientes no JSONB
- ✅ Formato: `{"modulo_id": ["colaborador_id1", "colaborador_id2"]}`

## 🎯 Como Usar

### 1. Vincular Trilha à Empresa
- Acesse: **Treinamento** → **Empresas**
- Clique no botão **"Vincular Trilha"** (ícone de link) na empresa desejada
- Selecione a **Trilha**
- Os módulos da trilha aparecerão automaticamente

### 2. Alocar Colaboradores aos Módulos
- Após selecionar a trilha, aparecerá a seção **"Alocar Colaboradores aos Módulos"**
- Para cada módulo, você verá uma lista de checkboxes com os colaboradores da empresa
- Marque os checkboxes dos colaboradores que participarão de cada módulo
- Os colaboradores selecionados aparecerão destacados em azul

### 3. Salvar
- Clique em **"Salvar"** para salvar a sequência de módulos e a alocação de colaboradores
- A alocação será salva no formato JSONB no banco de dados

## ✨ Funcionalidades

- ✅ Visualização clara de cada módulo com seus colaboradores
- ✅ Checkboxes interativos com feedback visual (azul quando selecionado)
- ✅ Alocação persistente no banco de dados
- ✅ Carregamento automático de alocações existentes ao editar
- ✅ Suporte a múltiplos colaboradores por módulo

## 🔍 Formato dos Dados

A alocação é armazenada como JSONB na coluna `alocacao_colaboradores`:

```json
{
  "modulo_id_1": ["colaborador_id_1", "colaborador_id_2"],
  "modulo_id_2": ["colaborador_id_3"]
}
```

## ✅ Após Executar

Após executar o script SQL com sucesso, você poderá:
- ✅ Alocar colaboradores específicos a cada módulo
- ✅ Visualizar quais colaboradores estão alocados em cada módulo
- ✅ Editar alocações existentes
- ✅ Usar essas alocações nos agendamentos de treinamento
