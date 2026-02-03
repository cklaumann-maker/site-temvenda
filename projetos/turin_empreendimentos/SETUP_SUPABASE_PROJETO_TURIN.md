# Setup Supabase — Projeto TURIN (Repositório de Documentos e Registro)

Execute no **SQL Editor** do seu projeto Supabase para criar as tabelas e políticas necessárias ao repositório de documentos e ao registro de atividades do projeto.

## 1. Tabela de documentos do projeto

```sql
-- Documentos anexados por projeto (formalização, contrato, outros)
CREATE TABLE IF NOT EXISTS projeto_documentos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_slug TEXT NOT NULL,
  document_type TEXT NOT NULL CHECK (document_type IN ('formalizacao', 'contrato', 'outro')),
  file_name TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  file_size BIGINT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_projeto_documentos_project_slug ON projeto_documentos(project_slug);
CREATE INDEX IF NOT EXISTS idx_projeto_documentos_type ON projeto_documentos(project_slug, document_type);
CREATE INDEX IF NOT EXISTS idx_projeto_documentos_created ON projeto_documentos(created_at DESC);

ALTER TABLE projeto_documentos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir leitura projeto_documentos"
  ON projeto_documentos FOR SELECT USING (true);

CREATE POLICY "Permitir insert projeto_documentos"
  ON projeto_documentos FOR INSERT WITH CHECK (true);

CREATE POLICY "Permitir delete projeto_documentos"
  ON projeto_documentos FOR DELETE USING (true);
```

## 2. Tabela de registro de atividades do projeto

```sql
-- Registro de tudo que é realizado no projeto (snapshots, eventos)
CREATE TABLE IF NOT EXISTS projeto_registro (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_slug TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_projeto_registro_project ON projeto_registro(project_slug);
CREATE INDEX IF NOT EXISTS idx_projeto_registro_created ON projeto_registro(created_at DESC);

ALTER TABLE projeto_registro ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir leitura projeto_registro"
  ON projeto_registro FOR SELECT USING (true);

CREATE POLICY "Permitir insert projeto_registro"
  ON projeto_registro FOR INSERT WITH CHECK (true);
```

## 3. Storage — usar o bucket existente `contratos`

**Não é preciso criar novo bucket.** O projeto TURIN usa o **mesmo bucket** que a Governança Comercial já usa.

| Item | Configuração |
|------|----------------|
| **Bucket** | `contratos` (já existente no projeto) |
| **Onde ver** | Supabase Dashboard → **Storage** → bucket `contratos` |
| **Políticas** | As mesmas do `SETUP_SUPABASE_CONTRATOS.md` (INSERT/SELECT/UPDATE/DELETE para `bucket_id = 'contratos'`) já permitem qualquer pasta dentro do bucket. |

Os arquivos do TURIN são salvos no caminho:

`projetos/turin_empreendimentos/{tipo}/`

Exemplos:
- `projetos/turin_empreendimentos/formalizacao/`
- `projetos/turin_empreendimentos/contrato/`
- `projetos/turin_empreendimentos/outro/`

**Se você já configurou o Supabase para a página de Governança Comercial** (bucket `contratos` + políticas do `SETUP_SUPABASE_CONTRATOS.md`), **não precisa fazer nada no Storage** para o TURIN: o mesmo bucket e as mesmas políticas já servem.

**Se ainda não tiver o bucket `contratos`:** crie-o e aplique as políticas conforme o arquivo **`SETUP_SUPABASE_CONTRATOS.md`** (seção 1 e 3). Depois disso, o TURIN passa a usar esse bucket automaticamente.

**Usar um bucket que já existe:** abra **`verificar-banco-projeto.html`** e clique em **Verificar agora**. A seção **Storage — buckets do seu projeto** mostra todos os buckets do Supabase. Anote o nome do bucket que quiser usar e, no arquivo **`index.html`** do TURIN, altere a linha onde está `const STORAGE_BUCKET = 'contratos';` para o nome desse bucket (ex.: `const STORAGE_BUCKET = 'meu-bucket';`). As políticas do bucket precisam permitir INSERT e SELECT para o front poder enviar e listar arquivos.

## 4. Verificar se as tabelas existem

**Opção A — No navegador:**  
Abra a página `verificar-banco-projeto.html` (na mesma pasta do projeto TURIN) e clique em **Verificar agora**. Ela mostra se as tabelas existem e quantos registros têm.

**Opção B — No Supabase (SQL Editor):**  
Execute o SQL abaixo. Se as tabelas existirem, você verá a contagem de linhas; se não existirem, aparecerá erro.

```sql
-- Verificar se as tabelas existem e contar registros
SELECT 'projeto_documentos' AS tabela, COUNT(*) AS total FROM projeto_documentos
UNION ALL
SELECT 'projeto_registro', COUNT(*) FROM projeto_registro;
```

Se aparecer erro do tipo *relation "projeto_documentos" does not exist*, execute o SQL da seção 1 e 2 deste arquivo para criar as tabelas.

---

## 5. Configuração na página

A página usa o mesmo `supabase-config.js` do site (URL e anon key). Certifique-se de que o arquivo existe na raiz do site e está acessível em relação à página do projeto (ex.: `../../supabase-config.js`).

## 6. O que fica armazenado

- **projeto_documentos:** cada anexo (PDF, etc.) com tipo (formalização da proposta, contrato, outros). O arquivo fica no Storage e o registro na tabela.
- **projeto_registro:** snapshots da formalização (plano selecionado, sponsor, periodicidade, alocação, fases, metodologia) ao imprimir/gerar PDF e ao anexar documentos, para não perder nenhuma informação do que foi realizado no projeto.
