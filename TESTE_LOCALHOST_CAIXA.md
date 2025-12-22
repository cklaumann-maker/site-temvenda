# 🧪 Como Testar no Localhost

## 📍 Estrutura Local

Para testar no localhost, você precisa manter a mesma estrutura que no servidor:

```
site-temvenda/
└── caixa/
    ├── index.html
    └── config-api.js
```

---

## 🚀 Testar no Localhost

### Opção 1: Servidor Python (Recomendado)

1. **Navegue até a pasta do projeto:**
   ```bash
   cd /Users/cesark/site-temvenda
   ```

2. **Inicie o servidor:**
   ```bash
   python3 -m http.server 8000
   ```

3. **Acesse no navegador:**
   ```
   http://localhost:8000/caixa/
   ```
   ou
   ```
   http://localhost:8000/caixa/index.html
   ```

### Opção 2: Servidor Node.js (se tiver instalado)

```bash
npx http-server -p 8000
```

Acesse: `http://localhost:8000/caixa/`

---

## ⚠️ Importante: Caminhos Relativos

O arquivo `index.html` usa caminhos relativos:
- `<script src="config-api.js">` → procura na mesma pasta

**Isso significa:**
- ✅ Se `index.html` está em `/caixa/index.html`
- ✅ `config-api.js` deve estar em `/caixa/config-api.js`
- ✅ Ambos na mesma pasta = funciona!

---

## 🔍 Verificar Estrutura

### No Seu Computador:

```
site-temvenda/
├── caixa/
│   ├── index.html      ← Deve estar aqui
│   └── config-api.js   ← Deve estar aqui
└── (outros arquivos...)
```

### No Servidor (htdocs/):

```
htdocs/
└── caixa/
    ├── index.html      ← Deve estar aqui
    └── config-api.js   ← Deve estar aqui
```

**A estrutura deve ser IDÊNTICA!**

---

## ❌ Problemas Comuns

### Problema 1: Arquivos em Pastas Diferentes

**Erro:** `Failed to load resource: config-api.js`

**Causa:** `index.html` e `config-api.js` não estão na mesma pasta

**Solução:**
- Verificar se ambos estão em `caixa/`
- Verificar se a estrutura está correta

### Problema 2: Servidor Não Está na Pasta Certa

**Erro:** 404 ao acessar `/caixa/`

**Causa:** Servidor iniciado na pasta errada

**Solução:**
```bash
# Certifique-se de estar na raiz do projeto
cd /Users/cesark/site-temvenda

# Inicie o servidor
python3 -m http.server 8000

# Acesse: http://localhost:8000/caixa/
```

### Problema 3: Caminho Absoluto vs Relativo

**Se você abrir o arquivo diretamente:**
- ❌ `file:///Users/cesark/site-temvenda/caixa/index.html`
- ❌ Pode dar erro de CORS ou caminhos

**Use sempre um servidor HTTP:**
- ✅ `http://localhost:8000/caixa/index.html`

---

## ✅ Checklist para Localhost

- [ ] Estrutura: `caixa/index.html` e `caixa/config-api.js` na mesma pasta
- [ ] Servidor iniciado na raiz do projeto (`site-temvenda/`)
- [ ] Acessando via `http://localhost:8000/caixa/` (não `file://`)
- [ ] Console mostra `window.FINANCE_API_URL` com a URL correta
- [ ] Página carrega sem erros de arquivos não encontrados

---

## 🎯 Teste Rápido

1. **Verificar estrutura:**
   ```bash
   ls -la caixa/
   ```
   Deve mostrar: `index.html` e `config-api.js`

2. **Iniciar servidor:**
   ```bash
   cd /Users/cesark/site-temvenda
   python3 -m http.server 8000
   ```

3. **Acessar:**
   ```
   http://localhost:8000/caixa/
   ```

4. **Verificar console (F12):**
   - Não deve ter erro de `config-api.js` não encontrado
   - `window.FINANCE_API_URL` deve retornar a URL

---

## 💡 Dica

Se você estava testando de `financeiro/` antes, agora precisa usar `caixa/`:

**Antes:**
```
http://localhost:8000/financeiro/
```

**Agora:**
```
http://localhost:8000/caixa/
```

A mudança de nome **não tem implicação técnica** - os caminhos são relativos, então funciona igual. Só precisa usar o novo nome da pasta!

