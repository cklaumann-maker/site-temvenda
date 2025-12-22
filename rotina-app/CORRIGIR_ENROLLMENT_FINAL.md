# 🔧 Corrigir Enrollment - Versão Final

## ⚠️ Problema

A constraint única é um índice parcial (`WHERE active = true`), então `ON CONFLICT` não funciona. Vamos usar `INSERT ... WHERE NOT EXISTS`.

## ✅ Solução - Execute cada parte separadamente

### **PASSO 1: Encontrar seu user_id**

```sql
SELECT 
  id as user_id,
  email
FROM auth.users
WHERE email = 'cesar@temvenda.com.br'; -- SUBSTITUA PELO SEU EMAIL
```

**Copie o `user_id` retornado**

---

### **PASSO 2: Verificar se enrollment já existe**

```sql
SELECT 
  id,
  user_id,
  program_id,
  start_date,
  active
FROM public.enrollments
WHERE user_id = 'SEU_USER_ID_AQUI'::UUID; -- COLE O ID AQUI
```

---

### **PASSO 3: Criar enrollment (se não existir)**

Substitua `'SEU_USER_ID_AQUI'` pelo ID copiado:

```sql
INSERT INTO public.enrollments (user_id, program_id, start_date, active)
SELECT 
  'SEU_USER_ID_AQUI'::UUID, -- COLE O ID AQUI
  '00000000-0000-0000-0000-000000000002',
  CURRENT_DATE,
  true
WHERE NOT EXISTS (
  SELECT 1 FROM public.enrollments
  WHERE user_id = 'SEU_USER_ID_AQUI'::UUID -- COLE O ID AQUI
    AND program_id = '00000000-0000-0000-0000-000000000002'
);
```

---

### **PASSO 4: Ativar enrollment se estiver inativo**

```sql
UPDATE public.enrollments
SET active = true,
    start_date = COALESCE(start_date, CURRENT_DATE)
WHERE user_id = 'SEU_USER_ID_AQUI'::UUID -- COLE O ID AQUI
  AND program_id = '00000000-0000-0000-0000-000000000002'
  AND active = false;
```

---

### **PASSO 5: Corrigir templates**

```sql
UPDATE plan_templates
SET meal_type = 'pre'
WHERE program_id = '00000000-0000-0000-0000-000000000002'
  AND meal_type = 'lanche_manha';
```

---

### **PASSO 6: Deletar refeições antigas**

```sql
DELETE FROM public.daily_meals 
WHERE user_id = 'SEU_USER_ID_AQUI'::UUID; -- COLE O ID AQUI
```

---

### **PASSO 7: Regerar refeições**

Substitua `'SEU_USER_ID_AQUI'` em todas as linhas:

```sql
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE);
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE + 1);
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE + 2);
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE + 3);
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE + 4);
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE + 5);
SELECT public.generate_daily_meals('SEU_USER_ID_AQUI'::UUID, CURRENT_DATE + 6);
```

---

### **PASSO 8: Verificar resultado**

```sql
SELECT 
  e.id,
  e.user_id,
  u.email,
  e.program_id,
  e.start_date,
  e.active,
  (SELECT COUNT(*) FROM daily_meals WHERE user_id = e.user_id) as total_refeicoes
FROM public.enrollments e
JOIN auth.users u ON u.id = e.user_id
WHERE u.email = 'cesar@temvenda.com.br' -- SUBSTITUA PELO SEU EMAIL
ORDER BY e.created_at DESC;
```

---

## 📋 Checklist

- [ ] PASSO 1: Executei e copiei o `user_id`
- [ ] PASSO 2: Verifiquei se enrollment existe
- [ ] PASSO 3: Criei o enrollment (usando `WHERE NOT EXISTS`)
- [ ] PASSO 4: Ativei o enrollment (se necessário)
- [ ] PASSO 5: Corrigi os templates
- [ ] PASSO 6: Deletei refeições antigas
- [ ] PASSO 7: Regenerei refeições (7 comandos)
- [ ] PASSO 8: Verifiquei o resultado

---

**Execute os passos acima e me informe se funcionou!** ✅

