#!/usr/bin/env python3
"""
Script de validação COMPLETA para todos os dias de dezembro.
Mostra valores esperados vs. calculados e identifica problemas.
"""

import sys
import os
from datetime import date
from collections import defaultdict

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from supabase import create_client
    from app.config import get_settings
    
    def get_supabase():
        settings = get_settings()
        return create_client(settings.supabase_url, settings.supabase_service_role_key)
        
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    month_code = "12-25"
    year, month = 2025, 12
    last_day = 31
    
    supabase = get_supabase()
    
    print("=" * 120)
    print(f"🔍 VALIDAÇÃO COMPLETA - TODOS OS DIAS DE DEZEMBRO 2025")
    print("=" * 120)
    print()
    
    # Busca expense_items
    items_resp = supabase.table("expense_items").select("*").eq("month_code", month_code).execute()
    items = items_resp.data or []
    
    # Busca finance_daily
    days_resp = supabase.table("finance_daily").select("*").eq("month_code", month_code).order("date").execute()
    days = days_resp.data or []
    
    print(f"📊 Total expense_items: {len(items)}")
    print(f"📅 Total dias finance_daily: {len(days)}")
    print()
    
    # Estatísticas
    itens_com_payment_date = [i for i in items if i.get("payment_date")]
    itens_sem_payment_date = [i for i in items if not i.get("payment_date")]
    
    print(f"✅ Itens COM payment_date: {len(itens_com_payment_date)}")
    print(f"❌ Itens SEM payment_date: {len(itens_sem_payment_date)}")
    print()
    
    if len(itens_com_payment_date) == 0:
        print("⚠️  PROBLEMA CRÍTICO: Nenhum expense_item tem payment_date!")
        print("   Execute 'Atualizar Fluxo' novamente após o deploy.")
        print()
        return
    
    # Agrupa por payment_date
    itens_por_payment_date = defaultdict(list)
    for item in itens_com_payment_date:
        payment_date = item.get("payment_date")
        itens_por_payment_date[payment_date].append(item)
    
    print(f"📅 Datas de pagamento únicas: {len(itens_por_payment_date)}")
    print()
    
    # Validação dia a dia
    problemas = []
    acertos = []
    dias_com_pagamentos = []
    
    for day_num in range(1, last_day + 1):
        d = date(year, month, day_num)
        d_iso = d.isoformat()
        
        day_record = next((d for d in days if d.get("date") == d_iso), None)
        if not day_record:
            continue
        
        expenses_paid_banco = float(day_record.get("expenses_paid", 0))
        
        # Calcula o que DEVERIA ser (baseado em payment_date)
        expenses_paid_esperado = 0.0
        itens_com_pagamento = []
        
        for item in items:
            payment_date_str = item.get("payment_date")
            amount_paid = float(item.get("amount_paid", 0))
            interest = float(item.get("interest", 0))
            
            if payment_date_str and payment_date_str == d_iso:
                valor_item = amount_paid + interest
                expenses_paid_esperado += valor_item
                itens_com_pagamento.append({
                    "supplier": item.get("supplier", "N/A"),
                    "category": item.get("category", "N/A"),
                    "amount_paid": amount_paid,
                    "interest": interest,
                    "total": valor_item,
                    "due_date": item.get("due_date")
                })
        
        diferenca = abs(expenses_paid_banco - expenses_paid_esperado)
        esta_correto = diferenca < 0.01
        
        if expenses_paid_esperado > 0.01:
            dias_com_pagamentos.append({
                "date": d_iso,
                "valor_esperado": expenses_paid_esperado,
                "valor_banco": expenses_paid_banco,
                "itens": itens_com_pagamento,
                "correto": esta_correto,
                "diferenca": diferenca
            })
        
        if not esta_correto:
            problemas.append({
                "date": d_iso,
                "banco": expenses_paid_banco,
                "esperado": expenses_paid_esperado,
                "diferenca": diferenca,
                "itens": itens_com_pagamento
            })
        else:
            acertos.append({
                "date": d_iso,
                "valor": expenses_paid_esperado,
                "itens": len(itens_com_pagamento)
            })
    
    # RELATÓRIO
    print("=" * 120)
    print("📋 RELATÓRIO DE VALIDAÇÃO")
    print("=" * 120)
    print()
    
    if dias_com_pagamentos:
        print(f"💰 DIAS COM PAGAMENTOS REGISTRADOS ({len(dias_com_pagamentos)} dias):")
        print()
        
        for dia in sorted(dias_com_pagamentos, key=lambda x: x['date']):
            d_obj = date.fromisoformat(dia['date'])
            status = "✅" if dia['correto'] else "❌"
            print(f"{status} {dia['date']} ({d_obj.strftime('%d/%m/%Y - %A')})")
            print(f"   Esperado (payment_date): {format_currency(dia['valor_esperado'])}")
            print(f"   Banco (expenses_paid): {format_currency(dia['valor_banco'])}")
            if not dia['correto']:
                print(f"   ⚠️  DIFERENÇA: {format_currency(dia['diferenca'])}")
            
            # Agrupa por categoria
            por_categoria = defaultdict(list)
            for item in dia['itens']:
                por_categoria[item['category']].append(item)
            
            if por_categoria:
                print(f"   Itens ({len(dia['itens'])}):")
                for cat, itens_cat in por_categoria.items():
                    total_cat = sum(i['total'] for i in itens_cat)
                    print(f"      [{cat}] {len(itens_cat)} itens = {format_currency(total_cat)}")
            print()
    else:
        print("⚠️  NENHUM DIA COM PAGAMENTOS encontrado!")
        print()
    
    print("=" * 120)
    print()
    
    if problemas:
        print(f"❌ PROBLEMAS: {len(problemas)} dias com valores incorretos")
        print(f"✅ ACERTOS: {len(acertos)} dias corretos")
        print()
        print("⚠️  AÇÃO: Execute 'Atualizar Fluxo' novamente para recalcular expenses_paid.")
    else:
        print(f"✅ SUCESSO: Todos os {len(acertos)} dias estão corretos!")
        if dias_com_pagamentos:
            total_geral = sum(d['valor_esperado'] for d in dias_com_pagamentos)
            print(f"   Total geral de despesas pagas: {format_currency(total_geral)}")
    
    print()
    
    # Validação específica do dia 1
    print("=" * 120)
    print("🔍 VALIDAÇÃO ESPECÍFICA - DIA 1/12/2025")
    print("=" * 120)
    print()
    
    dia_1 = next((d for d in dias_com_pagamentos if d['date'] == '2025-12-01'), None)
    if dia_1:
        desp_items_dia1 = [i for i in dia_1['itens'] if i['category'] == 'DESP']
        dist_items_dia1 = [i for i in dia_1['itens'] if i['category'] == 'DIST']
        
        desp_total = sum(i['total'] for i in desp_items_dia1)
        dist_total = sum(i['total'] for i in dist_items_dia1)
        total_dia1 = desp_total + dist_total
        
        print(f"   DESP 12-25: {format_currency(desp_total)} ({len(desp_items_dia1)} itens)")
        print(f"   DIST 12-25: {format_currency(dist_total)} ({len(dist_items_dia1)} itens)")
        print(f"   TOTAL: {format_currency(total_dia1)}")
        print()
        
        # Valores esperados
        desp_esperado = 5828.10
        dist_esperado = 11969.75
        total_esperado = 17797.85
        
        print(f"   Valores ESPERADOS:")
        print(f"      DESP: {format_currency(desp_esperado)}")
        print(f"      DIST: {format_currency(dist_esperado)}")
        print(f"      TOTAL: {format_currency(total_esperado)}")
        print()
        
        desp_ok = abs(desp_total - desp_esperado) < 0.01
        dist_ok = abs(dist_total - dist_esperado) < 0.01
        total_ok = abs(total_dia1 - total_esperado) < 0.01
        
        if desp_ok and dist_ok and total_ok:
            print("   ✅ DIA 1: VALIDAÇÃO CORRETA!")
        else:
            print("   ❌ DIA 1: VALIDAÇÃO INCORRETA!")
            if not desp_ok:
                print(f"      DESP: diferença de {format_currency(abs(desp_total - desp_esperado))}")
            if not dist_ok:
                print(f"      DIST: diferença de {format_currency(abs(dist_total - dist_esperado))}")
            if not total_ok:
                print(f"      TOTAL: diferença de {format_currency(abs(total_dia1 - total_esperado))}")
    else:
        print("   ⚠️  Dia 1/12/2025 não encontrado ou sem pagamentos registrados.")
    
    print()

if __name__ == "__main__":
    main()

