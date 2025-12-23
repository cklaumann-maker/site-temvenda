# Como Desabilitar PKCE para Magic Links no Supabase

## Problema
O erro PKCE ocorre porque o código verificador não está disponível quando o usuário clica no link do email. Isso é um problema conhecido com magic links em SSR frameworks.

## Solução: Desabilitar PKCE no Supabase Dashboard

### Passo 1: Acessar Configurações de Autenticação
1. Acesse o [Supabase Dashboard](https://supabase.com/dashboard)
2. Selecione seu projeto
3. Vá em **Authentication** (menu lateral esquerdo)

### Passo 2: Localizar Configuração de PKCE

**⚠️ IMPORTANTE**: A configuração de PKCE pode não estar visível diretamente. Siga estes passos:

#### Opção A: Configurações do Provider Email (PRIMEIRO PASSO)
1. Na tela **Sign In / Providers**, clique na **seta (→)** ao lado de **"Email"**
2. Isso abrirá as configurações específicas do Email
3. Procure por:
   - **"Enable PKCE"**
   - **"PKCE"**
   - **"Code Verifier"**
   - Configurações de segurança
4. Se encontrar, **desabilite** a opção PKCE

#### Opção B: URL Configuration
1. No menu **Authentication**, clique em **URL Configuration**
2. Procure por uma opção relacionada a **PKCE** ou **Code Verifier**
3. Se encontrar, desabilite

#### Opção C: Attack Protection
1. No menu **Authentication**, clique em **Attack Protection**
2. Verifique se há configurações relacionadas a PKCE
3. Se encontrar, ajuste conforme necessário

#### Opção D: Se NÃO encontrar a opção
Se não houver opção para desabilitar PKCE, isso significa que:
- PKCE pode estar sempre habilitado na sua versão do Supabase
- A solução será ajustar o código para funcionar com PKCE habilitado
- Veja a seção "Solução Alternativa" abaixo

### Passo 3: Testar
Após desabilitar, teste novamente o fluxo de magic link.

## ⚠️ Considerações de Segurança

**Desabilitar PKCE reduz a segurança**, mas:
- Magic links já são seguros por natureza (link único, expiração)
- O código de autenticação é enviado por email seguro
- Apenas o dono do email pode acessar o link

**Recomendação**: 
- Para produção, considere manter PKCE habilitado e orientar usuários a clicar no link no mesmo navegador
- Para desenvolvimento/testes, pode desabilitar temporariamente

## Alternativa: Usar Senha em vez de Magic Link

Se PKCE continuar causando problemas, considere:
1. Solicitar criação de senha durante cadastro
2. Usar `signUp` com senha em vez de `signInWithOtp`
3. Isso evita completamente o problema PKCE

## Verificar se PKCE está Habilitado

Execute no SQL Editor do Supabase:

```sql
-- Verificar configurações de autenticação
SELECT * FROM auth.config;
```

Ou verifique no Dashboard: **Authentication** > **Settings** > **PKCE**

