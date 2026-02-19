# 🔐 Logins e Senhas - Área Administrativa FDF

## 📋 Credenciais de Acesso

### 1. Usuário ROOT (Acesso Total)
- **Login:** `root`
- **Senha:** `root*26`
- **Tipo:** Root (acesso total a tudo)
- **Permissões:** Todas

### 2. Usuário CESAR (Admin)
- **Login:** `cesar`
- **Senha:** `cesar*26`
- **Tipo:** Admin
- **Permissões:**
  - ✅ Gerenciar indústrias
  - ✅ Gerenciar distribuidoras
  - ✅ Gerenciar corporativos
  - ✅ Gerenciar participantes
  - ✅ Gerenciar cotas
  - ✅ Gerenciar CNPJs
  - ✅ Visualizar dashboard
  - ✅ Exportar dados

## ⚠️ IMPORTANTE

**Antes de fazer login, você DEVE:**

1. **Gerar hashes bcrypt** para as senhas:
   - Acesse: https://bcrypt-generator.com/
   - Gere hash para `cesar*26`
   - Gere hash para `root*26`

2. **Executar o SQL** `ATUALIZAR_LOGINS_SENHAS.sql`:
   - Substitua `SEU_HASH_CEASR_AQUI` pelo hash de `cesar*26`
   - Substitua `SEU_HASH_ROOT_AQUI` pelo hash de `root*26`
   - Execute no Supabase SQL Editor

3. **Testar o login**:
   - Acesse: `projetos/feira-digital-farma/admin/login.html`
   - Use: `cesar` / `cesar*26` ou `root` / `root*26`

## 🔧 Desenvolvimento Temporário

Se você ainda não gerou os hashes bcrypt, o sistema permite login temporário apenas se os hashes no banco contiverem "placeholder":
- `cesar` / `cesar*26`
- `root` / `root*26`

**Isso é apenas para desenvolvimento. Em produção, sempre use hashes bcrypt reais!**
