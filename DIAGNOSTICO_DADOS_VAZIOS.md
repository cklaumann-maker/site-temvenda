# 🔍 Diagnóstico: "Days array: 0 dias"

## ✅ Situação Atual

O sistema está funcionando corretamente! O problema é que **não há dados no banco de dados** para o mês `12-25`.

Isso é **normal** no primeiro uso. Você precisa **importar os dados do Google Drive** primeiro.

---

## 🚀 Solução: Importar Dados

### Passo 1: Verificar Configuração

Certifique-se de que estas variáveis estão no `backend/.env`:

```env
DRIVE_FILE_ID=id-do-arquivo-excel-no-google-drive
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

### Passo 2: Fazer Login no Frontend

1. Acesse `http://localhost:8000/caixa/`
2. Digite a senha configurada em `APP_PASSWORD`
3. Clique em "Entrar"

### Passo 3: Atualizar o Fluxo

1. No campo "Mês", digite: `12-25` (ou o mês que você quer importar)
2. Clique no botão **"🔄 Atualizar Fluxo"**
3. Aguarde alguns segundos
4. O sistema vai:
   - ✅ Baixar o Excel do Google Drive
   - ✅ Processar os dados
   - ✅ Salvar no banco de dados
   - ✅ Carregar automaticamente

### Passo 4: Verificar Dados

Após o "Atualizar Fluxo", você deve ver:
- ✅ Tabela com os dias do mês
- ✅ Dados de entradas e saídas
- ✅ Saldos calculados

---

## 🔍 Se "Atualizar Fluxo" Der Erro

### Erro: "DRIVE_FILE_ID não configurado"

**Solução:**
1. Adicione no `backend/.env`:
   ```env
   DRIVE_FILE_ID=seu-id-aqui
   ```
2. Reinicie o backend

### Erro: "Credenciais de service account não configuradas"

**Solução:**
1. Converta o JSON do Service Account para uma linha:
   ```bash
   cat backend/service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))"
   ```
2. Adicione no `backend/.env`:
   ```env
   GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
   ```
3. Reinicie o backend

### Erro: "Aba DIST 12-25 não encontrada"

**Solução:**
- Verifique se o Excel tem abas com nomes no formato `DIST MM-AA` e `DESP MM-AA`
- Exemplo: `DIST 12-25`, `DESP 12-25`

### Erro: "Only files with binary content can be downloaded"

**Solução:**
- O arquivo é um Google Sheet (não um arquivo .xlsx)
- O código já trata isso automaticamente
- Verifique se o Service Account tem permissão de "Visualizador" no arquivo

---

## 🧪 Testar via cURL (Debug)

Se quiser testar diretamente via terminal:

```bash
# 1. Fazer login
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"sua-senha-aqui"}')

# 2. Extrair token
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 3. Testar refresh
curl -X POST "http://localhost:8001/api/admin/refresh?monthCode=12-25" \
  -H "Authorization: Bearer $TOKEN" \
  -v
```

---

## 📋 Checklist

- [ ] Backend rodando em `http://localhost:8001`
- [ ] `/health` retorna `{"status":"ok","database":"ok"}`
- [ ] `DRIVE_FILE_ID` configurado no `backend/.env`
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` configurado no `backend/.env`
- [ ] Service Account tem permissão no arquivo do Google Drive
- [ ] Login funciona no frontend
- [ ] "Atualizar Fluxo" funciona sem erros
- [ ] Dados aparecem na tabela após refresh

---

## 💡 Dica

Se você já tem dados no Excel do Google Drive:
1. Certifique-se de que o `DRIVE_FILE_ID` está correto
2. Certifique-se de que o Service Account tem acesso ao arquivo
3. Clique em "Atualizar Fluxo"
4. Os dados serão importados automaticamente!

---

## 🆘 Ainda Não Funciona?

Se após clicar em "Atualizar Fluxo" ainda não aparecer dados:

1. **Verificar logs do backend:**
   - Terminal onde o backend está rodando
   - Procurar por erros relacionados a Google Drive

2. **Verificar permissões do Service Account:**
   - O Service Account precisa ter acesso de "Visualizador" no arquivo do Google Drive

3. **Verificar formato do Excel:**
   - Abas devem ter nomes: `DIST MM-AA` e `DESP MM-AA`
   - Colunas: `Vencimento`, `Valor`, `Valor pago`

