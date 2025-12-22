# Criar Arquivo .env.local

O arquivo `.env.local` está protegido pelo sistema. Você precisa criá-lo manualmente.

## Opção 1: Executar Script (Recomendado)

```bash
cd rotina-app
./criar-env-local.sh
```

## Opção 2: Criar Manualmente

Execute este comando:

```bash
cd rotina-app
cp apps/web/env.local.CONFIGURAR apps/web/.env.local
```

## Opção 3: Criar Manualmente no Editor

Crie o arquivo `apps/web/.env.local` com este conteúdo:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://mgcoyeohqelystqmytah.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ

# Porta do servidor (padrão: 3001 para evitar conflitos)
PORT=3001
```

## Verificar se foi criado

```bash
cat apps/web/.env.local
```

Deve mostrar as 3 variáveis de ambiente acima.

