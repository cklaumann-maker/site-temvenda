#!/usr/bin/env python3
"""Reprocessa artigos existentes da SalesDay com a nova pipeline."""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from salesdaily_pipeline import (
    build_drive_service,
    build_supabase_client,
    load_env_values,
    load_local_env,
    process_pdf_file,
    utc_iso_now,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("reprocess_salesdaily")


def extract_file_id(url: str) -> Optional[str]:
    match = None
    if "/d/" in url:
        start = url.find("/d/") + 3
        end = url.find("/", start)
        if end == -1:
            end = len(url)
        match = url[start:end]
    return match


def reprocess_single_article(
    *,
    drive_service,
    openai_key: str,
    supabase_client,
    record: Dict,
) -> Optional[str]:
    file_id = extract_file_id(record.get("url", ""))
    if not file_id:
        return f"ID {record['id']}: URL inválida ({record.get('url')})"

    result = process_pdf_file(
        drive_service=drive_service,
        openai_key=openai_key,
        file_id=file_id,
        file_name=record.get("title", "SalesDay PDF"),
    )

    if not result:
        return f"ID {record['id']}: falha ao processar PDF no Drive."

    structured = result["structured"]
    html_content = result["html"]
    body_paragraphs = result["paragraphs"] or record.get("body_paragraphs")

    excerpt = " ".join(structured.get("summary", [])).strip() or record.get("excerpt")
    contexto = " ".join(structured.get("context", [])).strip() or record.get("executive_summary")
    insight = " ".join(structured.get("insight", [])).strip() or record.get("excerpt")

    payload = {
        "title": structured.get("title") or record.get("title"),
        "subtitle": structured.get("subtitle") or record.get("subtitle"),
        "kicker": structured.get("kicker") or record.get("kicker"),
        "author_name": structured.get("author", "SalesDay"),
        "content": html_content,
        "excerpt": excerpt,
        "executive_summary": contexto,
        "commercial_analysis": {"sales_opportunities": insight},
        "body_paragraphs": body_paragraphs,
        "updated_at": utc_iso_now(),
    }

    payload = {k: v for k, v in payload.items() if v is not None}
    supabase_client.table("news_articles").update(payload).eq("id", record["id"]).execute()
    return None


def main():
    load_local_env()
    supabase_url, supabase_key, openai_key, credentials_path, _ = load_env_values()

    supabase_client = build_supabase_client(supabase_url, supabase_key)
    drive_service = build_drive_service(credentials_path)

    response = supabase_client.table("news_articles").select(
        "id,title,slug,url,excerpt,executive_summary,kicker,subtitle,body_paragraphs"
    ).eq("source_id", 14).order("id").execute()

    articles: List[Dict] = response.data or []
    if not articles:
        logger.warning("⚠️ Nenhum artigo da fonte SalesDay encontrado.")
        return

    logger.info("🔁 Reprocessando %d artigos SalesDay...", len(articles))

    failures: List[str] = []
    for record in articles:
        logger.info("→ Processando ID %s: %s", record["id"], record.get("title"))
        error = reprocess_single_article(
            drive_service=drive_service,
            openai_key=openai_key,
            supabase_client=supabase_client,
            record=record,
        )
        if error:
            failures.append(error)
            logger.error(error)

    if failures:
        logger.warning("⚠️ Concluído com falhas em %d itens:", len(failures))
        for fail in failures:
            logger.warning("   %s", fail)
    else:
        logger.info("✅ Todos os artigos SalesDay foram reprocessados com sucesso!")


if __name__ == "__main__":
    main()

