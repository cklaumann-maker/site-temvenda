# Upload FTP - AXIS Club

## Arquivos para subir no FTP — Produção

Use a estrutura abaixo no servidor. Os caminhos são relativos à **raiz do site** (pasta pública do FTP, ex.: `public_html` ou `htdocs`).

---

## 1. Pasta do projeto

| Arquivo           | Caminho no FTP                    | Obrigatório |
|-------------------|-----------------------------------|-------------|
| index.html        | **projetos/axis/index.html**      | Sim (página principal) |
| logo.png          | **projetos/axis/logo.png**        | Opcional (logo/foto do fundador) |

---

## 2. Estrutura final no servidor

```
[raiz do site]/
└── projetos/
    └── axis/
        ├── index.html
        └── logo.png (opcional - foto do fundador)
```

---

## 3. Lista resumida

1. **projetos/axis/index.html** → dentro de `projetos/axis`  
2. **projetos/axis/logo.png** → dentro de `projetos/axis` (opcional - foto do fundador)

---

## 4. Ordem sugerida no FTP

1. Criar pasta **projetos/axis** (se não existir).  
2. Subir **index.html** em **projetos/axis/**.  
3. (Opcional) Subir **logo.png** (foto do fundador) em **projetos/axis/**.

Depois disso, o projeto deve abrir em `https://seusite.com/projetos/axis/`.

---

## 5. Observações

- O design é minimalista e institucional
- Cores: verde #5ee100, preto, branco e cinza
- Placeholder para foto do fundador na seção "Quem Lidera"
- CTA configurado para link "#" (deve ser ajustado para URL real de avaliação)
- Diagrama de Venn/orbital dos pilares criado com CSS puro
