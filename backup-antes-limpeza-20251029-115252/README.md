# TemVenda - Site Corporativo WordPress

Este repositório contém o código fonte do site corporativo TemVenda (www.temvenda.com.br).

## 🚀 Como executar localmente

### Pré-requisitos
- Docker e Docker Compose instalados
- Git

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/site-temvenda.git
cd site-temvenda
```

2. Execute o ambiente local:
```bash
docker-compose up -d
```

3. Acesse:
- **Site WordPress**: http://localhost:8080
- **phpMyAdmin**: http://localhost:8081

### Credenciais padrão do banco:
- **Usuário**: wordpress
- **Senha**: wordpress_password
- **Banco**: temvenda_db

## 📁 Estrutura do Projeto

```
site-temvenda/
├── docker-compose.yml    # Configuração Docker
├── uploads.ini          # Configurações PHP
├── .gitignore           # Arquivos ignorados pelo Git
├── wordpress/           # Arquivos WordPress
│   ├── wp-content/      # Temas, plugins, uploads
│   ├── wp-admin/        # Painel administrativo
│   └── wp-includes/     # Arquivos core WordPress
└── README.md           # Este arquivo
```

## 🔧 Desenvolvimento

### Comandos úteis:

```bash
# Iniciar ambiente
docker-compose up -d

# Parar ambiente
docker-compose down

# Ver logs
docker-compose logs -f

# Acessar container WordPress
docker exec -it temvenda_wordpress bash

# Backup do banco
docker exec temvenda_db mysqldump -u wordpress -pwordpress_password temvenda_db > backup.sql
```

## 📝 Notas Importantes

- O arquivo `wp-config.php` não é versionado por segurança
- Uploads são ignorados pelo Git (use backup manual)
- Sempre faça backup antes de fazer alterações importantes
- Use branches para desenvolvimento de novas funcionalidades

## 🚀 Deploy

Para fazer deploy das alterações:

1. Commit suas alterações
2. Push para o branch principal
3. Execute o script de deploy (configurar conforme seu servidor)

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
