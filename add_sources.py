#!/usr/bin/env python3
"""
📡 ADICIONAR NOVAS FONTES DE NOTÍCIAS - TEM VENDA
Script para adicionar novos sites ao coletor de notícias
"""

from supabase import create_client, Client

def add_news_sources():
    # Configurações Supabase
    supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Novas fontes para adicionar
    new_sources = [
        {
            'name': 'Portal da Farmácia',
            'url': 'https://www.portaldafarmacia.com.br',
            'rss_url': 'https://www.portaldafarmacia.com.br/feed',
            'scraping_frequency': 12,  # horas
            'is_active': True
        },
        {
            'name': 'Farmácia News',
            'url': 'https://www.farmacianews.com.br',
            'rss_url': 'https://www.farmacianews.com.br/feed',
            'scraping_frequency': 24,
            'is_active': True
        },
        {
            'name': 'Anvisa Notícias',
            'url': 'https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa',
            'rss_url': 'https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/feed',
            'scraping_frequency': 6,  # mais frequente para Anvisa
            'is_active': True
        },
        {
            'name': 'Conselho Federal de Farmácia',
            'url': 'https://www.cff.org.br',
            'rss_url': 'https://www.cff.org.br/feed',
            'scraping_frequency': 24,
            'is_active': True
        },
        {
            'name': 'Farmácia Popular',
            'url': 'https://www.farmaciapopular.gov.br',
            'rss_url': 'https://www.farmaciapopular.gov.br/feed',
            'scraping_frequency': 24,
            'is_active': True
        },
        {
            'name': 'Revista Farmácia & Saúde',
            'url': 'https://www.revistafarmaciaesaude.com.br',
            'rss_url': 'https://www.revistafarmaciaesaude.com.br/feed',
            'scraping_frequency': 12,
            'is_active': True
        },
        {
            'name': 'Portal do Farmacêutico',
            'url': 'https://www.portaldofarmaceutico.com.br',
            'rss_url': 'https://www.portaldofarmaceutico.com.br/feed',
            'scraping_frequency': 24,
            'is_active': True
        },
        {
            'name': 'Farmácia Digital',
            'url': 'https://www.farmaciadigital.com.br',
            'rss_url': 'https://www.farmaciadigital.com.br/feed',
            'scraping_frequency': 12,
            'is_active': True
        }
    ]
    
    print("📡 Adicionando novas fontes de notícias...")
    
    for source in new_sources:
        try:
            # Verificar se já existe
            existing = supabase.table('news_sources').select('id').eq('url', source['url']).execute()
            
            if existing.data:
                print(f"⚠️ Fonte já existe: {source['name']}")
                continue
            
            # Inserir nova fonte
            result = supabase.table('news_sources').insert(source).execute()
            
            if result.data:
                print(f"✅ Fonte adicionada: {source['name']}")
            else:
                print(f"❌ Erro ao adicionar: {source['name']}")
                
        except Exception as e:
            print(f"❌ Erro ao adicionar {source['name']}: {e}")
    
    print("\n🎉 Fontes adicionadas com sucesso!")
    print("Execute o coletor para testar as novas fontes:")
    print("python3 news_collector.py")

def list_current_sources():
    """Lista fontes atuais"""
    supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    try:
        sources = supabase.table('news_sources').select('*').execute()
        
        print("📡 FONTES ATUAIS NO SISTEMA:")
        print("=" * 50)
        
        for source in sources.data:
            status = "✅ Ativa" if source['is_active'] else "❌ Inativa"
            freq = f"{source['scraping_frequency']}h"
            print(f"• {source['name']}")
            print(f"  URL: {source['url']}")
            print(f"  RSS: {source['rss_url']}")
            print(f"  Status: {status} | Frequência: {freq}")
            print()
            
    except Exception as e:
        print(f"❌ Erro ao listar fontes: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_current_sources()
    else:
        add_news_sources()

