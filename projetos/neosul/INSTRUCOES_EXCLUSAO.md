# 🔧 Instruções: Funcionalidades de Exclusão e Pesquisa NPS

## 📋 Resumo das Alterações

### 1. Pesquisa NPS Vinculada ao Agendamento
- Cada agendamento agora tem sua própria pesquisa NPS
- Pesquisa é criada automaticamente ao salvar um agendamento
- QR Code continua funcionando, mas busca pesquisa específica do agendamento

### 2. Funcionalidades de Exclusão
- Botões de exclusão adicionados em todas as tabelas:
  - Agendamentos
  - Módulos
  - Trilhas
  - Colaboradores
  - Empresas
- Verificação automática de dependências antes de excluir
- Mensagens de alerta informando sobre dependências que serão excluídas

## 🔄 Passo a Passo

### 1. Executar Migração SQL
1. Acesse: https://supabase.com/dashboard/project/mgcoyeohqelystqmytah
2. Abra o **SQL Editor**
3. Execute o arquivo: `MODIFICAR_PESQUISA_NPS_VINCULAR_AGENDAMENTO.sql`
4. Verifique se a coluna `agendamento_id` foi adicionada:
   ```sql
   SELECT column_name, data_type, is_nullable
   FROM information_schema.columns 
   WHERE table_name = 'neosul_pesquisa_nps' 
   AND column_name = 'agendamento_id';
   ```

### 2. Testar Funcionalidades

#### Pesquisa NPS por Agendamento:
1. Crie um novo agendamento
2. Verifique se a pesquisa foi criada automaticamente vinculada ao agendamento
3. Acesse a pesquisa via QR Code e confirme que está funcionando

#### Exclusão:
1. Tente excluir um agendamento que tenha participantes
2. Verifique se a mensagem de dependências aparece corretamente
3. Confirme a exclusão e verifique se os dados relacionados foram excluídos (CASCADE)

## ⚠️ Observações Importantes

### Exclusões com CASCADE:
- **Agendamento**: Exclui automaticamente participantes e respostas NPS
- **Módulo**: Exclui automaticamente agendamentos e materiais relacionados
- **Trilha**: Exclui automaticamente módulos, vínculos e agendamentos
- **Empresa**: Exclui automaticamente colaboradores, vínculos e agendamentos
- **Colaborador**: Mantém participantes, mas remove vínculo

### Pesquisa NPS:
- Pesquisas antigas (sem `agendamento_id`) continuam funcionando como pesquisas globais
- Novos agendamentos criam pesquisas específicas automaticamente
- Se não houver pesquisa específica, o sistema busca pesquisa global (compatibilidade)

## 📝 Consultas SQL para Verificação

### Verificar dependências antes de excluir:
```sql
-- Ver dependências de um agendamento
SELECT * FROM verificar_dependencias_exclusao('agendamento', 'ID_DO_AGENDAMENTO');

-- Ver dependências de um módulo
SELECT * FROM verificar_dependencias_exclusao('modulo', 'ID_DO_MODULO');

-- Ver dependências de uma trilha
SELECT * FROM verificar_dependencias_exclusao('trilha', 'ID_DA_TRILHA');

-- Ver dependências de um colaborador
SELECT * FROM verificar_dependencias_exclusao('colaborador', 'ID_DO_COLABORADOR');

-- Ver dependências de uma empresa
SELECT * FROM verificar_dependencias_exclusao('empresa', 'ID_DA_EMPRESA');
```

### Verificar pesquisas vinculadas:
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
```

## ✅ Checklist de Validação

- [ ] Migração SQL executada com sucesso
- [ ] Coluna `agendamento_id` existe na tabela `neosul_pesquisa_nps`
- [ ] Função `verificar_dependencias_exclusao` criada no banco
- [ ] Botões de exclusão aparecem em todas as tabelas
- [ ] Mensagens de dependências aparecem corretamente
- [ ] Exclusões funcionam com CASCADE
- [ ] Pesquisa NPS é criada automaticamente ao salvar agendamento
- [ ] QR Code busca pesquisa específica do agendamento
- [ ] Pesquisa global continua funcionando (compatibilidade)
