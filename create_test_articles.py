#!/usr/bin/env python3
"""
📝 CRIADOR DE ARTIGOS DE TESTE - TEM VENDA NEWS
Cria artigos de exemplo para demonstrar o sistema
"""

import os
from datetime import datetime
from supabase import create_client, Client

def create_test_articles():
    # Configurações Supabase
    supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Artigos de teste
    test_articles = [
        {
            'title': 'Anvisa aprova novo medicamento para tratamento de diabetes',
            'excerpt': 'A Agência Nacional de Vigilância Sanitária (Anvisa) aprovou um novo medicamento para o tratamento de diabetes tipo 2, que promete reduzir os efeitos colaterais em até 40%.',
            'content': 'A Agência Nacional de Vigilância Sanitária (Anvisa) aprovou nesta segunda-feira um novo medicamento para o tratamento de diabetes tipo 2. O medicamento, desenvolvido por uma farmacêutica nacional, promete reduzir os efeitos colaterais em até 40% comparado aos tratamentos convencionais.\n\nO diretor da Anvisa, Antônio Barra Torres, destacou que a aprovação representa um avanço significativo no tratamento da doença que afeta mais de 16 milhões de brasileiros. "Este medicamento oferece uma alternativa mais segura e eficaz para os pacientes", afirmou.\n\nO medicamento estará disponível nas farmácias em até 90 dias, com preço sugerido de R$ 45 por caixa com 30 comprimidos.',
            'url': 'https://exemplo.com/anvisa-aprova-medicamento-diabetes',
            'category_id': 1,  # Regulamentação
            'source_id': 1,    # Abrafarma
            'status': 'approved',
            'priority': 2,
            'published_at': datetime.now().isoformat()
        },
        {
            'title': 'Mercado farmacêutico brasileiro cresce 12% no primeiro trimestre',
            'excerpt': 'O setor farmacêutico brasileiro registrou crescimento de 12% no primeiro trimestre de 2024, impulsionado pelo aumento da demanda por medicamentos genéricos e similares.',
            'content': 'O mercado farmacêutico brasileiro apresentou crescimento robusto de 12% no primeiro trimestre de 2024, segundo dados da Associação Brasileira da Indústria Farmacêutica (Abrafarma). O crescimento foi impulsionado principalmente pelo aumento da demanda por medicamentos genéricos e similares.\n\nOs medicamentos genéricos representaram 35% do total de vendas, seguidos pelos similares com 22% e os medicamentos de referência com 43%. O crescimento foi observado em todas as regiões do país, com destaque para o Nordeste, que registrou aumento de 15%.\n\n"Este crescimento reflete a confiança dos consumidores nos medicamentos genéricos e similares, que oferecem a mesma qualidade dos medicamentos de referência a preços mais acessíveis", comentou o presidente da Abrafarma.',
            'url': 'https://exemplo.com/mercado-farmaceutico-cresce-12',
            'category_id': 2,  # Mercado
            'source_id': 2,    # Revista Farmácia
            'status': 'approved',
            'priority': 1,
            'published_at': datetime.now().isoformat()
        },
        {
            'title': 'Farmácias investem em tecnologia para melhorar atendimento',
            'excerpt': 'Redes farmacêuticas estão investindo em inteligência artificial e sistemas digitais para otimizar o atendimento e reduzir o tempo de espera dos clientes.',
            'content': 'As principais redes farmacêuticas do país estão investindo pesadamente em tecnologia para revolucionar o atendimento ao cliente. Sistemas de inteligência artificial, aplicativos móveis e plataformas digitais estão sendo implementados para reduzir o tempo de espera e melhorar a experiência do cliente.\n\nA Farmácia Popular, por exemplo, lançou um sistema que utiliza IA para identificar medicamentos similares quando o produto solicitado não está disponível. O sistema já reduziu em 30% o tempo de atendimento.\n\nOutras redes estão implementando sistemas de gestão de estoque inteligente que preveem a demanda e evitam a falta de medicamentos essenciais. "A tecnologia está transformando o setor farmacêutico", afirma o especialista em tecnologia farmacêutica.',
            'url': 'https://exemplo.com/farmacias-investem-tecnologia',
            'category_id': 3,  # Tecnologia
            'source_id': 3,    # Portal Farma
            'status': 'pending',
            'priority': 1,
            'published_at': datetime.now().isoformat()
        },
        {
            'title': 'Curso de gestão farmacêutica capacita mais de 500 profissionais',
            'excerpt': 'Programa de capacitação em gestão farmacêutica formou mais de 500 profissionais em 2024, contribuindo para a melhoria da qualidade do atendimento.',
            'content': 'O programa de capacitação em gestão farmacêutica, desenvolvido em parceria com universidades e associações do setor, formou mais de 500 profissionais em 2024. O curso aborda temas como gestão de pessoas, controle de estoque, atendimento ao cliente e legislação farmacêutica.\n\nOs participantes relatam melhorias significativas na gestão de suas farmácias após o curso. "Aprendi técnicas de liderança que transformaram minha equipe", conta Maria Silva, farmacêutica de São Paulo.\n\nO programa será expandido em 2025, com previsão de capacitar mais de 1.000 profissionais. As inscrições para a nova turma já estão abertas.',
            'url': 'https://exemplo.com/curso-gestao-farmaceutica-500-profissionais',
            'category_id': 4,  # Gestão
            'source_id': 1,    # Abrafarma
            'status': 'approved',
            'priority': 0,
            'published_at': datetime.now().isoformat()
        },
        {
            'title': 'Campanha de vacinação contra gripe atinge 80% da meta',
            'excerpt': 'Campanha nacional de vacinação contra gripe atingiu 80% da meta estabelecida pelo Ministério da Saúde, com mais de 40 milhões de doses aplicadas.',
            'content': 'A campanha nacional de vacinação contra gripe atingiu 80% da meta estabelecida pelo Ministério da Saúde, com mais de 40 milhões de doses aplicadas em todo o país. A campanha, que teve início em abril, foi prorrogada até o final de maio para atingir a meta de 50 milhões de doses.\n\nO secretário de Vigilância em Saúde, Arnaldo Medeiros, destacou a importância da vacinação para prevenir complicações da gripe, especialmente em grupos de risco como idosos, gestantes e pessoas com comorbidades.\n\nAs farmácias particulares também estão oferecendo a vacina contra gripe, contribuindo para o aumento da cobertura vacinal. "É importante que todos se vacinem para proteger a si mesmos e a comunidade", reforça o secretário.',
            'url': 'https://exemplo.com/campanha-vacinacao-gripe-80-meta',
            'category_id': 5,  # Saúde Pública
            'source_id': 2,    # Revista Farmácia
            'status': 'approved',
            'priority': 1,
            'published_at': datetime.now().isoformat()
        }
    ]
    
    print("📝 Criando artigos de teste...")
    
    for i, article in enumerate(test_articles, 1):
        try:
            # Gerar slug único
            slug = f"{article['title'].lower().replace(' ', '-').replace(',', '').replace('ç', 'c').replace('ã', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}-{i}"
            
            # Adicionar slug ao artigo
            article['slug'] = slug
            article['scraped_at'] = datetime.now().isoformat()
            article['created_at'] = datetime.now().isoformat()
            article['updated_at'] = datetime.now().isoformat()
            
            # Inserir no banco
            result = supabase.table('news_articles').insert(article).execute()
            
            if result.data:
                print(f"✅ Artigo {i} criado: {article['title']}")
            else:
                print(f"❌ Erro ao criar artigo {i}")
                
        except Exception as e:
            print(f"❌ Erro ao criar artigo {i}: {e}")
    
    print("\n🎉 Artigos de teste criados com sucesso!")
    print("Acesse o painel admin para visualizar e gerenciar os artigos.")

if __name__ == "__main__":
    create_test_articles()
