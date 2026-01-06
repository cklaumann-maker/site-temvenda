#!/usr/bin/env python3
"""
Script para importar plano alimentar do CSV fornecido
"""

import csv
import sys
import os
from datetime import datetime, timedelta
import json

# Mapeamento de tipos de refeição
MEAL_TYPE_MAP = {
    'pre': 'pre',
    'post': 'post',
    'breakfast': 'cafe',
    'lunch': 'almoco',
    'snack': 'lanche_tarde',
    'dinner': 'jantar',
}

# Mapeamento de dias da semana
DAY_LABEL_MAP = {
    'Segunda': 1,
    'Terça': 2,
    'Quarta': 3,
    'Quinta': 4,
    'Sexta': 5,
    'Sábado': 6,
    'Domingo': 7,
}

def parse_csv_content(csv_content):
    """Parse CSV content and return structured data"""
    lines = csv_content.strip().split('\n')
    reader = csv.DictReader(lines)
    
    meals = []
    for row in reader:
        day_label = row.get('day_label', '').strip()
        meal_type = row.get('meal_type', '').strip()
        opt1 = row.get('opt1', '').strip()
        opt2 = row.get('opt2', '').strip()
        opt3 = row.get('opt3', '').strip()
        avoid = row.get('avoid', '').strip()
        
        if not day_label or not meal_type:
            continue
        
        # Determine week (S2 = week 2, otherwise week 1)
        week_index = 2 if '(S2)' in day_label else 1
        day_name = day_label.replace(' (S2)', '').strip()
        
        # Map day name to day_of_week
        day_of_week = DAY_LABEL_MAP.get(day_name)
        if not day_of_week:
            continue
        
        # Map meal type
        mapped_meal_type = MEAL_TYPE_MAP.get(meal_type)
        if not mapped_meal_type:
            continue
        
        meals.append({
            'week_index': week_index,
            'day_of_week': day_of_week,
            'meal_type': mapped_meal_type,
            'opt1': opt1,
            'opt2': opt2 or None,
            'opt3': opt3 or None,
            'avoid': avoid or None,
        })
    
    return meals

def generate_sql(meals, program_id='00000000-0000-0000-0000-000000000002'):
    """Generate SQL INSERT statements"""
    sql_statements = []
    
    sql_statements.append("-- Importar plano alimentar")
    sql_statements.append("-- Execute este SQL no Supabase SQL Editor\n")
    
    for meal in meals:
        sql = f"""INSERT INTO public.plan_templates (
    program_id, week_index, day_of_week, meal_type, opt1, opt2, opt3, avoid
) VALUES (
    '{program_id}',
    {meal['week_index']},
    {meal['day_of_week']},
    '{meal['meal_type']}',
    {f"'{meal['opt1'].replace("'", "''")}'" if meal['opt1'] else 'NULL'},
    {f"'{meal['opt2'].replace("'", "''")}'" if meal['opt2'] else 'NULL'},
    {f"'{meal['opt3'].replace("'", "''")}'" if meal['opt3'] else 'NULL'},
    {f"'{meal['avoid'].replace("'", "''")}'" if meal['avoid'] else 'NULL'}
)
ON CONFLICT (program_id, week_index, day_of_week, meal_type) 
DO UPDATE SET
    opt1 = EXCLUDED.opt1,
    opt2 = EXCLUDED.opt2,
    opt3 = EXCLUDED.opt3,
    avoid = EXCLUDED.avoid,
    updated_at = NOW();"""
        
        sql_statements.append(sql)
    
    return '\n\n'.join(sql_statements)

def main():
    # CSV content provided by user
    csv_content = """date,day_label,meal_type,option_selected,opt1,opt2,opt3,avoid
,Segunda,pre,,Venom + água,,,"Comer sólido"
,Segunda,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Segunda,breakfast,,Ovos mexidos (2-3) + 1 pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Segunda,lunch,,Arroz + feijão + carne,Macarrão + frango,Batata + peixe,"Arroz + batata juntos"
,Segunda,snack,,Ovos + maçã,Whey + pera,Frango + uva,"Bolacha, cavaquinho, bolo"
,Segunda,dinner,,Frango ou peixe,Ovos mexidos,1 pão + ovos,"Doce à noite"

,Terça,pre,,Venom + água,,,"Comer sólido"
,Terça,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Terça,breakfast,,Ovos mexidos (2-3) + 1 pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Terça,lunch,,Macarrão + carne,Arroz + feijão + frango,Batata + peixe,"Arroz + batata juntos"
,Terça,snack,,Whey + pera,Ovos + maçã,Frango + uva,"Bolacha, cavaquinho, bolo"
,Terça,dinner,,Ovos mexidos,Frango ou peixe,1 pão + ovos,"Doce à noite"

,Quarta,pre,,Venom + água,,,"Comer sólido"
,Quarta,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Quarta,breakfast,,Omelete de queijo + pão,Ovos mexidos (2-3) + 1 pão + requeijão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Quarta,lunch,,Arroz + feijão + peixe,Arroz + feijão + carne,Macarrão + frango,"Arroz + batata juntos"
,Quarta,snack,,Ovos + maçã,Whey + pera,Uva + (proteína: ovos ou whey),"Bolacha, cavaquinho, bolo"
,Quarta,dinner,,Frango ou peixe,Ovos mexidos,1 pão + ovos,"Doce à noite"

,Quinta,pre,,Venom + água,,,"Comer sólido"
,Quinta,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Quinta,breakfast,,Ovos mexidos (2-3) + 1 pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Quinta,lunch,,Arroz + feijão + carne,Macarrão + frango,Batata + peixe,"Arroz + batata juntos"
,Quinta,snack,,Whey + pera,Ovos + maçã,Frango + uva,"Bolacha, cavaquinho, bolo"
,Quinta,dinner,,Peixe,Frango,Ovos mexidos,"Doce à noite"

,Sexta,pre,,Venom + água,,,"Comer sólido"
,Sexta,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Sexta,breakfast,,Omelete de queijo + pão,Ovos mexidos (2-3) + 1 pão + requeijão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Sexta,lunch,,Macarrão + frango,Arroz + feijão + carne,Batata + peixe,"Arroz + batata juntos"
,Sexta,snack,,Ovos + maçã,Whey + pera,Frango + uva,"Bolacha, cavaquinho, bolo"
,Sexta,dinner,,Frango,Ovos mexidos,Peixe,"Doce à noite"

,Sábado,pre,,Venom + água,,,"Comer sólido"
,Sábado,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo cedo (gatilho)"
,Sábado,breakfast,,Ovos + pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Começar com doce"
,Sábado,lunch,,Churrasco + arroz,Carne + batata,Peixe + arroz,"Maionese em excesso + belisco"
,Sábado,snack,,Fruta + proteína (whey ou ovos),Whey + pera,Ovos + maçã,"Bolacha/cavaquinho automático"
,Sábado,dinner,,Jantar leve (frango/ovos/peixe),Livre moderado,,,"Doce tarde da noite"

,Domingo,pre,,Venom + água,,,"Comer sólido"
,Domingo,post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Belisco de manhã"
,Domingo,breakfast,,Ovos + pão,Omelete de queijo + pão,Whey + banana + pão,"Bolo/cuca cedo"
,Domingo,lunch,,Comida caseira (arroz+feijão+carne/peixe),Macarrão + carne,Batata + carne,"Exagero + repetir"
,Domingo,snack,,Whey + fruta,Ovos + maçã,Fruta + ovos,"Bolacha/cavaquinho"
,Domingo,dinner,,Pizza (2 salgadas + 2 doces),,,"Passar de 4 fatias (gatilho)"

,Segunda (S2),pre,,Venom + água,,,"Comer sólido"
,Segunda (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Segunda (S2),breakfast,,Ovos mexidos (2-3) + 1 pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Segunda (S2),lunch,,Arroz + feijão + peixe,Macarrão + frango,Batata + carne,"Arroz + batata juntos"
,Segunda (S2),snack,,Whey + pera,Ovos + maçã,Frango + uva,"Bolacha, cavaquinho, bolo"
,Segunda (S2),dinner,,Ovos mexidos,Frango,Peixe,"Doce à noite"

,Terça (S2),pre,,Venom + água,,,"Comer sólido"
,Terça (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Terça (S2),breakfast,,Omelete de queijo + pão,Ovos mexidos (2-3) + 1 pão + requeijão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Terça (S2),lunch,,Macarrão + carne,Arroz + feijão + frango,Batata + peixe,"Arroz + batata juntos"
,Terça (S2),snack,,Ovos + maçã,Whey + pera,Frango + uva,"Bolacha, cavaquinho, bolo"
,Terça (S2),dinner,,Frango,Peixe,Ovos mexidos,"Doce à noite"

,Quarta (S2),pre,,Venom + água,,,"Comer sólido"
,Quarta (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Quarta (S2),breakfast,,Ovos mexidos (2-3) + 1 pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Quarta (S2),lunch,,Arroz + feijão + frango,Macarrão + frango,Batata + peixe,"Arroz + batata juntos"
,Quarta (S2),snack,,Whey + pera,Ovos + maçã,Frango + uva,"Bolacha, cavaquinho, bolo"
,Quarta (S2),dinner,,Peixe,Frango,Ovos mexidos,"Doce à noite"

,Quinta (S2),pre,,Venom + água,,,"Comer sólido"
,Quinta (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Quinta (S2),breakfast,,Omelete de queijo + pão,Ovos mexidos (2-3) + 1 pão + requeijão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Quinta (S2),lunch,,Batata + carne,Arroz + feijão + carne,Macarrão + carne,"Arroz + batata juntos"
,Quinta (S2),snack,,Ovos + maçã,Whey + pera,Frango + uva,"Bolacha, cavaquinho, bolo"
,Quinta (S2),dinner,,Frango,Ovos mexidos,Peixe,"Doce à noite"

,Sexta (S2),pre,,Venom + água,,,"Comer sólido"
,Sexta (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo, pão, doce"
,Sexta (S2),breakfast,,Ovos mexidos (2-3) + 1 pão + requeijão,Omelete de queijo + pão,Whey + banana + pão,"Bolo, cuca, doce de leite"
,Sexta (S2),lunch,,Macarrão + frango,Arroz + feijão + carne,Batata + peixe,"Arroz + batata juntos"
,Sexta (S2),snack,,Whey + pera,Ovos + maçã,Frango + uva,"Bolacha, cavaquinho, bolo"
,Sexta (S2),dinner,,Ovos mexidos,Frango,Peixe,"Doce à noite"

,Sábado (S2),pre,,Venom + água,,,"Comer sólido"
,Sábado (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Bolo cedo (gatilho)"
,Sábado (S2),breakfast,,Ovos + pão,Omelete de queijo + pão,Whey + banana + pão,"Começar com doce"
,Sábado (S2),lunch,,Livre controlado (churrasco/comida),Carne + batata,Peixe + arroz,"Maionese em excesso"
,Sábado (S2),snack,,Fruta + proteína,Whey + pera,Ovos + maçã,"Bolacha/cavaquinho automático"
,Sábado (S2),dinner,,Jantar leve (frango/ovos/peixe),Livre moderado,,,"Doce tarde da noite"

,Domingo (S2),pre,,Venom + água,,,"Comer sólido"
,Domingo (S2),post,,Whey + banana + água de coco,Whey + morango,Whey + 1/2 banana,"Belisco de manhã"
,Domingo (S2),breakfast,,Ovos + pão,Omelete + pão,Whey + banana + pão,"Bolo/cuca cedo"
,Domingo (S2),lunch,,Comida caseira,Macarrão + carne,Batata + carne,"Exagero"
,Domingo (S2),snack,,Whey + fruta,Ovos + maçã,Fruta + ovos,"Bolacha/cavaquinho"
,Domingo (S2),dinner,,Pizza (2 salgadas + 2 doces),,,"Passar de 4 fatias"
"""
    
    meals = parse_csv_content(csv_content)
    sql = generate_sql(meals)
    
    # Write to file
    output_file = 'supabase/import_meal_plan.sql'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql)
    
    print(f"✅ SQL gerado com sucesso!")
    print(f"📁 Arquivo: {output_file}")
    print(f"📊 Total de refeições: {len(meals)}")
    print(f"\n📋 Próximos passos:")
    print(f"1. Acesse o Supabase SQL Editor")
    print(f"2. Execute o arquivo: {output_file}")
    print(f"3. Recarregue o app para ver o plano alimentar")

if __name__ == '__main__':
    main()







