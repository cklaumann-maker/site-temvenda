#!/usr/bin/env python3
"""
🔄 Re-scrape de artigos existentes
Atualiza o conteúdo de artigos que foram coletados sem preservação de parágrafos.
Usa a mesma lógica melhorada do news_collector.py.
"""

import os
import sys
import requests
import time
import logging
from bs4 import BeautifulSoup
from datetime import datetime

# Carregar .env
def load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rescrape.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://mgcoyeohqelystqmytah.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

if not SUPABASE_KEY:
    print("❌ SUPABASE_KEY não configurada. Defina no .env ou variável de ambiente.")
    sys.exit(1)

HEADERS_SUPABASE = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

HEADERS_SCRAPE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def scrape_article_content(url):
    """Extrai conteúdo preservando parágrafos (mesma lógica do news_collector.py)"""
    try:
        response = requests.get(url, headers=HEADERS_SCRAPE, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remover scripts, estilos, nav, footer, sidebar, ads
        for tag in soup(["script", "style", "nav", "footer", "aside", "header",
                         "iframe", "noscript", "form"]):
            tag.decompose()

        # Remover elementos de UI/social
        for selector in ['.social-share', '.share-buttons', '.related-posts',
                         '.comments', '.sidebar', '.breadcrumb', '.post-meta',
                         '.article-meta', '.author-box', '.newsletter',
                         '.ad', '.advertisement', '.wp-block-image figcaption']:
            for el in soup.select(selector):
                el.decompose()

        # Encontrar conteúdo principal
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
                text_check = element.get_text(strip=True)
                if len(text_check) > 200:
                    break
                element = None

        if not element:
            body = soup.find('body')
            if body:
                element = body

        if not element:
            return None

        # Extrair parágrafos preservando estrutura
        paragraphs = []
        for tag in element.find_all(['p', 'h2', 'h3', 'h4', 'li', 'blockquote']):
            text = tag.get_text(strip=True)
            if not text or len(text) < 15:
                continue

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

            if tag.name in ('h2', 'h3', 'h4'):
                text = f"\n{text}\n"

            paragraphs.append(text)

        # Deduplicar
        seen = set()
        unique = []
        for p in paragraphs:
            normalized = p.strip().lower()[:80]
            if normalized not in seen:
                seen.add(normalized)
                unique.append(p)

        content = '\n\n'.join(unique)

        # Fallback
        if len(content) < 200 and element:
            content = element.get_text(separator='\n')
            lines = [l.strip() for l in content.split('\n') if len(l.strip()) > 30]
            content = '\n\n'.join(lines)

        if len(content) > 5000:
            content = content[:5000] + "..."

        return content if len(content) > 100 else None

    except Exception as e:
        logger.warning(f"⚠️ Erro ao scrape {url}: {e}")
        return None


def fetch_articles_needing_rescrape(offset=0, limit=100):
    """Busca artigos que têm URL mas conteúdo sem quebras de linha"""
    url = f"{SUPABASE_URL}/rest/v1/news_articles"
    params = {
        'select': 'id,title,url,content',
        'url': 'neq.null',
        'order': 'created_at.desc',
        'offset': str(offset),
        'limit': str(limit)
    }
    resp = requests.get(url, headers={
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
    }, params=params)

    if resp.status_code >= 400:
        logger.error(f"Erro ao buscar artigos: {resp.status_code} {resp.text}")
        return []

    articles = resp.json()
    # Filtrar: só artigos cujo content NÃO tem \n (conteúdo antigo sem parágrafos)
    needs_rescrape = []
    for a in articles:
        content = a.get('content', '') or ''
        if content and '\n' not in content and len(content) > 100:
            needs_rescrape.append(a)
    return needs_rescrape


def update_article_content(article_id, new_content):
    """Atualiza conteúdo no Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/news_articles?id=eq.{article_id}"
    resp = requests.patch(url, headers=HEADERS_SUPABASE, json={
        'content': new_content,
        'updated_at': datetime.utcnow().isoformat()
    })
    return resp.status_code < 400


def main():
    """Executa re-scrape em lotes"""
    logger.info("🔄 Iniciando re-scrape de artigos existentes...")

    # Modo: --dry-run para apenas contar, sem atualizar
    dry_run = '--dry-run' in sys.argv
    # Modo: --limit N para limitar quantidade
    max_articles = None
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        if idx + 1 < len(sys.argv):
            max_articles = int(sys.argv[idx + 1])

    total_checked = 0
    total_updated = 0
    total_failed = 0
    total_skipped = 0
    offset = 0
    batch_size = 100

    while True:
        articles = fetch_articles_needing_rescrape(offset, batch_size)
        if not articles:
            # Pode ter acabado os que precisam, mas verificar se há mais no banco
            # Buscar qualquer artigo neste offset para saber se acabou
            url = f"{SUPABASE_URL}/rest/v1/news_articles?select=id&url=neq.null&offset={offset}&limit=1"
            resp = requests.get(url, headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
            })
            remaining = resp.json() if resp.status_code < 400 else []
            if not remaining:
                break
            offset += batch_size
            continue

        for article in articles:
            if max_articles and total_updated >= max_articles:
                logger.info(f"🛑 Limite de {max_articles} artigos atingido.")
                break

            total_checked += 1
            article_url = article.get('url', '')
            title = article.get('title', 'Sem título')[:60]

            if not article_url:
                total_skipped += 1
                continue

            logger.info(f"[{total_checked}] Scraping: {title}...")

            if dry_run:
                logger.info(f"  [DRY-RUN] Seria re-scraped: {article_url}")
                total_updated += 1
                continue

            new_content = scrape_article_content(article_url)

            if new_content and '\n' in new_content:
                old_len = len(article.get('content', '') or '')
                new_len = len(new_content)

                # Só atualizar se o novo conteúdo é razoável (pelo menos 50% do original)
                if new_len >= old_len * 0.4:
                    if update_article_content(article['id'], new_content):
                        total_updated += 1
                        logger.info(f"  ✅ Atualizado ({old_len} → {new_len} chars, {new_content.count(chr(10))} parágrafos)")
                    else:
                        total_failed += 1
                        logger.error(f"  ❌ Erro ao salvar no banco")
                else:
                    total_skipped += 1
                    logger.warning(f"  ⚠️ Novo conteúdo muito menor ({new_len} vs {old_len}), pulando")
            else:
                total_failed += 1
                logger.warning(f"  ⚠️ Scrape falhou ou sem parágrafos")

            # Rate limiting - ser gentil com os sites
            time.sleep(1.5)

        if max_articles and total_updated >= max_articles:
            break

        offset += batch_size

    logger.info(f"""
{'='*50}
📊 RESULTADO DO RE-SCRAPE {'(DRY-RUN)' if dry_run else ''}
{'='*50}
  Artigos verificados: {total_checked}
  Atualizados:         {total_updated}
  Falhas:              {total_failed}
  Pulados:             {total_skipped}
{'='*50}
""")


if __name__ == '__main__':
    main()
