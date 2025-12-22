# 🔧 Correção: CORS e Erro 500

## ✅ Correções Aplicadas

### 1. CORS Global
- ✅ Adicionado exception handlers globais para garantir CORS em todos os erros
- ✅ Headers CORS agora são sempre enviados, mesmo em erros 500

### 2. Tratamento de Erros Melhorado
- ✅ Endpoint `/api/admin/refresh` agora tem tratamento de erros detalhado
- ✅ Logs de erro para facilitar debug

---

## 🚀 Próximos Passos

### 1. Fazer Deploy no Render

Você precisa fazer commit e push das mudanças:

```bash
cd backend
git add app/main.py
git commit -m "fix: adicionar CORS em erros e melhorar tratamento de exceções"
git push
```

O Render vai fazer deploy automaticamente.

---

### 2. Verificar Variáveis de Ambiente no Render

Após o deploy, verifique se estas variáveis estão configuradas:

#### ✅ Obrigatórias:
- [ ] `DRIVE_FILE_ID` - ID do arquivo Excel no Google Drive
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` - Credenciais do Service Account (JSON em uma linha)
- [ ] `SUPABASE_URL` - Já configurado ✅
- [ ] `SUPABASE_SERVICE_ROLE_KEY` - Já configurado ✅
- [ ] `APP_PASSWORD` - Senha para login
- [ ] `JWT_SECRET_KEY` - Chave secreta para JWT

#### ⚠️ Opcionais (mas recomendadas):
- [ ] `FRONTEND_ORIGINS` - `https://www.temvenda.com.br` (para restringir CORS depois)
- [ ] `GOOGLE_PROJECTION_FILE_ID` - ID da planilha de projeção (se usar projeção D+60)

---

### 3. Verificar Logs do Render

Após fazer o deploy e tentar "Atualizar Fluxo" novamente:

1. Render Dashboard → Seu serviço → **Logs**
2. Procure por:
   - ✅ "Processando mês..." → funcionando
   - ❌ Erros sobre Google Drive → falta `DRIVE_FILE_ID` ou `GOOGLE_SERVICE_ACCOUNT_JSON`
   - ❌ Erros sobre Supabase → verificar `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY`

---

## 🔍 Diagnóstico de Erros Comuns

### Erro: "DRIVE_FILE_ID não configurado"
**Solução:** Adicione a variável `DRIVE_FILE_ID` no Render com o ID do arquivo do Google Drive.

### Erro: "GOOGLE_SERVICE_ACCOUNT_JSON não configurado"
**Solução:** 
1. Crie um Service Account no Google Cloud
2. Baixe o JSON
3. Converta para uma linha: `cat service_account.json | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), separators=(',', ':')))"`
4. Cole o resultado em `GOOGLE_SERVICE_ACCOUNT_JSON` no Render

### Erro: "Only files with binary content can be downloaded"
**Solução:** O arquivo é um Google Sheet. O código já trata isso automaticamente, mas verifique se o Service Account tem permissão de "Visualizador" no arquivo.

### Erro: "Aba DIST 12-25 não encontrada"
**Solução:** Verifique se o Excel tem abas com nomes no formato `DIST MM-AA` e `DESP MM-AA` (ex: `DIST 12-25`, `DESP 12-25`).

---

## 📋 Checklist Pós-Deploy

Após fazer o deploy:

- [ ] Render fez deploy com sucesso
- [ ] `/health` retorna `{"status":"ok","database":"ok"}`
- [ ] Login funciona
- [ ] "Atualizar Fluxo" não dá mais erro de CORS
- [ ] Se der erro 500, verificar logs do Render
- [ ] Dados aparecem na tabela após "Atualizar Fluxo"

---

## 🆘 Ainda Não Funciona?

Se após o deploy ainda houver problemas:

1. **Verificar logs do Render:**
   - Render Dashboard → Logs
   - Procurar por erros específicos

2. **Testar endpoint diretamente:**
   ```bash
   curl -X POST "https://temvenda-finance-api.onrender.com/api/admin/refresh?monthCode=12-25" \
     -H "Authorization: Bearer SEU_TOKEN_JWT"
   ```

3. **Verificar variáveis de ambiente:**
   - Render Dashboard → Environment
   - Confirmar que todas as variáveis obrigatórias estão configuradas

---

## 📝 Notas Técnicas

### CORS
- Agora todos os erros retornam com headers CORS
- `allow_origins=["*"]` permite todas as origens
- Para produção, pode restringir usando `FRONTEND_ORIGINS`

### Tratamento de Erros
- Exception handlers globais garantem que erros sempre retornem JSON com CORS
- Logs detalhados no console do Render para facilitar debug

