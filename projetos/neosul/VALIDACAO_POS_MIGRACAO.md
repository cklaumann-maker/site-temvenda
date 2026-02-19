# ✅ Validação Pós-Migração

## 🎯 Checklist de Validação

Após executar as migrações SQL, valide se tudo está funcionando corretamente:

### 1. ✅ Estrutura do Banco de Dados

Execute no SQL Editor do Supabase para verificar:

```sql
-- Verificar se a coluna agendamento_id foi adicionada
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'neosul_pesquisa_nps' 
AND column_name = 'agendamento_id';

-- Verificar se a função foi criada
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND routine_name = 'verificar_dependencias_exclusao';
```

**Resultado esperado:**
- Coluna `agendamento_id` existe e é do tipo `uuid`
- Função `verificar_dependencias_exclusao` existe

### 2. ✅ Funcionalidades de Pesquisa NPS

#### Teste 1: Criar Agendamento
1. Acesse a área de Treinamentos → Agendamentos
2. Crie um novo agendamento
3. Verifique no banco se uma pesquisa foi criada automaticamente:
   ```sql
   SELECT * FROM neosul_pesquisa_nps 
   WHERE agendamento_id IS NOT NULL 
   ORDER BY created_at DESC LIMIT 5;
   ```

#### Teste 2: Pesquisa via QR Code
1. Após criar um agendamento, copie o QR Code
2. Acesse a página de pesquisa NPS com o QR Code
3. Verifique se a pesquisa específica do agendamento é carregada

#### Teste 3: Pesquisa Global
1. Acesse Treinamentos → Pesquisa NPS
2. Deixe o campo "Agendamento" vazio
3. Preencha as perguntas e salve
4. Verifique se foi criada como pesquisa global (`agendamento_id IS NULL`)

### 3. ✅ Funcionalidades de Exclusão

#### Teste 1: Excluir Agendamento
1. Crie um agendamento com participantes
2. Tente excluir o agendamento
3. Verifique se aparece mensagem sobre dependências
4. Confirme a exclusão
5. Verifique se participantes foram excluídos automaticamente (CASCADE)

#### Teste 2: Excluir Módulo
1. Tente excluir um módulo que tenha agendamentos
2. Verifique se aparece mensagem sobre dependências
3. Confirme e verifique se agendamentos foram excluídos

#### Teste 3: Excluir Trilha
1. Tente excluir uma trilha que tenha módulos
2. Verifique se aparece mensagem sobre dependências
3. Confirme e verifique se módulos foram excluídos

#### Teste 4: Excluir Colaborador
1. Tente excluir um colaborador que participe de agendamentos
2. Verifique se aparece mensagem sobre dependências
3. Confirme e verifique se o colaborador foi excluído

#### Teste 5: Excluir Empresa
1. Tente excluir uma empresa que tenha colaboradores
2. Verifique se aparece mensagem sobre dependências
3. Confirme e verifique se colaboradores foram excluídos

### 4. ✅ Verificação de Dependências

Teste a função SQL de verificação:

```sql
-- Substitua 'ID_AQUI' pelo ID real de um registro
SELECT * FROM verificar_dependencias_exclusao('agendamento', 'ID_AQUI');
SELECT * FROM verificar_dependencias_exclusao('modulo', 'ID_AQUI');
SELECT * FROM verificar_dependencias_exclusao('trilha', 'ID_AQUI');
SELECT * FROM verificar_dependencias_exclusao('colaborador', 'ID_AQUI');
SELECT * FROM verificar_dependencias_exclusao('empresa', 'ID_AQUI');
```

**Resultado esperado:**
- Função retorna lista de dependências encontradas
- Cada linha mostra tipo de dependência e quantidade

## 🔍 Problemas Comuns e Soluções

### Problema 1: Pesquisa não é criada ao salvar agendamento
**Solução:** Verifique se a migração SQL foi executada corretamente. A coluna `agendamento_id` deve existir.

### Problema 2: Botões de exclusão não aparecem
**Solução:** Limpe o cache do navegador (Ctrl+F5 ou Cmd+Shift+R) e recarregue a página.

### Problema 3: Erro ao excluir (violação de foreign key)
**Solução:** Verifique se as constraints CASCADE estão configuradas corretamente nas foreign keys.

### Problema 4: Pesquisa NPS não carrega via QR Code
**Solução:** Verifique se a pesquisa foi criada com `agendamento_id` correto. A página pesquisa-nps.html busca primeiro a pesquisa específica, depois a global.

## 📊 Consultas Úteis para Monitoramento

```sql
-- Ver todas as pesquisas vinculadas a agendamentos
SELECT 
    p.id,
    p.agendamento_id,
    p.pergunta1,
    p.ativo,
    a.qr_code,
    e.nome as empresa_nome,
    t.nome as trilha_nome,
    m.nome as modulo_nome
FROM neosul_pesquisa_nps p
LEFT JOIN neosul_treinamentos_agendamentos a ON p.agendamento_id = a.id
LEFT JOIN neosul_empresas e ON a.empresa_id = e.id
LEFT JOIN neosul_trilhas t ON a.trilha_id = t.id
LEFT JOIN neosul_modulos m ON a.modulo_id = m.id
ORDER BY p.created_at DESC;

-- Ver pesquisas globais
SELECT * FROM neosul_pesquisa_nps 
WHERE agendamento_id IS NULL 
ORDER BY created_at DESC;

-- Contar pesquisas por tipo
SELECT 
    CASE 
        WHEN agendamento_id IS NULL THEN 'Global'
        ELSE 'Específica'
    END as tipo,
    COUNT(*) as quantidade
FROM neosul_pesquisa_nps
WHERE ativo = true
GROUP BY tipo;
```

## ✅ Status Final

Após validar todos os itens acima, marque como concluído:

- [ ] Estrutura do banco validada
- [ ] Pesquisa NPS por agendamento funcionando
- [ ] Pesquisa via QR Code funcionando
- [ ] Pesquisa global funcionando
- [ ] Exclusão de agendamento funcionando
- [ ] Exclusão de módulo funcionando
- [ ] Exclusão de trilha funcionando
- [ ] Exclusão de colaborador funcionando
- [ ] Exclusão de empresa funcionando
- [ ] Verificação de dependências funcionando
