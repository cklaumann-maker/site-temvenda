-- Migration para adicionar campos calculados (percent_paid e remaining_amount)
-- Execute apenas se a tabela expense_items já existir sem esses campos

-- Adiciona colunas se não existirem
DO $$ 
BEGIN
    -- Adiciona percent_paid se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'expense_items' AND column_name = 'percent_paid'
    ) THEN
        ALTER TABLE expense_items ADD COLUMN percent_paid numeric(5,2) default 0;
    END IF;
    
    -- Adiciona remaining_amount se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'expense_items' AND column_name = 'remaining_amount'
    ) THEN
        ALTER TABLE expense_items ADD COLUMN remaining_amount numeric(14,2) default 0;
    END IF;
END $$;

-- Atualiza a função do trigger para calcular os novos campos
create or replace function update_expense_status()
returns trigger as $$
declare
    total_due numeric(14,2);
    percent_calc numeric(5,2);
    remaining_calc numeric(14,2);
begin
    -- Calcula o total devido (valor + juros)
    total_due := NEW.amount + COALESCE(NEW.interest, 0);
    
    -- Calcula percentual pago
    if total_due > 0 then
        percent_calc := (NEW.amount_paid / total_due) * 100;
        if percent_calc > 100 then
            percent_calc := 100;
        end if;
    else
        percent_calc := 0;
    end if;
    
    -- Calcula saldo restante
    remaining_calc := total_due - NEW.amount_paid;
    if remaining_calc < 0 then
        remaining_calc := 0;
    end if;
    
    -- Atualiza campos calculados
    NEW.percent_paid := ROUND(percent_calc, 2);
    NEW.remaining_amount := remaining_calc;
    
    -- Calcula status baseado em valores e datas
    if NEW.amount_paid >= total_due then
        NEW.status := 'Quitada';
    elsif NEW.amount_paid > 0 then
        NEW.status := 'Parcialmente paga';
    elsif NEW.payment_date is null and NEW.due_date < CURRENT_DATE then
        NEW.status := 'Vencida';
    else
        NEW.status := 'Pendente';
    end if;
    
    NEW.updated_at := now();
    return NEW;
end;
$$ language plpgsql;

-- Atualiza registros existentes com os valores calculados
UPDATE expense_items
SET 
    percent_paid = CASE 
        WHEN (amount + COALESCE(interest, 0)) > 0 THEN
            LEAST(100.0, ROUND((amount_paid / (amount + COALESCE(interest, 0))) * 100, 2))
        ELSE 0
    END,
    remaining_amount = GREATEST(0, (amount + COALESCE(interest, 0)) - amount_paid);

