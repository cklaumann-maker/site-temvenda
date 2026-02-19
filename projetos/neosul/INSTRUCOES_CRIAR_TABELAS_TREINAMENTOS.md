# Instruções para Criar Tabelas de Treinamentos

## Projeto Supabase Configurado
- **URL**: `https://mgcoyeohqelystqmytah.supabase.co`
- **Status**: ✅ Código já está apontando para este projeto

## Passo a Passo

### 1. Acessar o Supabase
1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Faça login na sua conta

### 2. Abrir o SQL Editor
1. No menu lateral, clique em **"SQL Editor"**
2. Clique em **"New query"**

### 3. Executar o Script
1. Abra o arquivo: `CRIAR_TABELAS_TREINAMENTOS_COMPLETO.sql`
2. Copie TODO o conteúdo do arquivo
3. Cole no SQL Editor do Supabase
4. Clique em **"Run"** ou pressione `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac)

### 4. Verificar se Funcionou
Após executar, você deve ver uma mensagem de sucesso e o número de tabelas criadas.

Para verificar manualmente, execute esta query:
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' 
AND table_name LIKE 'neosul%'
ORDER BY table_name;
```

Você deve ver estas 13 tabelas:
- neosul_atividades_diarias
- neosul_cliente_trilhas
- neosul_clientes
- neosul_modulos
- neosul_pesquisa_nps
- neosul_planejamento_mensal
- neosul_planejamento_semanal
- neosul_respostas_nps
- neosul_reunioes_semanais
- neosul_treinamentos_agendamentos
- neosul_treinamentos_participantes
- neosul_trilhas
- neosul_usuarios

## Arquivos que Usam Este Projeto

✅ **index.html** - Linha 2473
```javascript
const SUPABASE_URL = 'https://mgcoyeohqelystqmytah.supabase.co';
```

✅ **pesquisa-nps.html** - Linha 227
```javascript
const SUPABASE_URL = 'https://mgcoyeohqelystqmytah.supabase.co';
```

## Tabelas que Serão Criadas

1. **neosul_trilhas** - Trilhas de treinamento
2. **neosul_modulos** - Módulos das trilhas
3. **neosul_clientes** - Clientes
4. **neosul_cliente_trilhas** - Vínculo cliente-trilha
5. **neosul_treinamentos_agendamentos** - Agendamentos
6. **neosul_treinamentos_participantes** - Participantes
7. **neosul_pesquisa_nps** - Configuração da pesquisa NPS
8. **neosul_respostas_nps** - Respostas da pesquisa

## Permissões Configuradas

- ✅ SELECT, INSERT, UPDATE, DELETE para `anon` e `authenticated`
- ✅ RLS (Row Level Security) desabilitado
- ✅ Índices criados para performance
- ✅ Triggers para `updated_at` automático

## Após Executar o Script

1. Limpe o cache do navegador
2. Acesse: `http://localhost:3000/projetos/neosul/index.html`
3. Faça login com: `Cesar` / `Cesar*26`
4. Clique em "Treinamento" no menu lateral
5. O sistema deve carregar sem erros

## Troubleshooting

Se ainda aparecer erro de "schema cache":
- Aguarde 1-2 minutos após executar o script
- Limpe o cache do navegador completamente
- O sistema tentará automaticamente até 3 vezes com retry
