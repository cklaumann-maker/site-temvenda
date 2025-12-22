# 🧪 Como Testar no Localhost - Módulo Financeiro

## ⚠️ Mudança de Nome: Sem Implicação Técnica

A mudança de `financeiro/` para `caixa/` **NÃO tem implicação técnica** porque:
- ✅ Caminhos são **relativos** (`config-api.js` na mesma pasta)
- ✅ Não há referências hardcoded ao nome da pasta
- ✅ Funciona igual, só muda o nome da URL

---

## 🚀 Como Testar no Localhost

### Passo 1: Verificar Estrutura

Certifique-se de que os arquivos estão assim:

```
site-temvenda/
└── caixa/
    ├── index.html      ← Deve estar aqui
    └── config-api.js   ← Deve estar aqui
```

**Verificar:**
```bash
cd /Users/cesark/site-temvenda
ls -la caixa/
```

Deve mostrar ambos os arquivos.

---

### Passo 2: Iniciar Servidor HTTP

**⚠️ IMPORTANTE:** Não abra o arquivo diretamente (`file://`). Use um servidor HTTP!

**Opção A: Python (Recomendado)**
```bash
cd /Users/cesark/site-temvenda
python3 -m http.server 8000
```

**Opção B: Node.js (se tiver)**
```bash
cd /Users/cesark/site-temvenda
npx http-server -p 8000
```

---

### Passo 3: Acessar no Navegador

**URL correta:**
```
http://localhost:8000/caixa/
```

ou

```
http://localhost:8000/caixa/index.html
```

**⚠️ NÃO use:**
- ❌ `file:///Users/cesark/site-temvenda/caixa/index.html` (não funciona)
- ❌ `http://localhost:8000/financeiro/` (pasta antiga não existe mais)

---

## ❌ Problemas Comuns

### Problema 1: "config-api.js não encontrado"

**Causa:** Arquivos não estão na mesma pasta

**Solução:**
```bash
# Verificar estrutura
ls -la caixa/

# Deve mostrar:
# index.html
# config-api.js
```

### Problema 2: "404 Not Found" no localhost

**Causa:** Servidor iniciado na pasta errada ou URL incorreta

**Solução:**
1. Certifique-se de estar na raiz: `cd /Users/cesark/site-temvenda`
2. Inicie o servidor: `python3 -m http.server 8000`
3. Acesse: `http://localhost:8000/caixa/` (não `/financeiro/`)

### Problema 3: Erro de CORS no Console

**Causa:** Tentando acessar API de `http://localhost:8000` mas API está em `https://...`

**Solução:**
- ✅ Isso é normal! A API está no Render (HTTPS)
- ✅ O frontend pode estar em localhost (HTTP)
- ✅ O Render está configurado para aceitar qualquer origem (`allow_origins=["*"]`)
- ✅ Deve funcionar mesmo assim

---

## ✅ Checklist

- [ ] Estrutura: `caixa/index.html` e `caixa/config-api.js` na mesma pasta
- [ ] Servidor iniciado na raiz (`site-temvenda/`)
- [ ] Acessando via `http://localhost:8000/caixa/` (não `file://`)
- [ ] Console mostra `window.FINANCE_API_URL` com a URL do Render
- [ ] Página carrega sem erro de arquivos não encontrados

---

## 🎯 Teste Rápido

1. **Verificar arquivos:**
   ```bash
   cd /Users/cesark/site-temvenda
   ls caixa/
   ```
   Deve mostrar: `index.html` e `config-api.js`

2. **Iniciar servidor:**
   ```bash
   python3 -m http.server 8000
   ```

3. **Acessar:**
   ```
   http://localhost:8000/caixa/
   ```

4. **Verificar Console (F12):**
   - Digite: `window.FINANCE_API_URL`
   - Deve retornar: `"https://temvenda-finance-api.onrender.com"`

---

## 💡 Importante

**A mudança de nome não afeta nada tecnicamente!**

- Antes: `http://localhost:8000/financeiro/`
- Agora: `http://localhost:8000/caixa/`

**Só muda a URL, o código funciona igual!**

---

## 🆘 Se Ainda Não Funcionar

1. **Verificar se o servidor está rodando:**
   - Deve aparecer: `Serving HTTP on 0.0.0.0 port 8000`

2. **Verificar se está na pasta certa:**
   ```bash
   pwd
   # Deve mostrar: /Users/cesark/site-temvenda
   ```

3. **Verificar estrutura:**
   ```bash
   ls -la caixa/
   # Deve mostrar index.html e config-api.js
   ```

4. **Testar acesso direto ao arquivo:**
   ```
   http://localhost:8000/caixa/config-api.js
   ```
   - Deve mostrar o conteúdo do arquivo
   - Se der 404 → arquivo não está na pasta certa

