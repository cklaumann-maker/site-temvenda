#!/usr/bin/env python3
"""
Re-analyzes articles that have fallback/generic AI analysis.
Finds articles with basic_analysis() output and re-runs OpenAI analysis.
"""

import os
import sys
import json
import time
import logging
import argparse
import requests
from datetime import datetime

# ---------------------------------------------------------------------------
# Env loading (same pattern as news_collector.py)
# ---------------------------------------------------------------------------

def load_env_file():
    """Carrega variáveis de ambiente de um arquivo .env"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reanalyze.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://mgcoyeohqelystqmytah.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

RATE_LIMIT_SECONDS = 1.5

# ---------------------------------------------------------------------------
# Supabase REST helpers
# ---------------------------------------------------------------------------

def supabase_headers():
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }


def fetch_generic_articles(published_first: bool = False):
    """Fetch articles whose executive_summary matches the basic_analysis() pattern.
    Fetches in batches and filters in Python to avoid PostgREST URL encoding issues."""
    all_generic = []
    offset = 0
    batch = 200

    while True:
        url = f"{SUPABASE_URL}/rest/v1/news_articles"
        params = {
            'select': 'id,title,content,is_published,executive_summary',
            'order': 'id.asc',
            'offset': str(offset),
            'limit': str(batch),
        }

        resp = requests.get(url, headers=supabase_headers(), params=params, timeout=30)
        resp.raise_for_status()
        articles = resp.json()

        if not articles:
            break

        # Filter in Python: find articles with the generic fallback text
        for a in articles:
            summary = a.get('executive_summary', '') or ''
            if 'Recomenda-se' in summary and 'oportunidades de crescimento' in summary:
                all_generic.append(a)

        offset += batch
        logger.info(f'  Scanned {offset} articles, found {len(all_generic)} generic so far...')

    # Sort: published first if requested
    if published_first:
        all_generic.sort(key=lambda a: (not a.get('is_published', False), a.get('id', 0)))

    logger.info(f'Total generic articles found: {len(all_generic)}')
    return all_generic


def update_article(article_id: str, data: dict):
    """PATCH an article by id."""
    url = f"{SUPABASE_URL}/rest/v1/news_articles?id=eq.{article_id}"
    resp = requests.patch(url, headers=supabase_headers(), json=data, timeout=30)
    resp.raise_for_status()
    return resp.status_code < 400

# ---------------------------------------------------------------------------
# OpenAI analysis
# ---------------------------------------------------------------------------

ANALYSIS_PROMPT = """Você é um especialista em gestão comercial farmacêutica. Analise este artigo e forneça insights estratégicos para gestores de farmácias.

Título: {title}
Conteúdo: {content}

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
}}"""


def analyze_with_openai(title: str, content: str) -> dict | None:
    """Send article to OpenAI and return parsed JSON analysis."""
    truncated_content = (content or '')[:2000]
    prompt = ANALYSIS_PROMPT.format(title=title, content=truncated_content)

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
    }

    resp = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()

    raw = resp.json()['choices'][0]['message']['content'].strip()

    # Strip markdown code fences if present
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1] if '\n' in raw else raw[3:]
        if raw.endswith('```'):
            raw = raw[:-3]
        raw = raw.strip()

    return json.loads(raw)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Re-analyze articles with generic AI analysis')
    parser.add_argument('--dry-run', action='store_true', help='Only count articles, do not re-analyze')
    parser.add_argument('--limit', type=int, default=None, help='Max number of articles to process')
    parser.add_argument('--published-first', action='store_true', help='Prioritize published articles')
    args = parser.parse_args()

    # Validate env
    if not SUPABASE_KEY:
        logger.error('SUPABASE_KEY not set')
        sys.exit(1)
    if not args.dry_run and not OPENAI_API_KEY:
        logger.error('OPENAI_API_KEY not set (required unless --dry-run)')
        sys.exit(1)

    logger.info('Fetching articles with generic analysis...')
    articles = fetch_generic_articles(published_first=args.published_first)
    total = len(articles)
    logger.info(f'Found {total} articles with generic analysis')

    published_count = sum(1 for a in articles if a.get('is_published'))
    logger.info(f'  - Published: {published_count}')
    logger.info(f'  - Draft: {total - published_count}')

    if args.dry_run:
        logger.info('Dry-run mode: no changes will be made.')
        for i, art in enumerate(articles):
            pub = 'PUBLISHED' if art.get('is_published') else 'draft'
            logger.info(f'  [{i+1}] [{pub}] {art["title"][:80]}')
        return

    to_process = articles[:args.limit] if args.limit else articles
    logger.info(f'Will re-analyze {len(to_process)} articles')

    success = 0
    errors = 0

    for i, art in enumerate(to_process):
        pub = 'PUBLISHED' if art.get('is_published') else 'draft'
        logger.info(f'[{i+1}/{len(to_process)}] [{pub}] Analyzing: {art["title"][:80]}...')

        try:
            analysis = analyze_with_openai(art['title'], art.get('content', ''))
            if not analysis:
                logger.warning(f'  Empty analysis returned, skipping')
                errors += 1
                continue

            # Build update payload
            commercial = analysis.get('commercial_analysis', {})
            update_data = {
                'executive_summary': analysis.get('executive_summary', ''),
                'commercial_analysis': json.dumps(commercial, ensure_ascii=False) if isinstance(commercial, dict) else str(commercial),
                'relevance_score': analysis.get('relevance_score', 5),
            }

            update_article(art['id'], update_data)
            logger.info(f'  Updated successfully (relevance_score={update_data["relevance_score"]})')
            success += 1

        except json.JSONDecodeError as e:
            logger.error(f'  JSON parse error: {e}')
            errors += 1
        except requests.exceptions.RequestException as e:
            logger.error(f'  API error: {e}')
            errors += 1
        except Exception as e:
            logger.error(f'  Unexpected error: {e}')
            errors += 1

        # Rate limit between calls
        if i < len(to_process) - 1:
            time.sleep(RATE_LIMIT_SECONDS)

    logger.info(f'Done. Success: {success}, Errors: {errors}, Total: {len(to_process)}')


if __name__ == '__main__':
    main()
