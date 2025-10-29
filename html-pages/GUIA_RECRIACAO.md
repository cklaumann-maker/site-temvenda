# 📋 Guia para Recriar Páginas no Elementor

## 🎯 Objetivo
Recriar todas as páginas do site TemVenda usando o Elementor, garantindo que funcionem perfeitamente.

## 📁 Arquivos HTML Extraídos
- `diagnostico.html` - Página de diagnóstico interativo
- `home.html` - Página inicial
- `consultoria.html` - Página de consultoria
- `formacao.html` - Página de formação
- `incompany.html` - Página incompany

## 🚀 Passo a Passo

### 1. **Instalar Tema Compatível com Elementor**
1. Acesse: `http://localhost:8080/wp-admin`
2. Vá em **Aparência > Temas**
3. Clique em **Adicionar novo**
4. Procure por **"Hello Elementor"**
5. Instale e ative o tema

### 2. **Recriar Página de Diagnóstico**
1. Vá em **Páginas > Todas as páginas**
2. Clique em **"DIAGNOSTICO"** para editar
3. Clique em **"Editar com Elementor"**
4. **Delete todo o conteúdo** atual
5. Adicione um **Widget HTML**
6. **Cole o conteúdo** do arquivo `diagnostico.html`
7. Clique em **Atualizar**

### 3. **Recriar Página Home**
1. Vá em **Páginas > Todas as páginas**
2. Clique em **"TEM VENDA - home"** para editar
3. Clique em **"Editar com Elementor"**
4. **Delete todo o conteúdo** atual
5. Adicione um **Widget HTML**
6. **Cole o conteúdo** do arquivo `home.html`
7. Clique em **Atualizar**

### 4. **Recriar Demais Páginas**
Repita o processo para:
- **Consultoria** (`consultoria.html`)
- **Formação** (`formacao.html`)
- **Incompany** (`incompany.html`)

### 5. **Configurar Menu de Navegação**
1. Vá em **Aparência > Menus**
2. Crie um menu principal
3. Adicione as páginas criadas
4. Atribua o menu ao local correto

## 🔧 Dicas Importantes

### **Para Widget HTML:**
- Sempre use **Widget HTML** para conteúdo complexo
- O HTML já está pronto e funcional
- Não precisa editar o código

### **Para CSS Personalizado:**
- Se precisar ajustar estilos, vá em **Elementor > Personalizar**
- Ou use **Elementor > Código Personalizado**

### **Para JavaScript:**
- O JavaScript já está incluído no HTML
- Não precisa de configuração adicional

## ✅ Verificação Final

Após recriar todas as páginas:

1. **Teste cada página:**
   - `http://localhost:8080/` (home)
   - `http://localhost:8080/diagnostico`
   - `http://localhost:8080/consultoria`
   - `http://localhost:8080/formacao-lideres-de-farmacia`
   - `http://localhost:8080/incompany`

2. **Verifique se:**
   - Todas as páginas carregam corretamente
   - O diagnóstico funciona (formulário interativo)
   - Os links de navegação funcionam
   - O design está correto

## 🚨 Troubleshooting

### **Se a página não carregar:**
- Verifique se o tema "Hello Elementor" está ativo
- Limpe o cache: **Elementor > Ferramentas > Regenerar CSS**

### **Se o JavaScript não funcionar:**
- Verifique se o HTML está completo no Widget HTML
- Não quebre o código ao colar

### **Se o design estiver quebrado:**
- Use **Elementor > Ferramentas > Regenerar CSS e dados**
- Verifique se não há conflitos de CSS

## 📝 Próximos Passos

Após recriar todas as páginas:

1. **Fazer commit do projeto:**
   ```bash
   git add .
   git commit -m "Páginas recriadas no Elementor"
   ```

2. **Configurar deploy** para produção

3. **Documentar alterações** futuras

---

**💡 Dica:** Mantenha os arquivos HTML como backup para futuras referências!
