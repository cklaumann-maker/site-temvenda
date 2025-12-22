# 🔧 Correção do Calendário - Respeitar Banco de Dados

## ✅ Correções Implementadas

### 1. **Carregamento do Banco de Dados**

- ✅ Carrega refeições diretamente do banco (`daily_meals`)
- ✅ Ordena por data primeiro, depois por tipo de refeição
- ✅ Gera refeições automaticamente se não existirem

### 2. **Ordenação Correta**

As refeições são ordenadas na ordem exata da planilha:
1. Pré-treino (`pre`)
2. Pós-treino (`post`)
3. Café da manhã (`cafe`)
4. Almoço (`almoco`)
5. Lanche da tarde (`lanche_tarde`)
6. Jantar (`jantar`)

### 3. **Salvamento no Banco**

- ✅ Quando você seleciona uma opção, salva imediatamente no banco
- ✅ Atualização otimista (mostra mudança antes de salvar)
- ✅ Se houver erro, recarrega do banco para garantir consistência

### 4. **Botão de Atualizar**

- ✅ Botão "🔄 Atualizar" adicionado para recarregar manualmente do banco
- ✅ Útil se você fez mudanças em outro lugar ou quer garantir dados atualizados

## 🔍 Como Funciona Agora

1. **Ao abrir `/app/today`:**
   - Carrega refeições da semana atual do banco
   - Ordena por data e tipo de refeição
   - Mostra todas as opções (opt1, opt2, opt3) do banco

2. **Ao selecionar uma opção:**
   - Atualiza imediatamente na tela (otimista)
   - Salva no banco (`daily_meals.option_selected`)
   - Se houver erro, recarrega do banco

3. **Ao clicar em um dia:**
   - Mostra as refeições daquele dia
   - Ordenadas na ordem correta
   - Todas as opções do banco são exibidas

## 📋 Verificação

Para verificar se está funcionando:

1. **Abra o console do navegador (F12)**
2. **Veja os logs** quando carregar a página
3. **Verifique no banco:**
   ```sql
   SELECT date, meal_type, opt1, opt2, opt3, option_selected, avoid
   FROM daily_meals
   WHERE user_id = auth.uid()
   ORDER BY date, meal_type
   LIMIT 10;
   ```

4. **Teste selecionar uma opção:**
   - Selecione uma opção no calendário
   - Verifique no banco se `option_selected` foi atualizado
   - Recarregue a página - a opção deve permanecer selecionada

## ⚠️ Se ainda não funcionar

1. **Verifique se as refeições existem no banco:**
   ```sql
   SELECT COUNT(*) FROM daily_meals 
   WHERE user_id = auth.uid() 
     AND date >= CURRENT_DATE;
   ```

2. **Verifique se os templates foram importados:**
   ```sql
   SELECT COUNT(*) FROM plan_templates 
   WHERE program_id = '00000000-0000-0000-0000-000000000002';
   ```

3. **Regere as refeições manualmente:**
   ```sql
   SELECT public.generate_daily_meals(auth.uid(), CURRENT_DATE);
   ```

4. **Use o botão "🔄 Atualizar"** no calendário para forçar recarregamento

---

**O calendário agora respeita completamente o banco de dados!** 🚀

