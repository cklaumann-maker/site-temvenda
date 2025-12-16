from datetime import date as date_type

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from .auth import create_access_token, verify_token
from .config import get_settings
from .finance_service import (
    get_month,
    refresh_month,
    refresh_projection,
    get_projection,
    get_starting_cash,
    set_starting_cash,
)
from .debts_service import (
    create_debt,
    list_debts,
    get_debt_with_payments,
    update_debt,
    pay_debt,
    get_debt_history,
)
from .schemas import (
    CashEntryRequest,
    LoginRequest,
    ManagementEntryRequest,
    MonthResponse,
    SalesEntryRequest,
    TokenResponse,
    FinanceDailyOut,
    DebtCreateRequest,
    DebtOut,
    DebtDetailResponse,
    DebtPaymentRequest,
    DebtPaymentOut,
    DebtHistoryResponse,
    DebtHistoryItem,
    ExpenseItemOut,
    ExpenseItemsResponse,
    ProjectionDayOut,
    ProjectionResponse,
    StartingCashRequest,
)
from .supabase_client import get_supabase

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    # Para desenvolvimento/local, liberar para qualquer origem.
    # Se quiser restringir depois, trocar para settings.frontend_origins.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Rota raiz - informações da API"""
    return {
        "message": "TEM VENDA Finance API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """Health check - valida Supabase e configuração"""
    from .config import get_settings
    
    settings = get_settings()
    health_info = {
        "status": "ok",
        "api": "running",
        "database": "unknown",
        "config": {}
    }
    
    # Verifica configuração básica
    has_supabase_url = bool(settings.supabase_url)
    has_supabase_key = bool(settings.supabase_service_role_key)
    
    health_info["config"] = {
        "supabase_url_configured": has_supabase_url,
        "supabase_key_configured": has_supabase_key,
    }
    
    # Tenta conectar ao Supabase
    if not has_supabase_url or not has_supabase_key:
        health_info["database"] = "error"
        health_info["error"] = "SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY não configurados"
        return health_info
    
    try:
        supabase = get_supabase()
        # Tenta fazer uma query simples
        result = supabase.table("finance_daily").select("id").limit(1).execute()
        health_info["database"] = "ok"
        health_info["database_tables"] = "accessible"
    except Exception as e:
        health_info["database"] = "error"
        health_info["error"] = str(e)
        # Não expor detalhes sensíveis em produção
        if settings.environment == "development":
            health_info["error_details"] = repr(e)
    
    return health_info


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    if payload.password != settings.app_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha inválida")
    token = create_access_token()
    return TokenResponse(access_token=token)


@app.get("/api/months/current", response_model=MonthResponse)
async def get_current_month(
    monthCode: str = Query(..., alias="monthCode"),
    _user=Depends(verify_token),
):
    days = await get_month(monthCode)
    return MonthResponse(
        month_code=monthCode,
        days=[FinanceDailyOut.model_validate(d) for d in days],
    )


@app.post("/api/days/{date}/cash-entry")
async def save_cash_entry(
    date: date_type,
    payload: CashEntryRequest,
    _user=Depends(verify_token),
):
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date.isoformat()).limit(1).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Dia não encontrado")
    day = resp.data[0]

    # Atualiza entradas reais
    day["cash_in_actual_money"] = payload.money
    day["cash_in_actual_pix"] = payload.pix
    day["cash_in_actual_card"] = payload.card
    day["cash_in_actual_convenio"] = payload.convenio

    cash_in_actual_total = (
        float(day["cash_in_actual_money"])
        + float(day["cash_in_actual_pix"])
        + float(day["cash_in_actual_card"])
        + float(day["cash_in_actual_convenio"])
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day["future_in_confirmed"])
    cash_out_planned = float(day["expenses_planned"]) + float(day["purchases_planned"]) + float(day["old_debts_paid"])
    cash_out_real = float(day["expenses_paid"]) + float(day["purchases_planned"]) + float(day["old_debts_paid"])

    day["balance_projected"] = float(day["sales"]) + cash_in_total - cash_out_planned
    day["balance_real"] = cash_in_total - cash_out_real

    supabase.table("finance_daily").update(
        {
            "cash_in_actual_money": day["cash_in_actual_money"],
            "cash_in_actual_pix": day["cash_in_actual_pix"],
            "cash_in_actual_card": day["cash_in_actual_card"],
            "cash_in_actual_convenio": day["cash_in_actual_convenio"],
            "balance_projected": day["balance_projected"],
            "balance_real": day["balance_real"],
        }
    ).eq("id", day["id"]).execute()

    return {"status": "ok"}


@app.post("/api/days/{date}/management")
async def save_management(
    date: date_type,
    payload: ManagementEntryRequest,
    _user=Depends(verify_token),
):
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date.isoformat()).limit(1).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Dia não encontrado")
    day = resp.data[0]

    day["purchases_planned"] = payload.purchases_planned
    day["future_in_confirmed"] = payload.future_in_confirmed

    cash_in_actual_total = (
        float(day["cash_in_actual_money"])
        + float(day["cash_in_actual_pix"])
        + float(day["cash_in_actual_card"])
        + float(day["cash_in_actual_convenio"])
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day["future_in_confirmed"])
    cash_out_planned = float(day["expenses_planned"]) + float(day["purchases_planned"]) + float(day.get("old_debts_paid", 0.0))
    cash_out_real = float(day["expenses_paid"]) + float(day["purchases_planned"]) + float(day.get("old_debts_paid", 0.0))

    day["balance_projected"] = float(day["sales"]) + cash_in_total - cash_out_planned
    day["balance_real"] = cash_in_total - cash_out_real

    supabase.table("finance_daily").update(
        {
            "purchases_planned": day["purchases_planned"],
            "future_in_confirmed": day["future_in_confirmed"],
            "balance_projected": day["balance_projected"],
            "balance_real": day["balance_real"],
        }
    ).eq("id", day["id"]).execute()

    return {"status": "ok"}


@app.post("/api/days/{date}/sales")
async def save_sales(
    date: date_type,
    payload: SalesEntryRequest,
    _user=Depends(verify_token),
):
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date.isoformat()).limit(1).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Dia não encontrado")
    day = resp.data[0]

    day["sales"] = payload.sales

    cash_in_actual_total = (
        float(day["cash_in_actual_money"])
        + float(day["cash_in_actual_pix"])
        + float(day["cash_in_actual_card"])
        + float(day["cash_in_actual_convenio"])
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day["future_in_confirmed"])
    cash_out_planned = float(day["expenses_planned"]) + float(day["purchases_planned"]) + float(day["old_debts_paid"])

    day["balance_projected"] = float(day["sales"]) + cash_in_total - cash_out_planned

    supabase.table("finance_daily").update(
        {
            "sales": day["sales"],
            "balance_projected": day["balance_projected"],
        }
    ).eq("id", day["id"]).execute()

    return {"status": "ok"}


@app.get("/api/days/{date}/expenses", response_model=ExpenseItemsResponse)
async def get_day_expenses(
    date: date_type,
    _user=Depends(verify_token),
):
    """
    Retorna todas as despesas que foram pagas no dia especificado.
    Inclui despesas com vencimento no dia ou pagas no dia.
    """
    supabase = get_supabase()
    date_str = date.isoformat()
    
    # Busca despesas pagas no dia
    resp_paid = (
        supabase.table("expense_items")
        .select("*")
        .eq("payment_date", date_str)
        .execute()
    )
    
    # Busca despesas com vencimento no dia
    resp_due = (
        supabase.table("expense_items")
        .select("*")
        .eq("due_date", date_str)
        .execute()
    )
    
    # Combina resultados, removendo duplicatas por ID
    items_dict = {}
    for item in (resp_paid.data or []):
        items_dict[item["id"]] = item
    for item in (resp_due.data or []):
        items_dict[item["id"]] = item
    
    items = list(items_dict.values())
    # Ordena por data de vencimento
    items.sort(key=lambda x: x.get("due_date", ""))
    
    return ExpenseItemsResponse(
        items=[ExpenseItemOut.model_validate(item) for item in items]
    )


@app.post("/api/admin/refresh")
async def admin_refresh(
    monthCode: str = Query(..., alias="monthCode"),
    _user=Depends(verify_token),
):
    await refresh_month(monthCode)
    return {"status": "ok", "month_code": monthCode}


@app.post("/api/admin/projection/refresh")
async def admin_refresh_projection(
    days: int = Query(60, alias="days"),
    _user=Depends(verify_token),
):
    await refresh_projection(days)
    return {"status": "ok", "days": days}


@app.get("/api/projection", response_model=ProjectionResponse)
async def get_projection_endpoint(
    days: int = Query(60, alias="days"),
    _user=Depends(verify_token),
):
    rows, starting_cash, last_updated = await get_projection(days)
    return ProjectionResponse(
        starting_cash=starting_cash,
        last_updated_at=last_updated,
        days=[ProjectionDayOut.model_validate(r) for r in rows],
    )


@app.get("/api/settings/finance")
async def get_finance_settings(_user=Depends(verify_token)):
    """
    Retorna configurações financeiras (atualmente apenas starting_cash).
    """
    starting = get_starting_cash()
    return {"starting_cash": starting}


@app.post("/api/admin/settings/starting-cash")
async def update_starting_cash(payload: StartingCashRequest, _user=Depends(verify_token)):
    """
    Atualiza o caixa inicial utilizado na projeção.
    """
    value = set_starting_cash(payload.starting_cash)
    return {"starting_cash": value}


# --- Debts (Dívidas Antigas) ---


@app.post("/api/debts", response_model=DebtOut)
async def api_create_debt(payload: DebtCreateRequest, _user=Depends(verify_token)):
    debt_dict = create_debt(payload.model_dump())
    # Enriquecer com totais
    debts = list_debts()
    enriched = next((d for d in debts if d["id"] == debt_dict["id"]), debt_dict)
    return DebtOut.model_validate(enriched)


@app.get("/api/debts", response_model=list[DebtOut])
async def api_list_debts(_user=Depends(verify_token)):
    debts = list_debts()
    return [DebtOut.model_validate(d) for d in debts]


@app.get("/api/debts/{debt_id}", response_model=DebtDetailResponse)
async def api_get_debt(debt_id: str, _user=Depends(verify_token)):
    debt, payments = get_debt_with_payments(debt_id)
    if not debt:
        raise HTTPException(status_code=404, detail="Dívida não encontrada")
    return DebtDetailResponse(
        debt=DebtOut.model_validate(debt),
        payments=[DebtPaymentOut.model_validate(p) for p in payments],
    )


@app.put("/api/debts/{debt_id}", response_model=DebtOut)
async def api_update_debt(debt_id: str, payload: DebtCreateRequest, _user=Depends(verify_token)):
    debt = update_debt(debt_id, payload.model_dump())
    if not debt:
        raise HTTPException(status_code=404, detail="Dívida não encontrada")
    return DebtOut.model_validate(debt)


@app.post("/api/debts/{debt_id}/pay")
async def api_pay_debt(
    debt_id: str,
    payload: DebtPaymentRequest,
    _user=Depends(verify_token),
):
    payment, err = pay_debt(
        debt_id,
        payload.payment_date,
        payload.amount_paid,
        payload.money_source,
        payload.notes,
    )
    if err:
        if "já está quitada" in err:
            raise HTTPException(status_code=409, detail=err)
        raise HTTPException(status_code=400, detail=err)
    return {"status": "ok", "payment": payment}


@app.get("/api/debts/{debt_id}/history", response_model=DebtHistoryResponse)
async def api_debt_history(debt_id: str, _user=Depends(verify_token)):
    items_raw = get_debt_history(debt_id)
    items = [DebtHistoryItem.model_validate(i) for i in items_raw]
    return DebtHistoryResponse(items=items)


