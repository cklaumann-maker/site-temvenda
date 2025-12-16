-- finance_month_runs
create table if not exists finance_month_runs (
    id uuid primary key default gen_random_uuid(),
    month_code text not null,
    created_at timestamptz not null default now(),
    source_file_id text not null,
    status text not null default 'completed',
    notes text
);

create index if not exists idx_finance_month_runs_month_code on finance_month_runs(month_code);

-- finance_daily
create table if not exists finance_daily (
    id uuid primary key default gen_random_uuid(),
    month_code text not null,
    date date not null,
    weekday text not null,
    sales numeric(14,2) not null default 0,
    cash_in_forecast_total numeric(14,2) not null default 0,
    cash_in_actual_money numeric(14,2) not null default 0,
    cash_in_actual_pix numeric(14,2) not null default 0,
    cash_in_actual_card numeric(14,2) not null default 0,
    cash_in_actual_convenio numeric(14,2) not null default 0,
    future_in_confirmed numeric(14,2) not null default 0,
    purchases_planned numeric(14,2) not null default 0,
    old_debts_paid numeric(14,2) not null default 0,
    expenses_planned numeric(14,2) not null default 0,
    expenses_paid numeric(14,2) not null default 0,
    balance_projected numeric(14,2) not null default 0,
    balance_real numeric(14,2) not null default 0,
    updated_at timestamptz not null default now()
);

create unique index if not exists uq_finance_daily_month_date on finance_daily(month_code, date);
create index if not exists idx_finance_daily_month_code on finance_daily(month_code);


