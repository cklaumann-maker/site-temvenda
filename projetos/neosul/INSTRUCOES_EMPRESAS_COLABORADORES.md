# Instruções para Criar Estrutura de Empresas e Colaboradores

## 📋 Passo a Passo

### 1. Execute o Script SQL
- Acesse: https://mgcoyeohqelystqmytah.supabase.co
- Vá em **SQL Editor** no menu lateral
- Abra o arquivo `CRIAR_ESTRUTURA_EMPRESAS_COLABORADORES.sql`
- Copie todo o conteúdo
- Cole no SQL Editor do Supabase
- Clique em **RUN** ou pressione `Ctrl+Enter`

### 2. O Script Criará:
- ✅ Tabela `neosul_empresas` - Empresas que receberão treinamentos
- ✅ Tabela `neosul_colaboradores` - Colaboradores vinculados às empresas
- ✅ Coluna `empresa_id` na tabela `neosul_cliente_trilhas`
- ✅ Coluna `empresa_id` na tabela `neosul_treinamentos_agendamentos`
- ✅ Coluna `colaborador_id` na tabela `neosul_treinamentos_participantes`

### 3. Verificação
Execute esta query para verificar:

```sql
SELECT 
    'Estrutura criada!' as status,
    (SELECT COUNT(*) FROM neosul_empresas) as total_empresas,
    (SELECT COUNT(*) FROM neosul_colaboradores) as total_colaboradores;
```

## 🎯 Nova Estrutura

### Hierarquia:
```
Empresa
  └─ Colaboradores (dentro da empresa)
      └─ Trilhas/Módulos (associados à empresa)
          └─ Participantes (colaboradores nos módulos)
```

### Fluxo de Uso:
1. **Cadastrar Empresa** → Aba "Empresas"
2. **Cadastrar Colaboradores** → Aba "Colaboradores" (filtrar por empresa)
3. **Vincular Trilha à Empresa** → Botão "Vincular Trilha" na empresa
4. **Agendar Módulo** → Selecionar empresa e incluir colaboradores

## ✅ Após Executar

Após executar o script com sucesso, você poderá:
- ✅ Cadastrar empresas completas (CNPJ, endereço, etc.)
- ✅ Cadastrar colaboradores vinculados a empresas
- ✅ Vincular trilhas e módulos às empresas
- ✅ Incluir colaboradores específicos nos módulos de treinamento
- ✅ Filtrar colaboradores por empresa

## 🔄 Migração de Dados Existentes

Se você já tinha clientes cadastrados, eles continuarão funcionando. A nova estrutura de empresas é complementar e permite uma organização mais estruturada.
