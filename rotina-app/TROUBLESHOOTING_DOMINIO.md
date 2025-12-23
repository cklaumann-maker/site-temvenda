# 🔧 Troubleshooting: Erro ERR_CONNECTION_CLOSED

## Problema
O link está correto (`https://rotina.temvenda.com.br`) mas dá erro:
```
ERR_CONNECTION_CLOSED
rotina.temvenda.com.br encerrou a conexão inesperadamente
```

---

## ✅ Verificações Necessárias

### 1. Verificar se o Domínio Está Configurado no Vercel

1. Acesse: https://vercel.com/dashboard
2. Clique no seu projeto
3. Vá em **Settings** > **Domains**
4. Verifique se `rotina.temvenda.com.br` está listado

**Se NÃO estiver listado:**
- Clique em **Add Domain**
- Digite: `rotina.temvenda.com.br`
- Clique em **Add**
- Siga as instruções de DNS

**Se estiver listado:**
- Verifique o status:
  - 🟢 **Valid**: DNS configurado corretamente
  - 🟡 **Pending**: Aguardando configuração DNS
  - 🔴 **Invalid**: Erro na configuração DNS

### 2. Verificar Configuração DNS

No seu provedor de DNS (onde está configurado `temvenda.com.br`):

#### Verificar se existe registro CNAME:

```
Nome: rotina
Tipo: CNAME
Valor: cname.vercel-dns.com
TTL: 3600 (ou padrão)
```

#### Ou verificar registros A (se usar A records):

```
Nome: rotina
Tipo: A
Valor: 76.76.21.21 (ou IP fornecido pelo Vercel)
TTL: 3600
```

### 3. Verificar Propagação DNS

Use ferramentas online para verificar:

1. **DNS Checker**: https://dnschecker.org
   - Digite: `rotina.temvenda.com.br`
   - Verifique se aponta para o Vercel

2. **No terminal**:
```bash
dig rotina.temvenda.com.br
# ou
nslookup rotina.temvenda.com.br
```

Deve mostrar o IP do Vercel ou `cname.vercel-dns.com`

### 4. Verificar se a Aplicação Está Rodando

1. No Vercel Dashboard, vá em **Deployments**
2. Verifique o último deploy:
   - 🟢 **Ready**: Deploy concluído
   - 🟡 **Building**: Ainda em construção
   - 🔴 **Error**: Erro no deploy

3. Se houver erro, veja os logs do deploy

### 5. Verificar SSL/HTTPS

O Vercel configura SSL automaticamente, mas pode levar alguns minutos.

1. No Vercel Dashboard, vá em **Settings** > **Domains**
2. Verifique se há um certificado SSL para `rotina.temvenda.com.br`
3. Pode levar até 1 hora para o certificado ser emitido

---

## 🔧 Soluções

### Solução 1: Reconfigurar Domínio no Vercel

1. No Vercel Dashboard, vá em **Settings** > **Domains**
2. Se o domínio estiver listado mas com erro:
   - Remova o domínio
   - Aguarde alguns minutos
   - Adicione novamente
   - Siga as instruções de DNS

### Solução 2: Verificar DNS Manualmente

1. Acesse seu provedor de DNS
2. Verifique se o registro está correto
3. Se necessário, delete e recrie o registro
4. Aguarde propagação (5-30 minutos)

### Solução 3: Usar URL do Vercel Temporariamente

Enquanto o domínio não está funcionando, você pode usar a URL do Vercel:

1. No Vercel Dashboard, vá em **Deployments**
2. Clique no último deploy
3. Copie a URL (ex: `https://rotina-xxxxx.vercel.app`)
4. Use essa URL temporariamente para testar

**IMPORTANTE**: Configure essa URL também no Supabase como Redirect URL temporária!

### Solução 4: Verificar Firewall/Proxy

Se você estiver em uma rede corporativa:

1. Verifique se há firewall bloqueando
2. Tente de outra rede (ex: celular)
3. Verifique se há proxy configurado

---

## 📋 Checklist de Diagnóstico

Execute estes comandos para diagnosticar:

### 1. Verificar DNS:
```bash
dig rotina.temvenda.com.br
# ou
nslookup rotina.temvenda.com.br
```

### 2. Verificar se o servidor responde:
```bash
curl -I https://rotina.temvenda.com.br
```

### 3. Verificar certificado SSL:
```bash
openssl s_client -connect rotina.temvenda.com.br:443 -servername rotina.temvenda.com.br
```

### 4. Verificar no navegador:
- Abra: `https://rotina.temvenda.com.br`
- Veja o erro exato no console (F12)

---

## 🎯 Passos Imediatos

1. **Verifique no Vercel Dashboard**:
   - Settings > Domains
   - Veja o status do domínio

2. **Se o domínio não estiver configurado**:
   - Adicione o domínio
   - Configure o DNS conforme instruções

3. **Se o domínio estiver configurado mas com erro**:
   - Verifique os logs do Vercel
   - Verifique a configuração DNS
   - Aguarde propagação DNS (pode levar até 24h)

4. **Teste com a URL do Vercel**:
   - Use `https://rotina-xxxxx.vercel.app` temporariamente
   - Configure essa URL no Supabase também

---

## 🔗 Links Úteis

- **Vercel Dashboard**: https://vercel.com/dashboard
- **DNS Checker**: https://dnschecker.org
- **Documentação Vercel Domains**: https://vercel.com/docs/concepts/projects/domains

---

## ⚠️ Importante

O erro `ERR_CONNECTION_CLOSED` geralmente significa:
- O domínio não está apontando para o Vercel
- O DNS não propagou ainda
- Há problema com SSL/HTTPS
- A aplicação não está rodando

**Solução mais comum**: Verificar e reconfigurar o DNS conforme instruções do Vercel.

