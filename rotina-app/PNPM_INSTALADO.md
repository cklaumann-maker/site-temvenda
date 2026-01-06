# ✅ pnpm Instalado

## Próximos Passos

Após instalar o pnpm via script, você precisa:

### 1. Recarregar o shell

```bash
source ~/.zshrc
```

Ou simplesmente feche e abra um novo terminal.

### 2. Verificar instalação

```bash
pnpm --version
```

Deve mostrar algo como: `8.x.x` ou `9.x.x`

### 3. Instalar dependências do projeto

```bash
# Você já está em rotina-app
pnpm install
```

### 4. Iniciar aplicativo

```bash
pnpm dev
```

---

## Se ainda não funcionar

Se após recarregar o shell o `pnpm` ainda não for encontrado, adicione manualmente ao seu `~/.zshrc`:

```bash
echo 'export PNPM_HOME="$HOME/.local/share/pnpm"' >> ~/.zshrc
echo 'export PATH="$PNPM_HOME:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Alternativa: Usar npx (sem instalar globalmente)

Se preferir não instalar globalmente:

```bash
npx pnpm install
npx pnpm dev
```







