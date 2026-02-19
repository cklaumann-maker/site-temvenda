# Como Gerar Hashes Bcrypt para Login Admin

## Método 1: Arquivo HTML (Mais Fácil) ⭐

1. **Abra o arquivo `gerar-hashes-admin.html` no navegador**
   - Você pode fazer isso de várias formas:
     - **Opção A**: Clique duas vezes no arquivo no Finder/Explorador
     - **Opção B**: Arraste o arquivo para o navegador
     - **Opção C**: Clique com botão direito → "Abrir com" → Escolha seu navegador
     - **Opção D**: No VS Code/Cursor, clique com botão direito no arquivo → "Open with Live Server" (se tiver extensão)
     - **Opção E**: Digite no navegador: `file:///caminho/completo/para/gerar-hashes-admin.html`

2. **A página mostrará automaticamente:**
   - Hash para usuário `cesar` (senha: `cesar*26`)
   - Hash para usuário `root` (senha: `root*26`)
   - SQL completo pronto para copiar

3. **Copie o SQL completo** clicando no botão "Copiar SQL Completo"

4. **Execute no Supabase:**
   - Acesse o Supabase Dashboard
   - Vá em SQL Editor
   - Cole o SQL copiado
   - Execute (Run)

5. **Teste o login novamente!**

## Método 2: Gerador Online

1. Acesse: https://bcrypt-generator.com/
2. Digite a senha: `cesar*26`
3. Rounds: `10`
4. Clique em "Generate"
5. Copie o hash gerado
6. Repita para `root*26`
7. Use este SQL:

```sql
UPDATE fdf_usuarios_admin 
SET senha_hash = 'HASH_GERADO_PARA_cesar*26'
WHERE email = 'cesar';

UPDATE fdf_usuarios_admin 
SET senha_hash = 'HASH_GERADO_PARA_root*26'
WHERE email = 'root';
```

## Método 3: Console do Navegador

1. Abra qualquer página do site no navegador
2. Abra o Console (F12)
3. Cole este código:

```javascript
// Carregar bcrypt se não estiver carregado
if (typeof bcrypt === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bcryptjs@2.4.3/dist/bcrypt.min.js';
    document.head.appendChild(script);
    script.onload = gerarHashes;
} else {
    gerarHashes();
}

function gerarHashes() {
    const hashCesar = bcrypt.hashSync('cesar*26', bcrypt.genSaltSync(10));
    const hashRoot = bcrypt.hashSync('root*26', bcrypt.genSaltSync(10));
    
    console.log('Hash para cesar:', hashCesar);
    console.log('Hash para root:', hashRoot);
    
    console.log('\nSQL para executar:');
    console.log(`UPDATE fdf_usuarios_admin SET senha_hash = '${hashCesar}' WHERE email = 'cesar';`);
    console.log(`UPDATE fdf_usuarios_admin SET senha_hash = '${hashRoot}' WHERE email = 'root';`);
}
```

4. Copie os hashes do console
5. Execute no Supabase

## Verificar se Funcionou

Após executar o SQL, rode esta query para verificar:

```sql
SELECT 
    email,
    LEFT(senha_hash, 20) as hash_start,
    LENGTH(senha_hash) as hash_length,
    CASE 
        WHEN senha_hash LIKE '$2a$%' OR senha_hash LIKE '$2b$%' THEN '✅ bcrypt válido'
        ELSE '❌ Precisa atualizar'
    END as status
FROM fdf_usuarios_admin;
```

Os hashes devem:
- Começar com `$2a$` ou `$2b$`
- Ter aproximadamente 60 caracteres
- Mostrar status "✅ bcrypt válido"

## Solução Temporária (Já Funciona)

Enquanto você não atualizar os hashes, o login funciona com:
- **Usuário**: `cesar` | **Senha**: `cesar*26`
- **Usuário**: `root` | **Senha**: `root*26`

Mas é importante atualizar os hashes para segurança!
