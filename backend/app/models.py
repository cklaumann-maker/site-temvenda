import uuid
from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from .db import Base


class FinanceMonthRun(Base):
    __tablename__ = "finance_month_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    month_code = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    source_file_id = Column(String, nullable=False)
    status = Column(String, nullable=False, default="completed")
    notes = Column(Text, nullable=True)


class FinanceDaily(Base):
    __tablename__ = "finance_daily"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    month_code = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)
    weekday = Column(String, nullable=False)

    sales = Column(Numeric(14, 2), nullable=False, default=0)

    cash_in_forecast_total = Column(Numeric(14, 2), nullable=False, default=0)

    cash_in_actual_money = Column(Numeric(14, 2), nullable=False, default=0)
    cash_in_actual_pix = Column(Numeric(14, 2), nullable=False, default=0)
    cash_in_actual_card = Column(Numeric(14, 2), nullable=False, default=0)
    cash_in_actual_convenio = Column(Numeric(14, 2), nullable=False, default=0)

    future_in_confirmed = Column(Numeric(14, 2), nullable=False, default=0)

    purchases_planned = Column(Numeric(14, 2), nullable=False, default=0)
    old_debts_paid = Column(Numeric(14, 2), nullable=False, default=0)

    expenses_planned = Column(Numeric(14, 2), nullable=False, default=0)
    expenses_paid = Column(Numeric(14, 2), nullable=False, default=0)
    interest_paid = Column(Numeric(14, 2), nullable=False, default=0)  # Soma dos juros pagos no dia

    balance_projected = Column(Numeric(14, 2), nullable=False, default=0)
    balance_real = Column(Numeric(14, 2), nullable=False, default=0)

    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("month_code", "date", name="uq_finance_daily_month_date"),
    )


