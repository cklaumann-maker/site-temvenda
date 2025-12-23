# Como Verificar e Configurar PKCE no Supabase

## Onde Procurar a Configuração de PKCE

Baseado na estrutura do menu Authentication que você mostrou, a configuração de PKCE pode estar em:

### 1. **URL Configuration** (Mais Provável)
- **Caminho**: Authentication > URL Configuration
- **O que procurar**: 
  - Opções relacionadas a "PKCE"
  - "Enable PKCE"
  - "Code Verifier"
  - Configurações de segurança de autenticação

### 2. **Sign In / Providers**
- **Caminho**: Authentication > Sign In / Providers
- **O que fazer**:
  - Clique em "Email" ou "Magic Link"
  - Verifique se há opções de segurança ou PKCE
  - Procure por "Enable PKCE" ou similar

### 3. **Attack Protection**
- **Caminho**: Authentication > Attack Protection
- **O que procurar**:
  - Configurações de segurança
  - Opções relacionadas a PKCE

### 4. **Sessions**
- **Caminho**: Authentication > Sessions
- **O que procurar**:
  - Configurações de sessão
  - Opções de segurança

## Se Não Encontrar a Opção

Se não encontrar uma opção explícita para desabilitar PKCE:

### Alternativa 1: Verificar via SQL
Execute no SQL Editor do Supabase:

```sql
-- Verificar configurações de autenticação
SELECT * FROM auth.config;
```

### Alternativa 2: Verificar na API
A configuração pode estar em:
- **Project Settings** > **API** > **Auth Settings**
- Ou em configurações avançadas

### Alternativa 3: Contatar Suporte
Se não encontrar, pode ser que:
- PKCE esteja sempre habilitado na sua versão do Supabase
- A configuração esteja em outro lugar
- Seja necessário usar uma abordagem diferente

## Solução Alternativa: Usar Senha

Se não conseguir desabilitar PKCE, considere:
1. Solicitar criação de senha durante cadastro
2. Usar `signUp` com senha em vez de apenas magic link
3. Isso evita completamente o problema PKCE

## Verificar Versão do Supabase

A configuração pode variar conforme a versão:
- Versões mais antigas podem não ter PKCE habilitado por padrão
- Versões mais recentes podem ter PKCE sempre habilitado

