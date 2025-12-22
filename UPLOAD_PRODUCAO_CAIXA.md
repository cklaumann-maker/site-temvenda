# 📤 Upload para Produção - Módulo Caixa

## 🎯 Arquivos Modificados

Com as últimas mudanças, apenas **1 arquivo** precisa ser enviado para produção:

### ✅ Arquivo Principal

```
caixa/index.html
```

---

## 📋 Instruções de Upload via FTP

### 1️⃣ Conecte-se ao servidor FTP

- **Host:** `ftp.temvenda.com.br` (ou o host fornecido pelo InfinityFree)
- **Usuário:** Seu usuário FTP
- **Senha:** Sua senha FTP
- **Porta:** 21 (padrão)

### 2️⃣ Navegue até a pasta correta

No servidor FTP, navegue até:
```
/htdocs/caixa/
```

**OU** (dependendo da estrutura do seu servidor):
```
/public_html/caixa/
```

### 3️⃣ Faça upload do arquivo

1. **Localize o arquivo local:**
   ```
   /Users/cesark/site-temvenda/caixa/index.html
   ```

2. **Faça upload para:**
   ```
   /htdocs/caixa/index.html
   ```

3. **Substitua o arquivo existente** (se solicitado)

---

## ✅ Verificação Pós-Upload

Após o upload, teste:

1. **Acesse:** `https://www.temvenda.com.br/caixa/`
2. **Faça login** (se necessário)
3. **Verifique:**
   - ✅ Login funciona corretamente
   - ✅ Carregamento do mês funciona
   - ✅ Seleção de dia na tabela funciona
   - ✅ Aba "Despesas" mostra o dia correto (não o dia anterior)
   - ✅ Se o token expirar, redireciona para login automaticamente

---

## 🔍 Mudanças Implementadas

As últimas correções incluem:

1. ✅ **Correção de sintaxe:** `await` em função `async`
2. ✅ **Correção de data:** Despesas agora mostram o dia correto (não o anterior)
3. ✅ **Tratamento de token expirado:** Redirecionamento automático para login quando token expira (erro 401)

---

## 📝 Notas Importantes

- ⚠️ **Backup:** Recomenda-se fazer backup do arquivo atual antes de substituir
- ⚠️ **Cache:** Após o upload, limpe o cache do navegador (`Ctrl+F5` ou `Cmd+Shift+R`)
- ⚠️ **Teste:** Sempre teste em produção após o upload

---

## 🚀 Comando Rápido (se usar cliente FTP via linha de comando)

```bash
# Exemplo com lftp (se instalado)
lftp -u usuario,senha ftp.temvenda.com.br -e "cd htdocs/caixa; put caixa/index.html; quit"
```

---

## 📞 Suporte

Se encontrar problemas após o upload:
1. Verifique os logs do console do navegador (F12)
2. Verifique se o arquivo foi enviado corretamente
3. Limpe o cache do navegador
4. Teste em modo anônimo/privado

