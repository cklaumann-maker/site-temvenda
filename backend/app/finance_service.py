from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import calendar
import io

import pandas as pd

from .google_drive import download_excel_from_drive
from .supabase_client import get_supabase
from .config import get_settings


@dataclass
class ForecastConfig:
    weekday_money: float
    weekday_pix: float
    weekday_card: float
    weekday_convenio: float
    monday_money: float
    monday_pix: float
    monday_card: float
    monday_convenio: float


FORECAST_CONFIG = ForecastConfig(
    weekday_money=13334.00,
    weekday_pix=6010.11,
    weekday_card=15706.20,
    weekday_convenio=179.11,
    monday_money=29296.30,
    monday_pix=13204.89,
    monday_card=34508.30,
    monday_convenio=393.52,
)


def parse_month_code(month_code: str) -> tuple[int, int]:
    """
    Converte monthCode no formato 'MM-YY' para (ano, mês).
    Ex.: '12-25' -> (2025, 12)
    """
    try:
        mm, yy = month_code.split("-")
        month = int(mm)
        year = 2000 + int(yy)
        return year, month
    except Exception as e:
        raise ValueError(f"monthCode inválido: {month_code}") from e


def build_forecast_for_day(d: date) -> dict[str, float]:
    """
    Calcula o forecast de entrada de caixa para um dia específico.
    Segunda = 0, Domingo = 6 em weekday().
    """
    wd = d.weekday()
    if wd >= 5:
        # Sábado (5) ou domingo (6): 0
        return {
            "money": 0.0,
            "pix": 0.0,
            "card": 0.0,
            "convenio": 0.0,
        }

    if wd == 0:
        return {
            "money": FORECAST_CONFIG.monday_money,
            "pix": FORECAST_CONFIG.monday_pix,
            "card": FORECAST_CONFIG.monday_card,
            "convenio": FORECAST_CONFIG.monday_convenio,
        }

    return {
        "money": FORECAST_CONFIG.weekday_money,
        "pix": FORECAST_CONFIG.weekday_pix,
        "card": FORECAST_CONFIG.weekday_card,
        "convenio": FORECAST_CONFIG.weekday_convenio,
    }


def _find_sheet(df_dict: dict[str, pd.DataFrame], prefix: str, month_code: str) -> pd.DataFrame:
    target = f"{prefix} {month_code}"
    # Tenta achar por nome exato
    if target in df_dict:
        return df_dict[target]
    # Fallback: procurar por prefixo
    for name, df in df_dict.items():
        if name.upper().startswith(prefix.upper()) and month_code in name:
            return df
    raise ValueError(f"Aba não encontrada para prefixo {prefix} e mês {month_code}")


def _get_column(df: pd.DataFrame, preferred_names: list[str], fallback_index: int) -> pd.Series:
    cols = {c.strip().lower(): c for c in df.columns if isinstance(c, str)}
    for name in preferred_names:
        key = name.strip().lower()
        if key in cols:
            return df[cols[key]]
    # Fallback por índice
    if fallback_index < len(df.columns):
        return df.iloc[:, fallback_index]
    return pd.Series(dtype=object)


def _get_column_optional(df: pd.DataFrame, preferred_names: list[str], fallback_index: int | None = None) -> pd.Series | None:
    """Tenta obter uma coluna, retorna None se não encontrar."""
    try:
        cols = {c.strip().lower(): c for c in df.columns if isinstance(c, str)}
        for name in preferred_names:
            key = name.strip().lower()
            if key in cols:
                return df[cols[key]]
        if fallback_index is not None and fallback_index < len(df.columns):
            return df.iloc[:, fallback_index]
    except Exception:
        pass
    return None


def _safe_float(value) -> float | None:
    """Converte valor para float de forma segura."""
    if pd.isna(value):
        return None
    try:
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            text = text.replace(".", "").replace(",", ".")
            return float(text)
        return float(value)
    except Exception:
        return None


def _safe_date(value) -> date | None:
    """Converte valor para date de forma segura."""
    if pd.isna(value):
        return None
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def _safe_str(value) -> str | None:
    """Converte valor para string de forma segura."""
    if pd.isna(value):
        return None
    try:
        s = str(value).strip()
        return s if s else None
    except Exception:
        return None


def process_excel_month(excel_bytes: bytes, month_code: str) -> list[dict]:
    """
    Lê o Excel e constrói dicionários compatíveis com a tabela finance_daily
    para o mês informado.
    """
    year, month = parse_month_code(month_code)
    _, last_day = calendar.monthrange(year, month)

    # Carrega todas as abas em dict (envolve bytes em BytesIO para evitar warning)
    xls = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None, engine="openpyxl")

    dist_df = _find_sheet(xls, "DIST", month_code)
    desp_df = _find_sheet(xls, "DESP", month_code)

    # Colunas esperadas
    dist_due = _get_column(dist_df, ["Vencimento"], 0)
    dist_value = _get_column(dist_df, ["Valor"], 4)
    dist_paid = _get_column(dist_df, ["Valor pago", "Valor pago "], 5)

    desp_due = _get_column(desp_df, ["Vencimento"], 0)
    desp_value = _get_column(desp_df, ["Valor"], 5)
    desp_paid = _get_column(desp_df, ["Valor pago", "Valor pago "], 6)

    # Normaliza datas e valores
    def normalize(df_dates, df_value):
        series = []
        for d, v in zip(df_dates, df_value):
            if pd.isna(d) or pd.isna(v):
                continue
            try:
                dt = pd.to_datetime(d).date()
            except Exception:
                continue
            # Tenta converter o valor para float, ignorando linhas com texto estranho
            try:
                if isinstance(v, str):
                    text = v.strip()
                    if not text:
                        continue
                    # Trata formatos brasileiros: 1.234,56
                    # Remove espaços e normaliza separador decimal
                    text = text.replace(".", "").replace(",", ".")
                    num = float(text)
                else:
                    num = float(v)
            except Exception:
                # Se não conseguir converter, ignora esta linha
                continue
            series.append((dt, num))
        return series

    dist_planned = normalize(dist_due, dist_value)
    dist_paid_s = normalize(dist_due, dist_paid)
    desp_planned = normalize(desp_due, desp_value)
    desp_paid_s = normalize(desp_due, desp_paid)

    # Acumula por dia
    expenses_planned_by_day: dict[date, float] = {}
    expenses_paid_by_day: dict[date, float] = {}

    for dt, v in dist_planned + desp_planned:
        expenses_planned_by_day[dt] = expenses_planned_by_day.get(dt, 0.0) + v

    for dt, v in dist_paid_s + desp_paid_s:
        expenses_paid_by_day[dt] = expenses_paid_by_day.get(dt, 0.0) + v

    # Cria registros para cada dia do mês
    records: list[dict] = []
    for day in range(1, last_day + 1):
        d = date(year, month, day)
        wd_name = calendar.day_name[d.weekday()]  # em inglês; front pode traduzir se quiser

        forecast = build_forecast_for_day(d)
        forecast_total = (
            forecast["money"]
            + forecast["pix"]
            + forecast["card"]
            + forecast["convenio"]
        )

        expenses_planned = expenses_planned_by_day.get(d, 0.0)
        expenses_paid = expenses_paid_by_day.get(d, 0.0)

        purchases_planned = 0.0
        old_debts_paid = 0.0
        future_in_confirmed = 0.0
        sales = 0.0

        cash_in_total = forecast_total + future_in_confirmed
        cash_out_planned = expenses_planned + purchases_planned + old_debts_paid
        cash_out_real = expenses_paid + purchases_planned + old_debts_paid

        balance_projected = sales + cash_in_total - cash_out_planned
        balance_real = cash_in_total - cash_out_real

        record = {
            "month_code": month_code,
            "date": d.isoformat(),
            "weekday": wd_name,
            "sales": sales,
            "cash_in_forecast_total": forecast_total,
            "cash_in_actual_money": 0.0,
            "cash_in_actual_pix": 0.0,
            "cash_in_actual_card": 0.0,
            "cash_in_actual_convenio": 0.0,
            "future_in_confirmed": future_in_confirmed,
            "purchases_planned": purchases_planned,
            "old_debts_paid": old_debts_paid,
            "expenses_planned": expenses_planned,
            "expenses_paid": expenses_paid,
            "balance_projected": balance_projected,
            "balance_real": balance_real,
            "updated_at": datetime.utcnow().isoformat(),
        }
        records.append(record)

    return records


def process_expense_items(excel_bytes: bytes, month_code: str) -> list[dict]:
    """
    Processa despesas individuais do Excel e retorna lista de expense_items.
    Extrai informações detalhadas: fornecedor, juros, forma de pagamento, etc.
    """
    year, month = parse_month_code(month_code)
    
    xls = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None, engine="openpyxl")
    
    dist_df = _find_sheet(xls, "DIST", month_code)
    desp_df = _find_sheet(xls, "DESP", month_code)
    
    expense_items: list[dict] = []
    
    def process_sheet(df: pd.DataFrame, category: str):
        """Processa uma aba (DIST ou DESP) e extrai despesas individuais."""
        # Colunas obrigatórias
        due_date_col = _get_column(df, ["Vencimento", "Data", "Data Vencimento"], 0)
        value_col = _get_column(df, ["Valor", "Valor Original"], 4 if category == "DIST" else 5)
        paid_col = _get_column(df, ["Valor pago", "Valor Pago", "Pago"], 5 if category == "DIST" else 6)
        
        # Colunas opcionais
        supplier_col = _get_column_optional(df, ["Fornecedor", "Credor", "Fornecedor/Credor", "Nome"], 1)
        desc_col = _get_column_optional(df, ["Descrição", "Descricao", "Observação", "Obs"], 2)
        interest_col = _get_column_optional(df, ["Juros", "Multa", "Juros/Multa", "Acréscimo"], None)
        payment_method_col = _get_column_optional(df, ["Forma Pagamento", "Forma de Pagamento", "Pagamento", "Tipo Pagamento"], None)
        payment_date_col = _get_column_optional(df, ["Data Pagamento", "Data Pago", "Dt Pagamento"], None)
        
        # Processa cada linha
        for idx in range(len(df)):
            due_date = _safe_date(due_date_col.iloc[idx] if idx < len(due_date_col) else None)
            if not due_date:
                continue
            
            amount = _safe_float(value_col.iloc[idx] if idx < len(value_col) else None)
            if amount is None or amount <= 0:
                continue
            
            amount_paid = _safe_float(paid_col.iloc[idx] if idx < len(paid_col) else None) or 0.0
            supplier = _safe_str(supplier_col.iloc[idx] if supplier_col is not None and idx < len(supplier_col) else None) or "Não informado"
            description = _safe_str(desc_col.iloc[idx] if desc_col is not None and idx < len(desc_col) else None)
            interest = _safe_float(interest_col.iloc[idx] if interest_col is not None and idx < len(interest_col) else None) or 0.0
            payment_method = _safe_str(payment_method_col.iloc[idx] if payment_method_col is not None and idx < len(payment_method_col) else None)
            payment_date = _safe_date(payment_date_col.iloc[idx] if payment_date_col is not None and idx < len(payment_date_col) else None)
            
            # Calcula valores para validação (será recalculado pelo trigger, mas definimos aqui para consistência)
            total_due = amount + interest
            if total_due > 0:
                percent_paid = min(100.0, (amount_paid / total_due) * 100)
            else:
                percent_paid = 0.0
            remaining_amount = max(0.0, total_due - amount_paid)
            
            if amount_paid >= total_due:
                status = "Quitada"
            elif amount_paid > 0:
                status = "Parcialmente paga"
            elif payment_date is None and due_date < date.today():
                status = "Vencida"
            else:
                status = "Pendente"
            
            expense_items.append({
                "month_code": month_code,
                "due_date": due_date.isoformat(),
                "payment_date": payment_date.isoformat() if payment_date else None,
                "supplier": supplier,
                "description": description,
                "category": category,
                "amount": amount,
                "amount_paid": amount_paid,
                "interest": interest,
                "payment_method": payment_method,
                "status": status,
                "percent_paid": round(percent_paid, 2),
                "remaining_amount": round(remaining_amount, 2),
            })
    
    process_sheet(dist_df, "DIST")
    process_sheet(desp_df, "DESP")
    
    return expense_items


async def refresh_month(month_code: str) -> None:
    """
    Regra de refresh:
    - apaga finance_daily do mês
    - apaga expense_items do mês
    - reimporta Excel e recria registros
    - registra em finance_month_runs
    """
    supabase = get_supabase()

    # Apaga registros existentes do mês
    supabase.table("finance_daily").delete().eq("month_code", month_code).execute()
    supabase.table("expense_items").delete().eq("month_code", month_code).execute()

    excel_bytes = download_excel_from_drive()
    records = process_excel_month(excel_bytes, month_code)
    expense_items = process_expense_items(excel_bytes, month_code)

    if records:
        supabase.table("finance_daily").insert(records).execute()
    
    if expense_items:
        supabase.table("expense_items").insert(expense_items).execute()

    supabase.table("finance_month_runs").insert(
        {
            "month_code": month_code,
            "source_file_id": "drive",
            "status": "completed",
            "notes": None,
        }
    ).execute()


# ---------- PROJEÇÃO D+60 ----------


def _load_projection_sheet() -> pd.DataFrame:
    """
    Lê a planilha de projeção (aba PROJECAO) usando GOOGLE_PROJECTION_FILE_ID.
    """
    settings = get_settings()
    if not settings.projection_file_id:
        raise RuntimeError("GOOGLE_PROJECTION_FILE_ID não configurado")

    excel_bytes = download_excel_from_drive(settings.projection_file_id)
    xls = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None, engine="openpyxl")
    # Tenta localizar aba PROJECAO (case-insensitive)
    target_name = None
    for name in xls.keys():
        if name.strip().upper() == "PROJECAO":
            target_name = name
            break
    if not target_name:
        raise RuntimeError("Aba PROJECAO não encontrada na planilha de projeção")
    return xls[target_name]


def _parse_projection_sheet(df: pd.DataFrame) -> dict[date, dict]:
    """
    Converte a aba PROJECAO em um dicionário:
    { date: { 'entrada_prevista': float, 'saida_prevista': float, 'observacao': str } }
    """
    # Mapear colunas por nome (case-insensitive)
    cols = {str(c).strip().lower(): c for c in df.columns}

    def col(name_candidates, fallback_idx=None):
        for n in name_candidates:
            key = n.strip().lower()
            if key in cols:
                return df[cols[key]]
        if fallback_idx is not None and fallback_idx < len(df.columns):
            return df.iloc[:, fallback_idx]
        return None

    date_col = col(["data"], 0)
    in_col = col(["entrada_prevista", "entrada prevista", "entrada"], 1)
    out_col = col(["saida_prevista", "saída_prevista", "saida prevista", "saída prevista", "saida", "saída"], 2)
    obs_col = col(["observacao", "observação", "obs"], 3)

    proj: dict[date, dict] = {}
    if date_col is None:
        return proj

    for idx in range(len(df)):
        d_raw = date_col.iloc[idx]
        d = _safe_date(d_raw)
        if not d:
            continue

        entrada = _safe_float(in_col.iloc[idx]) if in_col is not None and idx < len(in_col) else None
        saida = _safe_float(out_col.iloc[idx]) if out_col is not None and idx < len(out_col) else None
        obs = _safe_str(obs_col.iloc[idx]) if obs_col is not None and idx < len(obs_col) else None

        proj[d] = {
            "entrada_prevista": entrada or 0.0,
            "saida_prevista": saida or 0.0,
            "observacao": obs,
        }

    return proj


def _get_starting_cash_internal(supabase) -> float:
    resp = supabase.table("finance_settings").select("*").limit(1).execute()
    rows = resp.data or []
    if not rows:
        # Cria configuração padrão
        supabase.table("finance_settings").insert({"starting_cash": 0.0}).execute()
        return 0.0
    return float(rows[0].get("starting_cash", 0.0))


def set_starting_cash(value: float) -> float:
    supabase = get_supabase()
    resp = supabase.table("finance_settings").select("*").limit(1).execute()
    rows = resp.data or []
    if not rows:
        supabase.table("finance_settings").insert({"starting_cash": value}).execute()
    else:
        sid = rows[0]["id"]
        supabase.table("finance_settings").update({"starting_cash": value}).eq("id", sid).execute()
    return value


def get_starting_cash() -> float:
    supabase = get_supabase()
    return _get_starting_cash_internal(supabase)


def _compute_baseline_expenses(supabase, end_date: date, window_days: int = 14) -> float:
    """
    Calcula média móvel de expenses_paid dos últimos N dias até end_date.
    """
    start_date = end_date - timedelta(days=window_days - 1)
    resp = (
        supabase.table("finance_daily")
        .select("date,expenses_paid")
        .gte("date", start_date.isoformat())
        .lte("date", end_date.isoformat())
        .order("date")
        .execute()
    )
    rows = resp.data or []
    if not rows:
        return 0.0
    vals = [float(r.get("expenses_paid", 0.0)) for r in rows]
    if not vals:
        return 0.0
    return sum(vals) / len(vals)


async def refresh_projection(days: int = 60) -> None:
    """
    Calcula projeção D+N combinando:
    - Dados reais de finance_daily
    - Planilha PROJECAO (GOOGLE_PROJECTION_FILE_ID)
    - Forecast padrão como fallback
    """
    supabase = get_supabase()
    today = date.today()
    horizon = today + timedelta(days=days)

    # Carrega mapa de projeções da planilha
    proj_df = _load_projection_sheet()
    proj_map = _parse_projection_sheet(proj_df)

    # Calcula baseline de despesas (média móvel)
    baseline_expenses = _compute_baseline_expenses(supabase, today, window_days=14)

    starting_cash = _get_starting_cash_internal(supabase)

    # Apaga projeções existentes no horizonte
    supabase.table("finance_projection_daily").delete().gte("date", today.isoformat()).lte(
        "date", horizon.isoformat()
    ).execute()

    running_balance = starting_cash
    records: list[dict] = []

    for offset in range(0, days + 1):
        d = today + timedelta(days=offset)
        d_iso = d.isoformat()

        # Tenta buscar dado real do dia em finance_daily
        daily_resp = supabase.table("finance_daily").select("*").eq("date", d_iso).limit(1).execute()
        daily = daily_resp.data[0] if daily_resp.data else None

        # Fonte de entradas
        cash_in = 0.0
        source_in = "forecast"

        real_in = 0.0
        if daily:
            real_in = (
                float(daily.get("cash_in_actual_money", 0.0))
                + float(daily.get("cash_in_actual_pix", 0.0))
                + float(daily.get("cash_in_actual_card", 0.0))
                + float(daily.get("cash_in_actual_convenio", 0.0))
            )

        if real_in > 0:
            cash_in = real_in
            source_in = "real"
        else:
            proj_for_day = proj_map.get(d)
            if proj_for_day and proj_for_day.get("entrada_prevista") not in (None, 0):
                cash_in = float(proj_for_day["entrada_prevista"])
                source_in = "sheet"
            else:
                # Usa forecast padrão como fallback
                forecast = build_forecast_for_day(d)
                cash_in = (
                    forecast["money"]
                    + forecast["pix"]
                    + forecast["card"]
                    + forecast["convenio"]
                )
                source_in = "forecast"

        # Fonte de saídas
        cash_out = 0.0
        source_out = "rational"

        if d <= today and daily:
            # Para dias passados/hoje: saídas reais
            cash_out = (
                float(daily.get("expenses_paid", 0.0))
                + float(daily.get("purchases_planned", 0.0))
                + float(daily.get("old_debts_paid", 0.0))
            )
            source_out = "real"
        else:
            proj_for_day = proj_map.get(d)
            sheet_out = 0.0
            if proj_for_day and proj_for_day.get("saida_prevista") not in (None, 0):
                sheet_out = float(proj_for_day["saida_prevista"])

            # Componente racional baseado na média móvel
            rational_out = baseline_expenses

            cash_out = sheet_out + rational_out
            source_out = "rational"

        projected_balance_day = cash_in - cash_out
        running_balance += projected_balance_day

        notes = None
        proj_for_day = proj_map.get(d)
        if proj_for_day and proj_for_day.get("observacao"):
            notes = proj_for_day["observacao"]

        records.append(
            {
                "date": d_iso,
                "cash_in": cash_in,
                "cash_out": cash_out,
                "projected_balance_day": projected_balance_day,
                "projected_running_balance": running_balance,
                "source_in": source_in,
                "source_out": source_out,
                "notes": notes,
                "updated_at": datetime.utcnow().isoformat(),
            }
        )

    if records:
        supabase.table("finance_projection_daily").insert(records).execute()


async def get_projection(days: int = 60) -> tuple[list[dict], float, datetime | None]:
    """
    Retorna projeção armazenada em finance_projection_daily para os próximos N dias,
    junto com caixa inicial e data da última atualização.
    """
    supabase = get_supabase()
    today = date.today()
    horizon = today + timedelta(days=days)

    resp = (
        supabase.table("finance_projection_daily")
        .select("*")
        .gte("date", today.isoformat())
        .lte("date", horizon.isoformat())
        .order("date")
        .execute()
    )
    rows = resp.data or []

    last_updated: datetime | None = None
    for r in rows:
        ts = r.get("updated_at")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                if not last_updated or dt > last_updated:
                    last_updated = dt
            except Exception:
                continue

    starting_cash = _get_starting_cash_internal(supabase)
    return rows, starting_cash, last_updated


async def get_month(month_code: str) -> list[dict]:
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    return resp.data or []



