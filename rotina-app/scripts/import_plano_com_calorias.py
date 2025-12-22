#!/usr/bin/env python3
"""
Script para importar plano alimentar do CSV com calorias
Formato: CSV com ponto e vírgula, tipos em português, com colunas de calorias
"""

import csv
import sys
import os

# Mapeamento de tipos de refeição (português -> código)
MEAL_TYPE_MAP = {
    'Pré-treino': 'pre',
    'Pós-treino': 'post',
    'Café da manhã': 'cafe',
    'Almoço': 'almoco',
    'Lanche da tarde': 'lanche_tarde',
    'Jantar': 'jantar',
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

def clean_option_text(text):
    """Remove prefixos como 'Opção 1 (Principal):' do texto"""
    if not text:
        return None
    
    cleaned = text.strip()
    
    # Valores vazios
    if cleaned == '' or cleaned == '—' or cleaned == '-' or cleaned == 'NULL':
        return None
    
    # Remove prefixos comuns (com regex para ser mais flexível)
    import re
    cleaned = re.sub(r'^Opção \d+ \(Principal\):\s*', '', cleaned)
    cleaned = re.sub(r'^Opção \d+ \(Substituição\):\s*', '', cleaned)
    cleaned = re.sub(r'^Evitar:\s*', '', cleaned)
    
    cleaned = cleaned.strip()
    
    return cleaned if cleaned and cleaned != '—' else None

def parse_csv_file(csv_file_path):
    """Parse CSV file and return structured data"""
    meals = []
    
    with open(csv_file_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig remove BOM
        lines = f.readlines()
        
        # Parse header - detectar se usa vírgula ou ponto e vírgula
        header_line = lines[0].strip()
        # Remove BOM if present
        if header_line.startswith('\ufeff'):
            header_line = header_line[1:]
        
        # Detectar separador (vírgula ou ponto e vírgula)
        if ';' in header_line:
            separator = ';'
        elif ',' in header_line:
            separator = ','
        else:
            print("Erro: Não foi possível detectar o separador (vírgula ou ponto e vírgula)")
            return []
        
        header = [h.strip() for h in header_line.split(separator)]
        
        # Find column indices
        try:
            day_idx = header.index('day_label')
            meal_idx = header.index('meal_type')
            opt1_idx = header.index('opt1')
            opt2_idx = header.index('opt2')
            opt3_idx = header.index('opt3')
            avoid_idx = header.index('avoid')
            # Calorias
            kcal_opt1_idx = header.index('kcal_opt1')
            kcal_opt2_idx = header.index('kcal_opt2')
            kcal_opt3_idx = header.index('kcal_opt3')
        except ValueError as e:
            print(f"Erro ao encontrar colunas: {e}")
            print(f"Colunas encontradas: {header}")
            return []
        
        # Parse data lines
        for line in lines[1:]:
            if not line.strip():
                continue
                
            # Split by detected separator
            parts = line.split(separator)
            
            if len(parts) < 11:  # Mínimo de colunas esperadas
                continue
                
            day_label = parts[day_idx].strip() if day_idx < len(parts) else ''
            meal_type = parts[meal_idx].strip() if meal_idx < len(parts) else ''
            opt1_raw = parts[opt1_idx].strip() if opt1_idx < len(parts) else ''
            opt2_raw = parts[opt2_idx].strip() if opt2_idx < len(parts) else ''
            opt3_raw = parts[opt3_idx].strip() if opt3_idx < len(parts) else ''
            avoid_raw = parts[avoid_idx].strip() if avoid_idx < len(parts) else ''
            
            # Ler calorias
            try:
                kcal_opt1 = int(parts[kcal_opt1_idx].strip() or 0) if kcal_opt1_idx < len(parts) else 0
            except (ValueError, IndexError):
                kcal_opt1 = 0
            
            try:
                kcal_opt2 = int(parts[kcal_opt2_idx].strip() or 0) if kcal_opt2_idx < len(parts) else 0
            except (ValueError, IndexError):
                kcal_opt2 = 0
            
            try:
                kcal_opt3 = int(parts[kcal_opt3_idx].strip() or 0) if kcal_opt3_idx < len(parts) else 0
            except (ValueError, IndexError):
                kcal_opt3 = 0
            
            if not day_label or not meal_type:
                continue
            
            # Determine week (Semana 2 = week 2, otherwise week 1)
            week_index = 2 if 'Semana 2' in day_label else 1
            day_name = day_label.replace(' (Semana 2)', '').strip()
            
            # Map day name to day_of_week
            day_of_week = DAY_LABEL_MAP.get(day_name)
            if not day_of_week:
                continue
            
            # Map meal type
            mapped_meal_type = MEAL_TYPE_MAP.get(meal_type)
            if not mapped_meal_type:
                continue
            
            # Clean options
            opt1 = clean_option_text(opt1_raw)
            opt2 = clean_option_text(opt2_raw)
            opt3 = clean_option_text(opt3_raw)
            avoid = clean_option_text(avoid_raw)
            
            meals.append({
                'week_index': week_index,
                'day_of_week': day_of_week,
                'meal_type': mapped_meal_type,
                'opt1': opt1,
                'opt2': opt2,
                'opt3': opt3,
                'avoid': avoid,
                'kcal_opt1': kcal_opt1,
                'kcal_opt2': kcal_opt2,
                'kcal_opt3': kcal_opt3,
            })
    
    return meals

def generate_sql(meals, program_id='00000000-0000-0000-0000-000000000002'):
    """Generate SQL INSERT statements"""
    sql_statements = []
    
    sql_statements.append("-- Importar plano alimentar do CSV com calorias")
    sql_statements.append("-- Execute este SQL no Supabase SQL Editor\n")
    
    sql_statements.append("-- Limpar templates existentes")
    sql_statements.append(f"DELETE FROM public.plan_templates WHERE program_id = '{program_id}';\n")
    
    for meal in meals:
        def escape_sql(text):
            if not text:
                return 'NULL'
            return f"'{text.replace(chr(39), chr(39) + chr(39))}'"
        
        opt1_sql = escape_sql(meal['opt1'])
        opt2_sql = escape_sql(meal['opt2'])
        opt3_sql = escape_sql(meal['opt3'])
        avoid_sql = escape_sql(meal['avoid'])
        
        kcal_opt1_val = meal.get('kcal_opt1', 0) or 0
        kcal_opt2_val = meal.get('kcal_opt2', 0) or 0
        kcal_opt3_val = meal.get('kcal_opt3', 0) or 0
        
        sql = f"""INSERT INTO public.plan_templates (
    program_id, week_index, day_of_week, meal_type, opt1, opt2, opt3, avoid, kcal_opt1, kcal_opt2, kcal_opt3
) VALUES (
    '{program_id}',
    {meal['week_index']},
    {meal['day_of_week']},
    '{meal['meal_type']}',
    {opt1_sql},
    {opt2_sql},
    {opt3_sql},
    {avoid_sql},
    {kcal_opt1_val},
    {kcal_opt2_val},
    {kcal_opt3_val}
);"""
        sql_statements.append(sql)
    
    return '\n'.join(sql_statements)

def main():
    if len(sys.argv) < 2:
        print("Uso: python import_plano_com_calorias.py <arquivo.csv>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' não encontrado")
        sys.exit(1)
    
    print(f"Processando arquivo: {csv_file}")
    meals = parse_csv_file(csv_file)
    
    if not meals:
        print("Nenhuma refeição encontrada no arquivo")
        sys.exit(1)
    
    print(f"Encontradas {len(meals)} refeições")
    
    sql = generate_sql(meals)
    
    output_file = csv_file.replace('.csv', '_com_calorias.sql')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql)
    
    print(f"SQL gerado: {output_file}")
    print(f"\nExecute este SQL no Supabase SQL Editor para importar o plano alimentar com calorias.")

if __name__ == '__main__':
    main()

