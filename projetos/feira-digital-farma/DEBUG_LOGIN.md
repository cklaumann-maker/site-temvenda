# Debug de Login - Feira Digital Farma

## Problema Relatado
Ao tentar fazer login, o sistema sinaliza "senha incorreta".

## Possíveis Causas

1. **bcrypt.js não está carregando corretamente**
   - Verifique o console do navegador para erros de carregamento
   - Abra `test-bcrypt.html` para testar se o bcrypt está funcionando

2. **Hash não está sendo gerado corretamente no cadastro**
   - Verifique no console se aparece "Hash gerado com sucesso"
   - O hash deve começar com `$2a$` ou `$2b$`

3. **Hash está sendo salvo de forma diferente**
   - Verifique no banco de dados se o hash está correto
   - Deve ter aproximadamente 60 caracteres e começar com `$2a$` ou `$2b$`

## Como Testar

1. **Teste o bcrypt:**
   - Abra `test-bcrypt.html` no navegador
   - Verifique se todos os testes passam

2. **Verifique o cadastro:**
   - Abra o console do navegador (F12)
   - Faça um novo cadastro
   - Verifique se aparece "Hash gerado com sucesso"
   - Verifique o hash no banco de dados

3. **Verifique o login:**
   - Abra o console do navegador (F12)
   - Tente fazer login
   - Verifique as mensagens de log:
     - "Participante encontrado"
     - "Verificando senha..."
     - "Resultado bcrypt.compareSync"

## Solução Implementada

1. **Aguardar carregamento do bcrypt:**
   - O código agora aguarda até 1 segundo para o bcrypt carregar
   - Se não carregar, mostra um erro claro

2. **Validação do hash:**
   - Verifica se o hash gerado é válido (começa com `$2a$` ou `$2b$`)
   - Rejeita hash inválido

3. **Logs detalhados:**
   - Adicionados logs em cada etapa do processo
   - Facilita identificar onde está o problema

## Próximos Passos se o Problema Persistir

1. **Verificar se o hash no banco está correto:**
   ```sql
   SELECT cnpj, LEFT(senha_hash, 20) as hash_start, LENGTH(senha_hash) as hash_length 
   FROM fdf_participantes 
   WHERE cnpj = 'SEU_CNPJ';
   ```

2. **Recriar hash manualmente (apenas para teste):**
   - Use o arquivo `test-bcrypt.html` para gerar um novo hash
   - Atualize no banco de dados

3. **Verificar se há participantes com hash antigo:**
   - Se houver participantes cadastrados antes da correção, pode ser necessário recadastrar ou atualizar o hash

## Comandos SQL Úteis

```sql
-- Ver participantes e seus hashes
SELECT cnpj, nome_participante, 
       LEFT(senha_hash, 20) as hash_start,
       LENGTH(senha_hash) as hash_length,
       CASE 
         WHEN senha_hash LIKE '$2a$%' OR senha_hash LIKE '$2b$%' THEN 'bcrypt'
         ELSE 'outro'
       END as hash_type
FROM fdf_participantes;

-- Atualizar hash manualmente (SUBSTITUA os valores)
-- UPDATE fdf_participantes 
-- SET senha_hash = 'NOVO_HASH_AQUI'
-- WHERE cnpj = 'CNPJ_AQUI';
```
