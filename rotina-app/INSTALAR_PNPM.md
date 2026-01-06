# 📦 Instalar pnpm

## Opção 1: Instalar pnpm (Recomendado)

### macOS (Homebrew)
```bash
brew install pnpm
```

### Ou via npm
```bash
npm install -g pnpm
```

### Ou via curl
```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

Depois reinicie o terminal ou execute:
```bash
source ~/.zshrc
```

---

## Opção 2: Usar npx (Sem instalar)

Se não quiser instalar pnpm, pode usar npx:

```bash
# Na raiz do projeto (rotina-app)
npx pnpm install
npx pnpm dev
```

---

## Opção 3: Usar npm (Alternativa)

Se preferir usar npm:

```bash
# Instalar dependências
npm install

# Iniciar app (precisa ajustar scripts)
cd apps/web
npm run dev
```

---

## Verificar Instalação

Após instalar, verifique:

```bash
pnpm --version
```

Deve mostrar a versão (ex: `8.x.x`)

---

## Depois de Instalar pnpm

```bash
# Você já está em rotina-app, então:
pnpm install
pnpm dev
```

---

## Comandos Corretos

Como você já está em `rotina-app`, execute:

```bash
# 1. Instalar pnpm (se ainda não instalou)
brew install pnpm
# ou
npm install -g pnpm

# 2. Instalar dependências
pnpm install

# 3. Iniciar app
pnpm dev
```

**Não precisa fazer `cd rotina-app` novamente!**







