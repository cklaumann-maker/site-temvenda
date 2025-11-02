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
import ssl
# Desabilitar avisos de SSL para feeds que não têm certificado válido
ssl._create_default_https_context = ssl._create_unverified_context
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Usando REST API direta ao invés do cliente Python (para evitar problemas de compatibilidade)
# from supabase import create_client, Client
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
# Criar diretório de logs se não existir
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'news_collector.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        # Configurações Supabase (usando variáveis de ambiente ou valores padrão)
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://mgcoyeohqelystqmytah.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ')
        
        # Configurações OpenAI
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        # Não usar cliente Python do Supabase (problemas de compatibilidade)
        # Usar REST API direta
        self.supabase = None
        self.openai = OpenAI(api_key=self.openai_key) if self.openai_key else None
        
        # Configurações
        self.max_articles_per_run = 30  # Aumentado para coletar mais notícias
        self.min_content_length = 100  # Reduzido de 200 para 100
        
        # Palavras-chave para filtrar notícias relevantes (expandido)
        self.keywords = [
            'farmácia', 'farmacêutico', 'medicamento', 'drogaria',
            'anvisa', 'regulamentação', 'genérico', 'similar',
            'vendas farmacêuticas', 'mercado farmacêutico',
            'gestão farmácia', 'liderança farmácia', 'varejo',
            'farmacêutica', 'indústria farmacêutica', 'distribuição',
            'atacado', 'rede', 'loja', 'venda', 'comercial',
            'negócio', 'crescimento', 'receita', 'lucro', 'balanço'
        ]
        
        logger.info("🚀 NewsCollector inicializado com sucesso!")

    def _supabase_request(self, method, table, data=None, filters=None, select='*'):
        """Faz requisição REST direta ao Supabase"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        if filters:
            for key, value in filters.items():
                url += f"&{key}=eq.{value}" if '?' in url else f"?{key}=eq.{value}"
        
        if select != '*':
            url += f"{'&' if '?' in url else '?'}select={select}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Método não suportado: {method}")
            
            response.raise_for_status()
            return {'data': response.json() if response.content else []}
        except Exception as e:
            logger.error(f"❌ Erro na requisição Supabase ({method} {table}): {e}")
            raise
    
    def get_active_sources(self):
        """Busca fontes ativas no banco"""
        try:
            response = self._supabase_request('GET', 'news_sources', filters={'is_active': 'true'})
            return response['data'] if isinstance(response['data'], list) else []
        except Exception as e:
            logger.error(f"❌ Erro ao buscar fontes: {e}")
            return []

    def fetch_rss_articles(self, source):
        """Coleta artigos de uma fonte RSS com fallback para scraping direto"""
        articles = []
        
        if not source.get('rss_url'):
            logger.warning(f"⚠️ Fonte {source['name']} não tem RSS URL")
            return articles
            
        try:
            logger.info(f"📡 Coletando RSS de: {source['name']}")
            rss_url = source['rss_url']
            
            # Tentar com feedparser usando requests para evitar problemas de SSL
            try:
                # Baixar feed usando requests (melhor tratamento de SSL)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(rss_url, headers=headers, timeout=15, verify=False)
                response.raise_for_status()
                
                # Parsear com feedparser usando os dados baixados
                feed = feedparser.parse(response.content)
                
            except Exception as ssl_error:
                logger.warning(f"⚠️ Erro SSL ao baixar RSS, tentando feedparser direto: {ssl_error}")
                # Fallback: tentar feedparser direto
                feed = feedparser.parse(rss_url)
            
            # Verificar se o feed tem entradas
            if not feed.entries:
                logger.warning(f"⚠️ Feed de {source['name']} não retornou entradas")
                if hasattr(feed, 'bozo_exception') and feed.bozo_exception:
                    logger.warning(f"   Erro no feed: {feed.bozo_exception}")
                return articles
            
            logger.info(f"📰 Encontradas {len(feed.entries)} entradas no feed")
            
            # Processar até 20 entradas por fonte (aumentado de 10)
            for idx, entry in enumerate(feed.entries[:20]):
                try:
                    title = entry.get('title', '').strip()
                    url = entry.get('link', '').strip()
                    excerpt = entry.get('summary', entry.get('description', '')).strip()
                    
                    if not title or not url:
                        logger.debug(f"⏭️ Entrada {idx+1} ignorada (sem título ou URL)")
                        continue
                    
                    article = {
                        'title': title,
                        'url': url,
                        'excerpt': excerpt or '',  # Permitir excerpt vazio
                        'published_at': self.parse_date(entry.get('published')),
                        'source_id': source['id'],
                        'raw_content': excerpt or ''
                    }
                    
                    # Verificar relevância (mais flexível agora)
                    relevance_result = self.is_relevant_article(article)
                    
                    if relevance_result['relevant']:
                        logger.info(f"✅ Artigo relevante encontrado: {title[:60]}...")
                        logger.debug(f"   Score: {relevance_result['score']}, Razão: {relevance_result['reason']}")
                        articles.append(article)
                    else:
                        logger.debug(f"⏭️ Artigo ignorado: {title[:60]}... (Razão: {relevance_result['reason']})")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar entrada RSS {idx+1}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao coletar RSS de {source['name']}: {e}")
            
        logger.info(f"📊 Total de {len(articles)} artigos relevantes coletados de {source['name']}")
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
        """Verifica se o artigo é relevante para farmácias (validação melhorada)"""
        text = f"{article['title']} {article['excerpt']}".lower()
        
        # Verificar palavras-chave
        found_keywords = [kw for kw in self.keywords if kw in text]
        relevance_score = len(found_keywords)
        
        # Validação mais flexível
        reasons = []
        
        # 1. Se tem pelo menos 1 palavra-chave relevante, aceita
        if relevance_score >= 1:
            return {
                'relevant': True,
                'score': relevance_score,
                'reason': f'Encontradas {relevance_score} palavras-chave: {", ".join(found_keywords[:3])}',
                'keywords': found_keywords
            }
        
        # 2. Se o título tem termos relacionados mesmo sem palavras-chave exatas
        title_lower = article['title'].lower()
        related_terms = ['farmácia', 'farmacêutico', 'medicamento', 'drogaria', 'anvisa', 
                         'varejo', 'indústria', 'distribuição', 'atacado', 'rede', 'loja']
        if any(term in title_lower for term in related_terms):
            return {
                'relevant': True,
                'score': 0.5,
                'reason': 'Termos relacionados encontrados no título',
                'keywords': []
            }
        
        # 3. Rejeitar se não há nenhum indício de relevância
        return {
            'relevant': False,
            'score': 0,
            'reason': f'Nenhuma palavra-chave relevante encontrada (0 de {len(self.keywords)})',
            'keywords': []
        }

    def analyze_with_ai(self, article):
        """Usa IA para analisar e categorizar o artigo"""
        if not self.openai:
            logger.warning("⚠️ OpenAI não configurada, usando análise básica")
            return self.basic_analysis(article)
        
        try:
            prompt = f"""
            Você é um consultor prático de gestão comercial farmacêutica. Analise este artigo e forneça INSIGHTS PRÁTICOS E ACIONÁVEIS para gestores de farmácias que podem ser aplicados IMEDIATAMENTE.
            
            Título: {article['title']}
            Conteúdo: {article['content'][:2000]}
            
            FOCO: Seja CONCRETO, ESPECÍFICO e PRÁTICO. Cada insight deve ser algo que o gestor possa fazer HOJE.
            
            Responda em JSON com análise completa:
            {{
                "category": "regulamentacao|mercado|tecnologia|gestao|saude-publica",
                "tags": ["tag1", "tag2", "tag3"],
                "priority": 0|1|2,
                "summary": "resumo em 2-3 frases",
                "relevance_score": 1-10,
                "commercial_analysis": {{
                    "business_impact": "alta/média/baixa",
                    "sales_opportunities": "Oportunidades ESPECÍFICAS de vendas (ex: 'Aumentar estoque de X em 20% para atender demanda crescente')",
                    "competitive_advantage": "Como usar isso para vantagem competitiva (ex: 'Destaque este produto na vitrine e ofereça desconto de 10% para atrair clientes')",
                    "action_items": "AÇÕES IMEDIATAS em 3-5 itens numerados e específicos que o gestor pode fazer HOJE (ex: '1. Treinar equipe sobre X produto amanhã às 9h. 2. Criar promoção especial até sexta-feira. 3. Atualizar cardápio visual com novo produto.')",
                    "immediate_insights": "3 insights práticos e acionáveis que podem ser aplicados AGORA (formato: lista numerada com ações concretas)",
                    "quick_wins": "2-3 ações rápidas (menos de 1 hora) que geram resultado imediato",
                    "risk_factors": "Riscos específicos e como mitigá-los com ações práticas",
                    "market_trends": "Tendências identificadas e como capitalizar AGORA"
                }},
                "executive_summary": "Resumo executivo focando em 'O QUE FAZER AGORA' em 1 parágrafo"
            }}
            
            IMPORTANTE: 
            - action_items deve ter passos CONCRETOS e EXECUTÁVEIS
            - immediate_insights deve ter ações que podem ser feitas HOJE
            - quick_wins devem ser ações RÁPIDAS (< 1h) com resultado IMEDIATO
            - Seja ESPECÍFICO: evite genérico como "melhorar vendas", use "aumentar venda de X em 15% até semana que vem"
            """
            
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,  # Aumentado para insights mais detalhados
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
        
        # Extrair ações práticas do conteúdo
        action_items_list = []
        if 'treinar' in text or 'capacitar' in text:
            action_items_list.append("1. Agendar treinamento com equipe sobre o tema na próxima semana")
        if 'promoção' in text or 'desconto' in text:
            action_items_list.append("2. Criar promoção relacionada ao tema para aumentar vendas")
        if 'produto' in text or 'medicamento' in text:
            action_items_list.append("3. Revisar mix de produtos relacionados e ajustar estoque")
        if not action_items_list:
            action_items_list = ["1. Revisar informações detalhadas da notícia", "2. Compartilhar insights com equipe", "3. Avaliar impacto no negócio"]
        
        sales_opportunities = f"Analise oportunidades de vendas específicas baseadas no conteúdo: {article['title'][:100]}"
        competitive_advantage = "Use esta informação para se destacar: implemente ações práticas mencionadas na notícia"
        action_items = ". ".join(action_items_list) if action_items_list else "Analise a notícia e defina ações práticas"
        immediate_insights = "1. Revisar detalhes completos da notícia\n2. Identificar produtos/oportunidades específicas\n3. Compartilhar com equipe comercial"
        quick_wins = "1. Compartilhar notícia com equipe (5 min)\n2. Revisar mix de produtos relacionados (15 min)"
        risk_factors = "Avalie riscos mencionados e implemente ações preventivas imediatas"
        market_trends = "Identifique tendências e capitalize com ações práticas esta semana"
        
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
                'immediate_insights': immediate_insights,
                'quick_wins': quick_wins,
                'risk_factors': risk_factors,
                'market_trends': market_trends
            },
            'executive_summary': f"Notícia sobre {category} com impacto {business_impact}. AÇÕES IMEDIATAS: {action_items_list[0] if action_items_list else 'Revisar detalhes e definir ações práticas'}."
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
        """Salva artigo no banco de dados com verificação melhorada de duplicatas"""
        try:
            # Verificar duplicatas de múltiplas formas:
            # 1. Por URL exata
            existing = self._supabase_request('GET', 'news_articles', select='id', filters={'url': article['url']})
            if existing['data']:
                logger.info(f"📄 Artigo já existe (URL): {article['title'][:50]}...")
                return False
            
            # 2. Por título similar (usando filtro ilike via REST API)
            url_title = f"{self.supabase_url}/rest/v1/news_articles?select=id,title&title=ilike.*{requests.utils.quote(article['title'][:50])}*"
            headers_title = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json'
            }
            existing_by_title_resp = requests.get(url_title, headers=headers_title, timeout=10)
            existing_by_title_data = existing_by_title_resp.json() if existing_by_title_resp.ok else []
            
            if existing_by_title_data:
                # Verificar se o título é muito similar (evitar variações mínimas)
                for existing in existing_by_title_data:
                    existing_title_norm = re.sub(r'[^\w\s]', '', existing['title'].lower().strip())
                    new_title_norm = re.sub(r'[^\w\s]', '', article['title'].lower().strip())
                    
                    # Se mais de 90% dos caracteres são iguais, considerar duplicata
                    similarity = len(set(existing_title_norm) & set(new_title_norm)) / max(len(existing_title_norm), len(new_title_norm), 1)
                    if similarity > 0.9:
                        logger.info(f"📄 Artigo muito similar já existe: {article['title'][:50]}...")
                        return False
            
            # Buscar categoria
            category = self._supabase_request('GET', 'news_categories', select='id', filters={'slug': analysis['category']})
            category_id = category['data'][0]['id'] if category['data'] else None
            
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
            result = self._supabase_request('POST', 'news_articles', data=article_data)
            
            if result['data']:
                article_id = result['data'][0]['id']
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
        """Salva tags do artigo com tratamento melhorado de duplicatas"""
        try:
            for tag_name in tags:
                if not tag_name or not tag_name.strip():
                    continue
                    
                tag_name = tag_name.strip()
                tag_slug = tag_name.lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('õ', 'o').replace('ç', 'c')
                
                tag_id = None
                
                # 1. Tentar buscar por nome exato
                tag_result = self.supabase.table('news_tags').select('id').eq('name', tag_name).execute()
                if tag_result.data:
                    tag_id = tag_result.data[0]['id']
                    logger.debug(f"✅ Tag encontrada por nome: {tag_name}")
                
                # 2. Se não encontrou, tentar buscar por slug
                if not tag_id:
                    tag_result = self.supabase.table('news_tags').select('id').eq('slug', tag_slug).execute()
                    if tag_result.data:
                        tag_id = tag_result.data[0]['id']
                        logger.debug(f"✅ Tag encontrada por slug: {tag_slug}")
                
                # 3. Se ainda não encontrou, criar nova tag
                if not tag_id:
                    try:
                        new_tag = self.supabase.table('news_tags').insert({
                            'name': tag_name,
                            'slug': tag_slug
                        }).execute()
                        
                        if new_tag.data:
                            tag_id = new_tag.data[0]['id']
                            logger.debug(f"✅ Nova tag criada: {tag_name} ({tag_slug})")
                    except Exception as insert_error:
                        # Se der erro de duplicata no slug, buscar novamente pelo slug
                        if 'duplicate' in str(insert_error).lower() or '23505' in str(insert_error):
                            logger.warning(f"⚠️ Conflito de slug ao criar tag '{tag_name}', buscando por slug...")
                            tag_result = self.supabase.table('news_tags').select('id').eq('slug', tag_slug).execute()
                            if tag_result.data:
                                tag_id = tag_result.data[0]['id']
                                logger.debug(f"✅ Tag encontrada após conflito: {tag_slug}")
                            else:
                                logger.error(f"❌ Não foi possível criar nem encontrar tag: {tag_name}")
                                continue
                        else:
                            logger.error(f"❌ Erro ao criar tag '{tag_name}': {insert_error}")
                            continue
                
                # 4. Relacionar artigo com tag (verificar se já não existe)
                if tag_id:
                    try:
                        # Verificar se já existe relação
                        existing_relation = self.supabase.table('news_article_tags').select('id').eq('article_id', article_id).eq('tag_id', tag_id).execute()
                        
                        if not existing_relation.data:
                            # Inserir relação
                            self.supabase.table('news_article_tags').insert({
                                'article_id': article_id,
                                'tag_id': tag_id
                            }).execute()
                            logger.debug(f"✅ Relação artigo-tag criada: {tag_name}")
                        else:
                            logger.debug(f"⏭️ Relação artigo-tag já existe: {tag_name}")
                    except Exception as relation_error:
                        # Ignorar erro de duplicata na relação (já existe)
                        if 'duplicate' in str(relation_error).lower() or '23505' in str(relation_error):
                            logger.debug(f"⏭️ Relação artigo-tag já existe: {tag_name}")
                        else:
                            logger.warning(f"⚠️ Erro ao relacionar tag '{tag_name}' com artigo: {relation_error}")
                
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
                
                logger.info(f"📄 Processando {len(articles)} artigos de {source['name']}")
                
                for idx, article in enumerate(articles[:10]):  # Aumentado de 5 para 10 por fonte
                    try:
                        logger.info(f"📖 [{idx+1}/{len(articles)}] Processando: {article['title'][:60]}...")
                        
                        # Extrair conteúdo completo
                        article['content'] = self.scrape_article_content(article['url'])
                        
                        if len(article['content']) < self.min_content_length:
                            logger.warning(f"⏭️ Conteúdo muito curto ({len(article['content'])} chars): {article['title'][:50]}...")
                            continue
                        
                        logger.debug(f"✅ Conteúdo extraído: {len(article['content'])} caracteres")
                        
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
