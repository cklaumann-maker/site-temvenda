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
from openai import OpenAI
import time
import logging

# ---------------------------------------------------------------------------
# Sanitização de texto (corrige palavras coladas do scraping)
# ---------------------------------------------------------------------------

def sanitize_text(text):
    """Corrige palavras coladas comuns em textos scrapeados de sites brasileiros."""
    if not text:
        return text
    t = text
    # minúscula seguida de maiúscula: "regulamentacaoNova" → "regulamentacao Nova"
    t = re.sub(r'([a-záéíóúãõç])([A-ZÁÉÍÓÚÃÕÇ])', r'\1 \2', t)
    # Maiúscula isolada colada em palavra: "AProfarma" → "A Profarma"
    t = re.sub(r'\b([A-ZÁÉÍÓÚÃÕÇ])([A-ZÁÉÍÓÚÃÕÇ][a-záéíóúãõç]{2,})', r'\1 \2', t)
    # Pontuação colada: ".O governo" → ". O governo"
    t = re.sub(r'([.!?,;:])([A-ZÁÉÍÓÚÃÕÇ])', r'\1 \2', t)
    # Sufixo -ção/-são colado com próxima palavra: "Distribuiçãoinformou"
    t = re.sub(r'(ção|são)([a-záéíóúãõç]{2,})', r'\1 \2', t)
    # Verbos/palavras comuns colados à palavra anterior: "Unileveranunciou"
    STUCK_WORDS = (
        r'informou|anunciou|será|comunicou|apresentou|realizou|inaugurou|'
        r'confirmou|divulgou|publicou|segundo|durante|através|possui|oferece|'
        r'passou|previsto|prevista|localizado|localizada|lançou|disse|comprou|'
        r'vendeu|abriu|fechou|criou|liderou|produziu|registrou|expandiu|'
        r'investiu|adquiriu|assumiu|nomeou|contratou|demitiu|aprovou|'
        r'iniciou|concluiu|alcançou|atingiu|superou|manteve|reduziu|'
        r'aumentou|cresceu|caiu|subiu|dobrou|triplicou'
    )
    t = re.sub(rf'([a-záéíóúãõç]{{3,}})({STUCK_WORDS})', r'\1 \2', t)
    # Parênteses colados: "Hagge(foto)como" → "Hagge (foto) como"
    t = re.sub(r'([a-záéíóúãõçA-ZÁÉÍÓÚÃÕÇ])\(', r'\1 (', t)
    t = re.sub(r'\)([a-záéíóúãõçA-ZÁÉÍÓÚÃÕÇ])', r') \1', t)
    # Número colado em texto: "6aedição" → "6a edição"
    t = re.sub(r'(\d)([A-Za-záéíóúãõçÁÉÍÓÚÃÕÇ])', r'\1 \2', t)
    # Limpar espaços duplos
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()


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

# ============================================================
# Wrapper REST para Supabase (substitui SDK que não aceita sb_secret_)
# ============================================================
class SupabaseQueryResult:
    """Simula o resultado do SDK"""
    def __init__(self, data):
        self.data = data

class SupabaseQuery:
    """Builder de queries REST compatível com a API do SDK"""
    def __init__(self, client, table):
        self._client = client
        self._table = table
        self._params = []
        self._method = 'GET'
        self._body = None
        self._select_cols = '*'
        self._order_col = None
        self._order_desc = False
        self._limit_val = None

    def select(self, cols='*'):
        self._select_cols = cols
        return self

    def eq(self, col, val):
        self._params.append(f'{col}=eq.{val}')
        return self

    def neq(self, col, val):
        self._params.append(f'{col}=neq.{val}')
        return self

    def gt(self, col, val):
        self._params.append(f'{col}=gt.{val}')
        return self

    def gte(self, col, val):
        self._params.append(f'{col}=gte.{val}')
        return self

    def lt(self, col, val):
        self._params.append(f'{col}=lt.{val}')
        return self

    def lte(self, col, val):
        self._params.append(f'{col}=lte.{val}')
        return self

    def is_(self, col, val):
        self._params.append(f'{col}=is.{val}')
        return self

    def order(self, col, desc=False):
        self._order_col = col
        self._order_desc = desc
        return self

    def limit(self, val):
        self._limit_val = val
        return self

    def insert(self, data):
        self._method = 'POST'
        self._body = data
        return self

    def update(self, data):
        self._method = 'PATCH'
        self._body = data
        return self

    def delete(self):
        self._method = 'DELETE'
        return self

    def execute(self):
        url = f"{self._client.url}/rest/v1/{self._table}"
        params = list(self._params)
        if self._select_cols:
            params.append(f'select={self._select_cols}')
        if self._order_col:
            direction = '.desc' if self._order_desc else ''
            params.append(f'order={self._order_col}{direction}')
        if self._limit_val:
            params.append(f'limit={self._limit_val}')
        if params:
            url += '?' + '&'.join(params)

        headers = {
            'apikey': self._client.key,
            'Authorization': f'Bearer {self._client.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }

        if self._method == 'GET':
            resp = requests.get(url, headers=headers)
        elif self._method == 'POST':
            resp = requests.post(url, headers=headers, json=self._body)
        elif self._method == 'PATCH':
            resp = requests.patch(url, headers=headers, json=self._body)
        elif self._method == 'DELETE':
            resp = requests.delete(url, headers=headers)

        if resp.status_code >= 400:
            raise Exception(f"Supabase REST error {resp.status_code}: {resp.text}")

        try:
            data = resp.json()
        except Exception:
            data = []

        return SupabaseQueryResult(data if isinstance(data, list) else [data] if data else [])

class SupabaseRestClient:
    """Cliente REST leve que imita a interface do SDK"""
    def __init__(self, url, key):
        self.url = url.rstrip('/')
        self.key = key

    def table(self, name):
        return SupabaseQuery(self, name)


class NewsCollector:
    def __init__(self):
        # Configurações Supabase (via variáveis de ambiente)
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://mgcoyeohqelystqmytah.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_KEY', '')

        if not self.supabase_key:
            raise ValueError("SUPABASE_KEY não configurada. Defina a variável de ambiente SUPABASE_KEY.")

        # Configurações OpenAI
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        # Inicializar clientes
        self.supabase = SupabaseRestClient(self.supabase_url, self.supabase_key)
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

        # Mapeamento de categorias específicas por fonte
        self.category_overrides = {
            'https://ictq.com.br/opiniao': 'gestao',
            'https://ictq.com.br/industria-farmaceutica': 'mercado',
            'https://ictq.com.br/varejo-farmaceutico': 'mercado',
            'https://guiadafarmacia.com.br/noticias/': 'mercado'
        }
        
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

    def fetch_guia_da_farmacia_articles(self, source):
        """Coleta artigos diretamente do site Guia da Farmácia quando RSS não estiver disponível"""
        articles = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            logger.info("📰 Coletando via scraping: Guia da Farmácia")
            response = requests.get(source['url'], headers=headers, timeout=12)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.select('.posts-news .col-md-6.mb-40')
            seen_urls = set()

            for card in cards:
                title_el = card.select_one('.post-title a')
                if not title_el:
                    continue

                url = title_el.get('href')
                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)
                title = title_el.get_text(strip=True)

                excerpt_el = card.select_one('.excerpt')
                excerpt = excerpt_el.get_text(" ", strip=True) if excerpt_el else title

                time_el = card.select_one('time.post-date')
                published_at = None
                if time_el and time_el.get('datetime'):
                    published_at = self.parse_date(time_el['datetime'])

                articles.append({
                    'title': title,
                    'url': url,
                    'excerpt': excerpt,
                    'published_at': published_at or datetime.now().isoformat(),
                    'source_id': source['id'],
                    'raw_content': excerpt
                })

                if len(articles) >= 10:
                    break

        except Exception as e:
            logger.error(f"❌ Erro ao coletar Guia da Farmácia: {e}")

        return articles

    def scrape_article_content(self, url):
        """Extrai conteúdo completo de um artigo, preservando parágrafos"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remover scripts, estilos, nav, footer, sidebar, ads
            for tag in soup(["script", "style", "nav", "footer", "aside", "header",
                             "iframe", "noscript", "form"]):
                tag.decompose()

            # Remover elementos de UI/social/share
            for selector in ['.social-share', '.share-buttons', '.related-posts',
                             '.comments', '.sidebar', '.breadcrumb', '.post-meta',
                             '.article-meta', '.author-box', '.newsletter',
                             '.ad', '.advertisement', '.wp-block-image figcaption']:
                for el in soup.select(selector):
                    el.decompose()

            # Tentar encontrar o conteúdo principal
            content_selectors = [
                '.entry-content', '.article-content', '.post-content',
                '.td-post-content', '.article-body', '.post-body',
                '.single-content', '.news-content', '.texto',
                'article .content', 'article', 'main .content', 'main'
            ]

            element = None
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    # Verificar se tem conteúdo substancial
                    text_check = element.get_text(strip=True)
                    if len(text_check) > 200:
                        break
                    element = None

            if not element:
                body = soup.find('body')
                if body:
                    element = body

            if not element:
                return ""

            # Extrair parágrafos preservando estrutura
            paragraphs = []
            for tag in element.find_all(['p', 'h2', 'h3', 'h4', 'li', 'blockquote']):
                text = tag.get_text(strip=True)
                if not text or len(text) < 15:
                    continue

                # Filtrar lixo comum de metadados
                text_lower = text.lower()
                skip_patterns = [
                    'minutos de leitura', 'nenhum comentário', 'atualizado em:',
                    'compartilhe', 'whatsapp', 'telegram', 'facebook', 'twitter',
                    'leia também', 'leia mais', 'veja também', 'tags:',
                    'foto:', 'crédito:', 'reprodução', 'continue lendo',
                    'inscreva-se', 'newsletter', 'assine', 'publicidade',
                    'acompanhe as principais', 'notícias do setor'
                ]
                if any(pattern in text_lower for pattern in skip_patterns):
                    continue

                # Prefixar headers para contexto
                if tag.name in ('h2', 'h3', 'h4'):
                    text = f"\n{text}\n"

                paragraphs.append(text)

            # Deduplicar mantendo ordem
            seen = set()
            unique = []
            for p in paragraphs:
                normalized = p.strip().lower()[:80]
                if normalized not in seen:
                    seen.add(normalized)
                    unique.append(p)

            content = '\n\n'.join(unique)

            # Se a extração por tags falhou, fallback com separator
            if len(content) < 200 and element:
                content = element.get_text(separator='\n')
                # Limpar linhas curtas/lixo
                lines = [l.strip() for l in content.split('\n') if len(l.strip()) > 30]
                content = '\n\n'.join(lines)

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

    def get_feedback_examples(self):
        """Busca exemplos de feedback humano para calibrar a IA.
        Retorna dict com artigos bem avaliados e mal avaliados."""
        try:
            # Buscar artigos com human_score alto (8-10) — editor gostou
            good_resp = self.supabase.table('news_articles') \
                .select('title,category_id,human_score,human_feedback') \
                .gte('human_score', 8) \
                .order('feedback_at', desc=True) \
                .limit(10) \
                .execute()

            # Buscar artigos com human_score baixo (1-4) — editor rejeitou
            bad_resp = self.supabase.table('news_articles') \
                .select('title,category_id,human_score,human_feedback') \
                .lte('human_score', 4) \
                .gt('human_score', 0) \
                .order('feedback_at', desc=True) \
                .limit(10) \
                .execute()

            # Buscar artigos com feedback textual
            fb_good = self.supabase.table('news_articles') \
                .select('title,human_feedback,human_score') \
                .eq('human_feedback', 'bom') \
                .order('feedback_at', desc=True) \
                .limit(10) \
                .execute()

            fb_bad = self.supabase.table('news_articles') \
                .select('title,human_feedback,human_score') \
                .eq('human_feedback', 'ruim') \
                .order('feedback_at', desc=True) \
                .limit(10) \
                .execute()

            # Combinar: score alto OU feedback "bom"
            good_titles = set()
            good_articles = []
            for a in (good_resp.data or []) + (fb_good.data or []):
                t = a.get('title', '')
                if t and t not in good_titles:
                    good_titles.add(t)
                    good_articles.append(a)

            # Combinar: score baixo OU feedback "ruim"
            bad_titles = set()
            bad_articles = []
            for a in (bad_resp.data or []) + (fb_bad.data or []):
                t = a.get('title', '')
                if t and t not in bad_titles:
                    bad_titles.add(t)
                    bad_articles.append(a)

            return {
                'good': good_articles[:8],
                'bad': bad_articles[:8],
                'total_feedback': len(good_articles) + len(bad_articles)
            }

        except Exception as e:
            logger.warning(f"⚠️ Erro ao buscar feedback: {e}")
            return {'good': [], 'bad': [], 'total_feedback': 0}

    def build_feedback_prompt_section(self, feedback):
        """Constrói a seção do prompt com exemplos de feedback humano."""
        if feedback['total_feedback'] == 0:
            return ""

        lines = ["\n--- PREFERÊNCIAS DO EDITOR (use para calibrar o relevance_score) ---"]

        if feedback['good']:
            lines.append("Artigos que o editor APROVOU (score alto, dê preferência a artigos similares):")
            for a in feedback['good']:
                score_info = f" (score editor: {a['human_score']})" if a.get('human_score') else ""
                lines.append(f"  ✓ {a['title']}{score_info}")

        if feedback['bad']:
            lines.append("Artigos que o editor REJEITOU (score baixo, evite artigos similares):")
            for a in feedback['bad']:
                score_info = f" (score editor: {a['human_score']})" if a.get('human_score') else ""
                lines.append(f"  ✗ {a['title']}{score_info}")

        lines.append("Use essas preferências para ajustar o relevance_score. Artigos parecidos com os aprovados devem ter score mais alto. Artigos parecidos com os rejeitados devem ter score mais baixo.")
        lines.append("---")

        return "\n".join(lines)

    def analyze_with_ai(self, article):
        """Usa IA para analisar e categorizar o artigo, calibrado pelo feedback humano"""
        if not self.openai:
            logger.warning("⚠️ OpenAI não configurada, usando análise básica")
            return self.basic_analysis(article)

        try:
            # Buscar feedback humano para calibrar (cache por execução)
            if not hasattr(self, '_feedback_cache'):
                self._feedback_cache = self.get_feedback_examples()
                if self._feedback_cache['total_feedback'] > 0:
                    logger.info(f"📊 Calibrando IA com {self._feedback_cache['total_feedback']} exemplos de feedback humano ({len(self._feedback_cache['good'])} aprovados, {len(self._feedback_cache['bad'])} rejeitados)")

            feedback_section = self.build_feedback_prompt_section(self._feedback_cache)

            prompt = f"""
            Você é um especialista em gestão comercial farmacêutica. Analise este artigo e forneça insights estratégicos para gestores de farmácias.

            Título: {article['title']}
            Conteúdo: {article['content'][:2000]}
            {feedback_section}

            Responda APENAS em JSON válido com análise completa:
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

    def calculate_priority(self, relevance_score):
        """Calcula prioridade baseada no score de relevância"""
        if relevance_score >= 8:
            return 2  # Slot principal
        if relevance_score >= 5:
            return 1  # Slots premium
        return 0      # Outros

    def save_article(self, article, analysis):
        """Salva artigo no banco de dados com auto-publish"""
        try:
            # Verificar se já existe
            existing = self.supabase.table('news_articles').select('id').eq('url', article['url']).execute()
            if existing.data:
                logger.info(f"📄 Artigo já existe: {article['title']}")
                return False

            # Buscar categoria
            category = self.supabase.table('news_categories').select('id').eq('slug', analysis['category']).execute()
            category_id = category.data[0]['id'] if category.data else None

            relevance_score = analysis.get('relevance_score', 5)

            # Sanitizar textos (corrigir palavras coladas do scraping)
            clean_title = sanitize_text(article['title'])
            clean_content = sanitize_text(article['content'])
            clean_excerpt = sanitize_text(analysis['summary'])

            # Preparar dados — auto-publish: já entra como aprovado e publicado
            article_data = {
                'title': clean_title,
                'slug': self.generate_slug(clean_title),
                'excerpt': clean_excerpt,
                'content': clean_content,
                'url': article['url'],
                'source_id': article['source_id'],
                'category_id': category_id,
                'status': 'approved',
                'is_published': True,
                'priority': self.calculate_priority(relevance_score),
                'relevance_score': relevance_score,
                'published_at': article['published_at'],
                'scraped_at': datetime.now().isoformat()
            }

            # Adicionar análise comercial se disponível
            if 'commercial_analysis' in analysis:
                article_data['commercial_analysis'] = json.dumps(analysis['commercial_analysis'])

            if 'executive_summary' in analysis:
                article_data['executive_summary'] = sanitize_text(analysis['executive_summary'])

            # Inserir artigo
            result = self.supabase.table('news_articles').insert(article_data).execute()

            if result.data:
                article_id = result.data[0]['id']
                logger.info(f"✅ Artigo salvo e publicado: {article['title']} (ID: {article_id}, score: {relevance_score})")

                # Salvar tags
                self.save_article_tags(article_id, analysis['tags'])

                return True
            else:
                logger.error(f"❌ Erro ao salvar artigo: {article['title']}")
                return False

        except Exception as e:
            logger.error(f"❌ Erro ao salvar artigo: {e}")
            return False

    def get_feedback_weights(self):
        """Busca pesos de feedback da tabela news_settings (cache por execução)."""
        if hasattr(self, '_weights_cache'):
            return self._weights_cache
        try:
            resp = self.supabase.table('news_settings').select('key,value') \
                .execute()
            settings = {s['key']: s['value'] for s in (resp.data or [])}
            self._weights_cache = {
                'admin': float(settings.get('weight_admin', '0.5')),
                'user': float(settings.get('weight_user', '0.5'))
            }
        except Exception:
            self._weights_cache = {'admin': 0.5, 'user': 0.5}
        return self._weights_cache

    def get_effective_score(self, article):
        """Retorna score combinado usando pesos configuráveis:
        - Score do editor (human_score) ou da IA (relevance_score) → peso admin
        - Rating dos leitores (user_avg_rating, escala 1-5 → 0-10) → peso user
        Quando só existe uma fonte, usa ela com peso total."""
        weights = self.get_feedback_weights()
        w_admin = weights['admin']
        w_user = weights['user']

        # Score do admin/IA (escala 0-10)
        admin_score = None
        source = 'ai'
        human = article.get('human_score')
        ai = article.get('relevance_score')

        if human is not None:
            try:
                admin_score = float(human)
                source = 'human'
            except (ValueError, TypeError):
                pass

        if admin_score is None and ai is not None:
            try:
                admin_score = float(ai)
                source = 'ai'
            except (ValueError, TypeError):
                pass

        # Rating dos leitores (escala 1-5 → converter para 0-10)
        user_score = None
        user_avg = article.get('user_avg_rating')
        user_count = article.get('user_rating_count') or 0

        if user_avg is not None and user_count > 0:
            try:
                user_score = float(user_avg) * 2  # 1-5 → 2-10
            except (ValueError, TypeError):
                pass

        # Combinar scores com pesos
        if admin_score is not None and user_score is not None:
            total_weight = w_admin + w_user
            final = (admin_score * w_admin + user_score * w_user) / total_weight
            source = 'combined'
        elif admin_score is not None:
            final = admin_score
        elif user_score is not None:
            final = user_score
            source = 'user'
        else:
            final = 5.0
            source = 'default'

        return final, source

    def rotate_published_articles(self):
        """Mantém apenas os top 8 artigos publicados, despublicando os de menor score/mais antigos.
        human_score tem prioridade sobre relevance_score na ordenação.
        Retorna dict com stats da rotação."""
        stats = {'total_published': 0, 'pinned': 0, 'auto': 0, 'rotated_out': 0, 'published_titles': []}
        try:
            response = self.supabase.table('news_articles') \
                .select('id,title,relevance_score,human_score,human_feedback,user_avg_rating,user_rating_count,scraped_at,created_at,priority,manually_pinned') \
                .eq('is_published', True) \
                .execute()

            if not response.data:
                logger.info("📰 Nenhum artigo publicado encontrado")
                return stats

            articles = response.data
            pinned = [a for a in articles if a.get('manually_pinned')]
            unpinned = [a for a in articles if not a.get('manually_pinned')]

            available_slots = max(0, 8 - len(pinned))

            now = datetime.now()
            def sort_key(a):
                score, source = self.get_effective_score(a)
                # Bônus para artigos avaliados pelo editor (confiança maior)
                confidence_bonus = 0.5 if source == 'human' else 0
                # Penalidade para artigos marcados como "ruim"
                feedback_penalty = 3.0 if a.get('human_feedback') == 'ruim' else 0
                effective = score + confidence_bonus - feedback_penalty

                scraped = a.get('scraped_at') or a.get('created_at') or ''
                try:
                    clean = str(scraped).replace('Z', '').replace('+00:00', '').split('+')[0]
                    scraped_dt = datetime.fromisoformat(clean)
                except (ValueError, AttributeError):
                    scraped_dt = now - timedelta(days=30)
                age_days = (now - scraped_dt).days
                age_penalty = 0 if age_days <= 7 else age_days
                return (-effective, age_penalty, -scraped_dt.timestamp())

            unpinned.sort(key=sort_key)

            to_keep = unpinned[:available_slots]
            to_remove = unpinned[available_slots:]

            if to_remove:
                ids_to_remove = [a['id'] for a in to_remove]
                for aid in ids_to_remove:
                    self.supabase.table('news_articles') \
                        .update({'is_published': False}) \
                        .eq('id', aid).execute()
                logger.info(f"📤 Despublicados {len(ids_to_remove)} artigos (rotação automática)")

            all_published = pinned + to_keep
            all_published.sort(key=sort_key)

            for i, article in enumerate(all_published):
                if i == 0:
                    new_priority = 2
                elif i <= 3:
                    new_priority = 1
                else:
                    new_priority = 0
                if article.get('priority') != new_priority:
                    self.supabase.table('news_articles') \
                        .update({'priority': new_priority}) \
                        .eq('id', article['id']).execute()

            total_published = len(pinned) + len(to_keep)
            logger.info(f"📊 Rotação concluída: {total_published} artigos publicados ({len(pinned)} fixados, {len(to_keep)} automáticos)")

            # Stats com info de score source
            stats['total_published'] = total_published
            stats['pinned'] = len(pinned)
            stats['auto'] = len(to_keep)
            stats['rotated_out'] = len(to_remove)
            stats['published_titles'] = []
            for a in all_published:
                score, source = self.get_effective_score(a)
                stats['published_titles'].append({
                    'title': a.get('title', '')[:80],
                    'score': score,
                    'score_source': source,
                    'human_feedback': a.get('human_feedback'),
                    'priority': a.get('priority')
                })

        except Exception as e:
            logger.error(f"❌ Erro na rotação de artigos: {e}")
        return stats

    def promote_pending_articles(self):
        """Analisa artigos pendentes recentes, dá score via IA e publica os melhores.
        Retorna dict com stats da promoção."""
        stats = {'analyzed_ia': 0, 'analyzed_basic': 0, 'scores': [], 'errors': 0}
        try:
            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            response = self.supabase.table('news_articles') \
                .select('id,title,content,excerpt,category_id,source_id,relevance_score,status') \
                .eq('status', 'pending') \
                .is_('relevance_score', 'null') \
                .gte('created_at', cutoff) \
                .order('created_at', desc=True) \
                .limit(20) \
                .execute()

            pending = response.data if response.data else []
            if not pending:
                logger.info("📰 Nenhum artigo pendente sem score nos últimos 7 dias")
            else:
                logger.info(f"📊 Analisando {len(pending)} artigos pendentes para dar score...")

                for article in pending:
                    try:
                        fake_article = {
                            'title': article['title'],
                            'content': article.get('content') or article.get('excerpt') or '',
                            'excerpt': article.get('excerpt') or '',
                            'url': ''
                        }
                        analysis = self.analyze_with_ai(fake_article)
                        score = analysis.get('relevance_score', 5)
                        priority = self.calculate_priority(score)

                        update_data = {
                            'relevance_score': score,
                            'priority': priority,
                            'status': 'approved',
                            'is_published': True
                        }

                        if 'commercial_analysis' in analysis:
                            update_data['commercial_analysis'] = json.dumps(analysis['commercial_analysis'])
                        if 'executive_summary' in analysis:
                            update_data['executive_summary'] = analysis['executive_summary']

                        self.supabase.table('news_articles') \
                            .update(update_data) \
                            .eq('id', article['id']).execute()

                        stats['analyzed_ia'] += 1
                        stats['scores'].append({'title': article['title'][:60], 'score': score})
                        logger.info(f"  ✅ Score {score} → {article['title'][:60]}...")
                        time.sleep(1)

                    except Exception as e:
                        stats['errors'] += 1
                        logger.warning(f"  ⚠️ Erro ao analisar artigo {article['id']}: {e}")
                        continue

            # Backlog mais antigo — score básico
            response2 = self.supabase.table('news_articles') \
                .select('id,title,content,excerpt') \
                .eq('status', 'pending') \
                .is_('relevance_score', 'null') \
                .lt('created_at', cutoff) \
                .limit(50) \
                .execute()

            old_pending = response2.data if response2.data else []
            if old_pending:
                logger.info(f"📦 Dando score básico para {len(old_pending)} artigos antigos (sem IA)...")
                for article in old_pending:
                    basic = self.basic_analysis({
                        'title': article['title'],
                        'content': article.get('content') or '',
                        'excerpt': article.get('excerpt') or ''
                    })
                    self.supabase.table('news_articles') \
                        .update({
                            'relevance_score': basic['relevance_score'],
                            'priority': self.calculate_priority(basic['relevance_score']),
                            'status': 'approved'
                        }) \
                        .eq('id', article['id']).execute()
                    stats['analyzed_basic'] += 1

            logger.info("✅ Promoção de artigos pendentes concluída")

        except Exception as e:
            logger.error(f"❌ Erro na promoção de artigos: {e}")
        return stats

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
            # Tentar ISO direto
            try:
                cleaned = date_str.replace('Z', '+00:00')
                return datetime.fromisoformat(cleaned).isoformat()
            except ValueError:
                pass

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

        except Exception:
            pass

        return datetime.now().isoformat()

    def log_run_start(self):
        """Registra início de uma execução na tabela automation_runs"""
        try:
            result = self.supabase.table('automation_runs').insert({
                'run_type': 'full',
                'started_at': datetime.now().isoformat(),
                'status': 'running',
                'details': json.dumps({})
            }).execute()
            if result.data:
                return result.data[0]['id']
        except Exception as e:
            logger.warning(f"⚠️ Erro ao registrar início da execução: {e}")
        return None

    def log_run_end(self, run_id, status, stats):
        """Registra fim de uma execução na tabela automation_runs"""
        if not run_id:
            return
        try:
            all_scores = []
            for s in stats.get('promotion', {}).get('scores', []):
                all_scores.append(s.get('score', 0))
            avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else None

            self.supabase.table('automation_runs').update({
                'finished_at': datetime.now().isoformat(),
                'status': status,
                'sources_processed': stats.get('sources_processed', 0),
                'articles_collected': stats.get('articles_collected', 0),
                'articles_promoted': stats.get('promotion', {}).get('analyzed_ia', 0) + stats.get('promotion', {}).get('analyzed_basic', 0),
                'articles_rotated_out': stats.get('rotation', {}).get('rotated_out', 0),
                'total_published': stats.get('rotation', {}).get('total_published', 0),
                'avg_score': avg,
                'details': json.dumps(stats, ensure_ascii=False, default=str),
                'error_message': stats.get('error')
            }).eq('id', run_id).execute()
        except Exception as e:
            logger.warning(f"⚠️ Erro ao registrar fim da execução: {e}")

    def run_collection(self):
        """Executa a coleta completa com registro de automação"""
        logger.info("🚀 Iniciando coleta de notícias...")

        # Registrar início da execução
        run_id = self.log_run_start()
        run_stats = {'sources_processed': 0, 'articles_collected': 0, 'collected_titles': []}

        try:
            sources = self.get_active_sources()
            if not sources:
                logger.warning("⚠️ Nenhuma fonte ativa encontrada")
                self.log_run_end(run_id, 'success', run_stats)
                return

            total_collected = 0

            for source in sources:
                try:
                    logger.info(f"📡 Processando fonte: {source['name']}")
                    run_stats['sources_processed'] += 1

                    articles = self.fetch_rss_articles(source)

                    if ('guiadafarmacia.com.br' in source.get('url', '') and not articles):
                        articles.extend(self.fetch_guia_da_farmacia_articles(source))

                    unique_articles = []
                    seen_urls = set()
                    for article in articles:
                        url = article.get('url')
                        if not url or url in seen_urls:
                            continue
                        seen_urls.add(url)
                        unique_articles.append(article)
                    articles = unique_articles

                    category_hint = self.category_overrides.get(source['url'])

                    for article in articles[:5]:
                        try:
                            article['content'] = self.scrape_article_content(article['url'])

                            if len(article['content']) < self.min_content_length:
                                continue

                            article['excerpt'] = article['content'][:400]

                            if 'guiadafarmacia.com.br' in article['url']:
                                temp_article = {
                                    'title': article['title'],
                                    'excerpt': article['content']
                                }
                                if not self.is_relevant_article(temp_article):
                                    continue

                            analysis = self.analyze_with_ai(article)

                            if category_hint and isinstance(analysis, dict):
                                analysis['category'] = category_hint

                            if self.save_article(article, analysis):
                                total_collected += 1
                                run_stats['collected_titles'].append({
                                    'title': article['title'][:80],
                                    'source': source['name'],
                                    'score': analysis.get('relevance_score', 0)
                                })

                            if total_collected >= self.max_articles_per_run:
                                break

                            time.sleep(2)

                        except Exception as e:
                            logger.warning(f"⚠️ Erro ao processar artigo: {e}")
                            continue

                    self.supabase.table('news_sources').update({
                        'last_scraped': datetime.now().isoformat()
                    }).eq('id', source['id']).execute()

                except Exception as e:
                    logger.error(f"❌ Erro ao processar fonte {source['name']}: {e}")
                    continue

            run_stats['articles_collected'] = total_collected
            logger.info(f"✅ Coleta concluída! {total_collected} artigos coletados")

            # Promover artigos pendentes (dar score e aprovar)
            logger.info("📊 Promovendo artigos pendentes...")
            promotion_stats = self.promote_pending_articles()
            run_stats['promotion'] = promotion_stats

            # Executar rotação para manter apenas os top 8 publicados
            logger.info("🔄 Executando rotação de artigos publicados...")
            rotation_stats = self.rotate_published_articles()
            run_stats['rotation'] = rotation_stats

            # Registrar sucesso
            self.log_run_end(run_id, 'success', run_stats)

        except Exception as e:
            logger.error(f"❌ Erro crítico na coleta: {e}")
            run_stats['error'] = str(e)
            self.log_run_end(run_id, 'error', run_stats)

def main():
    """Função principal"""
    collector = NewsCollector()
    collector.run_collection()

if __name__ == "__main__":
    main()
