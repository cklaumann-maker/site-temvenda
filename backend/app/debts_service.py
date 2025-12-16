from __future__ import annotations

from datetime import date

from .supabase_client import get_supabase


def _compute_debt_status(debt: dict, total_paid: float) -> str:
    total = float(debt["total_amount"])
    if total_paid >= total:
        return "Quitada"
    if total_paid > 0:
        return "Parcialmente paga"
    return "Aberta"


def _compute_debt_totals(debt: dict) -> dict:
    supabase = get_supabase()
    pay_resp = (
        supabase.table("debt_payments")
        .select("amount_paid")
        .eq("debt_id", debt["id"])
        .execute()
    )
    payments = pay_resp.data or []
    total_paid = sum(float(p["amount_paid"]) for p in payments)
    remaining = float(debt["total_amount"]) - total_paid
    if remaining < 0:
        remaining = 0.0
    status = _compute_debt_status(debt, total_paid)
    return {"amount_paid": total_paid, "remaining_amount": remaining, "status": status}


def _recalc_debt_status(debt_id: str) -> None:
    supabase = get_supabase()
    debt_resp = supabase.table("debts").select("*").eq("id", debt_id).maybe_single().execute()
    debt = debt_resp.data
    if not debt:
        return
    totals = _compute_debt_totals(debt)
    supabase.table("debts").update({"status": totals["status"]}).eq("id", debt_id).execute()


def create_debt(payload: dict) -> dict:
    supabase = get_supabase()
    debt_resp = supabase.table("debts").insert(
        {
            "category": payload["category"],
            "creditor": payload["creditor"],
            "description": payload.get("description"),
            "total_amount": payload["total_amount"],
            "status": "Aberta",
        }
    ).execute()
    debt = debt_resp.data[0]
    totals = _compute_debt_totals(debt)
    return {**debt, **totals}


def list_debts() -> list[dict]:
    supabase = get_supabase()
    resp = supabase.table("debts").select("*").order("created_at", desc=True).execute()
    debts = resp.data or []
    enriched = []
    for d in debts:
        totals = _compute_debt_totals(d)
        enriched.append({**d, **totals})
    return enriched


def get_debt_with_payments(debt_id: str) -> tuple[dict | None, list[dict]]:
    supabase = get_supabase()
    debt_resp = supabase.table("debts").select("*").eq("id", debt_id).maybe_single().execute()
    debt = debt_resp.data
    if not debt:
        return None, []
    pay_resp = (
        supabase.table("debt_payments")
        .select("*")
        .eq("debt_id", debt_id)
        .order("payment_date", desc=True)
        .execute()
    )
    payments = pay_resp.data or []
    totals = _compute_debt_totals(debt)
    debt = {**debt, **totals}
    return debt, payments


def update_debt(debt_id: str, payload: dict) -> dict | None:
    supabase = get_supabase()
    update_fields = {}
    for field in ["category", "creditor", "description", "total_amount"]:
        if field in payload and payload[field] is not None:
            update_fields[field] = payload[field]
    if not update_fields:
        resp = supabase.table("debts").select("*").eq("id", debt_id).maybe_single().execute()
        debt = resp.data
        if debt:
            totals = _compute_debt_totals(debt)
            debt = {**debt, **totals}
        return debt
    resp = (
        supabase.table("debts")
        .update(update_fields)
        .eq("id", debt_id)
        .select("*")
        .maybe_single()
        .execute()
    )
    debt = resp.data
    if debt:
        totals = _compute_debt_totals(debt)
        debt = {**debt, **totals}
    return debt


def pay_debt(debt_id: str, payment_date: date, amount_paid: float, money_source: str | None, notes: str | None):
    supabase = get_supabase()
    debt_resp = supabase.table("debts").select("*").eq("id", debt_id).maybe_single().execute()
    debt = debt_resp.data
    if not debt:
        return None, "Dívida não encontrada"

    totals = _compute_debt_totals(debt)
    if totals["status"] == "Quitada" and totals["amount_paid"] >= float(debt["total_amount"]):
        return None, "Dívida já está quitada"

    # Cria pagamento
    pay_resp = supabase.table("debt_payments").insert(
        {
            "debt_id": debt_id,
            "payment_date": payment_date.isoformat(),
            "amount_paid": amount_paid,
            "money_source": money_source,
            "notes": notes,
        }
    ).execute()

    _recalc_debt_status(debt_id)

    # Integração com fluxo de caixa: soma em old_debts_paid do dia
    year, month = payment_date.year, payment_date.month
    month_code = f"{month:02d}-{year % 100:02d}"

    daily_resp = (
        supabase.table("finance_daily")
        .select("*")
        .eq("month_code", month_code)
        .eq("date", payment_date.isoformat())
        .maybe_single()
        .execute()
    )
    day = daily_resp.data
    if not day:
        # Se não existir registro para o dia, não criamos um novo; retornamos erro amigável
        return None, "Dia não encontrado em finance_daily. Atualize o mês primeiro."

    old_debts_paid = float(day.get("old_debts_paid", 0.0)) + amount_paid
    day["old_debts_paid"] = old_debts_paid

    cash_in_actual_total = (
        float(day.get("cash_in_actual_money", 0.0))
        + float(day.get("cash_in_actual_pix", 0.0))
        + float(day.get("cash_in_actual_card", 0.0))
        + float(day.get("cash_in_actual_convenio", 0.0))
    )
    cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day["cash_in_forecast_total"])
    cash_in_total = cash_in_used + float(day.get("future_in_confirmed", 0.0))
    cash_out_planned = float(day.get("expenses_planned", 0.0)) + float(day.get("purchases_planned", 0.0)) + old_debts_paid
    cash_out_real = float(day.get("expenses_paid", 0.0)) + float(day.get("purchases_planned", 0.0)) + old_debts_paid

    balance_projected = float(day.get("sales", 0.0)) + cash_in_total - cash_out_planned
    balance_real = cash_in_total - cash_out_real

    supabase.table("finance_daily").update(
        {
            "old_debts_paid": old_debts_paid,
            "balance_projected": balance_projected,
            "balance_real": balance_real,
        }
    ).eq("id", day["id"]).execute()

    return pay_resp.data[0], None


def get_debt_history(debt_id: str) -> list[dict]:
    supabase = get_supabase()
    pay_resp = (
        supabase.table("debt_payments")
        .select("*")
        .eq("debt_id", debt_id)
        .order("created_at")
        .execute()
    )
    payments = pay_resp.data or []
    items: list[dict] = []
    for p in payments:
        items.append(
            {
                "type": "payment",
                "created_at": p["created_at"],
                "payment_date": p["payment_date"],
                "amount_paid": float(p["amount_paid"]),
                "money_source": p.get("money_source"),
                "notes": p.get("notes"),
            }
        )
    return items
