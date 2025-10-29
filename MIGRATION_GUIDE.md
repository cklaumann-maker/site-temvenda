# 📋 Guia Completo de Migração WordPress para GitHub

## 🎯 Objetivo
Migrar o site www.temvenda.com.br do servidor atual para um ambiente de desenvolvimento local com versionamento no GitHub.

## 📦 Arquivos Criados

✅ `docker-compose.yml` - Ambiente Docker com WordPress, MySQL e phpMyAdmin  
✅ `uploads.ini` - Configurações PHP para uploads  
✅ `.gitignore` - Arquivos ignorados pelo Git  
✅ `README.md` - Documentação do projeto  
✅ `migrate.sh` - Script de migração automatizada  

## 🚀 Passo a Passo da Migração

### 1. **Baixar Arquivos do Servidor**

**Via FTP (FileZilla, WinSCP, etc.):**
```
Servidor: seu-servidor.com.br
Usuário: seu-usuario-ftp
Senha: sua-senha-ftp
Porta: 21 (ou 22 para SFTP)
```

**Arquivos para baixar:**
- Toda a pasta `public_html` (ou equivalente)
- Especialmente importante:
  - `wp-config.php`
  - `wp-content/` (temas, plugins, uploads)
  - `.htaccess`
  - Todos os arquivos PHP

### 2. **Exportar Banco de Dados**

**Via cPanel:**
1. Acesse phpMyAdmin
2. Selecione o banco de dados do WordPress
3. Clique em "Exportar"
4. Escolha "Personalizado"
5. Marque "Adicionar DROP TABLE"
6. Marque "Adicionar CREATE TABLE"
7. Clique em "Executar"

**Via linha de comando (se tiver acesso SSH):**
```bash
mysqldump -u usuario -p nome_do_banco > backup_temvenda.sql
```

### 3. **Preparar Ambiente Local**

```bash
# Navegar para o diretório do projeto
cd /Users/cesark/site-temvenda

# Baixar arquivos do servidor para a pasta wordpress/
# (copie todos os arquivos baixados para wordpress/)

# Executar script de migração
./migrate.sh
```

### 4. **Iniciar Ambiente Docker**

```bash
# Iniciar containers
docker-compose up -d

# Verificar se estão rodando
docker-compose ps
```

### 5. **Importar Banco de Dados**

1. Acesse phpMyAdmin: http://localhost:8081
2. Login: `wordpress` / `wordpress_password`
3. Selecione o banco `temvenda_db`
4. Clique em "Importar"
5. Escolha o arquivo `.sql` exportado
6. Clique em "Executar"

### 6. **Atualizar URLs no Banco**

**Via phpMyAdmin:**
```sql
-- Atualizar URLs do site
UPDATE wp_options SET option_value = 'http://localhost:8080' WHERE option_name = 'home';
UPDATE wp_options SET option_value = 'http://localhost:8080' WHERE option_name = 'siteurl';

-- Atualizar URLs em posts (se necessário)
UPDATE wp_posts SET post_content = REPLACE(post_content, 'https://www.temvenda.com.br', 'http://localhost:8080');
UPDATE wp_posts SET guid = REPLACE(guid, 'https://www.temvenda.com.br', 'http://localhost:8080');
```

### 7. **Configurar Git e GitHub**

```bash
# Inicializar repositório Git
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "Migração inicial do WordPress - TemVenda"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/seu-usuario/site-temvenda.git
git branch -M main
git push -u origin main
```

## 🔧 Configurações Importantes

### **Chaves de Segurança**
1. Acesse: https://api.wordpress.org/secret-key/1.1/salt/
2. Copie as chaves geradas
3. Substitua no arquivo `wordpress/wp-config.php`

### **Configurações de Desenvolvimento**
- Debug habilitado para desenvolvimento local
- Uploads limitados a 64MB
- Memória PHP configurada para 256MB

## 🚨 Troubleshooting

### **Problema: Site não carrega**
- Verifique se os containers estão rodando: `docker-compose ps`
- Verifique logs: `docker-compose logs wordpress`

### **Problema: Banco de dados não conecta**
- Verifique se o container `db` está rodando
- Teste conexão via phpMyAdmin

### **Problema: Uploads não funcionam**
- Verifique permissões da pasta `wp-content/uploads`
- Verifique configurações em `uploads.ini`

### **Problema: URLs quebradas**
- Execute as queries SQL para atualizar URLs
- Limpe cache se usar plugins de cache

## 📝 Próximos Passos

1. **Testar site localmente** em http://localhost:8080
2. **Configurar deploy automático** (GitHub Actions)
3. **Configurar backup automático** do banco
4. **Documentar processo de deploy**

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs`
2. Consulte a documentação do WordPress
3. Abra uma issue no repositório GitHub

---

**⚠️ Importante:** Sempre faça backup antes de fazer alterações importantes!
