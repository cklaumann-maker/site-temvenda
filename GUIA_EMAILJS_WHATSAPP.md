# 📧 Guia: Configurar E-mail com Link do Grupo WhatsApp no EmailJS

## 📋 Objetivo

Configurar um template no EmailJS para enviar automaticamente um e-mail aos leads da Formação LP contendo o link para entrar no grupo exclusivo do WhatsApp.

---

## 🔧 Passo a Passo

### 1. Obter Link do Grupo WhatsApp

1. Abra o WhatsApp no celular ou computador
2. Crie um grupo ou abra um grupo existente
3. Toque/clique no nome do grupo no topo
4. Role até encontrar **"Link do grupo"** ou **"Convidar para grupo via link"**
5. Copie o link (formato: `https://chat.whatsapp.com/XXXXXXXXXXXXX`)

### 2. Configurar Link no Código

1. Abra o arquivo `formacao-lp.html`
2. Localize a linha (aproximadamente linha 213):
   ```javascript
   window.WHATSAPP_GROUP_LINK = '';
   ```
3. Cole o link entre as aspas:
   ```javascript
   window.WHATSAPP_GROUP_LINK = 'https://chat.whatsapp.com/SEU_LINK_AQUI';
   ```

### 3. Criar Template no EmailJS

1. **Acesse:** https://www.emailjs.com/
2. Faça login na sua conta
3. Vá em **"Email Templates"** no menu lateral
4. Clique em **"Create New Template"**

### 4. Configurar Template

#### **Configurações Básicas:**
- **Template Name:** `Formação LP - Grupo WhatsApp`
- **Subject:** `Bem-vindo à Formação de Líderes - Acesse nosso grupo exclusivo!`

#### **Corpo do E-mail (HTML):**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Verdana, Geneva, Tahoma, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    
    <div style="background: linear-gradient(135deg, #5ee100 0%, #4bc800 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
        <h1 style="font-family: Verdana, Geneva, Tahoma, sans-serif; color: #000; margin: 0; font-size: 28px;">🎓 Formação de Líderes</h1>
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; color: #000; margin: 10px 0 0 0; font-size: 16px;">TEM VENDA</p>
    </div>
    
    <div style="background: #fff; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 10px 10px;">
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-size: 16px; margin-bottom: 20px;">
            Olá <strong style="font-family: Verdana, Geneva, Tahoma, sans-serif;">{{to_name}}</strong>,
        </p>
        
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-size: 15px; margin-bottom: 20px;">
            Obrigado pelo seu interesse na <strong style="font-family: Verdana, Geneva, Tahoma, sans-serif;">Formação de Líderes</strong> da TEM VENDA!
        </p>
        
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-size: 15px; margin-bottom: 20px;">
            Para continuar sua jornada e fazer parte da nossa <strong style="font-family: Verdana, Geneva, Tahoma, sans-serif;">comunidade exclusiva</strong>, clique no botão abaixo para entrar no grupo do WhatsApp:
        </p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{whatsapp_group_link}}" 
               style="font-family: Verdana, Geneva, Tahoma, sans-serif;
                      background: #25D366; 
                      color: #fff; 
                      padding: 15px 30px; 
                      text-decoration: none; 
                      border-radius: 8px; 
                      font-weight: bold; 
                      font-size: 16px; 
                      display: inline-block;
                      box-shadow: 0 4px 8px rgba(37, 211, 102, 0.3);">
                📱 Entrar no Grupo do WhatsApp
            </a>
        </div>
        
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-size: 14px; color: #666; margin-top: 30px;">
            Ou copie e cole este link no seu navegador:<br>
            <a href="{{whatsapp_group_link}}" style="font-family: Verdana, Geneva, Tahoma, sans-serif; color: #5ee100; word-break: break-all;">{{whatsapp_group_link}}</a>
        </p>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px;">
            <h3 style="font-family: Verdana, Geneva, Tahoma, sans-serif; margin-top: 0; color: #333; font-size: 18px;">No grupo você receberá:</h3>
            <ul style="font-family: Verdana, Geneva, Tahoma, sans-serif; margin: 10px 0; padding-left: 20px; color: #555;">
                <li style="font-family: Verdana, Geneva, Tahoma, sans-serif;">✅ Avisos sobre as aulas</li>
                <li style="font-family: Verdana, Geneva, Tahoma, sans-serif;">✅ Ofertas exclusivas</li>
                <li style="font-family: Verdana, Geneva, Tahoma, sans-serif;">✅ Suporte da equipe</li>
                <li style="font-family: Verdana, Geneva, Tahoma, sans-serif;">✅ Networking com outros participantes</li>
            </ul>
        </div>
        
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-size: 14px; color: #666; margin-top: 30px; border-top: 1px solid #e0e0e0; padding-top: 20px;">
            Se você não se inscreveu na Formação de Líderes, por favor ignore este e-mail.
        </p>
        
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-size: 14px; color: #999; margin-top: 20px;">
            Atenciosamente,<br>
            <strong style="font-family: Verdana, Geneva, Tahoma, sans-serif;">Equipe TEM VENDA</strong>
        </p>
    </div>
    
    <div style="text-align: center; margin-top: 20px; padding: 20px; color: #999; font-size: 12px;">
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif;">© 2024 TEM VENDA - Gestão Comercial Humanizada</p>
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif;">Este é um e-mail automático, por favor não responda.</p>
    </div>
    
</body>
</html>
```

#### **Variáveis do Template:**

O template usa as seguintes variáveis que serão preenchidas automaticamente:

- `{{to_name}}` - Nome do destinatário
- `{{to_email}}` - E-mail do destinatário
- `{{whatsapp_group_link}}` - Link do grupo WhatsApp
- `{{whatsapp_link}}` - Link alternativo (mesmo valor)
- `{{lead_name}}` - Nome do lead
- `{{lead_email}}` - E-mail do lead
- `{{lead_phone}}` - Telefone do lead

### 5. Salvar Template e Obter ID

1. Clique em **"Save"** para salvar o template
2. Copie o **Template ID** (aparece após salvar, formato: `template_xxxxxxx`)

### 6. Configurar Template ID no Código

1. Abra o arquivo `email-config.js`
2. Localize a linha:
   ```javascript
   whatsappTemplateId: '' // Template para envio do link do grupo WhatsApp (configure aqui)
   ```
3. Cole o Template ID entre as aspas:
   ```javascript
   whatsappTemplateId: 'template_xxxxxxx' // Substitua pelo seu Template ID
   ```

---

## ✅ Verificação

### Teste Local:

1. Preencha o formulário em `formacao-lp.html`
2. Verifique no console do navegador (F12):
   - ✅ `📧 Enviando e-mail com link do grupo WhatsApp...`
   - ✅ `✅ E-mail com link do WhatsApp enviado com sucesso para:`

### Teste Real:

1. Faça upload dos arquivos atualizados
2. Preencha o formulário com um e-mail real
3. Verifique se o e-mail chegou na caixa de entrada
4. Clique no link e verifique se abre o grupo do WhatsApp

---

## 🔍 Troubleshooting

### E-mail não chega:
- Verifique se o Template ID está correto no `email-config.js`
- Verifique se o link do grupo está configurado em `formacao-lp.html`
- Verifique o console do navegador para erros
- Verifique spam/lixo eletrônico

### Link não funciona:
- Verifique se o link do grupo WhatsApp está correto
- O link deve começar com `https://chat.whatsapp.com/`
- Verifique se o grupo ainda está ativo no WhatsApp

### Template não carrega:
- Verifique se o Template ID está correto
- Verifique se as variáveis estão escritas corretamente no template
- Verifique se o Service ID está correto

---

## 📝 Arquivos a Configurar

1. ✅ `formacao-lp.html` - Linha 213: `window.WHATSAPP_GROUP_LINK`
2. ✅ `email-config.js` - Linha 6: `whatsappTemplateId`

---

## 🎯 Resultado Final

Após configurar tudo:
- ✅ Lead preenche formulário
- ✅ Lead recebe mensagem de confirmação na página
- ✅ E-mail automático é enviado com link do grupo WhatsApp
- ✅ Lead clica no link e entra no grupo

**Tudo funcionando automaticamente!** 🚀

