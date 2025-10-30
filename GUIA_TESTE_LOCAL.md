# 🧪 Guia de Teste Local - TEM VENDA

## ✅ Status do Ambiente

- **Docker:** ✅ Rodando
- **WordPress:** ✅ Porta 8080
- **Página Home:** ✅ Acessível (Status 200)

---

## 🌐 URLs para Teste

### **📄 Páginas Principais**

#### **Home**
- **URL:** http://localhost:8080/home-corporativo.html
- **Teste:** Design, navegação, responsividade

#### **Serviços**
- **Consultoria:** http://localhost:8080/wp-content/temvenda/consultoria.html
- **Formação:** http://localhost:8080/wp-content/temvenda/formacao-lideres.html
- **Treinamento:** http://localhost:8080/wp-content/temvenda/treinamento-incompany.html
- **Palestras:** http://localhost:8080/wp-content/temvenda/palestras.html

#### **Recursos**
- **Diagnóstico:** http://localhost:8080/wp-content/temvenda/diagnostico.html
- **Notícias:** http://localhost:8080/wp-content/temvenda/noticias.html

#### **Área Administrativa**
- **Login:** http://localhost:8080/wp-content/temvenda/login-admin.html
- **Painel Notícias:** http://localhost:8080/wp-content/temvenda/admin-panel.html
- **Estatísticas:** http://localhost:8080/wp-content/temvenda/admin-stats.html
- **Usuários:** http://localhost:8080/wp-content/temvenda/admin-users.html

---

## ✅ Checklist de Testes

### **🎨 Design e Layout**

- [ ] **Home Page:**
  - [ ] Fundo branco (design corporativo)
  - [ ] Header translúcido funcionando
  - [ ] Logo carregando corretamente
  - [ ] Navegação responsiva
  - [ ] Footer com botão admin (preto)

- [ ] **Seção Sobre:**
  - [ ] 4 cards de estatísticas apenas
  - [ ] Sem card verde de admin
  - [ ] Informações de Cesar Klaumann corretas

- [ ] **Responsividade:**
  - [ ] Mobile (320px - 768px)
  - [ ] Tablet (768px - 1024px)
  - [ ] Desktop (1024px+)

### **🔗 Links e Navegação**

- [ ] **Links Internos:**
  - [ ] Consultoria → Página correta
  - [ ] Formação → Página correta
  - [ ] Treinamento → Página correta
  - [ ] Palestras → Página correta
  - [ ] Diagnóstico → Página correta
  - [ ] Notícias → Página correta

- [ ] **Botão Admin (Footer):**
  - [ ] Aparece na seção Admin
  - [ ] Fundo preto, texto branco
  - [ ] Link funciona corretamente
  - [ ] Hover effect funciona

- [ ] **Botão Hero:**
  - [ ] "Conhecer Metodologia" → Formação
  - [ ] "Diagnóstico Gratuito" → Diagnóstico

### **📊 Funcionalidades**

- [ ] **Sistema de Notícias:**
  - [ ] Carrega notícias do Supabase
  - [ ] Cards aparecem corretamente
  - [ ] Links funcionam

- [ ] **Estatísticas:**
  - [ ] Carregam do localStorage
  - [ ] Números aparecem corretamente
  - [ ] Animações funcionam

- [ ] **Header:**
  - [ ] Encolhe no scroll
  - [ ] Translúcido funcionando
  - [ ] Links funcionam

### **🔐 Área Administrativa**

- [ ] **Login:**
  - [ ] Página carrega
  - [ ] Formulário funciona
  - [ ] Autenticação funciona

- [ ] **Painéis:**
  - [ ] Painel de Notícias acessível
  - [ ] Estatísticas acessível
  - [ ] Usuários acessível (se tiver permissão)

---

## 🐛 Problemas Comuns e Soluções

### **Erro 404 Not Found**
- Verifique se o arquivo existe em `wordpress/home-corporativo.html`
- Verifique caminhos dos links

### **Imagens não carregam**
- Verifique se `logo-temvenda.png` está na pasta correta
- Verifique caminhos das imagens

### **JavaScript não funciona**
- Abra Console (F12) e verifique erros
- Verifique se `auth-manager.js` está carregando

### **Estilos não aplicam**
- Limpe cache do navegador (Ctrl+Shift+R)
- Verifique se CSS está inline no HTML

---

## 🚀 Iniciar Servidor Local (Alternativa)

Se preferir servir diretamente sem Docker:

```bash
# Navegue até a pasta
cd wordpress

# Servir com Python
python3 -m http.server 8000

# Ou com Node.js
npx http-server -p 8000

# Acesse: http://localhost:8000/home-corporativo.html
```

---

## 📱 Teste em Dispositivos

### **Chrome DevTools:**
1. Abra Chrome
2. F12 → Device Toolbar (Ctrl+Shift+M)
3. Teste diferentes dispositivos

### **Dispositivos para Testar:**
- iPhone SE (375px)
- iPhone 12 Pro (390px)
- iPad (768px)
- Desktop (1920px)

---

## ✅ Pronto para Teste!

**URL Principal:** http://localhost:8080/home-corporativo.html

**Última atualização:** $(date)
