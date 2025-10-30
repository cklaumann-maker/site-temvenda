# 📱 Guia - Sistema de Captura de Leads Instagram

## Visão Geral
Sistema completo de captura de leads para Instagram com:
- Página de captura responsiva e otimizada
- Gerenciamento de conteúdo via admin
- Integração com funil de vendas
- Envio automático de PDF por e-mail
- Notificações no admin

## 🚀 Configuração Inicial

### 1. Configurar Supabase
1. Acesse [supabase.com](https://supabase.com) e crie um projeto
2. Vá em **Settings > API**
3. Copie a **URL** e **anon key**
4. Edite o arquivo `supabase-config.js`:
```javascript
window.SUPABASE_CONFIG = {
    url: 'SUA_URL_AQUI',
    anonKey: 'SUA_CHAVE_AQUI'
};
```

### 2. Configurar Banco de Dados
Execute o SQL no Supabase (já foi criado anteriormente):
```sql
-- Tabela leads_funnel já existe
-- Tabela lead_activities já existe
```

### 3. Configurar E-mail (Opcional)
Para envio automático de PDF, integre com:
- **EmailJS** (gratuito, fácil)
- **SendGrid** (profissional)
- **AWS SES** (escalável)

## 📋 Como Usar

### 1. Configurar Página de Captura
1. Acesse `/admin-stats.html`
2. Vá para seção **"Página de Captura Instagram"**
3. Preencha os textos:
   - Título Principal
   - Subtítulo
   - 4 Benefícios
   - Texto do Botão
4. Clique em **"Salvar Configurações"**

### 2. Upload do E-book PDF
1. Na mesma seção, clique em **"Selecionar PDF"**
2. Escolha seu e-book em PDF
3. O arquivo será salvo automaticamente

### 3. Testar a Página
1. Acesse `/instagram` para ver a página
2. Teste o formulário de cadastro
3. Verifique se o lead aparece no funil de vendas

## 🔧 Funcionalidades

### Página de Captura (`/instagram`)
- ✅ Design responsivo e Instagram-friendly
- ✅ Formulário com validação (nome, e-mail, telefone)
- ✅ Carregamento dinâmico de textos do admin
- ✅ Integração com Supabase
- ✅ Envio automático para funil de vendas
- ✅ Feedback visual (loading, sucesso, erro)

### Admin (`/admin-stats.html`)
- ✅ Edição de todos os textos da página
- ✅ Upload e gerenciamento de PDF
- ✅ Preview da página em tempo real
- ✅ Salvamento em localStorage

### Integração com Funil
- ✅ Leads vão direto para estágio "ENTRADA"
- ✅ Source marcado como "instagram"
- ✅ Score inicial de 5/10
- ✅ Data de último contato registrada

## 📊 Monitoramento

### Ver Leads Capturados
1. Acesse `/admin-funil.html`
2. Filtre por source "instagram"
3. Monitore conversões e follow-ups

### Estatísticas
- Total de leads por fonte
- Taxa de conversão
- Leads atrasados (sem contato há 7+ dias)

## 🎨 Personalização

### Cores e Visual
A página usa as cores padrão do site TEM VENDA:
- Azul: `#667eea`
- Roxo: `#764ba2`
- Gradiente de fundo

### Textos Editáveis
Todos os textos são editáveis via admin:
- Título principal
- Subtítulo
- 4 benefícios
- Texto do botão

## 🔒 Segurança

### Validações
- ✅ Campos obrigatórios
- ✅ Formato de e-mail
- ✅ Telefone mínimo 10 dígitos
- ✅ Sanitização de dados

### Dados
- ✅ Salvos no Supabase (banco seguro)
- ✅ Configurações em localStorage
- ✅ PDF em base64 (localStorage)

## 🚨 Solução de Problemas

### Lead não aparece no funil
1. Verifique as credenciais do Supabase
2. Confirme se a tabela `leads_funnel` existe
3. Verifique o console do navegador

### PDF não é enviado
1. Verifique se o PDF foi carregado no admin
2. Configure serviço de e-mail
3. Verifique logs do console

### Página não carrega textos
1. Verifique se salvou as configurações no admin
2. Limpe o cache do navegador
3. Verifique localStorage

## 📈 Próximos Passos

### Melhorias Sugeridas
1. **Integração de E-mail Real**
   - EmailJS para envio automático
   - Templates de e-mail personalizados

2. **Analytics**
   - Google Analytics
   - Pixel do Facebook
   - Tracking de conversões

3. **A/B Testing**
   - Múltiplas versões da página
   - Teste de diferentes textos

4. **Automação**
   - Sequência de e-mails
   - Notificações no WhatsApp
   - Integração com CRM

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este guia
2. Consulte os logs do console
3. Teste em ambiente local primeiro

---

**Sistema criado para TEM VENDA** 🚀
