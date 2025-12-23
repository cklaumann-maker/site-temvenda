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
    desp_planned = normalize(desp_due, desp_value)

    # Acumula por dia - APENAS para expenses_planned (baseado em due_date)
    expenses_planned_by_day: dict[date, float] = {}
    
    for dt, v in dist_planned + desp_planned:
        expenses_planned_by_day[dt] = expenses_planned_by_day.get(dt, 0.0) + v

    # IMPORTANTE: expenses_paid NÃO é calculado aqui em process_excel_month
    # porque precisa ser baseado na DATA DE PAGAMENTO (payment_date), não na data de vencimento
    # O cálculo correto será feito por _recalculate_expenses_from_items() baseado nos expense_items
    # que têm payment_date e incluem juros
    expenses_paid_by_day: dict[date, float] = {}  # Sempre vazio aqui - será calculado depois

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
        # expenses_paid será calculado por _recalculate_expenses_from_items() baseado em payment_date
        # Inicializa zerado para evitar valores incorretos baseados em due_date
        expenses_paid = 0.0

        purchases_planned = 0.0
        old_debts_paid = 0.0
        future_in_confirmed = 0.0
        sales = 0.0

        cash_in_total = forecast_total + future_in_confirmed
        purchases_credit = 0.0  # Compras a prazo (será preenchido manualmente)
        store_expenses_total = 0.0  # Será calculado via trigger quando despesas de loja forem criadas
        
        cash_out_planned = expenses_planned + purchases_planned + purchases_credit + old_debts_paid + store_expenses_total
        # cash_out_real: inclui expenses_paid (já com juros pela data de pagamento, calculado via _recalculate_expenses_from_items)
        cash_out_real = (
            expenses_paid  # Despesas pagas (valor pago + juros, pela data de pagamento)
            + purchases_planned  # Compras à vista
            + purchases_credit  # Compras a prazo pagas
            + old_debts_paid
            + store_expenses_total  # Despesas de loja
        )

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
            "purchases_credit": 0.0,  # Compras a prazo (será preenchido manualmente)
            "old_debts_paid": old_debts_paid,
            "expenses_planned": expenses_planned,
            "expenses_paid": expenses_paid,
            "store_expenses_total": 0.0,  # Despesas de loja (será calculado via trigger)
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
        
        # IMPORTANTE: Baseado nas imagens fornecidas, a coluna "Data pag" está após "Juros"
        # Estrutura típica: Vencimento | Fornecedor | ... | Valor pago | Juros | Data pag | ...
        # DIST: índice 5 = "Valor pago", então 6 = "Juros", então 7 = "Data pag"
        # DESP: índice 6 = "Valor pago", então 7 = "Juros", então 8 = "Data pag"
        
        # PRIMEIRO: Tenta usar índice direto (mais confiável)
        payment_date_idx = 7 if category == "DIST" else 8
        payment_date_col = None
        
        if payment_date_idx < len(df.columns):
            try:
                col_name_at_idx = str(df.columns[payment_date_idx])
                payment_date_col = df.iloc[:, payment_date_idx]
                print(f"[{category}] ✅ Coluna 'Data pag' encontrada por índice ({payment_date_idx}): '{col_name_at_idx}'")
            except Exception as e:
                pass
        
        # SEGUNDO: Se não funcionou, tenta buscar pelo nome
        if payment_date_col is None:
            payment_date_col = _get_column_optional(df, [
                "data pag", "Data pag", "DATA PAG", "Data Pag", "data pagamento", "Data Pagamento", 
                "Data Pago", "Dt Pagamento", "Dt Pago", "Data Pgto", "Dt Pgto",
                "data de pagamento", "Data de Pagamento", "Data de Pago",
                "pagamento", "Pagamento", "PAGAMENTO",
                "data pag ", "Data Pag ", "DATA PAG "  # Com espaço no final
            ], None)
            
            if payment_date_col is not None:
                print(f"[{category}] ✅ Coluna 'Data pag' encontrada por nome: '{payment_date_col.name}'")
        
        # TERCEIRO: Fallback - busca qualquer coluna que contenha "pag" e "data"
        if payment_date_col is None:
            all_cols = [str(c) for c in df.columns]
            for col_name in df.columns:
                col_str = str(col_name).strip().lower()
                if 'pag' in col_str and 'data' in col_str:
                    try:
                        payment_date_col = df[col_name]
                        print(f"[{category}] ✅ Coluna encontrada (fallback): '{col_name}'")
                        break
                    except Exception as e:
                        pass
        
        # QUARTO: Fallback - busca qualquer coluna com "pag"
        if payment_date_col is None:
            for col_name in df.columns:
                col_str = str(col_name).strip().lower()
                if 'pag' in col_str:
                    try:
                        payment_date_col = df[col_name]
                        print(f"[{category}] ✅ Coluna encontrada (fallback 2): '{col_name}'")
                        break
                    except Exception as e:
                        pass
        
        # ÚLTIMA TENTATIVA: Se ainda não encontrou, mostra debug e tenta índices alternativos
        if payment_date_col is None:
            print(f"[{category}] ⚠️  Coluna 'Data pag' NÃO encontrada!")
            print(f"[{category}] Colunas disponíveis: {[str(c) for c in df.columns]}")
            # Tenta índices alternativos próximos
            for alt_idx in [payment_date_idx - 1, payment_date_idx + 1]:
                if 0 <= alt_idx < len(df.columns):
                    try:
                        payment_date_col = df.iloc[:, alt_idx]
                        print(f"[{category}] ✅ Usando coluna por índice alternativo ({alt_idx}): '{df.columns[alt_idx]}'")
                        break
                    except Exception as e:
                        pass
        
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


def _recalculate_expenses_from_items(supabase, month_code: str) -> None:
    """
    Recalcula expenses_paid e expenses_planned baseado em expense_items DO BANCO.
    
    IMPORTANTE: Esta função usa APENAS dados do banco (expense_items), nunca da planilha.
    
    Regras IMPORTANTES:
    - expenses_paid (Saída Real): 
      * SOMENTE itens com payment_date igual ao dia atual
      * Soma: amount_paid + interest (do banco)
      * NÃO considera data de vencimento para expenses_paid
      * Se não tem payment_date ou payment_date é diferente, NÃO entra em expenses_paid
    
    - expenses_planned (Saída Prevista):
      * Itens com due_date igual ao dia atual
      * Mas que NÃO foram pagos (sem payment_date) ou têm payment_date futuro
      * Soma: amount + interest (do banco)
    
    Isso garante que:
    - Saída real = amount_paid + interest, APENAS pela data de pagamento (payment_date)
    - Saída prevista = amount + interest, baseado na data de vencimento (due_date)
    - TUDO vem do banco, nunca da planilha
    """
    year, month = parse_month_code(month_code)
    last_day = calendar.monthrange(year, month)[1]
    
    print(f"[_recalculate_expenses_from_items] Iniciando recálculo para {month_code}")
    
    # Busca TODOS os expense_items do mês DO BANCO (uma única vez)
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    print(f"[_recalculate_expenses_from_items] {len(items)} expense_items encontrados no banco")
    
    # Conta quantos têm payment_date
    itens_com_payment_date = sum(1 for item in items if item.get("payment_date"))
    print(f"[_recalculate_expenses_from_items] {itens_com_payment_date} expense_items com payment_date no banco")
    
    # Para cada dia do mês
    for day in range(1, last_day + 1):
        d = date(year, month, day)
        d_iso = d.isoformat()
        
        expenses_paid_calc = 0.0
        expenses_planned_calc = 0.0
        itens_contados_paid = 0
        itens_contados_planned = 0
        
        for item in items:
            due_date_str = item.get("due_date")
            payment_date_str = item.get("payment_date")
            amount = float(item.get("amount", 0))
            amount_paid = float(item.get("amount_paid", 0))
            interest = float(item.get("interest", 0))
            
            # REGRA 1: expenses_paid (Saída Real)
            # SOMENTE se payment_date existe E é igual ao dia atual
            # Soma: amount_paid + interest (DO BANCO)
            # NÃO considera due_date para expenses_paid
            if payment_date_str and payment_date_str == d_iso:
                # Saída real = amount_paid + interest (do banco, pela data de pagamento)
                expenses_paid_calc += amount_paid + interest
                itens_contados_paid += 1
            
            # REGRA 2: expenses_planned (Saída Prevista)
            # Se due_date é igual ao dia atual
            # Mas NÃO foi pago neste dia (sem payment_date ou payment_date diferente/futuro)
            if due_date_str == d_iso:
                # Se não tem payment_date ou payment_date é futuro, conta como previsto
                if not payment_date_str or payment_date_str > d_iso:
                    # expenses_planned: amount + interest (do banco)
                    expenses_planned_calc += amount + interest
                    itens_contados_planned += 1
        
        # Atualiza finance_daily com valores calculados DO BANCO
        if expenses_paid_calc > 0.01 or expenses_planned_calc > 0.01:
            print(f"[_recalculate_expenses_from_items] {d_iso}: expenses_paid={expenses_paid_calc:.2f} ({itens_contados_paid} itens), expenses_planned={expenses_planned_calc:.2f} ({itens_contados_planned} itens)")
        
        supabase.table("finance_daily").update({
            "expenses_paid": expenses_paid_calc,
            "expenses_planned": expenses_planned_calc,
        }).eq("month_code", month_code).eq("date", d_iso).execute()
    
    print(f"[_recalculate_expenses_from_items] ✅ Recalculação concluída para {month_code}")


async def refresh_month(month_code: str) -> None:
    """
    Regra de refresh:
    - Salva valores manuais (entradas, compras, vendas) antes de apagar
    - Apaga finance_daily do mês
    - Apaga expense_items do mês
    - Reimporta Excel e recria registros
    - Restaura valores manuais (sobrescrevem valores da planilha)
    - Recalcula saldos com valores manuais preservados
    - Registra em finance_month_runs com timestamp e status
    """
    from datetime import datetime, timezone
    
    supabase = get_supabase()
    error_message = None
    records_count = 0
    expense_items_count = 0
    status = "completed"

    try:
        print(f"[refresh_month] Iniciando atualização do mês {month_code}")
        
        # IMPORTANTE: Salvar valores manuais ANTES de apagar
        # Valores manuais têm prioridade sobre valores da planilha
        manual_entries: dict[str, dict] = {}
        
        print(f"[refresh_month] Salvando valores manuais...")
        existing_days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).execute()
        for day in existing_days_resp.data or []:
            date_str = day.get("date")
            if not date_str:
                continue
            
            # Salva apenas valores que foram cadastrados manualmente (diferentes de zero ou padrão)
            manual_data = {}
            
            # Entradas manuais (se foram cadastradas)
            if float(day.get("cash_in_actual_money", 0)) > 0 or \
               float(day.get("cash_in_actual_pix", 0)) > 0 or \
               float(day.get("cash_in_actual_card", 0)) > 0 or \
               float(day.get("cash_in_actual_convenio", 0)) > 0:
                manual_data["cash_in_actual_money"] = float(day.get("cash_in_actual_money", 0))
                manual_data["cash_in_actual_pix"] = float(day.get("cash_in_actual_pix", 0))
                manual_data["cash_in_actual_card"] = float(day.get("cash_in_actual_card", 0))
                manual_data["cash_in_actual_convenio"] = float(day.get("cash_in_actual_convenio", 0))
            
            # Compras manuais (à vista)
            if float(day.get("purchases_planned", 0)) > 0:
                manual_data["purchases_planned"] = float(day.get("purchases_planned", 0))
            
            # Compras a prazo manuais
            if float(day.get("purchases_credit", 0)) > 0:
                manual_data["purchases_credit"] = float(day.get("purchases_credit", 0))
            
            # Despesas de loja manuais (store_expenses_total é calculado automaticamente, mas preservamos se houver)
            # Nota: store_expenses_total é calculado por trigger SQL, então não precisamos preservar manualmente
            
            # Futuras entradas confirmadas
            if float(day.get("future_in_confirmed", 0)) > 0:
                manual_data["future_in_confirmed"] = float(day.get("future_in_confirmed", 0))
            
            # Vendas manuais
            if float(day.get("sales", 0)) > 0:
                manual_data["sales"] = float(day.get("sales", 0))
            
            # Se houver algum valor manual, salva
            if manual_data:
                manual_entries[date_str] = manual_data
        
        print(f"[refresh_month] {len(manual_entries)} dias com valores manuais preservados")
        
        # Agora apaga e recria
        print(f"[refresh_month] Apagando registros antigos...")
        supabase.table("finance_daily").delete().eq("month_code", month_code).execute()
        supabase.table("expense_items").delete().eq("month_code", month_code).execute()

        # Baixa e processa Excel
        print(f"[refresh_month] Baixando planilha do Google Drive...")
        excel_bytes = download_excel_from_drive()
        print(f"[refresh_month] Planilha baixada ({len(excel_bytes)} bytes)")
        
        print(f"[refresh_month] Processando finance_daily...")
        records = process_excel_month(excel_bytes, month_code)
        print(f"[refresh_month] {len(records)} registros de finance_daily processados")
        
        print(f"[refresh_month] Processando expense_items...")
        expense_items = process_expense_items(excel_bytes, month_code)
        print(f"[refresh_month] {len(expense_items)} expense_items processados")
        
        # Conta quantos expense_items têm payment_date
        itens_com_payment_date = sum(1 for item in expense_items if item.get("payment_date"))
        print(f"[refresh_month] {itens_com_payment_date} expense_items com payment_date preenchido")

        # Insere registros da planilha
        if records:
            print(f"[refresh_month] Inserindo {len(records)} registros em finance_daily...")
            # Insere em lotes de 50 para evitar timeout
            batch_size = 50
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                print(f"[refresh_month] Inserindo lote {i//batch_size + 1} de finance_daily ({len(batch)} registros)...")
                supabase.table("finance_daily").insert(batch).execute()
            records_count = len(records)
        
        if expense_items:
            print(f"[refresh_month] Inserindo {len(expense_items)} expense_items...")
            # Insere em lotes de 100 para evitar timeout
            batch_size = 100
            for i in range(0, len(expense_items), batch_size):
                batch = expense_items[i:i + batch_size]
                print(f"[refresh_month] Inserindo lote {i//batch_size + 1} de expense_items ({len(batch)} itens)...")
                supabase.table("expense_items").insert(batch).execute()
            expense_items_count = len(expense_items)
        
        # Recalcula expenses_paid e expenses_planned baseado em expense_items
        # Considera: valor pago + juros, condicionado à data de pagamento
        print(f"[refresh_month] Recalculando expenses_paid e expenses_planned...")
        _recalculate_expenses_from_items(supabase, month_code)
        print(f"[refresh_month] Recalculação concluída")
        
        # IMPORTANTE: Restaurar valores manuais (sobrescrevem valores da planilha)
        if manual_entries:
            print(f"[refresh_month] Restaurando {len(manual_entries)} dias com valores manuais...")
            for date_str, manual_data in manual_entries.items():
                # Busca o registro recém-criado
                day_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).eq("date", date_str).limit(1).execute()
                if not day_resp.data:
                    continue
                
                day = day_resp.data[0]
                
                # Restaura valores manuais
                update_data = {}
                if "cash_in_actual_money" in manual_data:
                    day["cash_in_actual_money"] = manual_data["cash_in_actual_money"]
                    update_data["cash_in_actual_money"] = manual_data["cash_in_actual_money"]
                if "cash_in_actual_pix" in manual_data:
                    day["cash_in_actual_pix"] = manual_data["cash_in_actual_pix"]
                    update_data["cash_in_actual_pix"] = manual_data["cash_in_actual_pix"]
                if "cash_in_actual_card" in manual_data:
                    day["cash_in_actual_card"] = manual_data["cash_in_actual_card"]
                    update_data["cash_in_actual_card"] = manual_data["cash_in_actual_card"]
                if "cash_in_actual_convenio" in manual_data:
                    day["cash_in_actual_convenio"] = manual_data["cash_in_actual_convenio"]
                    update_data["cash_in_actual_convenio"] = manual_data["cash_in_actual_convenio"]
                if "purchases_planned" in manual_data:
                    day["purchases_planned"] = manual_data["purchases_planned"]
                    update_data["purchases_planned"] = manual_data["purchases_planned"]
                if "purchases_credit" in manual_data:
                    day["purchases_credit"] = manual_data["purchases_credit"]
                    update_data["purchases_credit"] = manual_data["purchases_credit"]
                if "future_in_confirmed" in manual_data:
                    day["future_in_confirmed"] = manual_data["future_in_confirmed"]
                    update_data["future_in_confirmed"] = manual_data["future_in_confirmed"]
                if "sales" in manual_data:
                    day["sales"] = manual_data["sales"]
                    update_data["sales"] = manual_data["sales"]
                
                # Recalcula saldos com valores manuais preservados
                cash_in_actual_total = (
                    float(day.get("cash_in_actual_money", 0))
                    + float(day.get("cash_in_actual_pix", 0))
                    + float(day.get("cash_in_actual_card", 0))
                    + float(day.get("cash_in_actual_convenio", 0))
                )
                cash_in_used = cash_in_actual_total if cash_in_actual_total > 0 else float(day.get("cash_in_forecast_total", 0))
                cash_in_total = cash_in_used + float(day.get("future_in_confirmed", 0))
                # Inclui purchases_credit (compras a prazo) em expenses_planned
                # Inclui store_expenses_total em ambas as saídas
                cash_out_planned = (
                    float(day.get("expenses_planned", 0)) 
                    + float(day.get("purchases_planned", 0))  # Compras à vista
                    + float(day.get("purchases_credit", 0))  # Compras a prazo
                    + float(day.get("old_debts_paid", 0))
                    + float(day.get("store_expenses_total", 0))
                )
                cash_out_real = (
                    float(day.get("expenses_paid", 0))  # Despesas pagas (valor pago + juros, pela data de pagamento)
                    + float(day.get("purchases_planned", 0))  # Compras à vista impactam imediatamente
                    + float(day.get("purchases_credit", 0))  # Compras a prazo pagas (também são despesas)
                    + float(day.get("old_debts_paid", 0))
                    + float(day.get("store_expenses_total", 0))  # Despesas de loja
                )
                
                balance_projected = float(day.get("sales", 0)) + cash_in_total - cash_out_planned
                balance_real = cash_in_total - cash_out_real
                
                update_data["balance_projected"] = balance_projected
                update_data["balance_real"] = balance_real
                
                # Atualiza o registro com valores manuais e saldos recalculados
                supabase.table("finance_daily").update(update_data).eq("id", day["id"]).execute()
                print(f"[refresh_month] ✅ Valores manuais restaurados para {date_str}: {list(manual_data.keys())}")
        
        print(f"[refresh_month] ✅ Restauração de valores manuais concluída")

    except Exception as e:
        # Em caso de erro, registra mas não interrompe
        status = "error"
        error_message = str(e)
        import traceback
        error_message = f"{str(e)}\n{traceback.format_exc()}"

    # Registra execução (sempre, mesmo em caso de erro)
    supabase.table("finance_month_runs").insert(
        {
            "month_code": month_code,
            "source_file_id": "drive",
            "status": status,
            "error_message": error_message,
            "records_imported": records_count,
            "expense_items_imported": expense_items_count,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "notes": None,
        }
    ).execute()
    
    # Se houve erro, levanta exceção para o endpoint tratar
    if status == "error":
        raise RuntimeError(f"Erro ao processar mês {month_code}: {error_message}")


# ---------- PROJEÇÃO D+60 ----------


def _load_projection_sheet() -> pd.DataFrame | None:
    """
    Lê a planilha de projeção (aba PROJECAO) usando GOOGLE_PROJECTION_FILE_ID.
    Retorna None se não estiver configurado (projeção opcional).
    """
    settings = get_settings()
    if not settings.projection_file_id:
        return None  # Projeção opcional - pode funcionar sem planilha

    try:
        excel_bytes = download_excel_from_drive(settings.projection_file_id)
        xls = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None, engine="openpyxl")
        # Tenta localizar aba PROJECAO (case-insensitive)
        target_name = None
        for name in xls.keys():
            if name.strip().upper() == "PROJECAO":
                target_name = name
                break
        if not target_name:
            print("⚠️ Aviso: Aba PROJECAO não encontrada na planilha de projeção. Usando apenas dados reais e forecast.")
            return None
        return xls[target_name]
    except Exception as e:
        print(f"⚠️ Aviso: Erro ao carregar planilha de projeção: {e}. Usando apenas dados reais e forecast.")
        return None


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
    - Planilha PROJECAO (GOOGLE_PROJECTION_FILE_ID) - opcional
    - Forecast padrão como fallback
    """
    supabase = get_supabase()
    today = date.today()
    horizon = today + timedelta(days=days)

    # Carrega mapa de projeções da planilha (opcional)
    proj_df = _load_projection_sheet()
    proj_map = {}
    if proj_df is not None:
        try:
            proj_map = _parse_projection_sheet(proj_df)
        except Exception as e:
            print(f"⚠️ Aviso: Erro ao processar planilha de projeção: {e}. Continuando sem ela.")
            proj_map = {}

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
            # Inclui todas as saídas: expenses_paid, purchases_planned, purchases_credit, old_debts_paid, store_expenses_total
            cash_out = (
                float(daily.get("expenses_paid", 0.0))
                + float(daily.get("purchases_planned", 0.0))  # Compras à vista
                + float(daily.get("purchases_credit", 0.0))  # Compras a prazo (já pagas)
                + float(daily.get("old_debts_paid", 0.0))
                + float(daily.get("store_expenses_total", 0.0))
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
    """
    Busca dados do mês do banco de dados (Supabase).
    A tela SEMPRE lê do banco, nunca da planilha diretamente.
    """
    supabase = get_supabase()
    resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    return resp.data or []


async def get_last_sync_info(month_code: str) -> dict | None:
    """
    Retorna informações da última sincronização do mês:
    - Data/hora da última atualização
    - Status (completed/error)
    - Quantidade de registros importados
    - Mensagem de erro (se houver)
    """
    supabase = get_supabase()
    resp = (
        supabase.table("finance_month_runs")
        .select("*")
        .eq("month_code", month_code)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )
    
    if not resp.data:
        return None
    
    run = resp.data[0]
    return {
        "month_code": run.get("month_code"),
        "updated_at": run.get("updated_at"),
        "status": run.get("status", "unknown"),
        "error_message": run.get("error_message"),
        "records_imported": run.get("records_imported", 0),
        "expense_items_imported": run.get("expense_items_imported", 0),
        "source_file_id": run.get("source_file_id"),
    }



