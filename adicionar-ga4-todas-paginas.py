#!/usr/bin/env python3
"""
Script para adicionar Google Analytics 4 em todas as páginas HTML
"""

import os
import re
from pathlib import Path

# ID do Google Analytics
GA4_SCRIPT = '    <!-- Google Analytics 4 -->\n    <script src="/ga4-config.js"></script>\n'

# Páginas que já têm o script (não adicionar novamente)
PAGINAS_COM_GA4 = ['index.html', 'instagram.html', 'consultoria-estrategica.html']

# Páginas para ignorar
IGNORAR = [
    'stats.html',  # Página admin
    'backup', 'wordpress', 'deploy', 'app', 'area',
    'test.html', 'a.html', 'index-mvp.html', 'index-redirect.html',
    'stats_', 'instagram_novo.html'
]

def tem_ga4(content):
    """Verifica se a página já tem o script GA4"""
    return 'ga4-config.js' in content or 'G-DR5X1GNCXV' in content

def deve_processar(arquivo):
    """Verifica se o arquivo deve ser processado"""
    nome = os.path.basename(arquivo)
    
    # Ignorar se já tem GA4
    if nome in PAGINAS_COM_GA4:
        return False
    
    # Ignorar se está na lista de ignorados
    for ignorar in IGNORAR:
        if ignorar in arquivo:
            return False
    
    return True

def adicionar_ga4(content, arquivo):
    """Adiciona o script GA4 no conteúdo HTML"""
    
    # Se já tem GA4, não adicionar
    if tem_ga4(content):
        return content, False
    
    # Padrões para encontrar onde inserir
    padroes = [
        # Após SUPABASE_CONFIG
        (r'(</script>\s*)(<!-- Meta Pixel|</head>|<link|<style)', r'\1' + GA4_SCRIPT + r'\2'),
        # Após Meta Pixel
        (r'(<script src="/meta-pixel-config.js"></script>\s*)(</head>|<link|<style)', r'\1' + GA4_SCRIPT + r'\2'),
        # Após title e antes de link/style
        (r'(<title>.*?</title>\s*)(<link|<style)', r'\1' + GA4_SCRIPT + r'\2'),
        # Antes de </head>
        (r'(</head>)', GA4_SCRIPT + r'\1'),
    ]
    
    for padrao, substituicao in padroes:
        novo_content = re.sub(padrao, substituicao, content, flags=re.DOTALL | re.IGNORECASE)
        if novo_content != content:
            return novo_content, True
    
    return content, False

def processar_arquivo(arquivo):
    """Processa um arquivo HTML"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se é HTML válido
        if '<!DOCTYPE html' not in content and '<html' not in content:
            return False, 'Não é HTML válido'
        
        # Adicionar GA4
        novo_content, modificado = adicionar_ga4(content, arquivo)
        
        if modificado:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(novo_content)
            return True, 'GA4 adicionado'
        else:
            return False, 'Já tinha GA4 ou não foi possível adicionar'
    
    except Exception as e:
        return False, f'Erro: {str(e)}'

def main():
    """Função principal"""
    base_dir = Path('.')
    html_files = list(base_dir.glob('*.html'))
    
    processados = 0
    adicionados = 0
    erros = 0
    
    print('🔍 Procurando páginas HTML...\n')
    
    for arquivo in sorted(html_files):
        if not deve_processar(str(arquivo)):
            continue
        
        processados += 1
        modificado, mensagem = processar_arquivo(arquivo)
        
        if modificado:
            adicionados += 1
            print(f'✅ {arquivo.name}: {mensagem}')
        elif 'Erro' in mensagem:
            erros += 1
            print(f'❌ {arquivo.name}: {mensagem}')
        else:
            print(f'ℹ️  {arquivo.name}: {mensagem}')
    
    print(f'\n📊 Resumo:')
    print(f'   Total processado: {processados}')
    print(f'   GA4 adicionado: {adicionados}')
    print(f'   Erros: {erros}')
    print(f'\n✅ Concluído!')

if __name__ == '__main__':
    main()

