# 🔧 Corrigir Enrollment - Passo a Passo

## ⚠️ Problema

O editor SQL do Supabase pode ter problemas com blocos `DO $$`. Vamos fazer passo a passo.

## ✅ Solução - Execute cada parte separadamente

### **PASSO 1: Encontrar seu user_id**

Execute este SQL primeiro:

```sql
SELECT 
  id as user_id,
  email
FROM auth.users
WHERE email = 'cesar@temvenda.com.br'; -- SUBSTITUA PELO SEU EMAIL
```

**Copie o `user_id` retornado** (será algo como `0c1494ed-66b0-4e3c-9bd4-2ee1c0b405a2`)

---

### **PASSO 2: Criar enrollment**

Substitua `'SEU_USER_ID_AQUI'` pelo ID copiado no PASSO 1:

```sql
INSERT INTO public.enrollments (user_id, program_id, start_date, active)
VALUES (
  'SEU_USER_ID_AQUI'::UUID, -- COLE O ID AQUI
  '00000000-0000-0000-0000-000000000002',
  CURRENT_DATE,
  true
)
ON CONFLICT (user_id, program_id) 
DO UPDATE SET
  active = true,
  start_date = COALESCE(excluded.start_date, CURRENT_DATE);
```

---

### **PASSO 3: Ativar enrollment se necessário**

```sql
UPDATE public.enrollments
SET active = true,
    start_date = COALESCE(start_date, CURRENT_DATE)
WHERE user_id = 'SEU_USER_ID_AQUI'::UUID -- COLE O ID AQUI
  AND program_id = '00000000-0000-0000-0000-000000000002'
  AND active = false;
```

---

### **PASSO 4: Corrigir templates**

```sql
UPDATE plan_templates
SET meal_type = 'pre'
WHERE program_id = '00000000-0000-0000-0000-000000000002'
  AND meal_type = 'lanche_manha';
```

---

### **PASSO 5: Deletar refeições antigas**

```sql
DELETE FROM public.daily_meals 
WHERE user_id = 'SEU_USER_ID_AQUI'::UUID; -- COLE O ID AQUI
```

---

### **PASSO 6: Regerar refeições**

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

### **PASSO 7: Verificar resultado**

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
- [ ] PASSO 2: Criei o enrollment
- [ ] PASSO 3: Ativei o enrollment (se necessário)
- [ ] PASSO 4: Corrigi os templates
- [ ] PASSO 5: Deletei refeições antigas
- [ ] PASSO 6: Regenerei refeições (7 comandos)
- [ ] PASSO 7: Verifiquei o resultado

---

**Execute os passos acima e me informe se funcionou!** ✅

