# Instruções de Login - Área Administrativa FDF

## 📋 Status

✅ Página de login criada: `admin/login.html`  
✅ Sistema de autenticação: `admin/auth-fdf.js`  
✅ Dashboard básico: `admin/dashboard.html`

## 🔐 Como Gerar Hashes Bcrypt para Senhas

### Opção 1: Online (Rápido)
1. Acesse: https://bcrypt-generator.com/
2. Digite a senha desejada
3. Rounds: 10 (padrão)
4. Clique em "Generate Hash"
5. Copie o hash gerado (começa com `$2a$10$` ou `$2b$10$`)

### Opção 2: Node.js
```bash
npm install bcryptjs
node -e "const bcrypt = require('bcryptjs'); console.log(bcrypt.hashSync('sua_senha', 10));"
```

### Opção 3: Python
```bash
pip install bcrypt
python -c "import bcrypt; print(bcrypt.hashpw(b'sua_senha', bcrypt.gensalt(10)).decode())"
```

## 📝 Atualizar Senhas no Banco

Após gerar os hashes, execute no Supabase SQL Editor:

```sql
-- Atualizar senha do root
UPDATE public.fdf_usuarios_admin 
SET senha_hash = '$2a$10$SEU_HASH_AQUI' 
WHERE email = 'root@fdf.com';

-- Atualizar senha do Cesar
UPDATE public.fdf_usuarios_admin 
SET senha_hash = '$2a$10$SEU_HASH_AQUI' 
WHERE email = 'cesar@fdf.com';
```

## 🚀 Como Usar

1. Acesse: `projetos/feira-digital-farma/admin/login.html`
2. Use o email cadastrado no banco
3. Digite a senha
4. Clique em "Entrar"

## ⚠️ Nota Importante

- As senhas placeholder no banco (`$2a$10$placeholder_...`) **NÃO funcionam**
- Você **DEVE** gerar hashes bcrypt reais antes de fazer login
- Use uma das opções acima para gerar os hashes

## 🔧 Desenvolvimento/Teste

Para desenvolvimento inicial, o sistema permite senhas de teste:
- `Cesar*26` (para usuário Cesar)
- `root123` (para usuário root)

**IMPORTANTE:** Isso só funciona se o hash no banco contiver "placeholder". Em produção, sempre use hashes bcrypt reais.
