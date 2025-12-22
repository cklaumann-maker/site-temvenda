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


class ManagementEntryRequest(BaseModel):
    purchases_planned: float = 0  # Compras à vista (impacto imediato)
    purchases_credit: float = 0  # Compras a prazo (saída prevista)
    future_in_confirmed: float = 0


class SalesEntryRequest(BaseModel):
    sales: float = 0


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
    store_expenses_total: float = 0  # Despesas de loja (retiradas, premiações, etc.)
    balance_projected: float
    balance_real: float

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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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


