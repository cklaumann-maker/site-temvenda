# 🚀 Guia de Deploy - Ajustes da Agenda

## ✅ Status Atual

- ✅ Migration SQL executada no Supabase (`006_store_expenses_and_purchase_types.sql`)
- ✅ Backend modificado (código Python)
- ⏳ Frontend ainda não foi atualizado (não precisa fazer upload ainda)

---

## 📤 Deploy do Backend (Render)

O backend está hospedado no **Render** e faz deploy automático via **Git Push**.

### Passos:

1. **Fazer commit das mudanças:**
```bash
cd backend
git add app/finance_service.py app/main.py app/schemas.py
git commit -m "feat: implementar ajustes da agenda - despesas de loja e compras a prazo"
git push
```

2. **Render fará deploy automaticamente:**
   - O Render detecta o push e inicia o deploy
   - Aguarde alguns minutos para o deploy completar
   - Verifique em: https://temvenda-finance-api.onrender.com/health

---

## 📋 Arquivos Modificados no Backend

### Arquivos que serão deployados automaticamente:
- ✅ `backend/app/finance_service.py`
- ✅ `backend/app/main.py`
- ✅ `backend/app/schemas.py`

### Migration SQL (já executada):
- ✅ `backend/migrations/006_store_expenses_and_purchase_types.sql`

---

## ⚠️ Frontend - NÃO Precisa Fazer Upload Ainda

O frontend (`caixa/index.html`) ainda **não foi atualizado** para usar as novas funcionalidades:
- ❌ Botão "Despesa de Loja" ainda não existe
- ❌ Modal de compras ainda não diferencia à vista vs a prazo
- ❌ Aba de consolidação mensal ainda não existe

**Portanto, NÃO precisa fazer upload via FTP do frontend ainda.**

---

## 🧪 Testar Backend Após Deploy

Após o deploy no Render, você pode testar os novos endpoints:

### 1. Testar criação de despesa de loja:
```bash
curl -X POST https://temvenda-finance-api.onrender.com/api/store-expenses \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-19",
    "amount": 100.00,
    "description": "Retirada de caixa",
    "category": "descontão",
    "expense_type": "retirada_caixa"
  }'
```

### 2. Testar listagem de despesas:
```bash
curl -X GET "https://temvenda-finance-api.onrender.com/api/store-expenses?month_code=12-25" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 3. Testar atualização de compras (com purchases_credit):
```bash
curl -X POST https://temvenda-finance-api.onrender.com/api/days/2025-12-19/management \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "purchases_planned": 500.00,
    "purchases_credit": 200.00,
    "future_in_confirmed": 0
  }'
```

---

## 📝 Próximos Passos (Frontend)

Quando for implementar o frontend, você precisará fazer upload via FTP de:
- `caixa/index.html` (após adicionar as novas funcionalidades)

Mas isso pode ser feito depois, quando as funcionalidades forem implementadas no frontend.

---

## ✅ Checklist de Deploy

- [x] Migration SQL executada no Supabase
- [ ] Git push do backend feito
- [ ] Render fez deploy automaticamente
- [ ] Backend testado (endpoints funcionando)
- [ ] Frontend atualizado (quando implementar)
- [ ] Upload do frontend via FTP (quando implementar)

---

## 🔍 Verificar Deploy

Após o git push, verifique:
1. **Render Dashboard:** https://dashboard.render.com
2. **Health Check:** https://temvenda-finance-api.onrender.com/health
3. **Logs do Render:** Verifique se não há erros no deploy

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs do Render
2. Teste os endpoints manualmente
3. Verifique se a migration foi executada corretamente no Supabase

