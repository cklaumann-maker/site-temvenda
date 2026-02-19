# Hierarquia e permissões – NEOSUL

## Hierarquia

```
Root / Diretor → Gerente → Gestor de Time → Vendedor
```

- **Vendedor** pertence a um **Gestor de Time** (`gestor_de_time_id`).
- **Gestor de Time** pertence a um **Gerente** (`gerente_id`).
- **Gerente** não tem superior na hierarquia (Root/Diretor são administrativos).

## Cadastro (quem cadastra quem)

| Quem              | Pode cadastrar                          |
|-------------------|-----------------------------------------|
| Root              | Qualquer perfil                         |
| Diretor           | Gerente, Gestor de Time, Vendedor       |
| Gerente           | Gestor de Time, Vendedor                |
| Gestor de Time    | Apenas Vendedor (vinculado a ele)       |

- Ao cadastrar **Vendedor**, é obrigatório escolher um **Gestor de Time**.
- Ao cadastrar **Gestor de Time**, é obrigatório escolher um **Gerente**.
- Gerente e Gestor de Time só podem cadastrar dentro da própria equipe/time.

## Visualização e edição na área de usuários

- **Root**: vê e pode editar/excluir todos.
- **Diretor**: vê Gerentes, Gestores de Time e Vendedores; pode editar/excluir (exceto Root).
- **Gerente**: vê Gestores de Time e Vendedores da sua equipe; pode editar/excluir apenas esses.
- **Gestor de Time**: vê apenas Vendedores do seu time; pode editar/excluir apenas esses.

## Calendário

- Cada um tem **seu próprio calendário** (atividades/planejamento por `gerente_nome` = nome do dono).
- **Quem vê (somente leitura)**:
  - **Diretor**: escolhe um Gerente e vê calendário desse Gerente + dos Gestores de Time e Vendedores dele.
  - **Gerente**: escolhe “Minhas atividades” ou um Gestor de Time / Vendedor da equipe e vê o calendário (somente leitura).
  - **Gestor de Time**: escolhe “Minhas atividades” ou um Vendedor do time e vê o calendário (somente leitura).
  - **Vendedor**: vê apenas o próprio calendário.
- **Quem edita**: cada um edita **somente o próprio calendário** (quando “Minhas atividades” ou equivalente está selecionado).

## Banco de dados

- Tabela: `neosul_usuarios`.
- Colunas de hierarquia:
  - `gerente_id`: preenchido em **Gestor de Time** (gerente responsável) e opcionalmente em **Vendedor** (gerente da área).
  - `gestor_de_time_id`: preenchido em **Vendedor** (gestor de time responsável).
- Perfis: `root`, `diretor`, `gerente`, `gestor_de_time`, `vendedor`.

Script de migração (adicionar coluna e migrar dados): `MIGRACAO_HIERARQUIA_GESTOR_DE_TIME.sql`.
