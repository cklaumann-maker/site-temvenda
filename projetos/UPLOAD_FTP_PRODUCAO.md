# Arquivos para subir no FTP — Produção (Projetos + TURIN)

Use a estrutura abaixo no servidor. Os caminhos são relativos à **raiz do site** (pasta pública do FTP, ex.: `public_html` ou `htdocs`).

---

## 1. Raiz do site (obrigatório para o TURIN funcionar)

O projeto TURIN carrega `../../supabase-config.js`, ou seja, o arquivo precisa estar **duas pastas acima** de `turin_empreendimentos`. Coloque na **raiz do site**:

| Arquivo             | Caminho no FTP      | Obrigatório |
|---------------------|---------------------|-------------|
| supabase-config.js  | **supabase-config.js** | Sim (repositório e listagem de documentos) |

---

## 2. Pasta de projetos

| Arquivo           | Caminho no FTP           | Obrigatório |
|-------------------|--------------------------|-------------|
| index.html        | **projetos/index.html**  | Sim (listagem de projetos) |
| logo-temvenda.png | **projetos/logo-temvenda.png** | Sim (logo no layout) |

---

## 3. Projeto TURIN Empreendimentos

| Arquivo   | Caminho no FTP                              | Obrigatório |
|-----------|---------------------------------------------|-------------|
| index.html | **projetos/turin_empreendimentos/index.html** | Sim (página do projeto) |
| logo-turin.png | **projetos/turin_empreendimentos/logo-turin.png** | Sim (logo no header) |
| banner.mp4 | **projetos/turin_empreendimentos/banner.mp4** | Sim (vídeo do banner) |
| cesar-klaumann.jpg | **projetos/turin_empreendimentos/cesar-klaumann.jpg** | Sim (foto Quem Somos) |
| ana-cristina.jpg | **projetos/turin_empreendimentos/ana-cristina.jpg** | Opcional (foto Quem Somos) |
| davi-daitx.jpg | **projetos/turin_empreendimentos/davi-daitx.jpg** | Opcional (foto Quem Somos) |
| verificar-banco-projeto.html | **projetos/turin_empreendimentos/verificar-banco-projeto.html** | Não (só para verificar banco/Storage) |

---

## 4. Estrutura final no servidor

```
[raiz do site]/
├── supabase-config.js
└── projetos/
    ├── index.html
    ├── logo-temvenda.png
    └── turin_empreendimentos/
        ├── index.html
        ├── logo-turin.png
        ├── banner.mp4
        ├── cesar-klaumann.jpg
        ├── ana-cristina.jpg       (opcional)
        ├── davi-daitx.jpg         (opcional)
        └── verificar-banco-projeto.html   (opcional)
```

---

## 5. Lista resumida — um a um

1. **supabase-config.js** → na raiz do site  
2. **projetos/index.html** → dentro da pasta `projetos`  
3. **projetos/logo-temvenda.png** → dentro da pasta `projetos`  
4. **projetos/turin_empreendimentos/index.html** → dentro de `projetos/turin_empreendimentos`  
5. **projetos/turin_empreendimentos/logo-turin.png** → dentro de `projetos/turin_empreendimentos`  
6. **projetos/turin_empreendimentos/banner.mp4** → dentro de `projetos/turin_empreendimentos`  
7. **projetos/turin_empreendimentos/cesar-klaumann.jpg** → dentro de `projetos/turin_empreendimentos`  
8. **projetos/turin_empreendimentos/ana-cristina.jpg** → dentro de `projetos/turin_empreendimentos` (opcional)  
9. **projetos/turin_empreendimentos/davi-daitx.jpg** → dentro de `projetos/turin_empreendimentos` (opcional)  
10. **projetos/turin_empreendimentos/verificar-banco-projeto.html** → dentro de `projetos/turin_empreendimentos` (opcional)

---

## 6. Não é preciso subir

- **CRIAR_TABELAS_PROJETO.sql** — usar só no Supabase (SQL Editor)  
- **CRIAR_BUCKET_CONTRATOS.md** — documentação  
- **SETUP_SUPABASE_PROJETO_TURIN.md** — documentação  

---

## 7. Ordem sugerida no FTP

1. Criar pasta **projetos** na raiz (se não existir).  
2. Subir **supabase-config.js** na raiz.  
3. Subir **index.html** e **logo-temvenda.png** em **projetos/**.  
4. Criar pasta **projetos/turin_empreendimentos**.  
5. Subir **index.html**, **logo-turin.png**, **banner.mp4** em **projetos/turin_empreendimentos/**.  
6. Subir as fotos **cesar-klaumann.jpg**, **ana-cristina.jpg**, **davi-daitx.jpg** em **projetos/turin_empreendimentos/** (se tiver as imagens).  
7. (Opcional) Subir **verificar-banco-projeto.html** em **projetos/turin_empreendimentos/**.

Depois disso, a listagem de projetos deve abrir em `https://seusite.com/projetos/` e o projeto TURIN em `https://seusite.com/projetos/turin_empreendimentos/`.
