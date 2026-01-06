# Instruções: Importar Alimentos do Excel

## 📋 Funcionalidade

Página de administração para importar alimentos de um arquivo Excel, verificando automaticamente duplicatas e inserindo apenas itens novos.

## 🚀 Configuração Inicial

### 1. Instalar Dependência

Execute no diretório do projeto:

```bash
cd rotina-app
pnpm add xlsx --filter @rotina/web
```

Ou manualmente, adicione ao `apps/web/package.json`:

```json
{
  "dependencies": {
    "xlsx": "^0.18.5"
  }
}
```

Depois execute:
```bash
pnpm install
```

## 📊 Formato do Arquivo Excel

O arquivo Excel deve ter as seguintes colunas (nomes podem variar):

| Categoria | Alimento | Porção Padrão | Calorias |
|-----------|----------|---------------|----------|
| Bebidas | Água | 200 ml | 0 |
| Proteínas | Frango grelhado | 100 g | 165 |

### Nomes Aceitos para Colunas

- **Categoria**: `Categoria`, `Category`, `categoria`, `category`
- **Alimento**: `Alimento`, `Alimento/Nome`, `Name`, `Nome`, `name`
- **Porção**: `Porção Padrão`, `Porção`, `Porcao`, `Portion`, `standard_portion`
- **Calorias**: `Calorias`, `Calorias (kcal)`, `Calories`, `kcal`, `Calorias kcal`

## 🎯 Como Usar

1. **Acesse a página de importação**
   - Faça login como usuário root
   - Vá em "Admin Alimentos" no menu
   - Clique em "Importar do Excel"

2. **Selecione o arquivo**
   - Clique em "Selecione o arquivo Excel"
   - Escolha um arquivo `.xlsx` ou `.xls`
   - O sistema mostrará um preview das primeiras 10 linhas

3. **Verifique o preview**
   - Confirme se as colunas foram identificadas corretamente
   - Verifique se os dados estão corretos

4. **Importe**
   - Clique em "Importar Alimentos"
   - Aguarde o processamento
   - Veja o resultado:
     - Total de itens no arquivo
     - Itens inseridos (novos)
     - Itens ignorados (duplicatas)
     - Erros encontrados (se houver)

## 🔍 Verificação de Duplicatas

O sistema verifica duplicatas pela combinação de:
- **Nome do alimento** (case-insensitive)
- **Porção padrão** (case-insensitive)

Exemplos de duplicatas que serão ignoradas:
- "Água" + "200 ml" (já existe)
- "água" + "200 ML" (mesmo que acima, ignorado)
- "Frango grelhado" + "100 g" (já existe)

Exemplos que serão inseridos:
- "Água" + "500 ml" (porção diferente, novo item)
- "Água mineral" + "200 ml" (nome diferente, novo item)

## ⚠️ Validações

O sistema valida:
- ✅ Campos obrigatórios (Categoria, Alimento, Porção)
- ✅ Calorias não negativas
- ✅ Formato do arquivo Excel

## 📝 Exemplo de Arquivo Excel

Crie um arquivo Excel com esta estrutura:

```
| Categoria      | Alimento          | Porção Padrão | Calorias |
|----------------|-------------------|----------------|----------|
| Bebidas        | Suco de laranja   | 200 ml         | 90       |
| Proteínas      | Peito de frango   | 100 g          | 165      |
| Carboidratos   | Arroz integral    | 100 g cozido   | 130      |
```

## 🔧 Processamento

- Itens são inseridos em lotes de 50 para melhor performance
- Erros são coletados e exibidos ao final
- Processo é interrompido apenas em caso de erro crítico

## 🎨 Interface

A página inclui:
- Preview das primeiras 10 linhas antes de importar
- Feedback visual durante o processamento
- Relatório detalhado após a importação
- Lista de erros (se houver)

## 🔒 Permissões

Apenas usuários **root** podem acessar esta funcionalidade.

## 📍 Localização

- **Rota**: `/app/admin/food-items/import`
- **Arquivo**: `apps/web/src/app/app/admin/food-items/import/page.tsx`

## 🐛 Troubleshooting

### Erro: "Nenhum item válido encontrado"
- Verifique se as colunas têm os nomes corretos
- Confira se há dados nas linhas (não apenas cabeçalhos)

### Erro: "Campos obrigatórios faltando"
- Certifique-se de que todas as colunas estão preenchidas
- Verifique se não há linhas vazias

### Erro: "Calorias inválidas"
- Certifique-se de que a coluna de calorias contém apenas números
- Remova caracteres não numéricos

### Preview não mostra dados corretos
- Verifique se os nomes das colunas estão corretos
- O sistema tenta identificar automaticamente, mas pode precisar de ajustes

