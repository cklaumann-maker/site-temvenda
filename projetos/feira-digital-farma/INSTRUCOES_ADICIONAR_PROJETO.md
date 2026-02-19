# Como Adicionar Feira Digital Farma à Lista de Projetos

Para que a Feira Digital Farma apareça na área administrativa do TEM VENDA, você precisa adicioná-la à tabela `projetos` no Supabase.

## 📋 Passo a Passo

### Opção 1: Adicionar apenas este projeto (Recomendado)

1. Acesse o **Supabase Dashboard**
2. Vá em **SQL Editor** → **New query**
3. Copie e cole o conteúdo do arquivo `ADICIONAR_PROJETO_SUPABASE.sql`
4. Clique em **Run** (ou pressione `Ctrl+Enter`)

### Opção 2: Via Supabase MCP (se disponível)

Se você tiver acesso ao MCP do Supabase, pode executar diretamente:

```sql
INSERT INTO public.projetos (nome, status, acesso, ordem) VALUES
    ('Feira Digital Farma', 'ativo', 'feira-digital-farma/', 6)
ON CONFLICT (acesso) DO UPDATE SET
    nome = EXCLUDED.nome,
    status = EXCLUDED.status,
    ordem = EXCLUDED.ordem,
    updated_at = now();
```

## ✅ Verificação

Após executar o SQL, verifique:

1. Acesse a área administrativa: `/app/` → aba "Projetos"
2. O projeto "Feira Digital Farma" deve aparecer na lista
3. O status deve estar como "Ativo"
4. O link de acesso deve apontar para `/projetos/feira-digital-farma/`

## 📝 Detalhes do Projeto

- **Nome:** Feira Digital Farma
- **Status:** ativo (pode ser alterado na área admin)
- **Acesso:** feira-digital-farma/
- **Ordem:** 6 (aparecerá após os outros projetos)

## 🔧 Alterar Status

Você pode alterar o status do projeto diretamente na área administrativa:
- **Ativo:** Projeto visível na lista pública
- **Aguardando:** Projeto em preparação
- **Inativo:** Projeto oculto da lista pública
