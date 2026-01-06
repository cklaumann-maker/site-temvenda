# Configuração do Vercel para Monorepo

## Problema
O Vercel não está encontrando os packages compartilhados (`@rotina/shared` e `@rotina/ui`) porque precisa construí-los antes do app web.

## Solução

### Opção 1: Configurar no Dashboard do Vercel (Recomendado)

1. Acesse o projeto no Vercel Dashboard
2. Vá em **Settings** > **General**
3. Configure:
   - **Root Directory**: `rotina-app`
   - **Build Command**: `pnpm install && pnpm --filter @rotina/shared build && pnpm --filter @rotina/ui build && pnpm --filter web build`
   - **Output Directory**: `apps/web/.next`
   - **Install Command**: `pnpm install`
   - **Framework Preset**: Next.js

### Opção 2: Usar vercel.json (já configurado)

O arquivo `rotina-app/vercel.json` já está configurado corretamente. Certifique-se de que o projeto no Vercel está apontando para a pasta `rotina-app` como root directory.

## Variáveis de Ambiente

Certifique-se de adicionar estas variáveis no Vercel:

```
NEXT_PUBLIC_SUPABASE_URL=https://mgcoyeohqelystqmytah.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ
```

## Próximos Passos

1. Configure o **Root Directory** no Vercel Dashboard para `rotina-app`
2. Adicione as variáveis de ambiente
3. Faça um novo deploy







