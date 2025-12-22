# 🚀 Iniciar Backend Local

## ❌ Problema

Erro: `ERR_CONNECTION_REFUSED` na porta 8001

**Causa:** O backend não está rodando.

---

## ✅ Solução: Iniciar o Backend

### Passo 1: Navegar para o diretório do backend

```bash
cd /Users/cesark/site-temvenda/backend
```

### Passo 2: Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

Se o ambiente virtual não existir, crie:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Passo 3: Iniciar o servidor

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

O `--reload` faz o servidor reiniciar automaticamente quando você modificar arquivos.

---

## ✅ Verificar se Está Funcionando

### Teste 1: Verificar processo

Em outro terminal:

```bash
lsof -i :8001
```

Deve mostrar um processo Python rodando.

### Teste 2: Testar endpoint de health

```bash
curl http://localhost:8001/health
```

Deve retornar:
```json
{
  "status": "ok",
  "api": "running",
  "database": "ok",
  ...
}
```

### Teste 3: Testar no navegador

Acesse: `http://localhost:8001/health`

Deve mostrar o JSON acima.

---

## 🧪 Testar Login no Frontend

Após o backend estar rodando:

1. Acesse `http://localhost:8000/caixa/`
2. Digite a senha configurada em `APP_PASSWORD` no `.env`
3. Clique em "Entrar"
4. Deve funcionar! ✅

---

## 📋 Checklist

- [ ] Backend rodando na porta 8001
- [ ] `/health` retorna `{"status":"ok"}`
- [ ] Login funciona no frontend
- [ ] "Atualizar Fluxo" funciona

---

## 🆘 Problemas Comuns

### Problema: "Port already in use"

**Solução:**
```bash
# Encontrar processo na porta 8001
lsof -i :8001

# Matar o processo (substitua PID pelo número)
kill -9 PID
```

### Problema: "Module not found"

**Solução:**
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

### Problema: "No such file or directory: .venv"

**Solução:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 💡 Dica: Script de Inicialização Rápida

Você pode criar um script para facilitar:

```bash
#!/bin/bash
# start-backend.sh

cd /Users/cesark/site-temvenda/backend

# Ativar venv
source .venv/bin/activate

# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Torne executável:
```bash
chmod +x start-backend.sh
```

Execute:
```bash
./start-backend.sh
```

