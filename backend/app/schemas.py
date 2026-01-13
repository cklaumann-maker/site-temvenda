from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    password: str


class CashEntryRequest(BaseModel):
    money: float = 0
    pix: float = 0
    card: float = 0
    convenio: float = 0
    opening_balance: float = 0  # Saldo inicial da conta no dia


class ManagementEntryRequest(BaseModel):
    purchases_planned: float = 0  # Compras à vista (impacto imediato)
    purchases_credit: float = 0  # Compras a prazo (saída prevista)
    future_in_confirmed: float = 0


class SalesEntryRequest(BaseModel):
    sales: float = 0
    notes: Optional[str] = None  # Observações sobre as vendas


class FinanceDailyOut(BaseModel):
    date: date
    weekday: str
    sales: float
    cash_in_forecast_total: float
    cash_in_actual_money: float
    cash_in_actual_pix: float
    cash_in_actual_card: float
    cash_in_actual_convenio: float
    future_in_confirmed: float
    purchases_planned: float  # Compras à vista (impacto imediato)
    purchases_credit: float = 0  # Compras a prazo (saída prevista)
    old_debts_paid: float
    expenses_planned: float
    expenses_paid: float
    interest_paid: float = 0  # Soma dos juros pagos no dia
    store_expenses_total: float = 0  # Despesas de loja (retiradas, premiações, etc.)
    balance_projected: float
    balance_real: float
    opening_balance: float  # Saldo inicial da conta no dia (obrigatório como os outros campos)
    checks_paid_total: float = 0  # Total de cheques compensados no dia
    sales_notes: Optional[str] = None  # Observações sobre as vendas

    class Config:
        from_attributes = True


class MonthResponse(BaseModel):
    month_code: str
    days: list[FinanceDailyOut]


class DebtCreateRequest(BaseModel):
    category: str
    creditor: str
    description: Optional[str] = None
    total_amount: float


class DebtOut(BaseModel):
    id: str
    category: str
    creditor: str
    description: Optional[str] = None
    total_amount: float
    status: str
    created_at: datetime
    amount_paid: float = 0
    remaining_amount: float = 0


class DebtPaymentOut(BaseModel):
    id: str
    payment_date: date
    amount_paid: float
    money_source: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime


class DebtDetailResponse(BaseModel):
    debt: DebtOut
    payments: list[DebtPaymentOut]


class DebtPaymentRequest(BaseModel):
    payment_date: date
    amount_paid: float
    money_source: Optional[str] = None
    notes: Optional[str] = None


class DebtHistoryItem(BaseModel):
    type: str  # "payment"
    created_at: datetime
    payment_date: date
    amount_paid: float
    money_source: Optional[str] = None
    notes: Optional[str] = None


class DebtHistoryResponse(BaseModel):
    items: list[DebtHistoryItem]


class ExpenseItemOut(BaseModel):
    id: str
    month_code: str
    due_date: date
    payment_date: Optional[date] = None
    supplier: str
    description: Optional[str] = None
    category: str
    amount: float
    amount_paid: float
    interest: float
    payment_method: Optional[str] = None
    status: str
    percent_paid: float  # Percentual pago (0-100)
    remaining_amount: float  # Valor que falta para quitar
    is_essential: bool = False  # Indica se a despesa é essencial
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExpenseEssentialUpdateRequest(BaseModel):
    is_essential: bool


class ExpenseItemsResponse(BaseModel):
    items: list[ExpenseItemOut]


class ProjectionDayOut(BaseModel):
    date: date
    cash_in: float
    cash_out: float
    projected_balance_day: float
    projected_running_balance: float
    source_in: str
    source_out: str
    notes: Optional[str] = None


class ProjectionResponse(BaseModel):
    starting_cash: float
    last_updated_at: Optional[datetime] = None
    days: list[ProjectionDayOut]


class StartingCashRequest(BaseModel):
    starting_cash: float


class SyncInfoOut(BaseModel):
    month_code: str
    updated_at: Optional[datetime]
    status: str
    error_message: Optional[str] = None
    records_imported: int = 0
    expense_items_imported: int = 0
    source_file_id: Optional[str] = None

    class Config:
        from_attributes = True


class StoreExpenseCreateRequest(BaseModel):
    date: date
    amount: float
    description: Optional[str] = None
    category: str  # 'descontão' ou 'mix_transformer'
    expense_type: str  # 'retirada_caixa', 'premiacao', 'teleentrega', 'outro'


class StoreExpenseOut(BaseModel):
    id: str
    month_code: str
    date: date
    amount: float
    description: Optional[str] = None
    category: str
    expense_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StoreExpensesResponse(BaseModel):
    items: list[StoreExpenseOut]


# Checks Module Schemas
class CheckCreateRequest(BaseModel):
    issue_date: date
    due_date: date
    amount: float
    payer: Optional[str] = None
    payee: str
    category: str  # 'emprestimo' | 'fornecedor' | 'imposto' | 'cartorio' | 'outros'
    bank: Optional[str] = None
    check_number: Optional[str] = None
    memo: Optional[str] = None
    linked_expense_item_id: Optional[str] = None


class CheckUpdateRequest(BaseModel):
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    amount: Optional[float] = None
    payer: Optional[str] = None
    payee: Optional[str] = None
    category: Optional[str] = None
    bank: Optional[str] = None
    check_number: Optional[str] = None
    memo: Optional[str] = None
    linked_expense_item_id: Optional[str] = None


class CheckClearRequest(BaseModel):
    cleared_date: date


class CheckOut(BaseModel):
    id: str
    issue_date: date
    due_date: date
    cleared_date: Optional[date] = None
    amount: float
    payer: Optional[str] = None
    payee: str
    category: str
    status: str
    bank: Optional[str] = None
    check_number: Optional[str] = None
    memo: Optional[str] = None
    linked_expense_item_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    delay_days: Optional[int] = None  # Calculado: cleared_date - due_date (se compensado)

    class Config:
        from_attributes = True


class ChecksResponse(BaseModel):
    items: list[CheckOut]
    total: int


class TopDelayerOut(BaseModel):
    payee: str
    avg_delay_days: float
    median_delay_days: float
    count: int
    total_amount: float


class TopDelayersResponse(BaseModel):
    items: list[TopDelayerOut]


# Analytics Schemas
class BottleneckDayOut(BaseModel):
    date: date
    cash_out_real: float
    cash_out_planned: float
    top_categories: list[dict]
    top_suppliers: list[dict]
    is_essential_day: bool


class BottlenecksResponse(BaseModel):
    month_code: str
    days: list[BottleneckDayOut]
    threshold_method: str  # 'moving_avg' | 'top_10_percent'


class EssentialsSummaryOut(BaseModel):
    month_code: str
    total_folha: float
    total_aluguel: float
    total_essential_suppliers: float
    total_cartorio: float
    upcoming_due_dates: list[dict]  # Lista de próximos vencimentos


class StrategyRecommendationOut(BaseModel):
    next_bottleneck_date: Optional[date]
    next_bottleneck_amount: float
    buffer_days: int
    buffer_amount: float
    daily_reserve_target: float
    days_until_bottleneck: Optional[int]
    recommendations: list[str]


