#!/usr/bin/env python3
"""
🤖 SISTEMA DE COLETA AUTOMÁTICA DE NOTÍCIAS TEM VENDA
Coleta notícias de sites farmacêuticos usando IA para análise e categorização
"""

import os
import json
import requests
import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import re
from supabase import create_client, Client
from openai import OpenAI
import time
import logging

# Carregar variáveis de ambiente do arquivo .env se existir
def load_env_file():
    """Carrega variáveis de ambiente de um arquivo .env"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        # Configurações Supabase
        self.supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
        
        # Configurações OpenAI
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        # Inicializar clientes
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.openai = OpenAI(api_key=self.openai_key) if self.openai_key else None
        
        # Configurações
        self.max_articles_per_run = 20
        self.min_content_length = 200
        
        # Palavras-chave para filtrar notícias relevantes
        self.keywords = [
            'farmácia', 'farmacêutico', 'medicamento', 'drogaria',
            'anvisa', 'regulamentação', 'genérico', 'similar',
            'vendas farmacêuticas', 'mercado farmacêutico',
            'gestão farmácia', 'liderança farmácia'
        ]
        
        logger.info("🚀 NewsCollector inicializado com sucesso!")

    def get_active_sources(self):
        """Busca fontes ativas no banco"""
        try:
            response = self.supabase.table('news_sources').select('*').eq('is_active', True).execute()
            return response.data
        except Exception as e:
            logger.error(f"❌ Erro ao buscar fontes: {e}")
            return []

    def fetch_rss_articles(self, source):
        """Coleta artigos de uma fonte RSS"""
        articles = []
        
        if not source.get('rss_url'):
            logger.warning(f"⚠️ Fonte {source['name']} não tem RSS URL")
            return articles
            
        try:
            logger.info(f"📡 Coletando RSS de: {source['name']}")
            feed = feedparser.parse(source['rss_url'])
            
            for entry in feed.entries[:10]:  # Limitar a 10 por fonte
                try:
                    article = {
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'excerpt': entry.get('summary', ''),
                        'published_at': self.parse_date(entry.get('published')),
                        'source_id': source['id'],
                        'raw_content': entry.get('summary', '')
                    }
                    
                    # Verificar se é relevante
                    if self.is_relevant_article(article):
                        articles.append(article)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar entrada RSS: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao coletar RSS de {source['name']}: {e}")
            
        return articles

    def scrape_article_content(self, url):
        """Extrai conteúdo completo de um artigo"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover scripts e estilos
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Tentar encontrar o conteúdo principal
            content_selectors = [
                'article', '.article-content', '.post-content', 
                '.entry-content', '.content', 'main'
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(strip=True)
                    break
            
            if not content:
                # Fallback: pegar todo o texto do body
                body = soup.find('body')
                if body:
                    content = body.get_text(strip=True)
            
            # Limitar tamanho
            if len(content) > 5000:
                content = content[:5000] + "..."
                
            return content
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair conteúdo de {url}: {e}")
            return ""

    def is_relevant_article(self, article):
        """Verifica se o artigo é relevante para farmácias"""
        text = f"{article['title']} {article['excerpt']}".lower()
        
        # Verificar palavras-chave
        relevance_score = sum(1 for keyword in self.keywords if keyword in text)
        
        # Verificar tamanho mínimo
        if len(article['excerpt']) < self.min_content_length:
            return False
            
        return relevance_score >= 2  # Pelo menos 2 palavras-chave

    def analyze_with_ai(self, article):
        """Usa IA para analisar e categorizar o artigo"""
        if not self.openai:
            logger.warning("⚠️ OpenAI não configurada, usando análise básica")
            return self.basic_analysis(article)
        
        try:
            prompt = f"""
            Você é um especialista em gestão comercial farmacêutica. Analise este artigo e forneça insights estratégicos para gestores de farmácias.
            
            Título: {article['title']}
            Conteúdo: {article['content'][:2000]}
            
            Responda em JSON com análise completa:
            {{
                "category": "regulamentacao|mercado|tecnologia|gestao|saude-publica",
                "tags": ["tag1", "tag2", "tag3"],
                "priority": 0|1|2,
                "summary": "resumo em 2-3 frases",
                "relevance_score": 1-10,
                "commercial_analysis": {{
                    "business_impact": "Como isso impacta o negócio farmacêutico (alta/média/baixa)",
                    "sales_opportunities": "Oportunidades de vendas identificadas",
                    "competitive_advantage": "Como usar isso para vantagem competitiva",
                    "action_items": "Ações práticas que o gestor pode tomar",
                    "risk_factors": "Riscos ou desafios para o negócio",
                    "market_trends": "Tendências de mercado identificadas"
                }},
                "executive_summary": "Resumo executivo para tomada de decisão em 1 parágrafo"
            }}
            """
            
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise IA: {e}")
            return self.basic_analysis(article)

    def basic_analysis(self, article):
        """Análise básica sem IA"""
        text = f"{article['title']} {article['content']}".lower()
        
        # Categorização básica
        if any(word in text for word in ['anvisa', 'regulamentação', 'lei', 'norma']):
            category = 'regulamentacao'
        elif any(word in text for word in ['mercado', 'vendas', 'crescimento', 'receita']):
            category = 'mercado'
        elif any(word in text for word in ['tecnologia', 'digital', 'app', 'sistema']):
            category = 'tecnologia'
        elif any(word in text for word in ['gestão', 'liderança', 'equipe', 'treinamento']):
            category = 'gestao'
        else:
            category = 'saude-publica'
        
        # Tags básicas
        tags = []
        if 'farmácia' in text:
            tags.append('farmacia')
        if 'medicamento' in text:
            tags.append('medicamentos')
        if 'anvisa' in text:
            tags.append('anvisa')
        
        # Análise comercial básica
        business_impact = 'média'
        if any(word in text for word in ['crescimento', 'aumento', 'expansão', 'novo']):
            business_impact = 'alta'
        elif any(word in text for word in ['redução', 'diminuição', 'crise', 'problema']):
            business_impact = 'baixa'
        
        sales_opportunities = "Analise oportunidades de vendas baseadas no conteúdo da notícia"
        competitive_advantage = "Identifique como usar esta informação para se destacar da concorrência"
        action_items = "Defina ações práticas baseadas nas informações apresentadas"
        risk_factors = "Avalie riscos e desafios mencionados na notícia"
        market_trends = "Identifique tendências de mercado relevantes"
        
        return {
            'category': category,
            'tags': tags[:3],
            'priority': 1 if 'urgente' in text or 'importante' in text else 0,
            'summary': article['excerpt'][:200] + "...",
            'relevance_score': 7,
            'commercial_analysis': {
                'business_impact': business_impact,
                'sales_opportunities': sales_opportunities,
                'competitive_advantage': competitive_advantage,
                'action_items': action_items,
                'risk_factors': risk_factors,
                'market_trends': market_trends
            },
            'executive_summary': f"Notícia sobre {category} com impacto {business_impact} no negócio farmacêutico. Recomenda-se análise detalhada para identificar oportunidades de crescimento."
        }

    def generate_slug(self, title):
        """Gera slug único para o artigo"""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug[:100]  # Limitar tamanho
        
        # Adicionar timestamp para garantir unicidade
        timestamp = int(time.time())
        return f"{slug}-{timestamp}"

    def save_article(self, article, analysis):
        """Salva artigo no banco de dados"""
        try:
            # Verificar se já existe
            existing = self.supabase.table('news_articles').select('id').eq('url', article['url']).execute()
            if existing.data:
                logger.info(f"📄 Artigo já existe: {article['title']}")
                return False
            
            # Buscar categoria
            category = self.supabase.table('news_categories').select('id').eq('slug', analysis['category']).execute()
            category_id = category.data[0]['id'] if category.data else None
            
            # Preparar dados
            article_data = {
                'title': article['title'],
                'slug': self.generate_slug(article['title']),
                'excerpt': analysis['summary'],
                'content': article['content'],
                'url': article['url'],
                'source_id': article['source_id'],
                'category_id': category_id,
                'status': 'pending',
                'priority': analysis['priority'],
                'published_at': article['published_at'],
                'scraped_at': datetime.now().isoformat()
            }
            
            # Adicionar análise comercial se disponível
            if 'commercial_analysis' in analysis:
                article_data['commercial_analysis'] = json.dumps(analysis['commercial_analysis'])
            
            if 'executive_summary' in analysis:
                article_data['executive_summary'] = analysis['executive_summary']
            
            # Inserir artigo
            result = self.supabase.table('news_articles').insert(article_data).execute()
            
            if result.data:
                article_id = result.data[0]['id']
                logger.info(f"✅ Artigo salvo: {article['title']} (ID: {article_id})")
                
                # Salvar tags
                self.save_article_tags(article_id, analysis['tags'])
                
                return True
            else:
                logger.error(f"❌ Erro ao salvar artigo: {article['title']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar artigo: {e}")
            return False

    def save_article_tags(self, article_id, tags):
        """Salva tags do artigo"""
        try:
            for tag_name in tags:
                # Buscar ou criar tag
                tag_result = self.supabase.table('news_tags').select('id').eq('name', tag_name).execute()
                
                if tag_result.data:
                    tag_id = tag_result.data[0]['id']
                else:
                    # Criar nova tag
                    new_tag = self.supabase.table('news_tags').insert({
                        'name': tag_name,
                        'slug': tag_name.lower().replace(' ', '-')
                    }).execute()
                    tag_id = new_tag.data[0]['id']
                
                # Relacionar artigo com tag
                self.supabase.table('news_article_tags').insert({
                    'article_id': article_id,
                    'tag_id': tag_id
                }).execute()
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao salvar tags: {e}")

    def parse_date(self, date_str):
        """Converte string de data para formato ISO"""
        if not date_str:
            return datetime.now().isoformat()
        
        try:
            # Tentar diferentes formatos
            formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%a, %d %b %Y %H:%M:%S %Z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt).isoformat()
                except ValueError:
                    continue
            
            return datetime.now().isoformat()
            
        except Exception:
            return datetime.now().isoformat()

    def run_collection(self):
        """Executa a coleta completa"""
        logger.info("🚀 Iniciando coleta de notícias...")
        
        sources = self.get_active_sources()
        if not sources:
            logger.warning("⚠️ Nenhuma fonte ativa encontrada")
            return
        
        total_collected = 0
        
        for source in sources:
            try:
                logger.info(f"📡 Processando fonte: {source['name']}")
                
                # Coletar artigos RSS
                articles = self.fetch_rss_articles(source)
                
                for article in articles[:5]:  # Limitar por fonte
                    try:
                        # Extrair conteúdo completo
                        article['content'] = self.scrape_article_content(article['url'])
                        
                        if len(article['content']) < self.min_content_length:
                            continue
                        
                        # Analisar com IA
                        analysis = self.analyze_with_ai(article)
                        
                        # Salvar no banco
                        if self.save_article(article, analysis):
                            total_collected += 1
                        
                        # Limite por execução
                        if total_collected >= self.max_articles_per_run:
                            break
                            
                        # Pausa entre artigos
                        time.sleep(2)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao processar artigo: {e}")
                        continue
                
                # Atualizar última coleta da fonte
                self.supabase.table('news_sources').update({
                    'last_scraped': datetime.now().isoformat()
                }).eq('id', source['id']).execute()
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar fonte {source['name']}: {e}")
                continue
        
        logger.info(f"✅ Coleta concluída! {total_collected} artigos coletados")

def main():
    """Função principal"""
    collector = NewsCollector()
    collector.run_collection()

if __name__ == "__main__":
    main()
