# Upload FTP - Ana Cristina Cardoso

## Arquivos para subir no FTP — Produção

Use a estrutura abaixo no servidor. Os caminhos são relativos à **raiz do site** (pasta pública do FTP, ex.: `public_html` ou `htdocs`).

---

## 1. Pasta do projeto

| Arquivo           | Caminho no FTP                              | Obrigatório |
|-------------------|---------------------------------------------|-------------|
| index.html        | **projetos/ana-cristina-cardoso/index.html** | Sim (página principal) |
| logo.png          | **projetos/ana-cristina-cardoso/logo.png**   | Opcional (logo no header) |

---

## 2. Estrutura final no servidor

```
[raiz do site]/
└── projetos/
    └── ana-cristina-cardoso/
        ├── index.html
        └── logo.png (opcional)
```

---

## 3. Lista resumida — um a um

1. **projetos/ana-cristina-cardoso/index.html** → dentro de `projetos/ana-cristina-cardoso`  
2. **projetos/ana-cristina-cardoso/logo.png** → dentro de `projetos/ana-cristina-cardoso` (opcional)

---

## 4. Ordem sugerida no FTP

1. Criar pasta **projetos/ana-cristina-cardoso** (se não existir).  
2. Subir **index.html** em **projetos/ana-cristina-cardoso/**.  
3. (Opcional) Subir **logo.png** em **projetos/ana-cristina-cardoso/**.

Depois disso, o projeto deve abrir em `https://seusite.com/projetos/ana-cristina-cardoso/`.

---

## 5. Observações

- O arquivo HTML está configurado para usar `logo.png` como imagem do logo (caminho relativo).
- Se a imagem não existir, ela será ocultada automaticamente.
- Para adicionar uma foto profissional na seção "Sobre", substitua o placeholder `[Espaço para foto profissional da Ana Cristina]` por uma tag `<img>` apontando para a imagem.
- Os depoimentos e artigos do blog estão com placeholders e podem ser preenchidos posteriormente.
