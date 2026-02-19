# Instruções para Criar Estrutura de Materiais dos Módulos

## 📋 Passo a Passo

### 1. Acesse o SQL Editor do Supabase
- Acesse: https://mgcoyeohqelystqmytah.supabase.co
- Vá em **SQL Editor** no menu lateral

### 2. Execute o Script SQL
- Abra o arquivo `CRIAR_ESTRUTURA_COMPLETA_MATERIAIS.sql`
- Copie todo o conteúdo
- Cole no SQL Editor do Supabase
- Clique em **RUN** ou pressione `Ctrl+Enter`

### 3. Verificar Criação
O script criará:
- ✅ Tabela `neosul_modulo_materiais`
- ✅ Bucket de Storage `modulo-materiais`
- ✅ Políticas de acesso ao Storage
- ✅ Índices para performance

### 4. Configurar Storage Manualmente (se necessário)
Se o bucket não aparecer automaticamente:
1. Vá em **Storage** no menu lateral
2. Verifique se o bucket `modulo-materiais` foi criado
3. Se não existir, crie manualmente:
   - Clique em **New bucket**
   - Nome: `modulo-materiais`
   - Público: **Sim**
   - Limite de tamanho: 50MB

### 5. Verificar Políticas de Storage
1. Vá em **Storage** > **Policies**
2. Verifique se as políticas foram criadas:
   - `Permitir leitura pública de materiais`
   - `Permitir upload de materiais`
   - `Permitir atualização de materiais`
   - `Permitir exclusão de materiais`

## ✅ Após Executar

Após executar o script com sucesso, você poderá:
- ✅ Adicionar materiais aos módulos
- ✅ Fazer upload de arquivos (PDF, Word, PowerPoint, Excel, Imagens, Vídeos)
- ✅ Adicionar links externos
- ✅ Visualizar materiais no layout em árvore

## 🔍 Verificação Final

Execute esta query no SQL Editor para verificar:

```sql
SELECT 
    'Tabela criada' as status,
    COUNT(*) as total_materiais
FROM neosul_modulo_materiais;
```

Se retornar `total_materiais: 0`, a tabela foi criada com sucesso!
