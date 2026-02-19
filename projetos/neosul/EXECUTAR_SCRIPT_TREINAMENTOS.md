# Como Executar o Script de Criação das Tabelas de Treinamento

## 📋 Tabelas que Serão Criadas (8 tabelas)

Este script criará apenas as tabelas de treinamento que estão faltando:

1. ✅ `neosul_trilhas` - Trilhas de treinamento
2. ✅ `neosul_modulos` - Módulos das trilhas  
3. ✅ `neosul_clientes` - Clientes
4. ✅ `neosul_cliente_trilhas` - Vínculo cliente-trilha
5. ✅ `neosul_treinamentos_agendamentos` - Agendamentos
6. ✅ `neosul_treinamentos_participantes` - Participantes
7. ✅ `neosul_pesquisa_nps` - Configuração da pesquisa NPS
8. ✅ `neosul_respostas_nps` - Respostas da pesquisa

## 🚀 Passo a Passo

### 1. Acessar o Supabase
1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Faça login na sua conta

### 2. Abrir o SQL Editor
1. No menu lateral esquerdo, clique em **"SQL Editor"**
2. Clique no botão **"New query"** (ou use o atalho)

### 3. Executar o Script
1. Abra o arquivo: `CRIAR_TABELAS_TREINAMENTOS_FALTANTES.sql`
2. **Copie TODO o conteúdo** do arquivo (Ctrl+A, Ctrl+C)
3. Cole no SQL Editor do Supabase (Ctrl+V)
4. Clique no botão **"Run"** (ou pressione `Ctrl+Enter` / `Cmd+Enter`)

### 4. Verificar Sucesso
Você deve ver uma mensagem de sucesso e o número de tabelas criadas.

Para verificar manualmente, execute esta query:
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' 
AND table_name LIKE 'neosul%'
ORDER BY table_name;
```

**Resultado esperado:** 13 tabelas no total (5 existentes + 8 novas)

## ✅ Tabelas Existentes (NÃO serão recriadas)
- neosul_atividades_diarias
- neosul_planejamento_mensal
- neosul_planejamento_semanal
- neosul_reunioes_semanais
- neosul_usuarios

## ⚠️ Importante

- O script usa `CREATE TABLE IF NOT EXISTS`, então é seguro executar mesmo se algumas tabelas já existirem
- Não vai deletar ou modificar tabelas existentes
- Apenas cria as que estão faltando

## 🔍 Após Executar

1. Aguarde 1-2 minutos para o cache do Supabase atualizar
2. Limpe o cache do navegador (`Ctrl+Shift+R` ou `Cmd+Shift+R`)
3. Acesse: `http://localhost:3000/projetos/neosul/index.html`
4. Faça login: `Cesar` / `Cesar*26`
5. Clique em "Treinamento" no menu lateral

## 🐛 Troubleshooting

**Se aparecer erro de "table already exists":**
- Isso é normal, significa que a tabela já existe
- O script continuará criando as outras tabelas

**Se aparecer erro de permissão:**
- Verifique se você está logado como administrador do projeto
- Verifique se está no projeto correto: `mgcoyeohqelystqmytah`

**Se ainda aparecer erro de cache:**
- Aguarde mais alguns minutos
- O sistema tentará automaticamente até 3 vezes com retry
