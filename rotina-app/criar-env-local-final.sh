#!/bin/bash

# Script para criar arquivo .env.local

cd "$(dirname "$0")"

ENV_FILE="apps/web/.env.local"

if [ -f "$ENV_FILE" ]; then
    echo "✅ Arquivo .env.local já existe!"
    echo ""
    echo "Conteúdo atual:"
    cat "$ENV_FILE"
else
    echo "📝 Criando arquivo .env.local..."
    
    cat > "$ENV_FILE" << 'EOF'
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://mgcoyeohqelystqmytah.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ

# Porta do servidor (padrão: 3001 para evitar conflitos)
PORT=3001
EOF

    echo "✅ Arquivo .env.local criado com sucesso!"
    echo ""
    echo "Conteúdo:"
    cat "$ENV_FILE"
fi

