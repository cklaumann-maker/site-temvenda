# Instruções: Lista de Substituição de Alimentos

## 📋 O que foi implementado

Sistema completo de substituição de alimentos nas refeições, permitindo:
- Selecionar alimentos de uma lista pré-cadastrada
- Calcular calorias automaticamente
- Cadastrar novos alimentos
- Manter as opções padrão da dieta

## 🗄️ Estrutura do Banco de Dados

### Tabela: `food_items`
- `id`: UUID (chave primária)
- `category`: Categoria do alimento (Bebidas, Carboidratos, etc.)
- `name`: Nome do alimento
- `standard_portion`: Porção padrão (ex: 100g, 200ml, 1 un)
- `calories_kcal`: Calorias em kcal para a porção padrão
- `created_at`: Data de criação
- `updated_at`: Data de atualização
- `created_by`: ID do usuário que criou (NULL para itens do sistema)

## 🚀 Passos para Configuração

### 1. Executar Migration

Execute no SQL Editor do Supabase:

```sql
-- Arquivo: rotina-app/supabase/migrations/20240101000012_create_food_items_table.sql
```

Isso cria:
- Tabela `food_items`
- Índices para performance
- Políticas RLS (Row Level Security)
- Trigger para atualizar `updated_at`

### 2. Popular Tabela com Dados

Execute no SQL Editor do Supabase:

```sql
-- Arquivo: rotina-app/supabase/popular_food_items.sql
```

Isso insere todos os alimentos da lista fornecida, organizados por categoria:
- Bebidas
- Carboidratos
- Doces/Ultraprocessados
- Frutas
- Gorduras
- Laticínios
- Proteínas
- Verduras/Legumes
- Temperos/Ingredientes
- Outros

### 3. Verificar Dados

Execute para verificar quantos itens foram inseridos:

```sql
SELECT 
  category,
  COUNT(*) as total_itens
FROM public.food_items
GROUP BY category
ORDER BY category;

SELECT COUNT(*) as total_alimentos FROM public.food_items;
```

## 🎨 Funcionalidades da Interface

### Seleção de Alimentos

1. **Botão "Selecionar alimentos da lista"**
   - Aparece quando não há alimentos selecionados
   - Abre a interface de busca

2. **Busca e Filtro**
   - Campo de busca por nome do alimento
   - Filtro por categoria
   - Lista de resultados com porção e calorias

3. **Seleção de Itens**
   - Clique no alimento para adicionar
   - Controle de quantidade (+/-)
   - Remover itens individualmente
   - Cálculo automático de calorias totais

4. **Cadastro de Novos Alimentos**
   - Botão "+ Cadastrar novo alimento"
   - Formulário com:
     - Categoria (dropdown)
     - Nome do alimento
     - Porção padrão
     - Calorias (kcal)
   - Item é adicionado automaticamente após cadastro

### Salvamento

- Calorias são calculadas automaticamente
- Descrição inclui todos os itens selecionados com quantidades
- Salva no campo `kcal_other` e `other_description` da tabela `daily_meals`

## 🔧 API Endpoints

### GET `/api/food-items`
Buscar alimentos com filtros opcionais.

**Query Parameters:**
- `search`: Buscar por nome (opcional)
- `category`: Filtrar por categoria (opcional)

**Exemplo:**
```
GET /api/food-items?search=frango&category=Proteínas
```

**Resposta:**
```json
{
  "items": [
    {
      "id": "uuid",
      "category": "Proteínas",
      "name": "Frango grelhado",
      "standard_portion": "100 g",
      "calories_kcal": 165
    }
  ]
}
```

### POST `/api/food-items`
Criar novo alimento.

**Body:**
```json
{
  "category": "Proteínas",
  "name": "Peito de frango",
  "standard_portion": "100 g",
  "calories_kcal": 165
}
```

**Resposta:**
```json
{
  "item": {
    "id": "uuid",
    "category": "Proteínas",
    "name": "Peito de frango",
    "standard_portion": "100 g",
    "calories_kcal": 165,
    "created_by": "user_id"
  }
}
```

## 📱 Como Usar

1. Acesse a página "Hoje" (`/app/today`)
2. Para cada refeição, você verá as opções padrão da dieta
3. Clique em "+ Selecionar alimentos da lista" para substituir
4. Busque e selecione os alimentos consumidos
5. Ajuste as quantidades conforme necessário
6. As calorias são calculadas automaticamente
7. Clique em "Salvar"

## ✨ Recursos Adicionais

- **Cálculo Automático**: Calorias são somadas automaticamente
- **Múltiplos Itens**: Selecione quantos alimentos quiser
- **Quantidades**: Ajuste a quantidade de cada item
- **Cadastro Rápido**: Adicione novos alimentos sem sair da tela
- **Busca Inteligente**: Filtre por nome ou categoria

## 🔒 Permissões

- **Visualização**: Todos podem ver alimentos
- **Criação**: Apenas usuários autenticados
- **Edição/Exclusão**: Apenas o criador ou usuário root

## 📝 Notas

- Os alimentos cadastrados pelo usuário ficam disponíveis para todos
- Itens do sistema (created_by = NULL) não podem ser deletados por usuários comuns
- A lista pode ser expandida conforme necessário

