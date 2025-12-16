-- Configurações financeiras gerais
create table if not exists finance_settings (
    id uuid primary key default gen_random_uuid(),
    starting_cash numeric(14,2) not null default 0,
    updated_at timestamptz not null default now()
);

-- Tabela de projeção diária de caixa (D+60)
create table if not exists finance_projection_daily (
    date date primary key,
    cash_in numeric(14,2) not null default 0,
    cash_out numeric(14,2) not null default 0,
    projected_balance_day numeric(14,2) not null default 0,
    projected_running_balance numeric(14,2) not null default 0,
    source_in text not null default 'forecast',  -- real | sheet | forecast
    source_out text not null default 'rational', -- real | sheet | rational
    notes text,
    updated_at timestamptz not null default now()
);

create index if not exists idx_finance_projection_date on finance_projection_daily(date);


