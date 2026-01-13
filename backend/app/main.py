from datetime import date as date_type, datetime
import os
from pathlib import Path as PathLib
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Path, status, Body
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
from .checks_service import (
    create_check,
    list_checks,
    get_check,
    update_check,
    clear_check,
    cancel_check,
    return_check,
    get_top_delayers,
)
from .analytics_service import (
    get_comprehensive_analytics,
    get_strategy_recommendations,
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
    StoreExpenseCreateRequest,
    CheckCreateRequest,
    CheckUpdateRequest,
    CheckClearRequest,
    CheckOut,
    ChecksResponse,
    TopDelayersResponse,
    StoreExpenseOut,
    StoreExpensesResponse,
    BottlenecksResponse,
    BottleneckDayOut,
    EssentialsSummaryOut,
    StrategyRecommendationOut,
    ExpenseEssentialUpdateRequest,
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
    # Garante que opening_balance está presente em todos os dias antes da validação
    # IMPORTANTE: opening_balance agora é obrigatório no schema, então deve estar sempre presente
    for day in days:
        if "opening_balance" not in day or day["opening_balance"] is None:
            day["opening_balance"] = 0.0
    
    validated_days = [FinanceDailyOut.model_validate(d) for d in days]
    
    return MonthResponse(
        month_code=monthCode,
        days=validated_days,
    )


@app.post("/api/days/{date}/cash-entry")
async def save_cash_entry(
    date: str = Path(..., description="Data no formato YYYY-MM-DD (data local, sem timezone)"),
    payload_data: dict = Body(...),
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
    
    # Debug: log do payload recebido completo
    print(f"[save_cash_entry] Payload completo recebido: {payload_data}")
    
    # Extrai valores do payload (aceita tanto do schema quanto direto do dict)
    money = payload_data.get('money', 0.0)
    pix = payload_data.get('pix', 0.0)
    card = payload_data.get('card', 0.0)
    convenio = payload_data.get('convenio', 0.0)
    opening_balance_value = payload_data.get('opening_balance', 0.0)
    
    # Debug: log dos valores extraídos
    print(f"[save_cash_entry] Valores extraídos: opening_balance={opening_balance_value} (tipo: {type(opening_balance_value)}), money={money}, pix={pix}, card={card}, convenio={convenio}")
    
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("date", date_obj.isoformat()).limit(1).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Dia não encontrado")
    day = resp.data[0]

    # Atualiza entradas reais
    day["cash_in_actual_money"] = float(money) if money is not None else 0.0
    day["cash_in_actual_pix"] = float(pix) if pix is not None else 0.0
    day["cash_in_actual_card"] = float(card) if card is not None else 0.0
    day["cash_in_actual_convenio"] = float(convenio) if convenio is not None else 0.0
    day["opening_balance"] = float(opening_balance_value) if opening_balance_value is not None else 0.0
    
    # Debug: log do valor que será salvo
    print(f"[save_cash_entry] Valores que serão salvos:")
    print(f"  - opening_balance: {day['opening_balance']}")
    print(f"  - cash_in_actual_money: {day['cash_in_actual_money']}")
    print(f"  - cash_in_actual_pix: {day['cash_in_actual_pix']}")
    print(f"  - cash_in_actual_card: {day['cash_in_actual_card']}")
    print(f"  - cash_in_actual_convenio: {day['cash_in_actual_convenio']}")

    cash_in_actual_total = (
        float(day["cash_in_actual_money"])
        + float(day["cash_in_actual_pix"])
        + float(day["cash_in_actual_card"])
        + float(day["cash_in_actual_convenio"])
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day["future_in_confirmed"])
    cash_out_planned = float(day["expenses_planned"]) + float(day["purchases_planned"]) + float(day["old_debts_paid"])
    cash_out_real = (
        float(day["expenses_paid"])  # Despesas pagas (valor pago, juros já incluídos, pela data de pagamento)
        + float(day["purchases_planned"])  # Compras à vista
        + float(day.get("purchases_credit", 0))  # Compras a prazo pagas (também são despesas)
        + float(day.get("old_debts_paid", 0))
        + float(day.get("store_expenses_total", 0))  # Despesas de loja
    )

    day["balance_projected"] = float(day["sales"]) + cash_in_total - cash_out_planned
    # balance_real será recalculado de forma acumulada
    # Não atualiza aqui, será feito por _recalculate_balance_real_accumulated_from_date

    update_result = supabase.table("finance_daily").update(
        {
            "cash_in_actual_money": day["cash_in_actual_money"],
            "cash_in_actual_pix": day["cash_in_actual_pix"],
            "cash_in_actual_card": day["cash_in_actual_card"],
            "cash_in_actual_convenio": day["cash_in_actual_convenio"],
            "opening_balance": day["opening_balance"],
            "balance_projected": day["balance_projected"],
        }
    ).eq("id", day["id"]).execute()
    
    # Recalcula balance_real acumulado a partir desta data
    from app.finance_service import _recalculate_balance_real_accumulated_from_date
    _recalculate_balance_real_accumulated_from_date(supabase, date_obj)

    # Busca o registro atualizado para retornar
    updated_resp = supabase.table("finance_daily").select("*").eq("id", day["id"]).limit(1).execute()
    if updated_resp.data:
        updated_day = updated_resp.data[0]
        # Garante que weekday está presente (se não estiver, calcula)
        if "weekday" not in updated_day or not updated_day["weekday"]:
            import calendar
            weekday_name = calendar.day_name[date_obj.weekday()]
            updated_day["weekday"] = weekday_name
        # Garante que opening_balance está presente no dict
        if "opening_balance" not in updated_day:
            updated_day["opening_balance"] = day.get("opening_balance", 0.0)
        # Debug: log do valor que será retornado
        print(f"[save_cash_entry] Valor opening_balance que será retornado: {updated_day.get('opening_balance', 'NÃO ENCONTRADO')}")
        # Converte para FinanceDailyOut (ignora campos extras como 'id')
        try:
            result = FinanceDailyOut.model_validate(updated_day)
            print(f"[save_cash_entry] Valor opening_balance no resultado: {result.opening_balance}")
            return result
        except Exception as e:
            # Fallback: se a validação falhar, retorna o dict diretamente
            print(f"[save_cash_entry] Erro ao validar FinanceDailyOut: {e}")
            print(f"[save_cash_entry] Retornando dict diretamente")
            # Remove campos que não devem ser retornados
            updated_day.pop("id", None)
            updated_day.pop("updated_at", None)
            updated_day.pop("month_code", None)
            return updated_day
    
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
    day["purchases_credit"] = payload.purchases_credit if hasattr(payload, 'purchases_credit') else 0.0
    day["future_in_confirmed"] = payload.future_in_confirmed

    cash_in_actual_total = (
        float(day["cash_in_actual_money"])
        + float(day["cash_in_actual_pix"])
        + float(day["cash_in_actual_card"])
        + float(day["cash_in_actual_convenio"])
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day["future_in_confirmed"])
    # Inclui purchases_credit (compras a prazo) em expenses_planned
    # Inclui store_expenses_total em ambas as saídas
    cash_out_planned = (
        float(day["expenses_planned"]) 
        + float(day["purchases_planned"])  # Compras à vista
        + float(day["purchases_credit"])  # Compras a prazo
        + float(day.get("old_debts_paid", 0.0))
        + float(day.get("store_expenses_total", 0.0))
    )
    cash_out_real = (
        float(day["expenses_paid"])  # Despesas pagas (valor pago, juros já incluídos, pela data de pagamento)
        + float(day["purchases_planned"])  # Compras à vista impactam imediatamente
        + float(day.get("purchases_credit", 0))  # Compras a prazo pagas (também são despesas)
        + float(day.get("old_debts_paid", 0.0))
        + float(day.get("store_expenses_total", 0.0))  # Despesas de loja
    )

    day["balance_projected"] = float(day["sales"]) + cash_in_total - cash_out_planned
    # balance_real será recalculado de forma acumulada
    # Não atualiza aqui, será feito por _recalculate_balance_real_accumulated_from_date

    supabase.table("finance_daily").update(
        {
            "purchases_planned": day["purchases_planned"],
            "purchases_credit": day["purchases_credit"],
            "future_in_confirmed": day["future_in_confirmed"],
            "balance_projected": day["balance_projected"],
        }
    ).eq("id", day["id"]).execute()
    
    # Recalcula balance_real acumulado a partir desta data
    from app.finance_service import _recalculate_balance_real_accumulated_from_date
    _recalculate_balance_real_accumulated_from_date(supabase, date_obj)

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
    day["sales_notes"] = payload.notes if payload.notes else None

    cash_in_actual_total = (
        float(day["cash_in_actual_money"])
        + float(day["cash_in_actual_pix"])
        + float(day["cash_in_actual_card"])
        + float(day["cash_in_actual_convenio"])
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day["future_in_confirmed"])
    # Inclui purchases_credit e store_expenses_total
    cash_out_planned = (
        float(day["expenses_planned"]) 
        + float(day["purchases_planned"]) 
        + float(day.get("purchases_credit", 0))
        + float(day["old_debts_paid"])
        + float(day.get("store_expenses_total", 0))
    )

    day["balance_projected"] = float(day["sales"]) + cash_in_total - cash_out_planned

    update_data = {
        "sales": day["sales"],
        "balance_projected": day["balance_projected"],
    }
    if payload.notes is not None:
        update_data["sales_notes"] = payload.notes

    supabase.table("finance_daily").update(update_data).eq("id", day["id"]).execute()

    # Retorna o dia atualizado
    updated_resp = supabase.table("finance_daily").select("*").eq("id", day["id"]).limit(1).execute()
    if updated_resp.data:
        updated_day = updated_resp.data[0]
        try:
            result = FinanceDailyOut.model_validate(updated_day)
            return result
        except Exception as e:
            print(f"[save_sales] Erro ao validar FinanceDailyOut: {e}")
            return {"status": "ok", "sales": updated_day.get("sales"), "sales_notes": updated_day.get("sales_notes")}
    
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


@app.get("/api/expense-items/search", response_model=ExpenseItemsResponse)
async def search_expense_items(
    month_code: Optional[str] = Query(None, alias="month_code"),
    supplier: Optional[str] = Query(None, alias="supplier"),
    description: Optional[str] = Query(None, alias="description"),
    category: Optional[str] = Query(None, alias="category"),
    status: Optional[str] = Query(None, alias="status"),
    due_date_from: Optional[str] = Query(None, alias="due_date_from"),
    due_date_to: Optional[str] = Query(None, alias="due_date_to"),
    payment_date_from: Optional[str] = Query(None, alias="payment_date_from"),
    payment_date_to: Optional[str] = Query(None, alias="payment_date_to"),
    amount_min: Optional[float] = Query(None, alias="amount_min"),
    amount_max: Optional[float] = Query(None, alias="amount_max"),
    amount_paid_min: Optional[float] = Query(None, alias="amount_paid_min"),
    amount_paid_max: Optional[float] = Query(None, alias="amount_paid_max"),
    _user=Depends(verify_token),
):
    """
    Busca expense_items com filtros opcionais.
    Todos os filtros são opcionais e podem ser combinados.
    """
    supabase = get_supabase()
    query = supabase.table("expense_items").select("*")
    
    # Filtro de mês
    if month_code:
        query = query.eq("month_code", month_code)
    
    # Filtro de categoria
    if category:
        query = query.eq("category", category)
    
    # Filtro de status
    if status:
        query = query.eq("status", status)
    
    # Filtros de data de vencimento
    if due_date_from:
        query = query.gte("due_date", due_date_from)
    if due_date_to:
        query = query.lte("due_date", due_date_to)
    
    # Filtros de data de pagamento
    if payment_date_from:
        query = query.gte("payment_date", payment_date_from)
    if payment_date_to:
        query = query.lte("payment_date", payment_date_to)
    
    # Filtros de valor
    if amount_min is not None:
        query = query.gte("amount", amount_min)
    if amount_max is not None:
        query = query.lte("amount", amount_max)
    
    # Filtros de valor pago
    if amount_paid_min is not None:
        query = query.gte("amount_paid", amount_paid_min)
    if amount_paid_max is not None:
        query = query.lte("amount_paid", amount_paid_max)
    
    # Executa a query
    resp = query.order("due_date", desc=True).execute()
    items = resp.data or []
    
    # Filtros de texto livre (aplicados após buscar do banco, pois Supabase não suporta ILIKE bem)
    if supplier:
        supplier_lower = supplier.lower()
        items = [item for item in items if supplier_lower in (item.get("supplier", "") or "").lower()]
    
    if description:
        description_lower = description.lower()
        items = [item for item in items if description_lower in (item.get("description", "") or "").lower()]
    
    return ExpenseItemsResponse(
        items=[ExpenseItemOut.model_validate(item) for item in items]
    )


@app.get("/api/months/available")
async def get_available_months(_user=Depends(verify_token)):
    """
    Retorna lista de meses disponíveis no banco de dados, ordenados do mais recente para o mais antigo.
    """
    supabase = get_supabase()
    
    # Busca month_codes distintos
    resp = supabase.table("expense_items").select("month_code").execute()
    
    # Extrai month_codes únicos
    month_codes = set()
    for item in (resp.data or []):
        if item.get("month_code"):
            month_codes.add(item["month_code"])
    
    # Converte para lista e ordena (mais recente primeiro)
    # Formato: MM-YY (ex: "12-25" = dezembro 2025)
    def month_key(mc):
        try:
            mm, yy = mc.split("-")
            return (2000 + int(yy), int(mm))
        except:
            return (0, 0)
    
    sorted_months = sorted(month_codes, key=month_key, reverse=True)
    
    return {"months": sorted_months}


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


# --- Store Expenses (Despesas de Loja) ---


def parse_month_code(month_code: str) -> tuple[int, int]:
    """Converte monthCode no formato 'MM-YY' para (ano, mês)."""
    try:
        mm, yy = month_code.split("-")
        month = int(mm)
        year = 2000 + int(yy)
        return year, month
    except Exception as e:
        raise ValueError(f"monthCode inválido: {month_code}") from e


@app.post("/api/store-expenses", response_model=StoreExpenseOut)
async def create_store_expense(
    payload: StoreExpenseCreateRequest,
    _user=Depends(verify_token),
):
    """
    Cria uma despesa de loja (retirada de caixa, premiação, teleentrega, etc.).
    """
    supabase = get_supabase()
    
    # Calcula month_code a partir da data
    year, month = payload.date.year, payload.date.month
    month_code = f"{month:02d}-{str(year)[-2:]}"
    
    # Valida categoria
    if payload.category not in ["descontão", "mix_transformer"]:
        raise HTTPException(
            status_code=400,
            detail="Categoria deve ser 'descontão' ou 'mix_transformer'"
        )
    
    # Valida tipo de despesa
    valid_types = ["retirada_caixa", "premiacao", "teleentrega", "outro"]
    if payload.expense_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de despesa deve ser um de: {', '.join(valid_types)}"
        )
    
    # Insere despesa
    result = supabase.table("store_expenses").insert({
        "month_code": month_code,
        "date": payload.date.isoformat(),
        "amount": payload.amount,
        "description": payload.description,
        "category": payload.category,
        "expense_type": payload.expense_type,
    }).execute()
    
    if not result.data:
        raise HTTPException(status_code=500, detail="Erro ao criar despesa de loja")
    
    # O trigger SQL recalcula store_expenses_total automaticamente
    # Recalcula balance_real acumulado a partir desta data
    from app.finance_service import _recalculate_balance_real_accumulated_from_date
    _recalculate_balance_real_accumulated_from_date(supabase, payload.date)
    
    return StoreExpenseOut.model_validate(result.data[0])


@app.get("/api/store-expenses", response_model=StoreExpensesResponse)
async def list_store_expenses(
    month_code: str = Query(..., alias="month_code"),
    _user=Depends(verify_token),
):
    """
    Lista todas as despesas de loja de um mês.
    """
    supabase = get_supabase()
    resp = (
        supabase.table("store_expenses")
        .select("*")
        .eq("month_code", month_code)
        .order("date")
        .execute()
    )
    
    items = [StoreExpenseOut.model_validate(item) for item in (resp.data or [])]
    return StoreExpensesResponse(items=items)


@app.put("/api/store-expenses/{expense_id}", response_model=StoreExpenseOut)
async def update_store_expense(
    expense_id: str,
    payload: StoreExpenseCreateRequest,
    _user=Depends(verify_token),
):
    """
    Atualiza uma despesa de loja.
    """
    supabase = get_supabase()
    
    # Valida categoria
    if payload.category not in ["descontão", "mix_transformer"]:
        raise HTTPException(
            status_code=400,
            detail="Categoria deve ser 'descontão' ou 'mix_transformer'"
        )
    
    # Valida tipo de despesa
    valid_types = ["retirada_caixa", "premiacao", "teleentrega", "outro"]
    if payload.expense_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de despesa deve ser um de: {', '.join(valid_types)}"
        )
    
    # Calcula month_code a partir da data
    year, month = payload.date.year, payload.date.month
    month_code = f"{month:02d}-{str(year)[-2:]}"
    
    # Atualiza despesa
    result = supabase.table("store_expenses").update({
        "month_code": month_code,
        "date": payload.date.isoformat(),
        "amount": payload.amount,
        "description": payload.description,
        "category": payload.category,
        "expense_type": payload.expense_type,
    }).eq("id", expense_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Despesa de loja não encontrada")
    
    # O trigger SQL recalcula store_expenses_total automaticamente
    # Recalcula balance_real acumulado a partir desta data
    from app.finance_service import _recalculate_balance_real_accumulated_from_date
    _recalculate_balance_real_accumulated_from_date(supabase, payload.date)
    
    return StoreExpenseOut.model_validate(result.data[0])


@app.delete("/api/store-expenses/{expense_id}")
async def delete_store_expense(
    expense_id: str,
    _user=Depends(verify_token),
):
    """
    Deleta uma despesa de loja.
    """
    supabase = get_supabase()
    
    # Busca a despesa para obter month_code
    resp = supabase.table("store_expenses").select("month_code").eq("id", expense_id).limit(1).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Despesa de loja não encontrada")
    
    # Busca a data da despesa antes de deletar
    resp_date = supabase.table("store_expenses").select("date").eq("id", expense_id).limit(1).execute()
    expense_date = None
    if resp_date.data:
        from datetime import datetime
        expense_date = datetime.fromisoformat(resp_date.data[0]["date"]).date()
    
    # Deleta despesa
    supabase.table("store_expenses").delete().eq("id", expense_id).execute()
    
    # O trigger SQL recalcula store_expenses_total automaticamente
    # Recalcula balance_real acumulado a partir desta data
    if expense_date:
        from app.finance_service import _recalculate_balance_real_accumulated_from_date
        _recalculate_balance_real_accumulated_from_date(supabase, expense_date)
    
    return {"status": "ok"}


# ==================== CHECKS ENDPOINTS ====================

@app.post("/api/checks", response_model=CheckOut)
async def create_check_endpoint(
    payload: CheckCreateRequest,
    _user=Depends(verify_token),
):
    """Cria um novo cheque"""
    try:
        check = create_check(payload.model_dump())
        return CheckOut.model_validate(check)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/checks", response_model=ChecksResponse)
async def list_checks_endpoint(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    from_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    payee: Optional[str] = Query(None, description="Filtrar por beneficiário"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    _user=Depends(verify_token),
):
    """Lista cheques com filtros"""
    from_date_obj = None
    to_date_obj = None
    
    if from_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="from_date inválido. Use YYYY-MM-DD")
    
    if to_date:
        try:
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="to_date inválido. Use YYYY-MM-DD")
    
    checks = list_checks(
        status=status,
        from_date=from_date_obj,
        to_date=to_date_obj,
        payee=payee,
        limit=limit,
        offset=offset
    )
    
    return ChecksResponse(
        items=[CheckOut.model_validate(c) for c in checks],
        total=len(checks)
    )


@app.get("/api/checks/{check_id}", response_model=CheckOut)
async def get_check_endpoint(
    check_id: str = Path(..., description="ID do cheque"),
    _user=Depends(verify_token),
):
    """Busca um cheque por ID"""
    check = get_check(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Cheque não encontrado")
    return CheckOut.model_validate(check)


@app.put("/api/checks/{check_id}", response_model=CheckOut)
async def update_check_endpoint(
    check_id: str = Path(..., description="ID do cheque"),
    payload: CheckUpdateRequest = None,
    _user=Depends(verify_token),
):
    """Atualiza um cheque"""
    try:
        update_data = payload.model_dump(exclude_unset=True)
        check = update_check(check_id, update_data)
        return CheckOut.model_validate(check)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/checks/{check_id}/clear", response_model=CheckOut)
async def clear_check_endpoint(
    check_id: str = Path(..., description="ID do cheque"),
    payload: CheckClearRequest = None,
    _user=Depends(verify_token),
):
    """Marca um cheque como compensado e registra no fluxo de caixa"""
    try:
        check = clear_check(check_id, payload.cleared_date)
        return CheckOut.model_validate(check)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/checks/{check_id}/cancel", response_model=CheckOut)
async def cancel_check_endpoint(
    check_id: str = Path(..., description="ID do cheque"),
    _user=Depends(verify_token),
):
    """Cancela um cheque"""
    try:
        check = cancel_check(check_id)
        return CheckOut.model_validate(check)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/checks/{check_id}/return", response_model=CheckOut)
async def return_check_endpoint(
    check_id: str = Path(..., description="ID do cheque"),
    _user=Depends(verify_token),
):
    """Marca um cheque como devolvido"""
    try:
        check = return_check(check_id)
        return CheckOut.model_validate(check)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/checks/analytics/top-delayers", response_model=TopDelayersResponse)
async def get_top_delayers_endpoint(
    from_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=100),
    _user=Depends(verify_token),
):
    """Retorna ranking de beneficiários que mais demoram para depositar cheques"""
    from_date_obj = None
    to_date_obj = None
    
    if from_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="from_date inválido. Use YYYY-MM-DD")
    
    if to_date:
        try:
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="to_date inválido. Use YYYY-MM-DD")
    
    results = get_top_delayers(from_date=from_date_obj, to_date=to_date_obj, limit=limit)
    
    from .schemas import TopDelayerOut
    return TopDelayersResponse(
        items=[TopDelayerOut.model_validate(r) for r in results]
    )


# ==================== ANALYTICS ENDPOINTS ====================

@app.get("/api/analytics/comprehensive")
async def get_comprehensive_analytics_endpoint(
    _user=Depends(verify_token),
):
    """
    Retorna análise abrangente usando dados do banco de forma otimizada.
    Processa tudo em Python no backend.
    Retorna dados estruturados para: resumo executivo, linha do tempo, tabela, gráficos, ações e histórico.
    """
    try:
        print("[get_comprehensive_analytics_endpoint] Iniciando...")
        analytics = get_comprehensive_analytics()
        print("[get_comprehensive_analytics_endpoint] ✅ Análise concluída")
        return analytics
    except ImportError as e:
        error_msg = f"Erro de importação: {str(e)}. Verifique se analytics_service.py existe."
        print(f"[ERROR] {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        import traceback
        error_msg = f"Erro ao gerar análises: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/api/analytics/bottlenecks", response_model=BottlenecksResponse)
async def get_bottlenecks_endpoint(
    monthCode: Optional[str] = Query(None, description="Código do mês (ex: 12-25). Se omitido, analisa todos os meses."),
    threshold_method: str = Query("moving_avg", description="Método: 'moving_avg' ou 'top_10_percent'"),
    _user=Depends(verify_token),
):
    """Retorna lista de dias gargalo. Se monthCode for None, analisa todos os meses."""
    # Usa análise abrangente e extrai gargalos da timeline
    analytics = get_comprehensive_analytics()
    timeline = analytics.get("timeline", [])
    bottlenecks_timeline = [b for b in timeline if b.get("is_bottleneck")]
    
    # Converte para formato BottleneckDayOut
    bottlenecks = []
    for b in bottlenecks_timeline:
        bottlenecks.append({
            "date": b["date"],
            "cash_out_real": b.get("bottleneck_amount", b.get("total_expenses", 0)),
            "cash_out_planned": 0,
            "top_categories": [],
            "top_suppliers": [],
            "is_essential_day": b.get("risk_zone") == "critical"
        })
    
    return BottlenecksResponse(
        month_code=monthCode or "all",
        days=[BottleneckDayOut.model_validate(b) for b in bottlenecks],
        threshold_method=threshold_method
    )


@app.get("/api/analytics/essentials/summary", response_model=EssentialsSummaryOut)
async def get_essentials_summary_endpoint(
    monthCode: Optional[str] = Query(None, description="Código do mês (ex: 12-25). Se omitido, analisa todos os meses."),
    _user=Depends(verify_token),
):
    """Retorna resumo de despesas essenciais. Se monthCode for None, analisa todos os meses."""
    # Usa análise abrangente
    analytics = get_comprehensive_analytics()
    expenses_table = analytics.get("expenses_table", [])
    
    # Palavras-chave
    folha_keywords = ['folha', 'salário', 'salarios', 'pagamento pessoal', 'rh']
    aluguel_keywords = ['aluguel', 'locação', 'locacao']
    
    # Busca fornecedores essenciais
    from .supabase_client import get_supabase
    supabase = get_supabase()
    essential_resp = supabase.table("essential_suppliers").select("*").execute()
    essential_suppliers = {e["supplier_name"].lower() for e in (essential_resp.data or [])}
    
    # Calcula totais por tipo
    total_folha = 0.0
    total_aluguel = 0.0
    total_essential_suppliers = 0.0
    total_cartorio = 0.0
    
    for e in expenses_table:
        supplier = (e.get("supplier", "") or "").lower()
        description = (e.get("description", "") or "").lower()
        category = e.get("category", "").upper()
        remaining = float(e.get("remaining_amount", 0))
        
        if any(kw in supplier or kw in description for kw in folha_keywords):
            total_folha += remaining
        elif any(kw in supplier or kw in description for kw in aluguel_keywords):
            total_aluguel += remaining
        elif supplier in essential_suppliers:
            total_essential_suppliers += remaining
        
        if category == "CARTORIO" or "cartorio" in supplier or "cartorio" in description:
            total_cartorio += remaining
    
    # Próximos vencimentos
    upcoming = [{
        "due_date": e.get("due_date"),
        "supplier": e.get("supplier"),
        "amount": e.get("amount"),
        "remaining_amount": e.get("remaining_amount"),
        "category": e.get("category")
    } for e in expenses_table if e.get("due_date")][:20]
    
    return EssentialsSummaryOut.model_validate({
        "month_code": monthCode or "all",
        "total_folha": total_folha,
        "total_aluguel": total_aluguel,
        "total_essential_suppliers": total_essential_suppliers,
        "total_cartorio": total_cartorio,
        "upcoming_due_dates": upcoming
    })


@app.get("/api/analytics/strategy", response_model=StrategyRecommendationOut)
async def get_strategy_endpoint(
    monthCode: Optional[str] = Query(None, description="Código do mês (ex: 12-25). Se omitido, analisa todos os meses."),
    _user=Depends(verify_token),
):
    """Retorna recomendações estratégicas. Se monthCode for None, analisa todos os meses."""
    strategy = get_strategy_recommendations(monthCode)
    return StrategyRecommendationOut.model_validate(strategy)


@app.put("/api/expense-items/{expense_id}/essential")
async def update_expense_essential(
    expense_id: str = Path(..., description="ID da despesa"),
    payload: ExpenseEssentialUpdateRequest = Body(...),
    _user=Depends(verify_token),
):
    """Marca ou desmarca uma despesa como essencial"""
    supabase = get_supabase()
    
    # Atualiza a despesa
    result = supabase.table("expense_items").update({
        "is_essential": payload.is_essential
    }).eq("id", expense_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    return {"status": "ok", "is_essential": payload.is_essential}


@app.post("/api/analytics/ai-recommendations")
async def get_ai_recommendations(
    days: int = Body(30, description="Período em dias para análise"),
    start_date: Optional[str] = Body(None, description="Data inicial (YYYY-MM-DD). Se não informado, usa últimos N dias"),
    _user=Depends(verify_token),
):
    """
    Gera recomendações usando ChatGPT baseado em TODOS os dados do banco.
    Analisa padrões históricos e sugere ações para evitar problemas de caixa.
    Salva automaticamente no banco de dados.
    """
    from .analytics_service import get_ai_financial_recommendations
    
    try:
        recommendations = get_ai_financial_recommendations(days, start_date, save_to_db=True)
        return recommendations
    except Exception as e:
        import traceback
        print(f"[ERROR] Erro ao gerar recomendações AI: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erro ao gerar recomendações: {str(e)}")


@app.get("/api/analytics/ai-recommendations/history")
async def get_ai_recommendations_history(
    limit: int = Query(10, description="Número máximo de recomendações a retornar"),
    _user=Depends(verify_token),
):
    """
    Retorna histórico de recomendações da IA ordenado por data (mais recente primeiro).
    """
    from .supabase_client import get_supabase
    supabase = get_supabase()
    
    try:
        response = supabase.table("ai_recommendations").select("*").order("created_at", desc=True).limit(limit).execute()
        recommendations = response.data or []
        
        # Formata para retorno
        formatted = []
        for rec in recommendations:
            formatted.append({
                "id": rec.get("id"),
                "created_at": rec.get("created_at"),
                "analysis_period_days": rec.get("analysis_period_days"),
                "analysis_start_date": rec.get("analysis_start_date"),
                "recommendations_text": rec.get("recommendations_text"),
                "recommendations_json": rec.get("recommendations_json")
            })
        
        return {
            "recommendations": formatted,
            "total": len(formatted)
        }
    except Exception as e:
        import traceback
        print(f"[ERROR] Erro ao buscar histórico de recomendações: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")


