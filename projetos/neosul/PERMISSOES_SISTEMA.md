# NEOSUL - Matriz de Permissões do Sistema

## Resumo das Permissões por Perfil

### 1. ROOT (Administrador)

#### Permissões Gerais
- ✅ **Acesso total** a todas as funcionalidades do sistema
- ✅ **Pode criar, editar e excluir** qualquer registro
- ✅ **Pode visualizar** dados de todos os usuários
- ✅ **Pode administrar usuários** (criar, editar, ativar/desativar)
- ✅ **Pode alterar permissões** de qualquer usuário

#### Funcionalidades Específicas

##### Administração de Usuários
- ✅ Criar novos usuários (diretor, gerente, vendedor)
- ✅ Editar informações de qualquer usuário
- ✅ Ativar/desativar usuários
- ✅ Vincular vendedores a gerentes
- ✅ Alterar perfil de usuários
- ✅ Redefinir senhas

##### Calendário e Atividades
- ✅ Visualizar atividades de todos os usuários
- ✅ Criar/editar/excluir atividades de qualquer usuário
- ✅ Visualizar contador de horas de qualquer usuário
- ✅ Acesso à opção "Consultoria Externa" (se necessário)

##### Planejamentos
- ✅ Visualizar todos os planejamentos (mensais e semanais)
- ✅ Visualizar anotações privadas de qualquer gerente
- ✅ Criar/editar planejamentos para qualquer gerente

---

### 2. DIRETOR

#### Permissões Gerais
- ✅ **Pode visualizar** dados dos gerentes selecionados
- ❌ **NÃO pode criar/editar** registros
- ❌ **NÃO pode administrar usuários**

#### Funcionalidades Específicas

##### Seletor de Gerente
- ✅ Dropdown na sidebar para selecionar qual gerente visualizar
- ✅ Ao selecionar gerente, todos os dados são filtrados para aquele gerente
- ✅ Contador de horas atualiza automaticamente

##### Calendário e Atividades
- ✅ Visualiza atividades do gerente selecionado
- ✅ Visualiza contador de horas do gerente selecionado
- ✅ Visualiza tabelas de atividades diárias e semanais
- ❌ **NÃO pode criar/editar/excluir atividades**

##### Planejamentos
- ✅ Visualiza planejamentos mensais e semanais do gerente selecionado
- ✅ **NÃO pode ver anotações privadas** dos gerentes
- ❌ **NÃO pode criar/editar planejamentos**

##### Consultoria Externa
- ❌ **NÃO tem acesso** à opção "Consultoria Externa"

---

### 3. GERENTE

#### Permissões Gerais
- ✅ **Pode criar, editar e excluir** seus próprios registros
- ✅ **Pode visualizar vendedores** vinculados à sua equipe
- ✅ **Pode selecionar vendedor** para visualizar seus dados
- ❌ **NÃO pode administrar usuários**

#### Funcionalidades Específicas

##### Calendário e Atividades
- ✅ Visualiza e gerencia **suas próprias atividades**
- ✅ Visualiza atividades dos **vendedores da sua equipe** (quando selecionado)
- ✅ Pode criar/editar/excluir suas atividades
- ✅ Visualiza contador de horas próprias e dos vendedores selecionados
- ✅ Visualiza tabelas de atividades diárias e semanais

##### Seletor de Vendedor
- ✅ Dropdown na sidebar para selecionar qual vendedor da equipe visualizar
- ✅ Apenas vendedores vinculados ao gerente aparecem no seletor
- ✅ Ao selecionar vendedor, calendário e contador de horas são filtrados
- ✅ Opção "Minhas atividades" para voltar a visualizar próprios dados

##### Planejamentos
- ✅ Cria e edita seus próprios planejamentos mensais e semanais
- ✅ Pode criar anotações privadas
- ❌ **NÃO pode visualizar** planejamentos de outros gerentes

##### Consultoria Externa
- ✅ **Apenas o usuário "Cesar"** tem acesso à opção "Consultoria Externa"
- ❌ Outros gerentes **NÃO** veem essa opção no formulário de atividades

---

### 4. VENDEDOR

#### Permissões Gerais
- ✅ **Pode criar, editar e excluir** suas próprias atividades
- ✅ **Vinculado obrigatoriamente a um gerente**
- ❌ **NÃO pode visualizar** dados de outros vendedores
- ❌ **NÃO pode administrar usuários**

#### Funcionalidades Específicas

##### Calendário e Atividades
- ✅ Visualiza e gerencia **apenas suas próprias atividades**
- ✅ Visualiza seu próprio contador de horas
- ✅ Pode criar/editar/excluir suas atividades
- ✅ Visualiza suas tabelas de atividades diárias e semanais

##### Planejamentos
- ❌ **NÃO pode criar/editar planejamentos** mensais ou semanais
- ❌ **NÃO pode visualizar** planejamentos de outros usuários

##### Consultoria Externa
- ❌ **NÃO tem acesso** à opção "Consultoria Externa"

---

## Regras Especiais

### Consultoria Externa
- **Acesso exclusivo**: Apenas o usuário com `username = 'Cesar'` pode criar atividades do tipo "Consultoria Externa"
- **Filtro no formulário**: A opção aparece apenas para Cesar
- **Contador separado**: Consultoria Externa tem contador próprio e não soma no contador geral de horas

### Vinculação Vendedor-Gerente
- **Obrigatória**: Vendedores devem estar vinculados a um gerente (`gerente_id`)
- **Validação**: Ao criar vendedor, campo `gerente_id` é obrigatório
- **Visualização**: Gerente pode ver calendário e horas dos vendedores vinculados

### Contador de Horas
- **Filtro por usuário**: Contador mostra horas do usuário logado ou selecionado
- **Exclusão**: Consultoria Externa não conta no contador geral
- **Atualização**: Atualiza automaticamente ao mudar de gerente/vendedor selecionado

### Planejamentos
- **Anotações privadas**: Apenas o gerente criador pode ver suas anotações privadas
- **Diretores**: Podem ver planejamentos mas não anotações privadas
- **Root**: Pode ver tudo, incluindo anotações privadas

---

## Matriz de Permissões

| Funcionalidade | Root | Diretor | Gerente | Vendedor |
|----------------|------|---------|---------|----------|
| **Criar Atividades** | ✅ Todos | ❌ | ✅ Próprias | ✅ Próprias |
| **Editar Atividades** | ✅ Todas | ❌ | ✅ Próprias | ✅ Próprias |
| **Visualizar Atividades** | ✅ Todos | ✅ Gerente selecionado | ✅ Próprias + Vendedores | ✅ Próprias |
| **Criar Planejamentos** | ✅ Todos | ❌ | ✅ Próprios | ❌ |
| **Editar Planejamentos** | ✅ Todos | ❌ | ✅ Próprios | ❌ |
| **Visualizar Planejamentos** | ✅ Todos | ✅ Gerente selecionado | ✅ Próprios | ❌ |
| **Ver Anotações Privadas** | ✅ Todas | ❌ | ✅ Próprias | ❌ |
| **Consultoria Externa** | ✅ (se necessário) | ❌ | ✅ Apenas Cesar | ❌ |
| **Administrar Usuários** | ✅ | ❌ | ❌ | ❌ |
| **Visualizar Vendedores** | ✅ Todos | ❌ | ✅ Da equipe | ❌ |
| **Contador de Horas** | ✅ Todos | ✅ Gerente selecionado | ✅ Próprias + Vendedores | ✅ Próprias |

---

## Permissões Administrativas (Root)

### Gerenciamento de Usuários
1. **Criar Usuário**
   - Nome completo
   - Username (login)
   - Senha
   - Perfil (root, diretor, gerente, vendedor)
   - Status (ativo/inativo)
   - Gerente responsável (se vendedor)

2. **Editar Usuário**
   - Alterar nome completo
   - Alterar username
   - Alterar senha
   - Alterar perfil
   - Alterar status (ativar/desativar)
   - Alterar gerente responsável (se vendedor)

3. **Ativar/Desativar Usuário**
   - Usuários desativados não podem fazer login
   - Dados permanecem no sistema

### Permissões que podem ser administradas
- **Perfil do usuário**: root, diretor, gerente, vendedor
- **Status ativo/inativo**: controla acesso ao sistema
- **Vinculação gerente-vendedor**: define hierarquia
- **Senha**: pode ser redefinida pelo root

---

## Observações Importantes

1. **Segurança**: As senhas estão em texto plano no banco. Para produção, considere implementar hash de senha.

2. **Validações**: 
   - Vendedores devem ter gerente_id obrigatório
   - Username deve ser único
   - Usuários inativos não podem fazer login

3. **Hierarquia**:
   - Root > Diretor > Gerente > Vendedor
   - Cada nível pode visualizar apenas o nível imediatamente abaixo (com exceções)

4. **Consultoria Externa**: É uma funcionalidade especial restrita ao usuário Cesar, não é um perfil.

---

## Próximos Passos Sugeridos

1. Implementar hash de senha (bcrypt/argon2)
2. Adicionar logs de auditoria
3. Implementar recuperação de senha
4. Adicionar permissões granulares (ex: gerente pode criar vendedores)
5. Implementar notificações entre níveis hierárquicos
