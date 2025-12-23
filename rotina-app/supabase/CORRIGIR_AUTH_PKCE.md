# Correção do Erro PKCE na Autenticação

## Problema
Erro ao criar novo usuário: `PKCE code verifier not found in storage`

## Causa
O código verificador PKCE não está sendo armazenado corretamente em cookies, causando falha na autenticação quando o usuário clica no magic link.

## Soluções Implementadas

### 1. Cliente Supabase Configurado com Cookies ✅
- Arquivo: `apps/web/src/lib/supabase/client.ts`
- Configurado para usar cookies corretamente no navegador
- Decodifica/encoda valores corretamente

### 2. Melhor Tratamento de Erros ✅
- Arquivo: `apps/web/src/app/login/page.tsx`
- Exibe mensagens de erro mais detalhadas
- Botão para limpar cookies e tentar novamente

## Verificações Necessárias no Supabase Dashboard

### 1. URLs de Redirecionamento
Verifique se as seguintes URLs estão configuradas no Supabase Dashboard:

**Authentication > URL Configuration > Redirect URLs:**
- `http://localhost:3001/auth/callback`
- `https://seu-dominio.vercel.app/auth/callback`
- `https://*.vercel.app/auth/callback` (wildcard para previews)

### 2. Site URL
**Authentication > URL Configuration > Site URL:**
- Desenvolvimento: `http://localhost:3001`
- Produção: `https://seu-dominio.vercel.app`

### 3. Verificar Variáveis de Ambiente
Certifique-se de que as seguintes variáveis estão configuradas:

**No Vercel (Produção):**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_SITE_URL` (deve ser a URL do seu site)

**Local (.env.local):**
```env
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-chave-anon
NEXT_PUBLIC_SITE_URL=http://localhost:3001
```

## Solução Imediata para o Usuário

Se o erro persistir, o usuário pode:

1. **Limpar cookies do navegador:**
   - Abrir DevTools (F12)
   - Application > Cookies
   - Deletar todos os cookies relacionados ao Supabase (começam com `sb-`)

2. **Usar o botão na página de login:**
   - O botão "Limpar cookies e tentar novamente" foi adicionado
   - Limpa automaticamente os cookies do Supabase e recarrega a página

3. **Tentar em modo anônimo/privado:**
   - Abrir uma janela anônima
   - Tentar criar o usuário novamente

## Próximos Passos

1. ✅ Cliente configurado com cookies
2. ✅ Melhor tratamento de erros
3. ⏳ Verificar URLs no Supabase Dashboard
4. ⏳ Testar criação de novo usuário
5. ⏳ Se necessário, atualizar `@supabase/ssr` para versão mais recente

## Atualizar @supabase/ssr (Opcional)

Se o problema persistir, considere atualizar o pacote:

```bash
cd rotina-app/apps/web
pnpm update @supabase/ssr@latest
```

A versão atual é `^0.0.10`, mas versões mais recentes têm melhor suporte para PKCE.

