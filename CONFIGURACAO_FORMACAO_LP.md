# 📋 Configuração da Página Formação LP

## ✅ Implementações Realizadas

### 1. **Salvamento no Funil** ✅
- O formulário agora salva corretamente os leads na tabela `leads_funnel` do Supabase
- Campo `source` definido como `'formacao-lp'` para identificação
- Fallback automático: SDK → REST API se necessário

### 2. **Envio de E-mail** ✅
- Integração com EmailJS configurada
- E-mail automático enviado ao lead após cadastro
- Template configurável via `email-config.js`

### 3. **Integração WhatsApp** ✅
- Opção 1: Link direto para conversa (mensagem pré-formatada)
- Opção 2: Link para grupo (configurável)

### 4. **Rastreamento GA4** ✅
- Evento `generate_lead` rastreado automaticamente
- Parâmetros: `lead_source`, `lead_type`, `page_path`

---

## 🔧 Como Configurar o Grupo WhatsApp

### Método 1: Criar Link de Grupo

1. **Criar um grupo no WhatsApp:**
   - Abra o WhatsApp
   - Vá em "Novo grupo"
   - Adicione pelo menos 1 contato (você mesmo ou um número temporário)
   - Nomeie o grupo (ex: "Formação de Líderes - TEM VENDA")
   - Crie o grupo

2. **Obter o link do grupo:**
   - Abra o grupo criado
   - Toque no nome do grupo no topo
   - Role até "Link do grupo" ou "Convidar para grupo via link"
   - Copie o link (formato: `https://chat.whatsapp.com/XXXXXXXXXXXXX`)

3. **Configurar no código:**
   - Abra o arquivo `formacao-lp.html`
   - Localize a linha: `window.WHATSAPP_GROUP_LINK = '';`
   - Cole o link entre as aspas:
     ```javascript
     window.WHATSAPP_GROUP_LINK = 'https://chat.whatsapp.com/XXXXXXXXXXXXX';
     ```

### Método 2: Usar Link Direto (Conversa Individual)

Se preferir que cada lead receba uma mensagem individual, deixe o campo vazio:
```javascript
window.WHATSAPP_GROUP_LINK = ''; // Vazio = mensagem direta
```

Neste caso, será aberta uma conversa individual com mensagem pré-formatada.

---

## 📧 Configuração do E-mail (EmailJS)

O e-mail está configurado via `email-config.js`. Para personalizar:

1. **Acesse:** https://www.emailjs.com/
2. **Configure o template** com as variáveis:
   - `{{to_email}}` - E-mail do destinatário
   - `{{to_name}}` - Nome do destinatário
   - `{{subject}}` - Assunto do e-mail
   - `{{message}}` - Mensagem do e-mail
   - `{{lead_name}}` - Nome do lead
   - `{{lead_email}}` - E-mail do lead
   - `{{lead_phone}}` - Telefone do lead

3. **Atualize `email-config.js`** se necessário:
   ```javascript
   window.EMAILJS_CONFIG = {
       publicKey: 'SUA_PUBLIC_KEY',
       serviceId: 'SEU_SERVICE_ID',
       templateId: 'SEU_TEMPLATE_ID'
   };
   ```

---

## 📊 Verificar Leads no Funil

1. Acesse: `https://temvenda.com.br/stats.html`
2. Clique na aba **"Funil"** (ou acesse `admin-funil.html`)
3. Os leads aparecerão na coluna **"Entrada"** com `source: formacao-lp`

---

## 🧪 Testar

1. Preencha o formulário em `formacao-lp.html`
2. Verifique no console do navegador (F12):
   - ✅ `💾 Salvando lead no funil...`
   - ✅ `✅ Lead salvo via SDK:` ou `✅ Lead salvo via REST API:`
   - ✅ `📧 Enviando e-mail...`
   - ✅ `✅ E-mail enviado com sucesso para:`
   - ✅ `📱 Abrindo WhatsApp direto` ou `📱 Redirecionando para grupo WhatsApp`

3. Verifique no Supabase:
   - Tabela `leads_funnel` deve ter um novo registro
   - Campo `source` = `'formacao-lp'`

4. Verifique o e-mail:
   - Lead deve receber e-mail de confirmação

5. Verifique WhatsApp:
   - Deve abrir conversa ou grupo conforme configurado

---

## ⚠️ Troubleshooting

### Lead não aparece no funil:
- Verifique console do navegador (F12) para erros
- Verifique se a tabela `leads_funnel` existe no Supabase
- Verifique permissões RLS no Supabase (deve permitir INSERT para `anon`)

### E-mail não enviado:
- Verifique se `email-config.js` está carregado
- Verifique configuração do EmailJS
- Verifique console para erros (não bloqueia o fluxo)

### WhatsApp não abre:
- Verifique se bloqueador de pop-up está desativado
- Verifique formato do link do grupo (deve começar com `https://chat.whatsapp.com/`)

---

## 📝 Notas Importantes

- O campo `phone` é salvo sem caracteres especiais (apenas números)
- O campo `source` identifica a origem do lead: `'formacao-lp'`
- O evento GA4 `generate_lead` é rastreado automaticamente
- O e-mail é enviado de forma assíncrona (não bloqueia o fluxo se falhar)

---

✅ **Tudo configurado!** Faça upload do arquivo `formacao-lp.html` atualizado para o servidor.

