#!/usr/bin/env python3
"""
📡 ADICIONAR FONTES ESPECÍFICAS - TEM VENDA
Script para adicionar fontes específicas solicitadas pelo usuário
"""

from supabase import create_client, Client

def add_specific_sources():
    # Configurações Supabase
    supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Fontes específicas solicitadas
    specific_sources = [
        {
            'name': 'Panorama Farmacêutico',
            'url': 'https://panoramafarmaceutico.com.br',
            'rss_url': 'https://panoramafarmaceutico.com.br/feed',
            'scraping_frequency': 6,  # Muito importante - coleta a cada 6h
            'is_active': True
        },
        {
            'name': 'Sincofarma SP',
            'url': 'https://sincofarmasp.com.br',
            'rss_url': 'https://sincofarmasp.com.br/news/feed',
            'scraping_frequency': 12,  # Importante - coleta a cada 12h
            'is_active': True
        }
    ]
    
    print("📡 Adicionando fontes específicas solicitadas...")
    
    for source in specific_sources:
        try:
            # Verificar se já existe
            existing = supabase.table('news_sources').select('id').eq('url', source['url']).execute()
            
            if existing.data:
                print(f"⚠️ Fonte já existe: {source['name']}")
                # Atualizar se necessário
                result = supabase.table('news_sources').update({
                    'is_active': True,
                    'scraping_frequency': source['scraping_frequency']
                }).eq('url', source['url']).execute()
                
                if result.data:
                    print(f"✅ Fonte atualizada: {source['name']}")
                continue
            
            # Inserir nova fonte
            result = supabase.table('news_sources').insert(source).execute()
            
            if result.data:
                print(f"✅ Fonte adicionada: {source['name']}")
                print(f"   📍 URL: {source['url']}")
                print(f"   📡 RSS: {source['rss_url']}")
                print(f"   ⏰ Frequência: {source['scraping_frequency']}h")
                print()
            else:
                print(f"❌ Erro ao adicionar: {source['name']}")
                
        except Exception as e:
            print(f"❌ Erro ao adicionar {source['name']}: {e}")
    
    print("🎉 Fontes específicas processadas!")
    print("\n📊 RESUMO DAS FONTES ADICIONADAS:")
    print("• Panorama Farmacêutico - Principal portal do setor")
    print("• Sincofarma SP - Sindicato farmacêutico de SP")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Execute o coletor para testar: python3 news_collector.py")
    print("2. Verifique no painel admin: admin-panel.html")
    print("3. Monitore os logs: tail -f logs/collection.log")

def test_rss_feeds():
    """Testa se os feeds RSS estão funcionando"""
    import requests
    import feedparser
    
    feeds_to_test = [
        ('Panorama Farmacêutico', 'https://panoramafarmaceutico.com.br/feed'),
        ('Sincofarma SP', 'https://sincofarmasp.com.br/news/feed')
    ]
    
    print("🔍 Testando feeds RSS...")
    
    for name, url in feeds_to_test:
        try:
            print(f"\n📡 Testando: {name}")
            print(f"   URL: {url}")
            
            # Testar com feedparser
            feed = feedparser.parse(url)
            
            if feed.bozo:
                print(f"   ⚠️ Feed com problemas: {feed.bozo_exception}")
            else:
                print(f"   ✅ Feed OK")
            
            if feed.entries:
                print(f"   📰 {len(feed.entries)} artigos encontrados")
                if feed.entries:
                    latest = feed.entries[0]
                    print(f"   📄 Último: {latest.get('title', 'Sem título')[:50]}...")
            else:
                print(f"   📰 Nenhum artigo encontrado")
                
        except Exception as e:
            print(f"   ❌ Erro ao testar {name}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_rss_feeds()
    else:
        add_specific_sources()
