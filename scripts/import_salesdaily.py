#!/usr/bin/env python3
"""Importa novos PDFs da SalesDay e cria artigos no Supabase."""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from salesdaily_pipeline import (
    build_drive_service,
    build_drive_url,
    build_supabase_client,
    generate_slug,
    list_drive_pdfs,
    load_env_values,
    load_local_env,
    process_pdf_file,
    utc_iso_now,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("import_salesdaily")

SOURCE_ID = 14
DEFAULT_PRIORITY = 0


def get_existing_file_ids(articles: List[Dict]) -> Set[str]:
    file_ids: Set[str] = set()
    for article in articles:
        url = article.get("url") or ""
        match = None
        if "/d/" in url:
            start = url.find("/d/") + 3
            end = url.find("/", start)
            if end == -1:
                end = len(url)
            match = url[start:end]
        if match:
            file_ids.add(match)
    return file_ids


def resolve_category_id(supabase_client, fallback_articles: List[Dict]) -> Optional[int]:
    for article in fallback_articles:
        category_id = article.get("category_id")
        if category_id:
            return category_id

    response = supabase_client.table("news_categories").select("id,name").eq("name", "Gestão").limit(1).execute()
    data = response.data or []
    if data:
        return data[0]["id"]
    return None


def main():
    load_local_env()
    supabase_url, supabase_key, openai_key, credentials_path, folder_id = load_env_values()

    supabase_client = build_supabase_client(supabase_url, supabase_key)
    drive_service = build_drive_service(credentials_path)

    existing = supabase_client.table("news_articles").select(
        "id,title,url,category_id"
    ).eq("source_id", SOURCE_ID).execute().data or []

    existing_ids = get_existing_file_ids(existing)
    logger.info("🔍 Já temos %d artigos SalesDay cadastrados.", len(existing_ids))

    category_id = resolve_category_id(supabase_client, existing)
    if not category_id:
        logger.warning("⚠️ Nenhuma categoria padrão encontrada; artigos serão inseridos sem category_id.")

    drive_files = list_drive_pdfs(drive_service, folder_id)
    logger.info("📁 %d PDFs disponíveis no Drive.", len(drive_files))

    new_files = [f for f in drive_files if f["id"] not in existing_ids]
    if not new_files:
        logger.info("✅ Nenhum PDF novo para importar.")
        return

    logger.info("🆕 Encontrados %d PDFs ainda não importados.", len(new_files))

    successes = 0
    failures: List[str] = []

    for file_info in new_files:
        file_id = file_info["id"]
        file_name = file_info.get("name", "SalesDay PDF")
        logger.info("→ Processando PDF %s (%s)", file_name, file_id)

        result = process_pdf_file(
            drive_service=drive_service,
            openai_key=openai_key,
            file_id=file_id,
            file_name=file_name,
        )

        if not result:
            failures.append(f"{file_name}: falha na extração/tradução")
            continue

        structured = result["structured"]
        html_content = result["html"]
        body_paragraphs = result["paragraphs"]

        excerpt = " ".join(structured.get("summary", [])).strip()
        contexto = " ".join(structured.get("context", [])).strip()
        insight = " ".join(structured.get("insight", [])).strip()

        title = structured.get("title") or file_name.replace(".pdf", "")
        slug = generate_slug(title)

        payload = {
            "title": title,
            "slug": slug,
            "subtitle": structured.get("subtitle"),
            "kicker": structured.get("kicker"),
            "author_name": structured.get("author", "SalesDay"),
            "excerpt": excerpt,
            "executive_summary": contexto,
            "content": html_content,
            "body_paragraphs": body_paragraphs,
            "commercial_analysis": {"sales_opportunities": insight},
            "source_id": SOURCE_ID,
            "status": "pending",
            "priority": DEFAULT_PRIORITY,
            "url": build_drive_url(file_id),
            "published_at": utc_iso_now(),
            "scraped_at": utc_iso_now(),
        }

        if category_id:
            payload["category_id"] = category_id

        try:
            supabase_client.table("news_articles").insert(payload).execute()
            successes += 1
        except Exception as err:  # noqa: BLE001
            msg = f"{file_name}: erro ao inserir no Supabase - {err}"
            logger.exception(msg)
            failures.append(msg)

    logger.info("✅ %d artigos novos importados.", successes)
    if failures:
        logger.warning("⚠️ Falhas em %d arquivos:", len(failures))
        for fail in failures:
            logger.warning("   %s", fail)


if __name__ == "__main__":
    main()
