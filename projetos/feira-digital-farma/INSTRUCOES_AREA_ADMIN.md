# Instruções - Área Administrativa Feira Digital Farma

## Acesso

1. Acesse qualquer página do site Feira Digital Farma
2. Role até o rodapé
3. Clique no link "Área Administrativa"
4. Faça login com:
   - **Login**: `cesar` ou `root`
   - **Senha**: `cesar*26` ou `root*26` (conforme o login escolhido)

## Dashboard

O dashboard exibe 11 métricas principais em tempo real:
- Indústrias (Ativas, Aguardando, Inativas)
- Total de Distribuidoras
- Total de Corporativos
- Total de Participantes
- Participantes Confirmados/Pendentes
- Cotas Pagas/Pendentes
- Receita Estimada

## Módulos CRUD

### Indústrias
- **Criar**: Clique em "+ Adicionar Indústrias"
- **Editar**: Clique no ícone ✏️ na linha desejada
- **Excluir**: Clique no ícone 🗑️ na linha desejada
- **Upload de Logo**: Ao criar/editar, selecione um arquivo PNG ou JPG (máx. 5MB, recomendado 300x300px)
  - Preview será exibido automaticamente antes de salvar

### Distribuidoras
- Mesmas funcionalidades das Indústrias
- Upload de logo disponível

### Corporativos
- Criar, Editar, Excluir
- Sem upload de logo (por enquanto)

### Participantes
- **Criar**: Preencha todos os campos obrigatórios (CNPJ, Nome da Farmácia, Nome do Participante, CPF, Telefone, Email)
- **Vincular a Parceiro**: Selecione Indústria, Distribuidora ou Corporativo no formulário
- **Confirmar Email**: Marque a checkbox "Email Confirmado" se o participante já confirmou o email

### CNPJs
- **Upload CSV em Lote**:
  1. Clique na aba "CNPJs"
  2. Na seção "Upload de CNPJs", selecione um arquivo CSV
  3. Formato esperado: CSV com colunas `CNPJ`, `Razão Social`, `Nome Fantasia` (opcional)
  4. Clique em "📤 Fazer Upload"
  5. Os CNPJs serão inseridos/atualizados automaticamente

- **Criar Manualmente**: Use o botão "+ Adicionar CNPJs" para inserir um CNPJ individual

### Cotas
- **Criar**: Selecione o Parceiro (Indústria ou Distribuidora), o valor será preenchido automaticamente
- **Marcar como Pago**: Clique no botão 💰 na linha da cota para marcar como paga (data será preenchida automaticamente)
- **Gerar Relatório**: Clique em "📊 Gerar Relatório" para baixar um CSV com todas as cotas
- **Isento**: Marque a checkbox "Isento de Cota" para cotas que não precisam pagar

## Funcionalidades Especiais

### Upload de Logos
- Formatos aceitos: PNG, JPG, JPEG
- Tamanho máximo: 5MB
- Tamanho recomendado: 300x300px
- Preview automático antes de salvar

### Exportação de Dados
- **Cotas**: Botão "Gerar Relatório" gera CSV com todas as informações
- Outros módulos: Em desenvolvimento

## Notas Importantes

1. **Autenticação**: A sessão é mantida no navegador. Faça logout ao terminar.
2. **Validações**: CNPJs devem ter 14 dígitos, CPFs 11 dígitos
3. **Vínculos**: Um participante pode estar vinculado a apenas um parceiro (Indústria, Distribuidora ou Corporativo)
4. **Cotas**: Ao criar uma cota vinculada a uma Indústria/Distribuidora, o valor será preenchido automaticamente com o valor da cota do parceiro

## Troubleshooting

- **Erro ao fazer upload de logo**: Verifique se o arquivo é PNG ou JPG e tem menos de 5MB
- **Erro ao fazer upload de CNPJs**: Verifique se o CSV está no formato correto (CNPJ, Razão Social, Nome Fantasia)
- **Dados não aparecem**: Verifique se você está na aba correta e se há dados no banco
