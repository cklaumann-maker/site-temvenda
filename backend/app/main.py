from datetime import date as date_type, datetime
import os
from pathlib import Path as PathLib

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Path, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Carregar .env antes de importar settings
env_path = PathLib(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Tentar carregar do diretório atual
    load_dotenv()

from .auth import create_access_token, verify_token
from .config import get_settings
from .finance_service import (
    get_month,
    refresh_month,
    refresh_projection,
    get_projection,
    get_starting_cash,
    set_starting_cash,
    get_last_sync_info,
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
    SyncInfoOut,
)
from .supabase_client import get_supabase

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Configurar CORS - permitir todas as origens para produção
# Se quiser restringir, usar: allow_origins=settings.frontend_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Exception handler global para garantir CORS em erros
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Garante que erros sempre retornem com headers CORS"""
    error_detail = str(exc)
    if hasattr(exc, "detail"):
        error_detail = exc.detail
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": error_detail,
            "error_type": type(exc).__name__,
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Garante que HTTPExceptions sempre retornem com headers CORS"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Garante que erros de validação sempre retornem com headers CORS"""
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
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
    date: str = Path(..., description="Data no formato YYYY-MM-DD (data local, sem timezone)"),
    payload: CashEntryRequest = None,
    _user=Depends(verify_token),
):
    """
    Salva entradas do dia. A data é tratada como data local (sem conversão de timezone).
    """
    # Parse da data como data local (sem conversão de timezone)
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Data inválida: {date}. Use formato YYYY-MM-DD")
    
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date_obj.isoformat()).limit(1).execute()
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

    update_result = supabase.table("finance_daily").update(
        {
            "cash_in_actual_money": day["cash_in_actual_money"],
            "cash_in_actual_pix": day["cash_in_actual_pix"],
            "cash_in_actual_card": day["cash_in_actual_card"],
            "cash_in_actual_convenio": day["cash_in_actual_convenio"],
            "balance_projected": day["balance_projected"],
            "balance_real": day["balance_real"],
        }
    ).eq("id", day["id"]).execute()

    # Busca o registro atualizado para retornar
    updated_resp = supabase.table("finance_daily").select("*").eq("id", day["id"]).limit(1).execute()
    if updated_resp.data:
        updated_day = updated_resp.data[0]
        # Garante que weekday está presente (se não estiver, calcula)
        if "weekday" not in updated_day or not updated_day["weekday"]:
            import calendar
            weekday_name = calendar.day_name[date_obj.weekday()]
            updated_day["weekday"] = weekday_name
        # Converte para FinanceDailyOut (ignora campos extras como 'id')
        return FinanceDailyOut.model_validate(updated_day)
    
    return {"status": "ok"}


@app.post("/api/days/{date}/management")
async def save_management(
    date: str = Path(..., description="Data no formato YYYY-MM-DD (data local, sem timezone)"),
    payload: ManagementEntryRequest = None,
    _user=Depends(verify_token),
):
    """
    Salva ajustes do dia (compras, futuras entradas). A data é tratada como data local (sem timezone).
    """
    # Parse da data como data local (sem conversão de timezone)
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Data inválida: {date}. Use formato YYYY-MM-DD")
    
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date_obj.isoformat()).limit(1).execute()
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
    date: str = Path(..., description="Data no formato YYYY-MM-DD (data local, sem timezone)"),
    payload: SalesEntryRequest = None,
    _user=Depends(verify_token),
):
    """
    Salva vendas do dia. A data é tratada como data local (sem timezone).
    """
    # Parse da data como data local (sem conversão de timezone)
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Data inválida: {date}. Use formato YYYY-MM-DD")
    
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date_obj.isoformat()).limit(1).execute()
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
    date: str = Path(..., description="Data no formato YYYY-MM-DD (data local, sem timezone)"),
    _user=Depends(verify_token),
):
    """
    Retorna todas as despesas que foram pagas no dia especificado.
    Inclui despesas com vencimento no dia ou pagas no dia.
    A data é tratada como data local (sem timezone).
    """
    # Parse da data como data local (sem conversão de timezone)
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Data inválida: {date}. Use formato YYYY-MM-DD")
    
    supabase = get_supabase()
    date_str = date_obj.isoformat()
    
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
    """
    Atualiza o fluxo de caixa de um mês específico, importando do Google Drive.
    
    Processo:
    1. Lê a planilha do Google Drive
    2. Processa e salva no Supabase (finance_daily e expense_items)
    3. Registra execução em finance_month_runs com timestamp e status
    4. A tela sempre lê do Supabase, nunca da planilha diretamente
    """
    try:
        await refresh_month(monthCode)
        # Retorna também informações da sincronização
        sync_info = await get_last_sync_info(monthCode)
        return {
            "status": "ok",
            "month_code": monthCode,
            "sync_info": sync_info
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro de validação: {str(e)}"
        )
    except Exception as e:
        # Log do erro para debug
        import traceback
        error_trace = traceback.format_exc()
        print(f"Erro ao atualizar mês {monthCode}: {error_trace}")
        # Retorna informações da sincronização mesmo em caso de erro
        sync_info = await get_last_sync_info(monthCode)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mês: {str(e)}",
            headers={"X-Sync-Info": str(sync_info) if sync_info else ""}
        )


@app.get("/api/months/{monthCode}/sync-info", response_model=SyncInfoOut)
async def get_sync_info(
    monthCode: str,
    _user=Depends(verify_token),
):
    """
    Retorna informações da última sincronização do mês:
    - Data/hora da última atualização
    - Status (completed/error)
    - Quantidade de registros importados
    - Mensagem de erro (se houver)
    """
    sync_info = await get_last_sync_info(monthCode)
    if not sync_info:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma sincronização encontrada para o mês {monthCode}"
        )
    return SyncInfoOut.model_validate(sync_info)


@app.post("/api/admin/projection/refresh")
async def admin_refresh_projection(
    days: int = Query(60, alias="days"),
    _user=Depends(verify_token),
):
    """
    Atualiza a projeção D+N de caixa.
    
    Se GOOGLE_PROJECTION_FILE_ID não estiver configurado, usa apenas:
    - Dados reais de finance_daily
    - Forecast padrão como fallback
    """
    try:
        await refresh_projection(days)
        return {"status": "ok", "days": days}
    except RuntimeError as e:
        # Erro específico (ex: GOOGLE_PROJECTION_FILE_ID não configurado)
        error_msg = str(e)
        if "GOOGLE_PROJECTION_FILE_ID" in error_msg:
            # Se não tem planilha de projeção, ainda pode calcular com dados reais e forecast
            raise HTTPException(
                status_code=400,
                detail=f"Planilha de projeção não configurada. Configure GOOGLE_PROJECTION_FILE_ID ou use apenas dados reais e forecast padrão. Erro: {error_msg}"
            )
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar projeção: {error_msg}"
        )
    except Exception as e:
        # Log do erro para debug
        import traceback
        error_trace = traceback.format_exc()
        print(f"Erro ao atualizar projeção: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar projeção: {str(e)}"
        )


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


