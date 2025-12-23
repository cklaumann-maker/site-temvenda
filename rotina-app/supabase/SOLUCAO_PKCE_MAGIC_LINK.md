# Solução para Problema PKCE com Magic Links

## Problema
O erro "PKCE code verifier not found" ocorre quando o usuário clica no link do email porque o código verificador não está disponível no contexto onde o callback é executado.

## Causa Raiz
1. O código verificador PKCE é gerado e armazenado em cookies quando `signInWithOtp` é chamado
2. Quando o usuário clica no link do email, o callback é executado no servidor
3. Se o usuário clicou em outro navegador/dispositivo ou limpou cookies, o código verificador não está disponível

## Soluções Implementadas

### 1. Logs de Debug ✅
- Adicionados logs no cliente para verificar criação de cookies
- Adicionados logs no servidor para verificar leitura de cookies
- Isso ajuda a diagnosticar onde o problema está ocorrendo

### 2. Configuração de Cookies ✅
- Cookies com `maxAge` de 1 hora
- `path: '/'` para garantir acesso global
- `sameSite: 'lax'` para compatibilidade
- `secure` em produção

## Próximos Passos

### Opção 1: Verificar Logs (Após Deploy)
1. Acesse os logs do Vercel após tentar criar usuário
2. Verifique se os cookies estão sendo criados no cliente
3. Verifique se os cookies estão sendo lidos no servidor
4. Isso ajudará a identificar onde está o problema

### Opção 2: Desabilitar PKCE para Magic Links (Se necessário)
Se o problema persistir, podemos tentar desabilitar PKCE para magic links:

```typescript
// No Supabase Dashboard > Authentication > Settings
// Desabilitar "Enable PKCE" temporariamente para testar
```

**⚠️ AVISO:** Desabilitar PKCE reduz a segurança, mas magic links já são seguros por natureza.

### Opção 3: Usar Senha em vez de Magic Link
Para novos usuários, podemos:
1. Solicitar criação de senha durante o cadastro
2. Usar `signUp` com senha em vez de `signInWithOtp`
3. Isso evita completamente o problema PKCE

## Verificações Necessárias

### No Supabase Dashboard
1. **Authentication > URL Configuration**
   - Verificar se `https://rotina-five.vercel.app/auth/callback` está nas Redirect URLs
   - Verificar se Site URL está correto

2. **Authentication > Settings**
   - Verificar configuração de PKCE
   - Verificar tempo de expiração de magic links (padrão: 1 hora)

### No Código
1. Verificar se `NEXT_PUBLIC_SITE_URL` está configurada no Vercel
2. Verificar se cookies estão sendo criados corretamente (logs)
3. Verificar se cookies estão sendo lidos corretamente (logs)

## Teste Após Deploy

1. Abrir DevTools > Console
2. Solicitar magic link
3. Verificar logs: "Magic link enviado. Cookies atuais: ..."
4. Clicar no link do email
5. Verificar logs do servidor no Vercel
6. Verificar se cookies PKCE estão presentes

## Solução Temporária

Se o problema persistir, oriente os usuários a:
1. Solicitar o magic link
2. **Clicar no link imediatamente** (não esperar)
3. **Usar o mesmo navegador** onde solicitou
4. **Não limpar cookies** entre solicitar e clicar

Isso garante que os cookies PKCE estejam disponíveis quando o callback for executado.

