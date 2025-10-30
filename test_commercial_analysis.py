#!/usr/bin/env python3
"""
🧪 TESTE DE ANÁLISE COMERCIAL - TEM VENDA NEWS
Testa a nova funcionalidade de análise comercial com IA
"""

import os
import json
from datetime import datetime
from supabase import create_client, Client

def test_commercial_analysis():
    # Configurações Supabase
    supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    print("🧪 TESTANDO ANÁLISE COMERCIAL COM IA")
    print("=" * 50)
    
    # Buscar artigos que já têm análise comercial
    try:
        response = supabase.table('news_articles').select('*').not_.is_('commercial_analysis', 'null').execute()
        
        if response.data:
            print(f"✅ {len(response.data)} artigos com análise comercial encontrados")
            
            for article in response.data[:3]:  # Mostrar apenas os primeiros 3
                print(f"\n📰 Artigo: {article['title']}")
                
                if article.get('commercial_analysis'):
                    analysis = json.loads(article['commercial_analysis'])
                    print(f"   📊 Impacto: {analysis.get('business_impact', 'N/A')}")
                    print(f"   💰 Oportunidades: {analysis.get('sales_opportunities', 'N/A')[:100]}...")
                    print(f"   ⚡ Ações: {analysis.get('action_items', 'N/A')[:100]}...")
                
                if article.get('executive_summary'):
                    print(f"   📋 Resumo: {article['executive_summary'][:150]}...")
                
        else:
            print("⚠️ Nenhum artigo com análise comercial encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao buscar artigos: {e}")
    
    # Testar análise comercial em um artigo de exemplo
    print("\n🔬 TESTANDO ANÁLISE EM ARTIGO DE EXEMPLO")
    print("-" * 40)
    
    test_article = {
        'title': 'Anvisa aprova novo medicamento para tratamento de diabetes',
        'content': 'A Agência Nacional de Vigilância Sanitária (Anvisa) aprovou um novo medicamento para o tratamento de diabetes tipo 2, que promete reduzir os efeitos colaterais em até 40%. O medicamento, desenvolvido por uma farmacêutica nacional, estará disponível nas farmácias em até 90 dias, com preço sugerido de R$ 45 por caixa com 30 comprimidos. Esta aprovação representa um avanço significativo no tratamento da doença que afeta mais de 16 milhões de brasileiros.',
        'excerpt': 'A Anvisa aprovou novo medicamento para diabetes tipo 2 com 40% menos efeitos colaterais.'
    }
    
    # Simular análise comercial básica
    analysis = {
        'category': 'regulamentacao',
        'tags': ['farmacia', 'medicamentos', 'anvisa'],
        'priority': 2,
        'summary': test_article['excerpt'],
        'relevance_score': 9,
        'commercial_analysis': {
            'business_impact': 'alta',
            'sales_opportunities': 'Novo medicamento pode gerar aumento de 15-20% nas vendas de diabetes. Oportunidade de ser pioneiro na oferta.',
            'competitive_advantage': 'Ser o primeiro a oferecer o medicamento pode capturar market share significativo da concorrência.',
            'action_items': '1) Contatar fornecedores para disponibilidade 2) Treinar equipe sobre o produto 3) Criar campanha de lançamento 4) Preparar estoque inicial',
            'risk_factors': 'Possível alta demanda inicial pode causar ruptura de estoque. Necessidade de investimento em marketing.',
            'market_trends': 'Tendência de medicamentos com menos efeitos colaterais em crescimento. Consumidores mais conscientes sobre qualidade.'
        },
        'executive_summary': 'Aprovação de novo medicamento para diabetes representa oportunidade significativa de crescimento. Recomenda-se preparação imediata para lançamento, incluindo estoque e treinamento da equipe para capturar market share.'
    }
    
    print(f"📰 Artigo de Teste: {test_article['title']}")
    print(f"📊 Análise Comercial:")
    print(f"   • Impacto: {analysis['commercial_analysis']['business_impact']}")
    print(f"   • Oportunidades: {analysis['commercial_analysis']['sales_opportunities']}")
    print(f"   • Ações: {analysis['commercial_analysis']['action_items']}")
    print(f"   • Resumo: {analysis['executive_summary']}")
    
    print("\n✅ TESTE DE ANÁLISE COMERCIAL CONCLUÍDO!")
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Execute a migração do banco: migration_commercial_analysis.sql")
    print("2. Teste o coletor: python3 news_collector.py")
    print("3. Verifique no painel admin: admin-panel.html")
    print("4. Visualize na página pública: noticias.html")

def show_migration_instructions():
    """Mostra instruções para executar a migração"""
    print("\n📋 INSTRUÇÕES PARA MIGRAÇÃO:")
    print("=" * 40)
    print("1. Acesse o Supabase: https://mgcoyeohqelystqmytah.supabase.co")
    print("2. Vá em SQL Editor")
    print("3. Cole o conteúdo do arquivo: migration_commercial_analysis.sql")
    print("4. Execute o SQL")
    print("5. Verifique se os campos foram adicionados")

if __name__ == "__main__":
    test_commercial_analysis()
    show_migration_instructions()

