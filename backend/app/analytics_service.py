"""
Service for financial analytics and bottleneck detection

IMPORTANTE: Este serviço busca TODOS os dados DIRETAMENTE do banco de dados (Supabase).
- SEM cache
- SEM dependências de outros endpoints
- SEM processos manuais
- TUDO é buscado em tempo real do banco

As análises são processadas em Python usando dados frescos do banco.
"""
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict
from statistics import mean, stdev, median
import calendar
from collections import defaultdict
import json
import os

from .supabase_client import get_supabase

# Tradução de dias da semana para português
WEEKDAYS_PT = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

WEEKDAYS_PT_SHORT = {
    'Monday': 'Seg',
    'Tuesday': 'Ter',
    'Wednesday': 'Qua',
    'Thursday': 'Qui',
    'Friday': 'Sex',
    'Saturday': 'Sáb',
    'Sunday': 'Dom'
}


def get_all_days_data() -> List[Dict]:
    """
    Busca todos os dias disponíveis no banco de dados.
    DIRETAMENTE do Supabase, sem cache.
    """
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").order("date").execute()
    return resp.data or []


def get_comprehensive_analytics() -> dict:
    """
    Análise abrangente buscando DIRETAMENTE do banco de dados.
    
    REGRAS:
    - SEM cache
    - SEM dependências de outros endpoints
    - SEM processos manuais
    - TUDO é buscado DIRETAMENTE do Supabase em tempo real
    
    Retorna análises qualificadas em Python para os próximos 30-45 dias.
    Todos os dados vêm DIRETAMENTE das tabelas do banco:
    - finance_daily
    - expense_items
    - checks
    - essential_suppliers
    """
    supabase = get_supabase()
    today = date.today()
    future_date = today + timedelta(days=45)
    today_str = today.isoformat()
    future_date_str = future_date.isoformat()
    
    print(f"[get_comprehensive_analytics] 🔄 Buscando dados DIRETAMENTE do banco para período {today_str} a {future_date_str}")
    
    # ============================================================
    # BUSCA DIRETA DO BANCO - Sem cache, sem dependências
    # ============================================================
    
    # 1. Busca dias futuros DIRETAMENTE do finance_daily
    print("[get_comprehensive_analytics] 📊 Buscando finance_daily do banco...")
    days_resp = supabase.table("finance_daily").select("*").gte("date", today_str).lte("date", future_date_str).order("date").execute()
    future_days = days_resp.data or []
    print(f"[get_comprehensive_analytics] ✅ {len(future_days)} dias encontrados no banco")
    
    # 2. Busca despesas futuras DIRETAMENTE do expense_items
    print("[get_comprehensive_analytics] 📋 Buscando expense_items do banco...")
    future_expenses_resp = supabase.table("expense_items").select("*").gte("due_date", today_str).lte("due_date", future_date_str).execute()
    future_expenses = future_expenses_resp.data or []
    print(f"[get_comprehensive_analytics] ✅ {len(future_expenses)} despesas futuras encontradas no banco")
    
    # 3. Busca despesas pagas DIRETAMENTE do expense_items (para gargalos)
    print("[get_comprehensive_analytics] 💰 Buscando despesas pagas do banco...")
    paid_expenses_resp = supabase.table("expense_items").select("*").gte("payment_date", today_str).lte("payment_date", future_date_str).execute()
    paid_expenses = paid_expenses_resp.data or []
    print(f"[get_comprehensive_analytics] ✅ {len(paid_expenses)} despesas pagas encontradas no banco")
    
    # Agrupa despesas pagas por data (em memória - muito mais rápido)
    expenses_by_payment_date = defaultdict(list)
    for exp in paid_expenses:
        payment_date_str = exp.get("payment_date")
        if payment_date_str:
            expenses_by_payment_date[payment_date_str].append(exp)
    
    # 4. Busca dados históricos DIRETAMENTE do banco (últimos 6 meses)
    print("[get_comprehensive_analytics] 📈 Buscando dados históricos do banco...")
    six_months_ago = today - timedelta(days=180)
    historical_days_resp = supabase.table("finance_daily").select("*").gte("date", six_months_ago.isoformat()).order("date").execute()
    historical_days = historical_days_resp.data or []
    print(f"[get_comprehensive_analytics] ✅ {len(historical_days)} dias históricos encontrados no banco")
    
    # 5. Busca despesas históricas DIRETAMENTE do banco
    historical_expenses_resp = supabase.table("expense_items").select("*").gte("due_date", six_months_ago.isoformat()).execute()
    historical_expenses = historical_expenses_resp.data or []
    print(f"[get_comprehensive_analytics] ✅ {len(historical_expenses)} despesas históricas encontradas no banco")
    
    # 6. Busca cheques compensados DIRETAMENTE do banco
    print("[get_comprehensive_analytics] 🏦 Buscando checks do banco...")
    all_checks_resp = supabase.table("checks").select("*").eq("status", "COMPENSADO").execute()
    all_checks = all_checks_resp.data or []
    print(f"[get_comprehensive_analytics] ✅ {len(all_checks)} cheques compensados encontrados no banco")
    
    # 7. Busca fornecedores essenciais DIRETAMENTE do banco
    print("[get_comprehensive_analytics] ⭐ Buscando essential_suppliers do banco...")
    essential_resp = supabase.table("essential_suppliers").select("*").execute()
    essential_suppliers = {e["supplier_name"].lower() for e in (essential_resp.data or [])}
    print(f"[get_comprehensive_analytics] ✅ {len(essential_suppliers)} fornecedores essenciais encontrados no banco")
    
    # Palavras-chave
    folha_keywords = ['folha', 'salário', 'salarios', 'pagamento pessoal', 'rh']
    aluguel_keywords = ['aluguel', 'locação', 'locacao']
    
    # ========== RESUMO EXECUTIVO ==========
    # Status atual
    today_day = next((d for d in future_days if d.get("date") == today_str), None)
    current_balance = float(today_day.get("balance_real", 0)) if today_day else 0.0
    
    # Próximo gargalo (usa dados futuros e despesas já agrupadas)
    print("[get_comprehensive_analytics] Detectando gargalos...")
    bottlenecks = _detect_bottlenecks_optimized(future_days, expenses_by_payment_date, essential_suppliers, folha_keywords, aluguel_keywords, today, future_date)
    next_bottleneck = None
    if bottlenecks:
        future_bottlenecks = [b for b in bottlenecks if datetime.strptime(b["date"], "%Y-%m-%d").date() >= today]
        if future_bottlenecks:
            next_bottleneck = min(future_bottlenecks, key=lambda x: x["date"])
    
    # Meta de caixa (soma de essenciais nos próximos 45 dias)
    essentials_total = _calculate_essentials_total(future_expenses, essential_suppliers, folha_keywords, aluguel_keywords)
    
    # Reserva diária recomendada
    daily_reserve = 0.0
    days_until_bottleneck = None
    if next_bottleneck:
        bottleneck_date = datetime.strptime(next_bottleneck["date"], "%Y-%m-%d").date()
        days_until_bottleneck = (bottleneck_date - today).days
        if days_until_bottleneck > 0:
            daily_reserve = next_bottleneck["cash_out_real"] / days_until_bottleneck
    
    # Alertas críticos
    critical_alerts = []
    if next_bottleneck and days_until_bottleneck:
        if days_until_bottleneck <= 3:
            critical_alerts.append({
                "type": "urgent",
                "message": f"⚠️ Gargalo crítico em {days_until_bottleneck} dias! Valor: {next_bottleneck['cash_out_real']:,.2f}",
                "date": next_bottleneck["date"]
            })
        elif days_until_bottleneck <= 7:
            critical_alerts.append({
                "type": "warning",
                "message": f"🟡 Atenção: Gargalo em {days_until_bottleneck} dias",
                "date": next_bottleneck["date"]
            })
    
    # Indicadores-chave
    total_essentials = essentials_total["total_folha"] + essentials_total["total_aluguel"] + essentials_total["total_essential_suppliers"] + essentials_total["total_cartorio"]
    critical_periods = [b for b in bottlenecks if b.get("is_essential_day") and datetime.strptime(b["date"], "%Y-%m-%d").date() >= today]
    
    # Ação principal sugerida
    main_action = "✅ Nenhuma ação urgente"
    if next_bottleneck and days_until_bottleneck:
        if days_until_bottleneck <= 7:
            main_action = f"🔴 URGENTE: Reservar R$ {daily_reserve:,.2f}/dia até {format_date(next_bottleneck['date'])}"
        elif days_until_bottleneck <= 14:
            main_action = f"🟡 Planejar reserva de R$ {daily_reserve:,.2f}/dia"
        else:
            main_action = f"📊 Monitorar gargalo previsto para {format_date(next_bottleneck['date'])}"
    
    # ========== LINHA DO TEMPO (30-45 dias) ==========
    print("[get_comprehensive_analytics] Construindo linha do tempo...")
    timeline_data = _build_timeline(today, future_date, future_days, future_expenses, bottlenecks, essential_suppliers, folha_keywords, aluguel_keywords)
    
    # ========== TABELA DE DESPESAS ==========
    print("[get_comprehensive_analytics] Construindo tabela de despesas...")
    expenses_table = _build_expenses_table(future_expenses, essential_suppliers, folha_keywords, aluguel_keywords)
    
    # ========== GRÁFICOS ==========
    print("[get_comprehensive_analytics] Construindo dados de gráficos...")
    charts_data = _build_charts_data(future_days, future_date, today)
    
    # ========== AÇÕES RECOMENDADAS ==========
    print("[get_comprehensive_analytics] Construindo ações recomendadas...")
    actions = _build_recommended_actions(bottlenecks, next_bottleneck, days_until_bottleneck, daily_reserve, essentials_total, today, future_date)
    
    # ========== ANÁLISE HISTÓRICA ==========
    print("[get_comprehensive_analytics] Construindo análise histórica...")
    historical_analysis = _build_historical_analysis(historical_days, historical_expenses)
    
    print("[get_comprehensive_analytics] ✅ Análise concluída! Todos os dados foram buscados DIRETAMENTE do banco.")
    
    # Retorna dados processados - TUDO veio diretamente do banco, sem cache, sem dependências
    return {
        "executive_summary": {
            "current_balance": current_balance,
            "next_bottleneck": {
                "date": next_bottleneck["date"] if next_bottleneck else None,
                "amount": next_bottleneck["cash_out_real"] if next_bottleneck else 0.0,
                "is_essential": next_bottleneck.get("is_essential_day", False) if next_bottleneck else False
            },
            "days_until_bottleneck": days_until_bottleneck,
            "cash_target_45_days": essentials_total["total_45_days"],
            "current_cash": current_balance,
            "daily_reserve_recommended": daily_reserve,
            "critical_alerts": critical_alerts,
            "key_indicators": {
                "total_essentials": total_essentials,
                "total_bottlenecks": len([b for b in bottlenecks if datetime.strptime(b["date"], "%Y-%m-%d").date() >= today]),
                "critical_periods_count": len(critical_periods),
                "most_critical_week": _find_most_critical_week(bottlenecks, today)
            },
            "main_action": main_action
        },
        "timeline": timeline_data,
        "expenses_table": expenses_table,
        "charts": charts_data,
        "recommended_actions": actions,
        "historical_analysis": historical_analysis
    }


def format_date(date_str: str) -> str:
    """Formata data para exibição"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return d.strftime("%d/%m/%Y")
    except:
        return date_str


def _detect_bottlenecks_optimized(future_days, expenses_by_payment_date, essential_suppliers, folha_keywords, aluguel_keywords, today, future_date):
    """
    Detecta gargalos de forma otimizada.
    IMPORTANTE: Considera APENAS datas FUTURAS (>= hoje).
    Usa dados já filtrados e despesas já agrupadas em memória (sem queries no loop).
    Todos os dados vêm DIRETAMENTE do banco.
    """
    days_with_cash_out = []
    for day in future_days:
        day_date_str = day.get("date")
        if not day_date_str:
            continue
        
        # GARANTE que só considera datas futuras
        try:
            day_date = datetime.strptime(day_date_str, "%Y-%m-%d").date()
            if day_date < today:  # Ignora dias do passado
                continue
        except:
            continue
        
        cash_out_real = (
            float(day.get("expenses_paid", 0))
            + float(day.get("purchases_planned", 0))
            + float(day.get("old_debts_paid", 0))
            + float(day.get("store_expenses_total", 0))
            + float(day.get("purchases_credit", 0))
            + float(day.get("checks_paid_total", 0))
        )
        cash_out_planned = (
            float(day.get("expenses_planned", 0))
            + float(day.get("purchases_planned", 0))
            + float(day.get("purchases_credit", 0))
            + float(day.get("store_expenses_total", 0))
        )
        
        days_with_cash_out.append({
            "date": day_date_str,
            "month_code": day.get("month_code"),
            "cash_out_real": cash_out_real,
            "cash_out_planned": cash_out_planned,
            "day_data": day
        })
    
    # Calcula limiar (média + 2 desvios) - APENAS para dias futuros
    cash_out_values = [d["cash_out_real"] for d in days_with_cash_out]
    if cash_out_values:
        global_avg = mean(cash_out_values)
        global_std = stdev(cash_out_values) if len(cash_out_values) > 1 else 0
        threshold = global_avg + (2 * global_std)
    else:
        threshold = 0
    
    # Identifica gargalos (OTIMIZADO: usa despesas já agrupadas em memória)
    # GARANTE que só retorna gargalos futuros
    bottlenecks = []
    for day_info in days_with_cash_out:
        day_date_str = day_info["date"]
        try:
            day_date = datetime.strptime(day_date_str, "%Y-%m-%d").date()
            # DUPLA VERIFICAÇÃO: só considera se for futuro
            if day_date < today:
                continue
        except:
            continue
        
        if day_info["cash_out_real"] >= threshold:
            # OTIMIZAÇÃO: Busca despesas do dict em memória (não faz query)
            expenses = expenses_by_payment_date.get(day_date_str, [])
            
            categories = defaultdict(float)
            suppliers = defaultdict(float)
            for exp in expenses:
                cat = exp.get("category", "Outros")
                categories[cat] += float(exp.get("amount_paid", 0))
                supplier = exp.get("supplier", "Não informado")
                suppliers[supplier] += float(exp.get("amount_paid", 0))
            
            top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
            top_suppliers = sorted(suppliers.items(), key=lambda x: x[1], reverse=True)[:5]
            
            is_essential = _is_essential_day(day_date, expenses, essential_suppliers, folha_keywords, aluguel_keywords)
            
            bottlenecks.append({
                "date": day_date_str,
                "month_code": day_info.get("month_code"),
                "cash_out_real": day_info["cash_out_real"],
                "cash_out_planned": day_info["cash_out_planned"],
                "top_categories": [{"category": k, "amount": v} for k, v in top_categories],
                "top_suppliers": [{"supplier": k, "amount": v} for k, v in top_suppliers],
                "is_essential_day": is_essential
            })
    
    # Retorna apenas gargalos futuros, ordenados por data
    return sorted([b for b in bottlenecks if datetime.strptime(b["date"], "%Y-%m-%d").date() >= today], key=lambda x: x["date"])


def _calculate_essentials_total(expenses, essential_suppliers, folha_keywords, aluguel_keywords):
    """Calcula total de essenciais nos próximos 45 dias"""
    total_folha = 0.0
    total_aluguel = 0.0
    total_essential_suppliers = 0.0
    total_cartorio = 0.0
    
    for exp in expenses:
        supplier = (exp.get("supplier", "") or "").lower()
        description = (exp.get("description", "") or "").lower()
        category = exp.get("category", "").upper()
        amount = float(exp.get("amount", 0))
        remaining = float(exp.get("remaining_amount", amount))
        
        if any(kw in supplier or kw in description for kw in folha_keywords):
            total_folha += remaining
        elif any(kw in supplier or kw in description for kw in aluguel_keywords):
            total_aluguel += remaining
        elif supplier in essential_suppliers:
            total_essential_suppliers += remaining
        
        if category == "CARTORIO" or "cartorio" in supplier or "cartorio" in description:
            total_cartorio += remaining
    
    return {
        "total_folha": total_folha,
        "total_aluguel": total_aluguel,
        "total_essential_suppliers": total_essential_suppliers,
        "total_cartorio": total_cartorio,
        "total_45_days": total_folha + total_aluguel + total_essential_suppliers + total_cartorio
    }


def _build_timeline(today, future_date, all_days, future_expenses, bottlenecks, essential_suppliers, folha_keywords, aluguel_keywords):
    """Constrói dados da linha do tempo"""
    timeline = []
    
    # Agrupa despesas por data
    expenses_by_date = defaultdict(list)
    for exp in future_expenses:
        due_date_str = exp.get("due_date")
        if due_date_str:
            expenses_by_date[due_date_str].append(exp)
    
    # Cria eventos para cada dia
    current_date = today
    while current_date <= future_date:
        date_str = current_date.isoformat()
        
        # Busca dia no banco
        day_data = next((d for d in all_days if d.get("date") == date_str), None)
        
        # Despesas do dia
        day_expenses = expenses_by_date.get(date_str, [])
        
        # Verifica se é gargalo
        bottleneck = next((b for b in bottlenecks if b["date"] == date_str), None)
        
        # Calcula total de despesas
        total_expenses = sum(float(e.get("remaining_amount", e.get("amount", 0))) for e in day_expenses)
        
        # Verifica essenciais
        essentials_day = sum(
            float(e.get("remaining_amount", e.get("amount", 0)))
            for e in day_expenses
            if _is_expense_essential(e, essential_suppliers, folha_keywords, aluguel_keywords)
        )
        
        # Zona de risco
        risk_zone = "low"
        if bottleneck:
            if bottleneck.get("is_essential_day"):
                risk_zone = "critical"
            else:
                risk_zone = "high"
        elif essentials_day > 0:
            risk_zone = "medium"
        
        # Meta de caixa (acumulado)
        # Simplificado: soma de essenciais até esta data
        cash_target = sum(
            float(e.get("remaining_amount", e.get("amount", 0)))
            for exp_list in [expenses_by_date.get(d.isoformat(), []) for d in [today + timedelta(days=i) for i in range((current_date - today).days + 1)]]
            for e in exp_list
            if _is_expense_essential(e, essential_suppliers, folha_keywords, aluguel_keywords)
        )
        
        weekday_en = calendar.day_name[current_date.weekday()]
        timeline.append({
            "date": date_str,
            "formatted_date": format_date(date_str),
            "weekday": WEEKDAYS_PT.get(weekday_en, weekday_en),
            "weekday_short": WEEKDAYS_PT_SHORT.get(weekday_en, weekday_en[:3]),
            "total_expenses": total_expenses,
            "essentials": essentials_day,
            "non_essentials": total_expenses - essentials_day,
            "risk_zone": risk_zone,
            "cash_target": cash_target,
            "is_bottleneck": bottleneck is not None,
            "bottleneck_amount": bottleneck["cash_out_real"] if bottleneck else 0,
            "events": [
                {
                    "type": "expense",
                    "supplier": e.get("supplier"),
                    "amount": float(e.get("remaining_amount", e.get("amount", 0))),
                    "is_essential": _is_expense_essential(e, essential_suppliers, folha_keywords, aluguel_keywords)
                }
                for e in day_expenses[:5]  # Limita a 5 por dia
            ],
            "suggested_actions": _get_suggested_actions_for_day(current_date, bottleneck, essentials_day, today)
        })
        
        current_date += timedelta(days=1)
    
    return timeline


def _is_expense_essential(exp, essential_suppliers, folha_keywords, aluguel_keywords):
    """
    Verifica se despesa é essencial.
    Prioridade: campo is_essential do banco > fornecedores essenciais > palavras-chave
    """
    # PRIMEIRA PRIORIDADE: Campo is_essential do banco (marcação manual)
    if exp.get("is_essential") is True:
        return True
    
    supplier = (exp.get("supplier", "") or "").lower()
    description = (exp.get("description", "") or "").lower()
    category = exp.get("category", "").upper()
    
    # SEGUNDA PRIORIDADE: Fornecedores essenciais cadastrados
    if supplier in essential_suppliers:
        return True
    
    # TERCEIRA PRIORIDADE: Palavras-chave
    if any(kw in supplier or kw in description for kw in folha_keywords):
        return True
    if any(kw in supplier or kw in description for kw in aluguel_keywords):
        return True
    if category in ["IMPOSTO", "CARTORIO"]:
        return True
    
    return False


def _get_suggested_actions_for_day(day_date, bottleneck, essentials, today):
    """Gera ações sugeridas para um dia"""
    actions = []
    days_until = (day_date - today).days
    
    if bottleneck:
        if days_until <= 7:
            actions.append(f"🔴 Reservar R$ {bottleneck['cash_out_real']:,.2f} para este dia")
        else:
            actions.append(f"📊 Planejar para gargalo de R$ {bottleneck['cash_out_real']:,.2f}")
    
    if essentials > 0:
        if days_until <= 3:
            actions.append(f"⚠️ Despesa essencial: R$ {essentials:,.2f}")
    
    return actions


def _build_expenses_table(expenses, essential_suppliers, folha_keywords, aluguel_keywords):
    """
    Constrói dados da tabela de despesas.
    Inclui campo is_essential do banco e calculado.
    """
    table_data = []
    
    for exp in expenses:
        # Usa is_essential do banco se existir, senão calcula
        is_essential_db = exp.get("is_essential", False)
        is_essential_calculated = _is_expense_essential(exp, essential_suppliers, folha_keywords, aluguel_keywords)
        # Prioriza marcação manual do banco
        is_essential = is_essential_db if is_essential_db else is_essential_calculated
        
        table_data.append({
            "id": exp.get("id"),
            "due_date": exp.get("due_date"),
            "formatted_due_date": format_date(exp.get("due_date", "")),
            "supplier": exp.get("supplier", "Não informado"),
            "description": exp.get("description"),
            "category": exp.get("category", "Outros"),
            "amount": float(exp.get("amount", 0)),
            "remaining_amount": float(exp.get("remaining_amount", exp.get("amount", 0))),
            "status": exp.get("status", "Pendente"),
            "is_essential": is_essential,
            "is_essential_manual": is_essential_db,  # Indica se foi marcado manualmente
            "month_code": exp.get("month_code")
        })
    
    # Ordena por data de vencimento
    table_data.sort(key=lambda x: x["due_date"] or "9999-12-31")
    
    return table_data


def _build_charts_data(future_days, future_date, today):
    """Constrói dados para gráficos (já recebe dias futuros otimizados)"""
    # Gráfico de linha: Saldo projetado
    balance_projected = [
        {
            "date": d.get("date"),
            "value": float(d.get("balance_projected", 0))
        }
        for d in future_days
    ]
    
    # Gráfico de barras: Saídas por semana
    weekly_out = defaultdict(float)
    for d in future_days:
        date_obj = datetime.strptime(d.get("date"), "%Y-%m-%d").date()
        week_key = f"{date_obj.year}-W{date_obj.isocalendar()[1]}"
        weekly_out[week_key] += (
            float(d.get("expenses_paid", 0))
            + float(d.get("purchases_planned", 0))
            + float(d.get("checks_paid_total", 0))
        )
    
    # Heatmap: Intensidade por dia
    heatmap_data = [
        {
            "date": d.get("date"),
            "intensity": min(100, (
                float(d.get("expenses_paid", 0))
                + float(d.get("purchases_planned", 0))
            ) / 1000 * 100)  # Normaliza para 0-100
        }
        for d in future_days
    ]
    
    return {
        "balance_projected": balance_projected,
        "weekly_out": dict(weekly_out),
        "heatmap": heatmap_data
    }


def _build_recommended_actions(bottlenecks, next_bottleneck, days_until, daily_reserve, essentials, today, future_date):
    """Constrói lista de ações recomendadas"""
    actions = []
    
    if next_bottleneck:
        bottleneck_date = datetime.strptime(next_bottleneck["date"], "%Y-%m-%d").date()
        
        if days_until <= 7:
            actions.append({
                "priority": "urgent",
                "title": f"Reservar para gargalo em {format_date(next_bottleneck['date'])}",
                "description": f"Reservar R$ {daily_reserve:,.2f} por dia até {format_date(next_bottleneck['date'])}",
                "amount": next_bottleneck["cash_out_real"],
                "deadline": next_bottleneck["date"]
            })
        else:
            actions.append({
                "priority": "high",
                "title": f"Planejar para gargalo em {format_date(next_bottleneck['date'])}",
                "description": f"Iniciar reserva de R$ {daily_reserve:,.2f} por dia",
                "amount": next_bottleneck["cash_out_real"],
                "deadline": next_bottleneck["date"]
            })
    
    # Ações baseadas em essenciais
    if essentials["total_45_days"] > 0:
        buffer_days = 7
        buffer_amount = (essentials["total_45_days"] / 45) * buffer_days
        actions.append({
            "priority": "medium",
            "title": "Manter colchão de segurança",
            "description": f"Manter R$ {buffer_amount:,.2f} em caixa (7 dias de essenciais)",
            "amount": buffer_amount,
            "deadline": None
        })
    
    # Ordena por prioridade
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    actions.sort(key=lambda x: priority_order.get(x["priority"], 99))
    
    return actions


def _build_historical_analysis(all_days, all_expenses):
    """Constrói análise histórica"""
    # Agrupa por mês
    monthly_stats = defaultdict(lambda: {
        "total_in": 0.0,
        "total_out": 0.0,
        "days_count": 0,
        "avg_daily_out": 0.0
    })
    
    for day in all_days:
        month = day.get("month_code", "unknown")
        monthly_stats[month]["total_in"] += (
            float(day.get("cash_in_actual_money", 0))
            + float(day.get("cash_in_actual_pix", 0))
            + float(day.get("cash_in_actual_card", 0))
            + float(day.get("cash_in_actual_convenio", 0))
        )
        monthly_stats[month]["total_out"] += (
            float(day.get("expenses_paid", 0))
            + float(day.get("purchases_planned", 0))
            + float(day.get("checks_paid_total", 0))
        )
        monthly_stats[month]["days_count"] += 1
    
    # Calcula médias
    for month, stats in monthly_stats.items():
        if stats["days_count"] > 0:
            stats["avg_daily_out"] = stats["total_out"] / stats["days_count"]
    
    # Padrões por dia da semana (em português)
    weekday_patterns = defaultdict(lambda: {"total": 0.0, "count": 0})
    for day in all_days:
        date_str = day.get("date")
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                weekday_en = calendar.day_name[date_obj.weekday()]
                weekday_pt = WEEKDAYS_PT.get(weekday_en, weekday_en)
                weekday_patterns[weekday_pt]["total"] += (
                    float(day.get("expenses_paid", 0))
                    + float(day.get("purchases_planned", 0))
                )
                weekday_patterns[weekday_pt]["count"] += 1
            except:
                pass
    
    weekday_avg = {
        day: stats["total"] / stats["count"] if stats["count"] > 0 else 0
        for day, stats in weekday_patterns.items()
    }
    
    # Prepara despesas históricas com informações de essenciais
    historical_expenses_list = []
    for exp in all_expenses:
        historical_expenses_list.append({
            "id": exp.get("id"),
            "due_date": exp.get("due_date"),
            "formatted_due_date": format_date(exp.get("due_date", "")),
            "payment_date": exp.get("payment_date"),
            "formatted_payment_date": format_date(exp.get("payment_date", "")) if exp.get("payment_date") else None,
            "supplier": exp.get("supplier", "Não informado"),
            "description": exp.get("description"),
            "category": exp.get("category", "Outros"),
            "amount": float(exp.get("amount", 0)),
            "amount_paid": float(exp.get("amount_paid", 0)),
            "remaining_amount": float(exp.get("remaining_amount", exp.get("amount", 0))),
            "status": exp.get("status", "Pendente"),
            "is_essential": exp.get("is_essential", False),
            "month_code": exp.get("month_code")
        })
    
    # Ordena despesas por data de vencimento (mais recentes primeiro)
    historical_expenses_list.sort(key=lambda x: x["due_date"] or "9999-12-31", reverse=True)
    
    return {
        "monthly_comparison": dict(monthly_stats),
        "weekday_patterns": weekday_avg,
        "historical_expenses": historical_expenses_list[:500],  # Limita a 500 mais recentes
        "trends": {
            "avg_monthly_out": mean([s["total_out"] for s in monthly_stats.values()]) if monthly_stats else 0,
            "most_expensive_month": max(monthly_stats.items(), key=lambda x: x[1]["total_out"])[0] if monthly_stats else None
        }
    }


def _find_most_critical_week(bottlenecks, today):
    """Encontra semana mais crítica"""
    if not bottlenecks:
        return None
    
    future_bottlenecks = [
        b for b in bottlenecks
        if datetime.strptime(b["date"], "%Y-%m-%d").date() >= today
    ]
    
    if not future_bottlenecks:
        return None
    
    # Agrupa por semana
    week_totals = defaultdict(float)
    for b in future_bottlenecks:
        date_obj = datetime.strptime(b["date"], "%Y-%m-%d").date()
        week_key = f"{date_obj.year}-W{date_obj.isocalendar()[1]}"
        week_totals[week_key] += b["cash_out_real"]
    
    if week_totals:
        most_critical = max(week_totals.items(), key=lambda x: x[1])
        return {
            "week": most_critical[0],
            "total": most_critical[1]
        }
    
    return None


def get_ai_financial_recommendations(days: int = 30, start_date: Optional[str] = None) -> dict:
    """
    Gera recomendações usando ChatGPT baseado em TODOS os dados do banco.
    
    Analisa:
    - Padrões de entradas e saídas
    - Despesas essenciais vs não essenciais
    - Gargalos históricos
    - Comportamento de caixa nos últimos N dias
    
    Retorna recomendações estratégicas para evitar problemas de caixa.
    """
    try:
        try:
            from openai import OpenAI
        except ImportError:
            return {
                "error": "Módulo openai não instalado",
                "recommendations": [
                    "O módulo 'openai' não está instalado no servidor.",
                    "Execute: pip install openai==1.54.5",
                    "Ou adicione 'openai==1.54.5' ao requirements.txt do backend"
                ],
                "analysis_period": f"{days} dias"
            }
        
        # Verifica se API key está configurada
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "error": "OPENAI_API_KEY não configurada",
                "recommendations": [
                    "Configure a variável de ambiente OPENAI_API_KEY no Render para habilitar análises com IA"
                ],
                "analysis_period": f"{days} dias"
            }
        
        client = OpenAI(api_key=api_key)
        supabase = get_supabase()
        
        # Calcula período de análise
        today = date.today()
        if start_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
            except:
                start = today - timedelta(days=days)
        else:
            start = today - timedelta(days=days)
        
        print(f"[get_ai_financial_recommendations] Analisando período {start} a {today}")
        
        # Busca TODOS os dados do período
        days_resp = supabase.table("finance_daily").select("*").gte("date", start.isoformat()).lte("date", today.isoformat()).order("date").execute()
        days_data = days_resp.data or []
        
        expenses_resp = supabase.table("expense_items").select("*").gte("due_date", start.isoformat()).lte("due_date", today.isoformat()).execute()
        expenses_data = expenses_resp.data or []
        
        # Prepara dados para análise
        analysis_data = {
            "period": {
                "start": start.isoformat(),
                "end": today.isoformat(),
                "days": len(days_data)
            },
            "cash_flow": {
                "total_in": sum(float(d.get("cash_in_actual_money", 0)) + float(d.get("cash_in_actual_pix", 0)) + float(d.get("cash_in_actual_card", 0)) + float(d.get("cash_in_actual_convenio", 0)) for d in days_data),
                "total_out": sum(float(d.get("expenses_paid", 0)) + float(d.get("purchases_planned", 0)) + float(d.get("checks_paid_total", 0)) for d in days_data),
                "avg_daily_in": sum(float(d.get("cash_in_actual_money", 0)) + float(d.get("cash_in_actual_pix", 0)) + float(d.get("cash_in_actual_card", 0)) + float(d.get("cash_in_actual_convenio", 0)) for d in days_data) / len(days_data) if days_data else 0,
                "avg_daily_out": sum(float(d.get("expenses_paid", 0)) + float(d.get("purchases_planned", 0)) + float(d.get("checks_paid_total", 0)) for d in days_data) / len(days_data) if days_data else 0,
            },
            "expenses": {
                "total": len(expenses_data),
                "essential": len([e for e in expenses_data if e.get("is_essential")]),
                "non_essential": len([e for e in expenses_data if not e.get("is_essential")]),
                "total_amount": sum(float(e.get("amount", 0)) for e in expenses_data),
                "essential_amount": sum(float(e.get("amount", 0)) for e in expenses_data if e.get("is_essential")),
            },
            "bottlenecks": [],
            "balance_trend": [float(d.get("balance_real", 0)) for d in days_data[-10:]]  # Últimos 10 dias
        }
        
        # Identifica gargalos no período (apenas passados para análise histórica)
        for day in days_data:
            day_date_str = day.get("date")
            if day_date_str:
                try:
                    day_date = datetime.strptime(day_date_str, "%Y-%m-%d").date()
                    if day_date >= today:  # Ignora dias futuros na análise histórica
                        continue
                except:
                    continue
            
            cash_out = float(day.get("expenses_paid", 0)) + float(day.get("purchases_planned", 0)) + float(day.get("checks_paid_total", 0))
            if cash_out > analysis_data["cash_flow"]["avg_daily_out"] * 1.5:  # 50% acima da média
                analysis_data["bottlenecks"].append({
                    "date": day.get("date"),
                    "amount": cash_out
                })
        
        # Prepara prompt para ChatGPT
        prompt = f"""Você é um analista financeiro experiente. Analise os dados financeiros abaixo e forneça recomendações estratégicas para evitar problemas de caixa no próximo período.

DADOS DO PERÍODO ({analysis_data['period']['start']} a {analysis_data['period']['end']}):
- Total de entradas: R$ {analysis_data['cash_flow']['total_in']:,.2f}
- Total de saídas: R$ {analysis_data['cash_flow']['total_out']:,.2f}
- Média diária de entradas: R$ {analysis_data['cash_flow']['avg_daily_in']:,.2f}
- Média diária de saídas: R$ {analysis_data['cash_flow']['avg_daily_out']:,.2f}
- Total de despesas: {analysis_data['expenses']['total']} ({analysis_data['expenses']['essential']} essenciais, {analysis_data['expenses']['non_essential']} não essenciais)
- Valor total de despesas: R$ {analysis_data['expenses']['total_amount']:,.2f}
- Valor de despesas essenciais: R$ {analysis_data['expenses']['essential_amount']:,.2f}
- Gargalos identificados: {len(analysis_data['bottlenecks'])} dias
- Tendência de saldo (últimos 10 dias): {analysis_data['balance_trend']}

Forneça:
1. Análise do comportamento atual (2-3 parágrafos)
2. Principais riscos identificados (lista)
3. Ações recomendadas para os próximos 30 dias (lista priorizada)
4. Meta de reserva diária sugerida
5. Sugestões de reprogramação de despesas não essenciais

Seja específico, prático e focado em evitar problemas de caixa. Responda em português brasileiro."""

        # Chama ChatGPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo mais econômico
            messages=[
                {"role": "system", "content": "Você é um analista financeiro especializado em gestão de fluxo de caixa para pequenas e médias empresas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        recommendations_text = response.choices[0].message.content
        
        return {
            "recommendations": recommendations_text,
            "analysis_period": f"{start.isoformat()} a {today.isoformat()}",
            "data_summary": analysis_data,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        import traceback
        error_msg = f"Erro ao gerar recomendações com IA: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(traceback.format_exc())
        return {
            "error": error_msg,
            "recommendations": [
                "Não foi possível gerar recomendações automáticas.",
                "Verifique se OPENAI_API_KEY está configurada corretamente.",
                f"Erro: {str(e)}",
                "Tente novamente mais tarde."
            ],
            "analysis_period": f"{days} dias"
        }


def get_strategy_recommendations(month_code: Optional[str] = None) -> dict:
    """
    Retorna recomendações estratégicas baseadas nos dados do banco.
    Usa get_comprehensive_analytics para obter dados diretamente do banco.
    """
    analytics = get_comprehensive_analytics()
    actions = analytics.get("recommended_actions", [])
    
    # Converte ações para formato de estratégia
    recommendations = [action.get("description", "") for action in actions]
    
    # Adiciona recomendações baseadas em essenciais
    executive_summary = analytics.get("executive_summary", {})
    essentials_total = executive_summary.get("key_indicators", {}).get("total_essentials", 0)
    
    if essentials_total > 0:
        buffer_days = 7
        buffer_amount = (essentials_total / 45) * buffer_days
        recommendations.append(f"Colchão mínimo recomendado: R$ {buffer_amount:,.2f} ({buffer_days} dias de essenciais)")
    
    next_bottleneck = executive_summary.get("next_bottleneck", {})
    if next_bottleneck.get("date"):
        recommendations.append(f"Próximo gargalo: {format_date(next_bottleneck['date'])} - R$ {next_bottleneck.get('amount', 0):,.2f}")
    
    return {
        "next_bottleneck_date": next_bottleneck.get("date"),
        "next_bottleneck_amount": next_bottleneck.get("amount", 0.0),
        "buffer_days": 7,
        "buffer_amount": (essentials_total / 45) * 7 if essentials_total > 0 else 0.0,
        "daily_reserve_target": executive_summary.get("daily_reserve_recommended", 0.0),
        "days_until_bottleneck": executive_summary.get("days_until_bottleneck"),
        "recommendations": recommendations
    }


def _is_essential_day(day_date: date, expenses: list[dict], essential_suppliers: set = None, folha_keywords: list = None, aluguel_keywords: list = None) -> bool:
    """Verifica se um dia contém despesas essenciais"""
    if essential_suppliers is None:
        supabase = get_supabase()
        essential_resp = supabase.table("essential_suppliers").select("*").execute()
        essential_suppliers = {e["supplier_name"].lower() for e in (essential_resp.data or [])}
    
    if folha_keywords is None:
        folha_keywords = ['folha', 'salário', 'salarios', 'pagamento pessoal', 'rh']
    
    if aluguel_keywords is None:
        aluguel_keywords = ['aluguel', 'locação', 'locacao']
    
    for exp in expenses:
        # Prioriza marcação manual
        if exp.get("is_essential") is True:
            return True
        
        supplier = (exp.get("supplier", "") or "").lower()
        description = (exp.get("description", "") or "").lower()
        
        if supplier in essential_suppliers:
            return True
        
        if any(kw in supplier or kw in description for kw in folha_keywords):
            return True
        if any(kw in supplier or kw in description for kw in aluguel_keywords):
            return True
        
        category = exp.get("category", "").upper()
        if category in ["IMPOSTO", "CARTORIO"]:
            return True
    
    return False
