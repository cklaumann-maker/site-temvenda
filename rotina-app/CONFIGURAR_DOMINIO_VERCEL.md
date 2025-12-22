# 🌐 Configurar Domínio Personalizado no Vercel

## Configurar `rotina.temvenda.com.br` no Vercel

---

## 📋 Passo 1: Adicionar Domínio no Vercel

### 1.1 Acesse o Dashboard do Vercel

1. Vá para: https://vercel.com/dashboard
2. Clique no seu projeto (`rotina` ou `site-temvenda`)

### 1.2 Adicionar Domínio

1. Vá em **Settings** (Configurações)
2. Clique na aba **Domains** (Domínios)
3. Clique no botão **Add Domain** (Adicionar Domínio)
4. Digite: `rotina.temvenda.com.br`
5. Clique em **Add**

---

## 🔧 Passo 2: Configurar DNS

O Vercel mostrará instruções de DNS. Você precisa configurar no seu provedor de DNS (onde está configurado `temvenda.com.br`).

### Opção A: Configuração CNAME (Recomendada)

1. **No seu provedor de DNS** (ex: Cloudflare, GoDaddy, Registro.br, etc.)
2. **Adicione um registro CNAME**:
   - **Nome/Host**: `rotina`
   - **Valor/Target**: `cname.vercel-dns.com`
   - **TTL**: 3600 (ou padrão)

### Opção B: Configuração A Record (Alternativa)

Se CNAME não funcionar, use A Records:

1. **Adicione 4 registros A**:
   - **Nome/Host**: `rotina`
   - **Valor/Target**: `76.76.21.21` (ou o IP fornecido pelo Vercel)
   - **TTL**: 3600

   Repita para os outros IPs que o Vercel fornecer.

---

## ⏱️ Passo 3: Aguardar Propagação DNS

- **Tempo estimado**: 5 minutos a 24 horas
- **Normalmente**: 5-30 minutos

### Verificar Status:

1. No Vercel, vá em **Settings** > **Domains**
2. Você verá o status:
   - 🟡 **Pending**: Aguardando configuração DNS
   - 🟢 **Valid**: DNS configurado corretamente
   - 🔴 **Invalid**: Erro na configuração DNS

### Verificar DNS Online:

Use ferramentas online para verificar:
- https://dnschecker.org
- Digite: `rotina.temvenda.com.br`
- Verifique se aponta para `cname.vercel-dns.com`

---

## 🔒 Passo 4: Configurar SSL/HTTPS

O Vercel configura **automaticamente** SSL/HTTPS gratuito!

- Não precisa fazer nada
- O certificado é emitido automaticamente pela Let's Encrypt
- HTTPS funcionará automaticamente após o DNS propagar

---

## ✅ Passo 5: Verificar Funcionamento

Após a propagação DNS:

1. Acesse: `https://rotina.temvenda.com.br`
2. Você deve ver sua aplicação funcionando
3. O Vercel redireciona automaticamente HTTP → HTTPS

---

## 🛠️ Troubleshooting

### Problema: Domínio não resolve

**Solução**:
1. Verifique se o registro DNS está correto
2. Aguarde mais tempo (pode levar até 24h)
3. Use `dig rotina.temvenda.com.br` ou `nslookup rotina.temvenda.com.br` para verificar

### Problema: Erro "Invalid Configuration"

**Solução**:
1. Verifique se o nome do domínio está correto
2. Certifique-se de que o DNS está apontando para o Vercel
3. Remova e adicione o domínio novamente no Vercel

### Problema: SSL não funciona

**Solução**:
1. Aguarde alguns minutos após o DNS propagar
2. O Vercel emite o certificado automaticamente
3. Se não funcionar em 1 hora, entre em contato com o suporte do Vercel

---

## 📝 Exemplo de Configuração DNS

### Cloudflare:

```
Tipo: CNAME
Nome: rotina
Conteúdo: cname.vercel-dns.com
Proxy: Desativado (DNS only)
TTL: Auto
```

### Registro.br / GoDaddy:

```
Tipo: CNAME
Host: rotina
Aponta para: cname.vercel-dns.com
TTL: 3600
```

### Route 53 (AWS):

```
Tipo: CNAME
Nome: rotina.temvenda.com.br
Valor: cname.vercel-dns.com
TTL: 300
```

---

## 🔗 Links Úteis

- **Dashboard Vercel**: https://vercel.com/dashboard
- **Documentação Vercel Domains**: https://vercel.com/docs/concepts/projects/domains
- **Verificar DNS**: https://dnschecker.org

---

## ✅ Checklist Final

- [ ] Domínio adicionado no Vercel
- [ ] Registro CNAME configurado no DNS
- [ ] DNS propagado (verificado)
- [ ] Domínio mostra status "Valid" no Vercel
- [ ] Aplicação acessível em `https://rotina.temvenda.com.br`
- [ ] HTTPS funcionando (cadeado verde no navegador)

---

## 🎉 Pronto!

Após completar esses passos, sua aplicação estará acessível em:

**https://rotina.temvenda.com.br**

O Vercel gerencia automaticamente:
- ✅ SSL/HTTPS
- ✅ CDN global
- ✅ Deploys automáticos
- ✅ Rollback de versões

