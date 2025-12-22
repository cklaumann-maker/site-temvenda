# 🚀 Primeiro Uso - Módulo Financeiro

## ✅ Status Atual

O sistema está **funcionando corretamente**! 

O que você está vendo:
- ✅ Página carrega
- ✅ Login funciona
- ✅ Conexão com API OK
- ⚠️ **Nenhum dado no banco** (normal no primeiro uso)

---

## 📋 Passo a Passo: Carregar Dados

### 1. Fazer Login

1. Acesse: `https://www.temvenda.com.br/caixa/`
2. Digite a senha configurada em `APP_PASSWORD` no Render
3. Clique em **"Entrar"**

---

### 2. Selecionar o Mês

1. No topo da página, há um seletor de mês
2. Selecione o mês que você quer carregar
   - Formato: `MM-AA` (ex: `12-25` para dezembro 2025)
   - Ou use o mês atual

---

### 3. Atualizar o Fluxo (Importar do Google Drive)

1. Clique no botão **"🔄 Atualizar Fluxo"**
2. Aguarde alguns segundos
3. O sistema vai:
   - ✅ Baixar o Excel do Google Drive
   - ✅ Processar os dados
   - ✅ Salvar no banco de dados
   - ✅ Carregar automaticamente

---

### 4. Verificar Dados Carregados

Após o "Atualizar Fluxo", você deve ver:
- ✅ Tabela com os dias do mês
- ✅ Dados de entradas e saídas
- ✅ Saldos calculados

---

## ⚠️ Importante: Variáveis Necessárias

Para o "Atualizar Fluxo" funcionar, você precisa ter configurado no Render:

- ✅ `DRIVE_FILE_ID` - ID do arquivo Excel no Google Drive
- ✅ `GOOGLE_SERVICE_ACCOUNT_JSON` - Credenciais do Service Account
- ✅ `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` - Já configurados ✅

---

## 🔍 Verificar se Está Tudo Configurado

### Teste 1: Verificar Variáveis no Render

No Render Dashboard → Environment, verifique:
- [ ] `DRIVE_FILE_ID` configurado
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` configurado
- [ ] `SUPABASE_URL` configurado ✅
- [ ] `SUPABASE_SERVICE_ROLE_KEY` configurado ✅

### Teste 2: Verificar Logs do Render

1. Render Dashboard → Seu serviço → **Logs**
2. Clique em "Atualizar Fluxo"
3. Veja os logs:
   - ✅ Se aparecer "Processando mês..." → está funcionando
   - ❌ Se aparecer erro sobre Google Drive → falta configurar `DRIVE_FILE_ID` ou `GOOGLE_SERVICE_ACCOUNT_JSON`

---

## ❌ Problemas Comuns

### Problema: "Nenhum dado encontrado" após atualizar

**Possíveis causas:**

1. **Excel não encontrado no Google Drive:**
   - Verificar se `DRIVE_FILE_ID` está correto
   - Verificar se o Service Account tem permissão no arquivo

2. **Mês não existe no Excel:**
   - O Excel precisa ter abas com nomes: `DIST 12-25` e `DESP 12-25`
   - Verificar se o formato do nome da aba está correto

3. **Erro ao processar Excel:**
   - Verificar logs do Render
   - Verificar se as colunas do Excel estão corretas

---

## ✅ Checklist de Primeiro Uso

- [ ] Login funcionando
- [ ] Mês selecionado
- [ ] Botão "Atualizar Fluxo" clicado
- [ ] Aguardou processamento
- [ ] Dados apareceram na tabela

---

## 🎯 Próximos Passos

Após carregar os dados:

1. **Verificar dados:** Confira se os valores estão corretos
2. **Registrar entradas:** Use o botão "💰 Entradas do Dia"
3. **Registrar compras:** Use o botão "🛒 Compras do Dia"
4. **Ver despesas:** Clique em um dia para ver detalhes
5. **Gerenciar dívidas:** Use a aba "Dívidas Antigas"

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

1. **Verificar logs do Render:**
   - Render Dashboard → Logs
   - Procurar por erros relacionados a Google Drive

2. **Verificar permissões do Service Account:**
   - O Service Account precisa ter acesso de "Visualizador" no arquivo do Google Drive

3. **Verificar formato do Excel:**
   - Abas devem ter nomes: `DIST MM-AA` e `DESP MM-AA`
   - Colunas: `Vencimento`, `Valor`, `Valor pago`

