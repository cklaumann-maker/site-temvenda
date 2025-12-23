# Solução Final para Erro PKCE

## Problema
Erro persistente: `PKCE code verifier not found in storage` mesmo após limpar cache.

## Causa Raiz
A versão do `@supabase/ssr` estava muito desatualizada (`^0.0.10`) e não tinha suporte adequado para PKCE com cookies.

## Soluções Implementadas

### 1. Atualização do @supabase/ssr ✅
- **Arquivo**: `apps/web/package.json`
- **Mudança**: `^0.0.10` → `^0.5.1`
- **Ação necessária**: Execute `pnpm install` na raiz do projeto

### 2. Callback Route Corrigido ✅
- **Arquivo**: `apps/web/src/app/auth/callback/route.ts`
- **Mudanças**:
  - Usa `NextRequest` em vez de `Request`
  - Cria cliente do servidor diretamente no callback
  - Garante que cookies sejam passados na resposta
  - Configura cookies com `httpOnly`, `sameSite: 'lax'` e `secure` em produção

### 3. Cliente do Navegador ✅
- **Arquivo**: `apps/web/src/lib/supabase/client.ts`
- **Status**: Já configurado corretamente com cookies

## Passos para Resolver

### 1. Instalar Dependências Atualizadas
```bash
cd rotina-app
pnpm install
```

### 2. Verificar URLs no Supabase Dashboard
✅ Já configuradas corretamente:
- Site URL: `https://rotina-five.vercel.app`
- Redirect URLs: Todas as URLs necessárias estão configuradas

### 3. Testar Novamente
1. Limpar cookies do navegador (ou usar modo anônimo)
2. Tentar criar novo usuário
3. Verificar se o magic link funciona

## Verificações Adicionais

### Variáveis de Ambiente no Vercel
Certifique-se de que estão configuradas:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_SITE_URL` (deve ser `https://rotina-five.vercel.app`)

### Cookies no Navegador
Após o login, verifique se os seguintes cookies são criados:
- `sb-<project-ref>-auth-token`
- `sb-<project-ref>-auth-token.0` (se muito grande)
- Cookies relacionados ao PKCE (geralmente começam com `sb-`)

## Se o Problema Persistir

### Opção 1: Verificar Logs do Supabase
1. Vá para Authentication > Logs no Supabase Dashboard
2. Verifique se há erros relacionados ao PKCE

### Opção 2: Testar em Modo de Desenvolvimento
```bash
cd rotina-app
pnpm dev
```
Acesse `http://localhost:3001` e teste o fluxo completo.

### Opção 3: Verificar Configuração do Supabase
No Supabase Dashboard:
1. Authentication > Settings
2. Verifique se "Enable PKCE" está habilitado (deve estar)
3. Verifique se "Enable email confirmations" está configurado corretamente

## Notas Técnicas

### Por que PKCE é necessário?
PKCE (Proof Key for Code Exchange) é um protocolo de segurança que previne ataques de interceptação de código de autorização. É especialmente importante para aplicações públicas (SPAs).

### Como funciona com Next.js SSR?
1. Cliente inicia o fluxo de autenticação (`signInWithOtp`)
2. Código verificador PKCE é armazenado em cookie
3. Usuário clica no magic link
4. Callback route troca o código pela sessão usando o código verificador do cookie
5. Sessão é armazenada em cookie seguro

### Por que a versão antiga não funcionava?
A versão `0.0.10` do `@supabase/ssr` tinha bugs conhecidos com PKCE e não armazenava o código verificador corretamente em cookies para frameworks SSR.

