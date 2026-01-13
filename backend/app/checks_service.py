"""
Service for checks management
"""
from datetime import date, datetime, timedelta
from typing import Optional
from statistics import median

from .supabase_client import get_supabase


def create_check_event(supabase, check_id: str, event_type: str, payload: Optional[dict] = None):
    """Cria um evento de auditoria para um cheque"""
    supabase.table("check_events").insert({
        "check_id": check_id,
        "event_type": event_type,
        "payload": payload
    }).execute()


def create_check(data: dict) -> dict:
    """Cria um novo cheque"""
    supabase = get_supabase()
    
    check_data = {
        "issue_date": data["issue_date"].isoformat() if isinstance(data["issue_date"], date) else data["issue_date"],
        "due_date": data["due_date"].isoformat() if isinstance(data["due_date"], date) else data["due_date"],
        "amount": data["amount"],
        "payee": data["payee"],
        "category": data["category"],
        "status": "EM_ABERTO",
    }
    
    if data.get("payer"):
        check_data["payer"] = data["payer"]
    if data.get("bank"):
        check_data["bank"] = data["bank"]
    if data.get("check_number"):
        check_data["check_number"] = data["check_number"]
    if data.get("memo"):
        check_data["memo"] = data["memo"]
    if data.get("linked_expense_item_id"):
        check_data["linked_expense_item_id"] = data["linked_expense_item_id"]
    
    resp = supabase.table("checks").insert(check_data).execute()
    
    if resp.data:
        check_id = resp.data[0]["id"]
        create_check_event(supabase, check_id, "CRIADO")
        return resp.data[0]
    
    raise Exception("Erro ao criar cheque")


def list_checks(
    status: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    payee: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> list[dict]:
    """Lista cheques com filtros"""
    supabase = get_supabase()
    query = supabase.table("checks").select("*")
    
    if status:
        query = query.eq("status", status)
    if from_date:
        query = query.gte("due_date", from_date.isoformat())
    if to_date:
        query = query.lte("due_date", to_date.isoformat())
    if payee:
        query = query.ilike("payee", f"%{payee}%")
    
    query = query.order("due_date", desc=False).limit(limit).offset(offset)
    resp = query.execute()
    
    checks = resp.data or []
    
    # Calcula delay_days para cheques compensados
    for check in checks:
        if check.get("cleared_date") and check.get("due_date"):
            cleared = datetime.strptime(check["cleared_date"], "%Y-%m-%d").date()
            due = datetime.strptime(check["due_date"], "%Y-%m-%d").date()
            check["delay_days"] = (cleared - due).days
        else:
            check["delay_days"] = None
    
    return checks


def get_check(check_id: str) -> Optional[dict]:
    """Busca um cheque por ID"""
    supabase = get_supabase()
    resp = supabase.table("checks").select("*").eq("id", check_id).limit(1).execute()
    
    if resp.data:
        check = resp.data[0]
        # Calcula delay_days
        if check.get("cleared_date") and check.get("due_date"):
            cleared = datetime.strptime(check["cleared_date"], "%Y-%m-%d").date()
            due = datetime.strptime(check["due_date"], "%Y-%m-%d").date()
            check["delay_days"] = (cleared - due).days
        else:
            check["delay_days"] = None
        return check
    
    return None


def update_check(check_id: str, data: dict) -> dict:
    """Atualiza um cheque"""
    supabase = get_supabase()
    
    update_data = {}
    if "issue_date" in data:
        update_data["issue_date"] = data["issue_date"].isoformat() if isinstance(data["issue_date"], date) else data["issue_date"]
    if "due_date" in data:
        update_data["due_date"] = data["due_date"].isoformat() if isinstance(data["due_date"], date) else data["due_date"]
    if "amount" in data:
        update_data["amount"] = data["amount"]
    if "payer" in data:
        update_data["payer"] = data["payer"]
    if "payee" in data:
        update_data["payee"] = data["payee"]
    if "category" in data:
        update_data["category"] = data["category"]
    if "bank" in data:
        update_data["bank"] = data["bank"]
    if "check_number" in data:
        update_data["check_number"] = data["check_number"]
    if "memo" in data:
        update_data["memo"] = data["memo"]
    if "linked_expense_item_id" in data:
        update_data["linked_expense_item_id"] = data["linked_expense_item_id"]
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    resp = supabase.table("checks").update(update_data).eq("id", check_id).execute()
    
    if resp.data:
        create_check_event(supabase, check_id, "EDITADO", {"updated_fields": list(update_data.keys())})
        return resp.data[0]
    
    raise Exception("Erro ao atualizar cheque")


def clear_check(check_id: str, cleared_date: date) -> dict:
    """
    Marca um cheque como compensado e registra no fluxo de caixa.
    Executa em transação: atualiza cheque + lança no finance_daily.
    """
    supabase = get_supabase()
    
    # Busca o cheque
    check = get_check(check_id)
    if not check:
        raise Exception("Cheque não encontrado")
    
    if check["status"] == "COMPENSADO":
        raise Exception("Cheque já está compensado")
    
    amount = float(check["amount"])
    cleared_date_str = cleared_date.isoformat()
    
    # Atualiza o cheque
    resp = supabase.table("checks").update({
        "status": "COMPENSADO",
        "cleared_date": cleared_date_str,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", check_id).execute()
    
    if not resp.data:
        raise Exception("Erro ao atualizar cheque")
    
    # Cria evento
    create_check_event(supabase, check_id, "COMPENSADO", {"cleared_date": cleared_date_str})
    
    # Busca ou cria o dia no finance_daily
    day_resp = supabase.table("finance_daily").select("*").eq("date", cleared_date_str).limit(1).execute()
    
    if day_resp.data:
        # Atualiza o dia existente
        day = day_resp.data[0]
        current_checks_paid = float(day.get("checks_paid_total", 0))
        supabase.table("finance_daily").update({
            "checks_paid_total": current_checks_paid + amount
        }).eq("id", day["id"]).execute()
    else:
        # Cria novo dia (caso não exista)
        # Precisa de month_code e weekday
        from calendar import day_name
        date_obj = cleared_date
        month_code = f"{date_obj.month:02d}-{str(date_obj.year)[2:]}"
        weekday = day_name[date_obj.weekday()]
        
        supabase.table("finance_daily").insert({
            "month_code": month_code,
            "date": cleared_date_str,
            "weekday": weekday,
            "checks_paid_total": amount
        }).execute()
    
    # Recalcula saldo real acumulado a partir desta data
    from .finance_service import _recalculate_balance_real_accumulated_from_date
    _recalculate_balance_real_accumulated_from_date(supabase, cleared_date)
    
    return resp.data[0]


def cancel_check(check_id: str) -> dict:
    """Cancela um cheque"""
    supabase = get_supabase()
    
    resp = supabase.table("checks").update({
        "status": "CANCELADO",
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", check_id).execute()
    
    if resp.data:
        create_check_event(supabase, check_id, "CANCELADO")
        return resp.data[0]
    
    raise Exception("Erro ao cancelar cheque")


def return_check(check_id: str) -> dict:
    """Marca um cheque como devolvido"""
    supabase = get_supabase()
    
    resp = supabase.table("checks").update({
        "status": "DEVOLVIDO",
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", check_id).execute()
    
    if resp.data:
        create_check_event(supabase, check_id, "DEVOLVIDO")
        return resp.data[0]
    
    raise Exception("Erro ao marcar cheque como devolvido")


def get_top_delayers(from_date: Optional[date] = None, to_date: Optional[date] = None, limit: int = 10) -> list[dict]:
    """
    Retorna ranking de beneficiários que mais demoram para depositar cheques.
    Considera apenas cheques compensados.
    """
    supabase = get_supabase()
    
    query = supabase.table("checks").select("*").eq("status", "COMPENSADO").not_.is_("cleared_date", "null")
    
    if from_date:
        query = query.gte("cleared_date", from_date.isoformat())
    if to_date:
        query = query.lte("cleared_date", to_date.isoformat())
    
    resp = query.execute()
    checks = resp.data or []
    
    # Agrupa por payee
    payee_groups = {}
    for check in checks:
        payee = check["payee"]
        if payee not in payee_groups:
            payee_groups[payee] = []
        
        cleared = datetime.strptime(check["cleared_date"], "%Y-%m-%d").date()
        due = datetime.strptime(check["due_date"], "%Y-%m-%d").date()
        delay = (cleared - due).days
        
        payee_groups[payee].append({
            "delay": delay,
            "amount": float(check["amount"])
        })
    
    # Calcula estatísticas por payee
    results = []
    for payee, items in payee_groups.items():
        delays = [item["delay"] for item in items]
        amounts = [item["amount"] for item in items]
        
        # Apenas atrasos positivos (depositaram depois do vencimento)
        positive_delays = [d for d in delays if d > 0]
        
        if positive_delays:
            avg_delay = sum(positive_delays) / len(positive_delays)
            median_delay = median(positive_delays) if len(positive_delays) > 1 else positive_delays[0]
        else:
            avg_delay = 0
            median_delay = 0
        
        results.append({
            "payee": payee,
            "avg_delay_days": round(avg_delay, 2),
            "median_delay_days": round(median_delay, 2),
            "count": len(items),
            "total_amount": sum(amounts)
        })
    
    # Ordena por média de atraso (decrescente)
    results.sort(key=lambda x: x["avg_delay_days"], reverse=True)
    
    return results[:limit]

