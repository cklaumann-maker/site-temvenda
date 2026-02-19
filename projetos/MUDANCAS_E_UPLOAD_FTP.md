# Resumo das alterações e upload FTP

Tudo que foi modificado e o que subir via FTP para produção.

---

## 1. Arquivos modificados (resumo)

| Arquivo | O que foi alterado |
|---------|--------------------|
| **projetos/index.html** | Página exige login (redirect para /area/ se não logado). Nav e footer: link "Projetos" trocado por "Área Administrativa" (/app/). Lista de projetos passou a vir do Supabase (API); fallback estático se falhar. |
| **area/admin-projetos.html** | Página da aba "Projetos" na área admin. Passou a usar só a API REST do Supabase (fetch), sem script do CDN. Config do Supabase inline. Link "Ver página pública" → "Ver lista de projetos". |
| **auth-manager.js** | Init: redireciona para login só na página de login (/area/ ou /area/index.html). Páginas como /area/admin-projetos.html passam a exigir login. |
| **app/index.html** | Nova aba "Projetos" no painel administrativo, carregando /area/admin-projetos.html em iframe. |
| **projetos/turin_empreendimentos/index.html** | Exige login da área admin (redirect para /area/). Link "Voltar" que ia para /projetos/ passou a ir para /app/. |
| **projetos/axis/index.html** | Exige login da área admin (redirect para /area/). |
| **projetos/ana-cristina-cardoso/index.html** | Exige login da área admin (redirect para /area/). |
| **projetos/CRIAR_TABELA_PROJETOS.sql** | Incluído `DROP POLICY IF EXISTS` antes dos `CREATE POLICY` para o script poder ser executado de novo no Supabase sem erro. *(Não sobe no FTP; só no Supabase.)* |

---

## 2. O que subir via FTP (arquivos e locais)

Subir **na mesma estrutura de pastas** do projeto. Raiz do FTP = raiz do site (ex.: `public_html` ou `htdocs`).

### Raiz do site

| Arquivo local | No FTP (caminho) |
|---------------|------------------|
| auth-manager.js | **auth-manager.js** |

### Área administrativa

| Arquivo local | No FTP (caminho) |
|---------------|------------------|
| area/admin-projetos.html | **area/admin-projetos.html** |

### App (painel admin)

| Arquivo local | No FTP (caminho) |
|---------------|------------------|
| app/index.html | **app/index.html** |

### Projetos

| Arquivo local | No FTP (caminho) |
|---------------|------------------|
| projetos/index.html | **projetos/index.html** |
| projetos/turin_empreendimentos/index.html | **projetos/turin_empreendimentos/index.html** |
| projetos/axis/index.html | **projetos/axis/index.html** |
| projetos/ana-cristina-cardoso/index.html | **projetos/ana-cristina-cardoso/index.html** |

---

## 3. Lista para upload — um a um

1. **auth-manager.js** → na **raiz** do site  
2. **area/admin-projetos.html** → dentro da pasta **area/**  
3. **app/index.html** → dentro da pasta **app/**  
4. **projetos/index.html** → dentro da pasta **projetos/**  
5. **projetos/turin_empreendimentos/index.html** → dentro de **projetos/turin_empreendimentos/**  
6. **projetos/axis/index.html** → dentro de **projetos/axis/**  
7. **projetos/ana-cristina-cardoso/index.html** → dentro de **projetos/ana-cristina-cardoso/**  

---

## 4. Estrutura no servidor (após upload)

```
[raiz do site]/
├── auth-manager.js
├── area/
│   └── admin-projetos.html
├── app/
│   └── index.html
└── projetos/
    ├── index.html
    ├── turin_empreendimentos/
    │   └── index.html
    ├── axis/
    │   └── index.html
    └── ana-cristina-cardoso/
        └── index.html
```

*(As demais pastas e arquivos que você já tem no FTP permanecem; só substitua/adicione os listados acima.)*

---

## 5. Não sobe no FTP

- **projetos/CRIAR_TABELA_PROJETOS.sql** — executar apenas no **Supabase** (SQL Editor).  
- **projetos/MUDANCAS_E_UPLOAD_FTP.md** — só documentação local.

---

## 6. Conferência rápida

Depois do upload:

1. **Login:** acessar `/area/` e fazer login.  
2. **Lista de projetos:** em `/app/`, abrir a aba **Projetos** e ver se a tabela carrega do Supabase.  
3. **Página de projetos:** acessar `/projetos/` (após login) e ver se os projetos aparecem por status.  
4. **Projetos protegidos:** sem login, `/projetos/`, `/projetos/turin_empreendimentos/`, `/projetos/axis/`, `/projetos/ana-cristina-cardoso/` devem redirecionar para `/area/`.  
5. **NEOSUL:** `/projetos/neosul/` continua público (login próprio).
