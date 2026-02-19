# 📚 Estrutura de Treinamentos - NEOSUL

## 🎯 Visão Geral

Sistema completo de gestão de treinamentos com trilhas, módulos, clientes, agendamentos e pesquisa NPS.

## 📊 Estrutura de Dados

### 1. **Trilhas** (`neosul_trilhas`)
- Nome, descrição
- Status ativo/inativo
- Exemplo: "Trilha de Gestão de Pessoas"

### 2. **Módulos** (`neosul_modulos`)
- Vinculados a uma trilha
- Nome próprio, descrição, duração em horas
- Ordem padrão (pode ser personalizada por cliente)
- Exemplo: "Módulo 1: Recrutamento", "Módulo 2: Seleção"

### 3. **Clientes** (`neosul_clientes`)
- Nome, empresa, telefone, email
- Um cliente pode ter múltiplas trilhas
- Mesma trilha pode ser aplicada múltiplas vezes

### 4. **Vínculo Cliente-Trilha** (`neosul_cliente_trilhas`)
- Vincula cliente a uma trilha específica
- **Sequência personalizada de módulos** (JSONB)
- Permite aplicar módulos em ordem diferente para cada cliente

### 5. **Agendamentos** (`neosul_treinamentos_agendamentos`)
- **Cria atividade no calendário automaticamente**
- Cliente + Trilha + Módulo
- Data/hora início e fim
- Status: previsto, em_andamento, realizado, cancelado
- **QR Code único** para pesquisa NPS
- **Atualização automática de status** após data/hora

### 6. **Participantes** (`neosul_treinamentos_participantes`)
- Cadastrados por agendamento/módulo
- Nome, email, telefone, empresa
- Importação via CSV ou cadastro manual

### 7. **Pesquisa NPS** (`neosul_pesquisa_nps`)
- 2 perguntas editáveis
- Sempre a mesma pesquisa
- Ativa/inativa

### 8. **Respostas NPS** (`neosul_respostas_nps`)
- Vinculada ao agendamento e participante
- Pergunta 1: Nota 0-10
- Pergunta 2: Texto livre
- Acesso via QR Code

## 🔄 Fluxos Principais

### 1. Cadastro de Trilha e Módulos
1. Criar trilha (ex: "Gestão de Pessoas")
2. Adicionar módulos à trilha (ex: "Módulo 1: Recrutamento")
3. Definir ordem padrão (opcional)

### 2. Cadastro de Cliente e Vínculo
1. Cadastrar cliente
2. Vincular cliente a uma trilha
3. Definir sequência personalizada de módulos (arrastar/soltar ou setas)
4. Um cliente pode ter múltiplas trilhas

### 3. Agendamento de Módulo
1. Selecionar cliente + trilha + módulo
2. Definir data/hora início e fim
3. Cadastrar participantes (CSV ou manual)
4. **Sistema cria atividade no calendário automaticamente**
   - Título: "Cliente/Trilha/Módulo"
   - Status: "previsto"
   - Aparece na lista de atividades
5. **Sistema gera QR Code único** para pesquisa NPS

### 4. Execução do Treinamento
1. Status muda automaticamente após data/hora fim
2. Pode ser alterado manualmente (botão)
3. Ao marcar como "realizado":
   - Pesquisa NPS pode ser enviada por email automaticamente
   - QR Code disponível na tela

### 5. Pesquisa NPS
1. Participante acessa via QR Code
2. Responde 2 perguntas
3. Resposta gravada no banco
4. Pode responder a qualquer momento

## 📋 Funcionalidades da Interface

### Área de Treinamentos (Menu Lateral)
1. **Cadastro de Trilhas**
   - Lista de trilhas
   - Criar/editar trilha
   - Adicionar/editar módulos

2. **Cadastro de Clientes**
   - Lista de clientes
   - Criar/editar cliente
   - Vincular trilhas ao cliente
   - Definir sequência de módulos (arrastar/soltar ou setas)

3. **Agendamentos**
   - Lista de agendamentos
   - Criar novo agendamento
   - Cadastrar participantes (CSV ou manual)
   - Visualizar QR Code
   - Alterar status manualmente

4. **Pesquisa NPS**
   - Editar perguntas
   - Visualizar respostas
   - Relatórios por módulo

5. **Relatórios**
   - Trilhas por cliente
   - Módulos executados
   - NPS por módulo

## 🔗 Integração com Calendário

- **Criação automática**: Ao agendar módulo, cria atividade em `neosul_atividades_diarias`
- **Título**: Formato "Cliente/Trilha/Módulo"
- **Status**: "previsto" (inicial)
- **Tipo**: Novo tipo "treinamento" (se necessário)
- **Aparece**: Na lista de atividades do dia
- **Atualização**: Status sincronizado com agendamento

## 📱 Pesquisa NPS via QR Code

- **Página pública**: `/projetos/neosul/pesquisa-nps.html?qr=TRN-...`
- **Validação**: Verifica QR Code no banco
- **Formulário**: 2 perguntas
- **Gravação**: Resposta vinculada ao agendamento e participante
- **QR Code**: Gerado automaticamente no agendamento

## 🎨 Próximas Etapas de Implementação

1. ✅ Estrutura de banco de dados criada
2. ⏳ Interface de cadastro de trilhas e módulos
3. ⏳ Interface de cadastro de clientes
4. ⏳ Interface de vínculo cliente-trilha com sequência
5. ⏳ Interface de agendamento
6. ⏳ Cadastro de participantes (CSV e manual)
7. ⏳ Integração com calendário (criação automática de atividades)
8. ⏳ Página de pesquisa NPS (QR Code)
9. ⏳ Relatórios
10. ⏳ Envio automático de email para pesquisa NPS

## 📝 Observações Importantes

- **Módulos são reutilizáveis**: Não criamos módulos personalizados por cliente
- **Sequência personalizada**: Cada cliente pode ter ordem diferente dos módulos
- **Múltiplas aplicações**: Mesmo módulo pode ser aplicado várias vezes ao mesmo cliente
- **Histórico completo**: Todas as execuções ficam registradas
- **QR Code único**: Cada agendamento tem seu próprio código
