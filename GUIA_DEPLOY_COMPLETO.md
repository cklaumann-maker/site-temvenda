# 🚀 Guia de Deploy Completo - TEM VENDA

## 📋 **Checklist Pré-Deploy**

### **1. Configurações Sensíveis**
- [ ] `supabase-config.js` - Credenciais do Supabase
- [ ] `email-config.js` - Credenciais do EmailJS
- [ ] `.env` - Chave OpenAI (se necessário)

### **2. Arquivos de Produção**
- [ ] Todos os arquivos HTML atualizados
- [ ] Imagens e assets organizados
- [ ] Scripts funcionando localmente

---

## 🐙 **Deploy para GitHub**

### **Passo 1: Criar Repositório**
1. Acesse [github.com](https://github.com)
2. Clique em **"New repository"**
3. Nome: `temvenda-site`
4. Descrição: `Site TEM VENDA - Sistema de captura de leads`
5. Marque **"Public"** ou **"Private"**
6. **NÃO** marque "Add README" (já temos arquivos)
7. Clique **"Create repository"**

### **Passo 2: Executar Script de Deploy**
```bash
# No terminal, no diretório do projeto
./deploy-github-infinityfree.sh
```

### **Passo 3: Configurar Remote (se necessário)**
```bash
git remote add origin https://github.com/SEU_USUARIO/temvenda-site.git
git branch -M main
git push -u origin main
```

---

## 🌐 **Deploy para InfinityFree**

### **Método 1: File Manager (Recomendado)**
1. **Acesse o painel do InfinityFree**
2. **Vá em "File Manager"**
3. **Navegue para a pasta do domínio** (temvenda.com.br)
4. **Faça upload dos arquivos:**
   - `index.html`
   - `instagram.html`
   - `admin.html`, `admin-*.html`
   - `login-admin.html`
   - `diagnostico.html`
   - `consultoria.html`, `formacao-lideres.html`, etc.
   - `noticias.html`
   - `home-corporativo.html`
   - `favicon.ico`, `favicon-32.png`
   - `supabase-config.js`
   - `email-config.js`
   - `auth-manager.js`
   - `server-temvenda.py` (se necessário)

### **Método 2: FTP (Alternativo)**
1. **Configure cliente FTP** (FileZilla, WinSCP)
2. **Host:** `ftpupload.net`
3. **Porta:** `21`
4. **Usuário/Senha:** Do painel InfinityFree
5. **Faça upload** de todos os arquivos

---

## ⚙️ **Configurações Pós-Deploy**

### **1. Configurar Supabase**
- Edite `supabase-config.js` com suas credenciais
- Verifique se as tabelas existem no Supabase
- Teste a conexão

### **2. Configurar EmailJS**
- Edite `email-config.js` com suas credenciais
- Verifique se o template está correto
- Teste o envio de e-mail

### **3. Configurar Domínio**
- Verifique se o DNS está apontando para InfinityFree
- Teste: `https://temvenda.com.br`
- Teste: `https://temvenda.com.br/instagram`

---

## 🧪 **Testes de Validação**

### **1. Páginas Principais**
- [ ] `https://temvenda.com.br` - Página inicial
- [ ] `https://temvenda.com.br/instagram` - Captura de leads
- [ ] `https://temvenda.com.br/admin` - Painel administrativo
- [ ] `https://temvenda.com.br/diagnostico` - Diagnóstico

### **2. Funcionalidades**
- [ ] Formulário de captura envia e-mail
- [ ] Lead aparece no funil de vendas
- [ ] Admin carrega textos do banco
- [ ] Upload de PDF funciona
- [ ] Login admin funciona

### **3. Mobile**
- [ ] Páginas responsivas no celular
- [ ] Formulários funcionam no mobile
- [ ] Links e botões clicáveis

---

## 🔧 **Manutenção**

### **Atualizações Futuras**
1. **Edite arquivos localmente**
2. **Teste em localhost**
3. **Commit no GitHub:**
   ```bash
   git add .
   git commit -m "Descrição da atualização"
   git push origin main
   ```
4. **Faça upload no InfinityFree**

### **Backup**
- **GitHub** = Backup automático do código
- **Supabase** = Backup automático dos dados
- **InfinityFree** = Backup manual (recomendado)

---

## 🚨 **Solução de Problemas**

### **Página não carrega**
- Verifique se o arquivo foi enviado corretamente
- Verifique permissões do arquivo (644)
- Limpe cache do navegador

### **E-mail não envia**
- Verifique credenciais do EmailJS
- Verifique template no EmailJS
- Verifique logs no console

### **Banco não conecta**
- Verifique credenciais do Supabase
- Verifique políticas RLS
- Verifique CORS no Supabase

### **Admin não funciona**
- Verifique se `auth-manager.js` foi enviado
- Verifique se `supabase-config.js` está correto
- Verifique permissões do usuário

---

## 📞 **Suporte**

Para problemas:
1. Verifique este guia
2. Consulte logs do console
3. Teste em localhost primeiro
4. Verifique configurações sensíveis

---

**🎉 Deploy concluído com sucesso!**

**URLs do site:**
- **Principal:** https://temvenda.com.br
- **Instagram:** https://temvenda.com.br/instagram
- **Admin:** https://temvenda.com.br/admin
