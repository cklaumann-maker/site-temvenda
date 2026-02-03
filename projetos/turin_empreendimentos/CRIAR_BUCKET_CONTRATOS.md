# Criar bucket `contratos` no Supabase Storage

Como a verificação mostrou **"Bucket contratos não encontrado"** e **"Buckets existentes: nenhum"**, siga estes passos no Supabase.

---

## Passo 1 — Criar o bucket (no Dashboard)

1. Acesse **https://app.supabase.com** e abra seu projeto.
2. No menu lateral, clique em **Storage**.
3. Clique em **New bucket**.
4. Preencha:
   - **Name:** `contratos` (exatamente assim, minúsculo).
   - **Public bucket:** marque **Sim** (para os links dos PDFs funcionarem sem login).
5. Clique em **Create bucket**.

---

## Passo 2 — Criar políticas do Storage (SQL Editor)

Sem políticas, o front não consegue fazer upload nem listar arquivos. No Supabase:

1. Vá em **SQL Editor** no menu lateral.
2. Clique em **New query**.
3. Cole o SQL abaixo e execute (**Run**).

```sql
-- Políticas do bucket contratos (upload, leitura, atualização, exclusão)
CREATE POLICY "Permitir upload de arquivos"
  ON storage.objects
  FOR INSERT
  TO public
  WITH CHECK (bucket_id = 'contratos');

CREATE POLICY "Permitir leitura de arquivos"
  ON storage.objects
  FOR SELECT
  TO public
  USING (bucket_id = 'contratos');

CREATE POLICY "Permitir atualização de arquivos"
  ON storage.objects
  FOR UPDATE
  TO public
  USING (bucket_id = 'contratos')
  WITH CHECK (bucket_id = 'contratos');

CREATE POLICY "Permitir exclusão de arquivos"
  ON storage.objects
  FOR DELETE
  TO public
  USING (bucket_id = 'contratos');
```

4. Confirme que apareceu **Success** (ou que as 4 políticas foram criadas).

---

## Passo 3 — Verificar de novo

1. Abra a página **`verificar-banco-projeto.html`** no navegador.
2. Clique em **Verificar agora**.
3. Em **Storage — bucket contratos** deve aparecer: **Bucket `contratos` existe** e a pasta do TURIN acessível.

Depois disso, o repositório de documentos da página TURIN (formalização, contrato, demais documentos) passa a conseguir enviar e listar arquivos.
