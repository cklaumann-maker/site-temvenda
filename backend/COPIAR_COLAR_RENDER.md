# 📋 Copiar e Colar - Variáveis para Render

Use este guia para copiar e colar as variáveis diretamente no Render.

## 🎯 Como Adicionar no Render

1. No Dashboard do Render, vá até seu serviço
2. Clique em **"Environment"** (no menu lateral)
3. Para cada variável abaixo, clique em **"Add Environment Variable"**
4. Cole o **Key** e o **Value** correspondente
5. Clique em **"Save"**

---

## ✅ Variáveis Prontas (Copiar e Colar)

### 1. ENVIRONMENT
```
Key: ENVIRONMENT
Value: production
```

### 2. APP_PASSWORD
```
Key: APP_PASSWORD
Value: <ESCOLHA_UMA_SENHA_FORTE>
```
⚠️ **Exemplo**: `MinhaSenhaForte123!@#`

### 3. JWT_SECRET_KEY
```
Key: JWT_SECRET_KEY
Value: bl25A1GqcJZSM0-MgdPVJA75FZkzRw4YyI3dokfHHwg
```
✅ **Já gerado!**

### 4. JWT_ACCESS_EXPIRES_HOURS
```
Key: JWT_ACCESS_EXPIRES_HOURS
Value: 8
```

### 5. SUPABASE_URL
```
Key: SUPABASE_URL
Value: <https://seu-projeto.supabase.co>
```
💡 **Onde encontrar**: Supabase Dashboard → Settings → API → Project URL

### 6. SUPABASE_SERVICE_ROLE_KEY
```
Key: SUPABASE_SERVICE_ROLE_KEY
Value: <sua-service-role-key>
```
💡 **Onde encontrar**: Supabase Dashboard → Settings → API → service_role key  
⚠️ **IMPORTANTE**: Use a **service_role** key, NÃO a anon key!

### 7. DRIVE_FILE_ID
```
Key: DRIVE_FILE_ID
Value: <id-do-arquivo-google-drive>
```
💡 **Como encontrar**:
1. Abra o arquivo Excel no Google Drive
2. A URL será: `https://drive.google.com/file/d/ID_AQUI/view`
3. Copie apenas o `ID_AQUI`

### 8. GOOGLE_PROJECTION_FILE_ID
```
Key: GOOGLE_PROJECTION_FILE_ID
Value: <id-do-arquivo-projecao>
```
💡 Mesmo processo do DRIVE_FILE_ID, mas para o arquivo de projeção D+60

### 9. GOOGLE_SERVICE_ACCOUNT_JSON
```
Key: GOOGLE_SERVICE_ACCOUNT_JSON
Value: {"type":"service_account","project_id":"noticias-site-476917","private_key_id":"0e041a32236c91a0764ded5a5dafe311433ca763","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCP9EJ2Vue4mpWK\nhvMgEETlfTWDV+RDgaH8O/uJY8WYqjxHy+PVicQajfdrtssuSw5mHYj78QVJqJY/\niJVL5Vp0dlqO3ph9zGcPZZSD57Ok9Eic6hHeD+TA9q+JK1h8aJhbOhnDfb3Ru6k+\nSPCn101F+ea7dM5K7kfEl4k7XRmN6vUsRSYZlyvGwc9XOILG7tM7+fwEG3oiWwC4\n3h6jrMHPRyRs6HMt8mIh3qwRDBxQDEwJS1cNwwEC1vP3YQ/aHwDG8Fq605rNuBwt\npjj/0NwQeLGlHNPpxqw6juNBbHcLNFbo/j4apphLrq9wpVz9fcctLNh7i92jgoZy\ni+VuI0AhAgMBAAECggEABaXyI1uut01HJ6qWJBdawUHPR7W7IWHN4CMoFJUX4ENN\nsQye8+Q/WPkZB5V9p/Wgz5Mv86BsxLA/kF6bj07Jm4OkvEQNV6tmn80siOT55TOV\nHKVSgG92ESVTlLmqGEnUnj+5WetuQGEDd4vgif6Bx2P2x1+UwbLA4rOGSBBKhPbv\ndv3MKfZavgdTSzl0XezZWkdjYK99eVl3TQRDc1vclLhJSpfJ5Il7fUwhj0K+uBkU\nEVHXXiRavJ5pKTp9zpr37ywvpWwJsIKgmQ4xxmmel+CWiJqwq0H0NCN0xgFocyiY\n5WNrIgbxcFM9c4gvClSzADLg9dYPV3HQwAAiL+uowQKBgQDCBtgJMatnLE9rEg4S\n+6R7njFtuVMk8pnYQp3XrkIHXxLpw5IVlLuEjMxcZiubVXXBqLkyoM4mGpTG7Nx+\nAiEIls3D2yaAuAMBEA1H/aippwhV8/e+XgpuOmDpMTFswjqqemVuUETJ8PPK4yiA\nfieARjZUTc7eJRLJUpzGdJyVzwKBgQC97xXfYEZSY6CubU/L5u5eMEFkwYIzidu3\nobNfr6A1tywB8OjrgPwnUWlZ6UD2AC7t6+3ke/ImlhxICtY+kB7/JJMekHYfNQWM\n3jrLAMuJ3yqoJU3NupQEu5r/uHYhfwd9+9Iakb3ZPHRYKM1jMADBESh2kWQw5PLn\nuXIz54k3DwKBgQCuxKtj3LGfxXHj5+d1geWu09eCFiSmaz/YZGj5FaW0LhdDKT40\n4jvmMU0DDaTJzji7r9bhm6cU+2x3onMZraFDs1K00HnmB9ns4yCTcBC0gBgqFA9c\nEikjEMKqSf1TEcD2PjmPHA5aOAfhAKxC0V+TU6ssVMm5n3tEjH1a5T8GUQKBgQCT\n08HyWbxh46jsGahByzs7k9NR2Eq+Uk3wXqp9jvPi2u4llJu0sG+RKowUrrcgwIPG\nKhq9+ro9zhe0+rpFd2aoro7S+xz0rQ/k1BJube/9HvTUajRkKxOJm3rIDYnkCDqM\nk7KzezuIGMV02E0DJhlwKyqTHhYc+BUWxf9c5pilgQKBgQC21CX/Qah12i4FT0+I\n8UbZCIMm6YUu635VHbrWME+CAET0RpFMLkArl8amTtJUJh93zITkdAPObYu6jB59\nBea3hqCMkruWvMlEzrdvt9bqRT1spgBsd4UC4msBykp2/JYWBaQ6DQHkRs9jFJNh\nr+Mp1YamkHsHIq7WgQPOjo2FUg==\n-----END PRIVATE KEY-----\n","client_email":"id-drive-reader@noticias-site-476917.iam.gserviceaccount.com","client_id":"104736699678140979526","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/id-drive-reader%40noticias-site-476917.iam.gserviceaccount.com","universe_domain":"googleapis.com"}
```
✅ **Já convertido para uma linha!**  
⚠️ **IMPORTANTE**: Cole TODO o JSON acima em uma única linha no campo Value

### 10. FRONTEND_ORIGINS
```
Key: FRONTEND_ORIGINS
Value: https://www.temvenda.com.br,https://temvenda.com.br
```

---

## 📝 Checklist

Após adicionar todas as variáveis, verifique:

- [ ] Todas as 10 variáveis foram adicionadas
- [ ] `APP_PASSWORD` tem uma senha forte
- [ ] `SUPABASE_URL` está correto (sem barra no final)
- [ ] `SUPABASE_SERVICE_ROLE_KEY` é a service_role key
- [ ] `DRIVE_FILE_ID` está correto
- [ ] `GOOGLE_PROJECTION_FILE_ID` está correto
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` está em uma linha completa
- [ ] Todas as variáveis foram salvas

---

## 🚀 Próximo Passo

Após adicionar todas as variáveis:
1. Clique em **"Save Changes"**
2. O Render vai fazer um novo deploy automaticamente
3. Aguarde o build terminar
4. Teste: `https://sua-url.onrender.com/health`

---

## 💡 Dicas

- Você pode adicionar todas as variáveis de uma vez ou uma por uma
- O Render salva automaticamente, mas é bom clicar em "Save" após cada grupo
- Se alguma variável estiver errada, você pode editar depois
- As variáveis sensíveis (como senhas) ficam ocultas no dashboard por segurança

