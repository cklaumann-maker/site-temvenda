# Solução para Erro de Conexão NEOSUL

## Problema Identificado

**Erro**: `TypeError: Failed to fetch`

**Causa**: O navegador está bloqueando as requisições ao Supabase. Isso acontece por:

1. **CORS (Cross-Origin Resource Sharing)** - Configuração do Supabase
2. **Mixed Content** - Requisições HTTP para HTTPS
3. **Extensões do navegador** bloqueando requisições

## Soluções (tente na ordem)

### Solução 1: Configurar CORS no Supabase ⭐ RECOMENDADO

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto: `site-temvenda`
3. Vá em **Settings** (⚙️) → **API**
4. Role até **"Configuration"**
5. Procure por:
   - **"Additional URLs"** ou
   - **"Allowed origins"** ou
   - **"Site URL"**
6. Adicione estas URLs (uma por linha ou separadas por vírgula):
   ```
   http://localhost:3000
   http://127.0.0.1:3000
   http://localhost:*
   ```
7. Salve as alterações
8. Aguarde 1-2 minutos para propagar
9. Teste novamente

### Solução 2: Desabilitar Extensões do Navegador

1. Abra o Chrome em **Modo Anônimo** (Cmd+Shift+N no Mac)
2. Acesse: `http://localhost:3000/projetos/neosul/teste-conexao.html`
3. Teste a conexão novamente

Se funcionar no modo anônimo, o problema é uma extensão.

**Extensões que costumam causar problema:**
- AdBlock / uBlock Origin
- Privacy Badger
- HTTPS Everywhere
- Qualquer VPN ou proxy

### Solução 3: Verificar Row Level Security (RLS)

O Supabase pode estar bloqueando acesso devido ao RLS:

1. Acesse: https://supabase.com/dashboard
2. Vá em **Authentication** → **Policies**
3. Selecione a tabela `neosul_usuarios`
4. Verifique se há políticas ativas

**Para testar**, você pode **temporariamente desabilitar RLS**:

No SQL Editor do Supabase, execute:

```sql
-- Desabilitar RLS temporariamente (APENAS PARA TESTE)
ALTER TABLE neosul_usuarios DISABLE ROW LEVEL SECURITY;
ALTER TABLE neosul_planejamento_mensal DISABLE ROW LEVEL SECURITY;
ALTER TABLE neosul_planejamento_semanal DISABLE ROW LEVEL SECURITY;
ALTER TABLE neosul_reunioes_semanais DISABLE ROW LEVEL SECURITY;
```

⚠️ **ATENÇÃO**: Isso deixa seus dados sem proteção. Use apenas para teste!

### Solução 4: Verificar se o Projeto Supabase está "Pausado"

1. Acesse: https://supabase.com/dashboard
2. Verifique o status do projeto
3. Se estiver "Paused", clique em "Resume"

### Solução 5: Usar Servidor HTTPS Local

O Supabase pode estar rejeitando requisições HTTP. Você pode:

1. Usar o Cloudflare Tunnel (gratuito)
2. Usar ngrok (gratuito)
3. Configurar certificado SSL local

**Opção mais simples - Cloudflare Tunnel:**

```bash
# Instalar (se não tiver)
brew install cloudflare/cloudflare/cloudflared

# Executar tunnel
cloudflared tunnel --url http://localhost:3000
```

Isso vai gerar uma URL HTTPS pública que você pode usar para testar.

### Solução 6: Verificar Network no DevTools

1. Abra o Chrome DevTools (F12)
2. Vá na aba **Network**
3. Tente fazer login
4. Procure pela requisição que falhou (linha vermelha)
5. Clique nela e veja:
   - **Headers** → Response Headers
   - **Preview** → Mensagem de erro
6. Me envie um screenshot ou copie o erro completo

## Teste Rápido: Verificar se é CORS

Abra o Console do DevTools (F12) e execute:

```javascript
fetch('https://yfiqwkjpxzqdsstzivfc.supabase.co/rest/v1/', {
  headers: {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlmaXF3a2pweHpxZHNzdHppdmZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc0MDI3MzcsImV4cCI6MjA1Mjk3ODczN30.kE0T_3bDFhtFPJRGq3pYy0KpzXRYOl8zQkHjdRF-kK4'
  }
})
.then(r => console.log('✅ Conexão OK', r.status))
.catch(e => console.error('❌ Erro:', e.message));
```

Se retornar "Conexão OK", o problema é no código.
Se retornar erro, é problema de rede/CORS.

## Solução Temporária: Modo Desenvolvimento sem Supabase

Se nenhuma solução acima funcionar imediatamente, posso criar uma versão do sistema que funciona com **localStorage** (dados salvos no navegador) para você testar a interface enquanto resolve o problema de conexão.

## Próximos Passos

1. **Comece pela Solução 1** (configurar CORS no Supabase)
2. Se não funcionar, tente **Solução 2** (modo anônimo)
3. Execute o **Teste Rápido** no console
4. Me informe os resultados

## Informações Úteis

- **URL do Projeto**: https://yfiqwkjpxzqdsstzivfc.supabase.co
- **Região**: Provavelmente US East (padrão)
- **Navegador**: Chrome 144 no Mac
- **Sistema**: macOS 10.15.7
