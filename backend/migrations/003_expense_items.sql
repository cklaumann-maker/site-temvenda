-- Tabela para armazenar despesas individuais (detalhadas)
create table if not exists expense_items (
    id uuid primary key default gen_random_uuid(),
    month_code text not null,
    due_date date not null,  -- Data de vencimento
    payment_date date,  -- Data em que foi paga (null se não foi paga)
    supplier text not null,  -- Fornecedor/credor
    description text,  -- Descrição da despesa
    category text,  -- Categoria (DIST ou DESP)
    amount numeric(14,2) not null,  -- Valor original da despesa
    amount_paid numeric(14,2) default 0,  -- Valor pago
    interest numeric(14,2) default 0,  -- Juros/multa
    payment_method text,  -- Forma de pagamento (pix, dinheiro, cartão, boleto, etc)
    status text not null default 'Pendente',  -- Pendente, Paga, Vencida, Parcialmente paga
    percent_paid numeric(5,2) default 0,  -- Percentual pago (0-100)
    remaining_amount numeric(14,2) default 0,  -- Valor que falta para quitar
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index idx_expense_items_month_code on expense_items(month_code);
create index idx_expense_items_due_date on expense_items(due_date);
create index idx_expense_items_payment_date on expense_items(payment_date);
create index idx_expense_items_status on expense_items(status);

-- Função para atualizar o status, percentual pago e saldo restante automaticamente
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

-- Trigger para atualizar status automaticamente
create trigger trigger_update_expense_status
    before insert or update on expense_items
    for each row
    execute function update_expense_status();

