# 🚀 Como Carregar Arquivos do GitHub para InfinityFree

## ✅ SIM, É POSSÍVEL!

Existem várias formas de fazer upload dos arquivos do GitHub para o InfinityFree. Vou mostrar todas as opções:

---

## 🎯 OPÇÃO 1: Baixar ZIP do GitHub e Fazer Upload via FTP ⭐ (Mais Simples)

### **Passo a Passo:**

1. **Baixar do GitHub:**
   - Acesse: https://github.com/seu-usuario/site-temvenda
   - Clique em **"Code"** → **"Download ZIP"**
   - Extraia o arquivo ZIP

2. **Preparar Arquivos:**
   ```bash
   cd site-temvenda-master
   ./preparar-ftp.sh
   ```

3. **Fazer Upload via FTP:**
   - Conecte via FileZilla
   - Navegue até `htdocs/` ou `public_html/`
   - Faça upload dos arquivos de `deploy-ftp/`

**✅ Vantagem:** Simples e direto

---

## 🎯 OPÇÃO 2: Clonar Repositório e Fazer Upload ⭐⭐ (Recomendado)

### **Passo a Passo:**

1. **Clonar Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/site-temvenda.git
   cd site-temvenda
   ```

2. **Preparar Arquivos:**
   ```bash
   ./preparar-ftp.sh
   ```

3. **Fazer Upload via FTP:**
   - Conecte via FileZilla
   - Navegue até `htdocs/` ou `public_html/`
   - Faça upload dos arquivos de `deploy-ftp/`

**✅ Vantagem:** Sempre atualizado com o código do GitHub

---

## 🎯 OPÇÃO 3: Git via SSH (Avançado)

### **Verificar se InfinityFree suporta SSH:**

1. Acesse o painel InfinityFree
2. Vá em **"Manage"** → **"SSH Access"**
3. Se disponível, ative SSH

### **Configurar Git:**

```bash
# Conectar via SSH
ssh usuario@servidor.infinityfree.net

# Dentro do servidor
cd htdocs

# Clonar repositório
git clone https://github.com/seu-usuario/site-temvenda.git .

# Preparar arquivos
./preparar-ftp.sh

# Fazer upload
git pull origin main
```

**✅ Vantagem:** Atualização automática via Git

**⚠️ Limitação:** Nem todos os planos gratuitos têm SSH

---

## 🎯 OPÇÃO 4: Script Automatizado (Melhor Opção)

Vou criar um script que automatiza tudo:

```bash
#!/bin/bash
# deploy-github-to-infinityfree.sh

echo "🚀 Deploy do GitHub para InfinityFree"
echo "======================================"

# 1. Clonar ou atualizar repositório
if [ -d "site-temvenda" ]; then
    echo "📥 Atualizando repositório..."
    cd site-temvenda
    git pull origin main
else
    echo "📥 Clonando repositório..."
    git clone https://github.com/seu-usuario/site-temvenda.git
    cd site-temvenda
fi

# 2. Preparar arquivos
echo "🔧 Preparando arquivos..."
./preparar-ftp.sh

# 3. Instruções para FTP
echo ""
echo "✅ Arquivos preparados em: deploy-ftp/"
echo ""
echo "📤 Próximos passos:"
echo "  1. Abra FileZilla"
echo "  2. Conecte ao servidor FTP"
echo "  3. Faça upload dos arquivos de deploy-ftp/"
```

---

## 🛠️ Configuração Recomendada

### **Estrutura Ideal:**

```
Seu Computador:
├── site-temvenda/          (Repositório Git)
│   ├── deploy-ftp/         (Arquivos prontos para upload)
│   └── preparar-ftp.sh     (Script de preparação)
│
InfinityFree:
└── htdocs/                  (Arquivos do site)
    ├── home-corporativo.html
    ├── consultoria.html
    └── ...
```

---

## 🔄 Workflow Recomendado (Atualização Contínua)

### **1. Desenvolvimento Local:**
```bash
# Fazer alterações nos arquivos
# Testar localmente
# Commit e push para GitHub
git add .
git commit -m "Descrição das alterações"
git push origin main
```

### **2. Deploy para InfinityFree:**
```bash
# Preparar arquivos
./preparar-ftp.sh

# Fazer upload via FTP
# (Use FileZilla ou script automático)
```

---

## 📋 Script Completo de Deploy

Salve este script como `deploy-to-infinityfree.sh`:

```bash
#!/bin/bash

# Configurações
GITHUB_REPO="https://github.com/seu-usuario/site-temvenda.git"
FTP_HOST="ftp.infinityfree.net"
FTP_USER="seu-usuario"
FTP_PASS="sua-senha"
FTP_DIR="htdocs"

echo "🚀 Deploy do GitHub para InfinityFree"
echo "======================================"

# 1. Clonar/Atualizar
if [ -d "temp-site" ]; then
    cd temp-site
    git pull
else
    git clone $GITHUB_REPO temp-site
    cd temp-site
fi

# 2. Preparar arquivos
./preparar-ftp.sh

# 3. Upload via FTP (usando curl)
echo "📤 Fazendo upload via FTP..."
cd deploy-ftp

for file in *; do
    curl -T "$file" ftp://$FTP_USER:$FTP_PASS@$FTP_HOST/$FTP_DIR/
done

echo "✅ Deploy concluído!"
```

---

## 💡 Dicas Importantes

### **1. Sempre Prepare os Arquivos:**
```bash
./preparar-ftp.sh
```
Isso remove `/wp-content/temvenda/` dos caminhos.

### **2. Mantenha Backup:**
Sempre faça backup antes de fazer deploy:
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz deploy-ftp/
```

### **3. Teste Localmente:**
Sempre teste localmente antes de fazer deploy:
```bash
# Servir localmente
cd deploy-ftp
python3 -m http.server 8000
# Acesse: http://localhost:8000
```

### **4. Use GitHub Actions (Avançado):**
Crie um workflow automático no GitHub para fazer deploy automaticamente.

---

## 🚨 Problemas Comuns

### **Erro: Arquivos não encontrados**
- Verifique se executou `./preparar-ftp.sh`
- Verifique se os arquivos estão em `deploy-ftp/`

### **Erro: Caminhos incorretos**
- Execute `./preparar-ftp.sh` novamente
- Verifique se removeu `/wp-content/temvenda/`

### **Erro: Permissões FTP**
- Verifique credenciais FTP
- Verifique se a pasta `htdocs/` existe

---

## ✅ Checklist de Deploy

- [ ] Repositório atualizado no GitHub
- [ ] Script `preparar-ftp.sh` executado
- [ ] Arquivos preparados em `deploy-ftp/`
- [ ] Backup feito
- [ ] Teste local realizado
- [ ] Upload via FTP concluído
- [ ] Site testado em produção

---

## 🎯 Resumo das Opções

| Opção | Dificuldade | Automatização | Recomendado |
|-------|-------------|---------------|-------------|
| **Download ZIP** | Fácil | Manual | ⭐ Para iniciantes |
| **Git Clone** | Fácil | Manual | ⭐⭐ Para desenvolvedores |
| **Git + SSH** | Médio | Automático | ⭐⭐⭐ Para avançados |
| **Script Automático** | Fácil | Automático | ⭐⭐⭐⭐ Melhor opção |

---

**Última atualização:** $(date)


