-- Remover tabelas antigas se existirem (estrutura com parcelas)
drop table if exists debt_installment_adjustments cascade;
drop table if exists debt_installments cascade;
drop table if exists debt_payments cascade;
drop table if exists debts cascade;

-- Criar tabela principal para Dívidas Antigas
create table debts (
    id uuid primary key default gen_random_uuid(),
    category text not null,
    creditor text not null,
    description text,
    total_amount numeric(14,2) not null,
    status text not null default 'Aberta',
    created_at timestamptz not null default now()
);

-- Criar tabela para registrar pagamentos de dívidas
create table debt_payments (
    id uuid primary key default gen_random_uuid(),
    debt_id uuid not null references debts(id) on delete cascade,
    payment_date date not null,
    amount_paid numeric(14,2) not null,
    money_source text,
    notes text,
    created_at timestamptz not null default now()
);

-- Criar índices
create index idx_debt_payments_debt_id on debt_payments(debt_id);
create index idx_debt_payments_date on debt_payments(payment_date);


