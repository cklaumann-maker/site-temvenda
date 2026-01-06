# ✅ Página Raiz Criada

## O que foi feito

Criei o arquivo `apps/web/src/app/page.tsx` que:

1. **Verifica se o usuário está autenticado**
2. **Redireciona automaticamente:**
   - Se **autenticado** → `/app/today`
   - Se **não autenticado** → `/login`

## Como funciona

A página raiz (`/`) agora funciona como um "hub" que direciona o usuário para o lugar certo:

```
localhost:3001/
  ↓
  Verifica autenticação
  ↓
  ├─ Autenticado → /app/today
  └─ Não autenticado → /login
```

## Teste agora

1. **Acesse:** http://localhost:3001
2. **Deve redirecionar para:** http://localhost:3001/login
3. **Após fazer login:** Será redirecionado para `/app/today`

---

## Se o servidor ainda estiver rodando

O Next.js deve detectar a mudança automaticamente (hot reload). Se não funcionar:

1. Pare o servidor (Ctrl+C)
2. Reinicie: `pnpm dev`
3. Acesse: http://localhost:3001

---

## Estrutura de rotas

Agora você tem:

- `/` → Redireciona para login ou app
- `/login` → Página de login
- `/app/today` → Página principal do usuário
- `/app/plan` → Plano de refeições
- `/app/dashboard` → Dashboard do usuário
- `/app/checkin` → Check-in diário
- `/admin/members` → Área admin (coaches/owners)







