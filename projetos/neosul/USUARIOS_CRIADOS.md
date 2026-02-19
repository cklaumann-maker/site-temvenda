# NEOSUL - Usuários Criados

## Sistema de Autenticação Implementado

O sistema agora possui autenticação completa com usuários e senhas.

## Usuários Cadastrados

### 1. Administrador (Root)
- **Usuário**: `root`
- **Senha**: `root`
- **Perfil**: Administrador
- **Permissões**: Acesso total ao sistema

### 2. Machado (Diretor)
- **Usuário**: `Machado`
- **Senha**: `Machado*26`
- **Perfil**: Diretor
- **Permissões**: Visualiza todos os planejamentos (de todos os gerentes), não edita

### 3. Teo (Diretor)
- **Usuário**: `Teo`
- **Senha**: `Teo*26`
- **Perfil**: Diretor
- **Permissões**: Visualiza todos os planejamentos (de todos os gerentes), não edita

### 4. Cesar (Gerente)
- **Usuário**: `Cesar`
- **Senha**: `Cesar*26`
- **Perfil**: Gerente de Vendas
- **Permissões**: Cria e edita apenas seus próprios planejamentos

## Como Configurar no Supabase

### Opção 1: Primeira Instalação (se ainda não executou o setup)
Execute o arquivo completo no SQL Editor do Supabase:
```sql
/projetos/neosul/setup-database.sql
```

### Opção 2: Adicionar Autenticação (se já tem as outras tabelas)
Execute apenas o arquivo de usuários:
```sql
/projetos/neosul/criar-usuarios.sql
```

## Segurança

⚠️ **IMPORTANTE**: Este sistema usa senhas em texto plano para simplicidade interna.

Para uso em produção, considere:
- Usar hash de senha (bcrypt, argon2)
- Implementar Supabase Auth nativo
- Adicionar políticas RLS (Row Level Security)
- Adicionar tokens JWT

## Testando o Sistema

1. Acesse: `http://localhost:3000/projetos/neosul/`
2. Use um dos usuários cadastrados
3. Perfis diferentes terão visualizações diferentes:
   - **Root/Diretor**: Vê todos os planejamentos
   - **Gerente**: Vê apenas seus próprios planejamentos
   - **Equipe**: Visualização limitada (futura)

## Adicionando Novos Usuários

Para adicionar novos usuários, execute no SQL Editor:

```sql
INSERT INTO neosul_usuarios (username, senha, nome_completo, perfil) VALUES
  ('novo_usuario', 'senha_aqui', 'Nome Completo', 'gerente');
```

Perfis disponíveis: `root`, `diretor`, `gerente`, `equipe`
