# 🚀 Push do rotina-app para GitHub

## Status Atual

- ✅ Git já está inicializado
- ✅ Remote configurado: `github.com/cklaumann-maker/site-temvenda.git`
- ✅ Branch: `main`
- ⚠️ Pasta `rotina-app/` ainda não está commitada

---

## 📋 Passos para Fazer Push

### Opção 1: Adicionar rotina-app ao repositório existente

```bash
cd /Users/cesark/site-temvenda/rotina-app

# Adicionar todos os arquivos do rotina-app
git add .

# Fazer commit
git commit -m "feat: adicionar aplicação Rotina App completa

- Sistema de controle de dieta e calorias
- Integração com Supabase
- Dashboard de calorias e aderência
- Sistema de check-in diário
- Gerenciamento de plano alimentar
- Perfil de usuário com IMC
- Deploy configurado para Vercel"

# Fazer push
git push origin main
```

### Opção 2: Criar repositório separado (Recomendado)

Se você quiser um repositório separado para o rotina-app:

```bash
cd /Users/cesark/site-temvenda/rotina-app

# Inicializar Git (se ainda não estiver)
git init

# Adicionar arquivos
git add .

# Commit inicial
git commit -m "feat: aplicação Rotina App - sistema completo de controle de dieta e calorias"

# Criar repositório no GitHub primeiro (via web)
# Depois adicionar remote:
git remote add origin https://github.com/seu-usuario/rotina-app.git
git branch -M main
git push -u origin main
```

---

## ⚠️ Arquivos que NÃO serão commitados

O `.gitignore` já está configurado para ignorar:
- `node_modules/`
- `.next/`
- `.env*` (arquivos de ambiente)
- Arquivos de build

---

## 🔒 Segurança

**IMPORTANTE**: Certifique-se de que arquivos sensíveis não sejam commitados:

- ✅ `.env.production` está no `.gitignore`
- ✅ Credenciais do Supabase devem estar apenas nas variáveis de ambiente do Vercel
- ✅ Não commite chaves de API ou senhas

---

## ✅ Após o Push

1. Acesse: https://github.com/cklaumann-maker/site-temvenda
2. Verifique se a pasta `rotina-app/` aparece
3. Configure deploy no Vercel usando o repositório

