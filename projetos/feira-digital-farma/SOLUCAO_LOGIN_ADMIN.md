# Solução para Login Admin - Feira Digital Farma

## Problema Identificado

Os hashes de senha no banco de dados são placeholders (`SEU_HASH_CEASR_AQUI` e `SEU_HASH_ROOT_AQUI`) e não são hashes bcrypt reais.

## Solução Temporária (Já Implementada)

O código agora detecta esses placeholders e permite login temporário com as senhas:
- **cesar**: `cesar*26`
- **root**: `root*26`

⚠️ **IMPORTANTE**: Esta é uma solução temporária. Você DEVE atualizar os hashes no banco o quanto antes.

## Solução Definitiva: Gerar Hashes Bcrypt Reais

### Opção 1: Usar o arquivo test-bcrypt.html (Recomendado)

1. Abra o arquivo `test-bcrypt.html` no navegador
2. A página mostrará automaticamente os hashes gerados para ambos os usuários
3. Copie os hashes gerados
4. Execute o SQL abaixo no Supabase SQL Editor:

```sql
-- Substitua os hashes pelos gerados no test-bcrypt.html
UPDATE fdf_usuarios_admin 
SET senha_hash = 'HASH_GERADO_PARA_cesar*26'
WHERE email = 'cesar';

UPDATE fdf_usuarios_admin 
SET senha_hash = 'HASH_GERADO_PARA_root*26'
WHERE email = 'root';
```

### Opção 2: Usar Gerador Online

1. Acesse: https://bcrypt-generator.com/
2. Digite a senha: `cesar*26`
3. Rounds: `10`
4. Copie o hash gerado
5. Repita para `root*26`
6. Execute os UPDATEs acima

### Opção 3: Usar Node.js (se tiver instalado)

```javascript
const bcrypt = require('bcryptjs');

// Gerar hash para cesar
const hashCesar = bcrypt.hashSync('cesar*26', 10);
console.log('Hash cesar:', hashCesar);

// Gerar hash para root
const hashRoot = bcrypt.hashSync('root*26', 10);
console.log('Hash root:', hashRoot);
```

## Verificar se os Hashes Foram Atualizados

Execute este SQL para verificar:

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

Os hashes válidos devem:
- Começar com `$2a$` ou `$2b$`
- Ter aproximadamente 60 caracteres
- Não conter "SEU_HASH" ou "placeholder"

## Após Atualizar os Hashes

1. Teste o login novamente
2. O código detectará automaticamente que são hashes bcrypt válidos
3. A solução temporária de placeholder será ignorada

## Arquivos Criados

- `test-bcrypt.html` - Gera hashes automaticamente e mostra SQL pronto
- `ATUALIZAR_HASHES_ADMIN.sql` - Template SQL para atualizar
- `GERAR_HASHES_BCRYPT_ADMIN.sql` - Instruções detalhadas
