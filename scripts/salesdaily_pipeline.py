"""
Funções utilitárias compartilhadas para processamento de materiais SalesDay.
"""

from __future__ import annotations

import json
import logging
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

# Dependências PDF (carregadas de forma segura)
try:
    import PyPDF2  # type: ignore
except ImportError:
    PyPDF2 = None  # type: ignore

try:
    import pdfplumber  # type: ignore
except ImportError:
    pdfplumber = None  # type: ignore
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from openai import OpenAI
from supabase import Client, create_client

logger = logging.getLogger("salesdaily_pipeline")


# -----------------------------------------------------------------------------
# Carregamento de ambiente
# -----------------------------------------------------------------------------
def load_local_env():
    """Carrega variáveis do arquivo .env na raiz do projeto, se existir."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    with env_path.open("r", encoding="utf-8") as handler:
        for line in handler:
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.strip().split("=", 1)
            if key and value and key not in os.environ:
                os.environ[key] = value


def load_env_values():
    """Valida e retorna os valores essenciais do ambiente."""
    supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
    supabase_key = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
        "Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6"
        "MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pft"
        "GhhU-BGKYv9TQ"
    )
    openai_key = os.getenv("OPENAI_API_KEY")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    folder_id = os.getenv("SALESDAILY_FOLDER_ID")

    if not openai_key:
        raise EnvironmentError("⚠️ OPENAI_API_KEY não definido.")
    if not credentials_path or not os.path.exists(credentials_path):
        raise EnvironmentError(
            f"⚠️ GOOGLE_APPLICATION_CREDENTIALS inválido: {credentials_path}"
        )
    if not folder_id:
        raise EnvironmentError("⚠️ SALESDAILY_FOLDER_ID não configurado.")

    return supabase_url, supabase_key, openai_key, credentials_path, folder_id


# -----------------------------------------------------------------------------
# Clientes externos
# -----------------------------------------------------------------------------
def build_supabase_client(url: str, key: str) -> Client:
    client = create_client(url, key)
    logger.info("✅ Conexão Supabase estabelecida.")
    return client


def build_drive_service(credentials_path: str):
    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    creds = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=scopes,
    )
    service = build("drive", "v3", credentials=creds)
    logger.info("✅ Autenticado no Google Drive (Service Account).")
    return service


def list_drive_pdfs(service, folder_id: str) -> List[Dict]:
    """Lista todos os PDFs da pasta (paginação simples)."""
    query = (
        "mimeType='application/pdf' and trashed=false "
        f"and '{folder_id}' in parents"
    )
    files: List[Dict] = []
    page_token = None

    while True:
        try:
            response = (
                service.files()
                .list(
                    q=query,
                    spaces="drive",
                    pageToken=page_token,
                    fields="nextPageToken, files(id,name,modifiedTime,size,webViewLink)",
                )
                .execute()
            )
        except HttpError as err:
            logger.error("❌ Falha ao listar PDFs: %s", err)
            break

        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    logger.info("📁 %d PDFs listados no Drive.", len(files))
    return files


# -----------------------------------------------------------------------------
# Utilidades de PDF
# -----------------------------------------------------------------------------
def download_pdf_to_temp(service, file_id: str) -> Optional[str]:
    """Baixa o PDF para um caminho temporário."""
    try:
        request = service.files().get_media(fileId=file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            downloader = MediaIoBaseDownload(tmp, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug("   %s: %.1f%%", file_id, status.progress() * 100)
        return tmp.name
    except HttpError as err:
        logger.error("❌ Erro ao baixar PDF %s: %s", file_id, err)
        return None


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrai texto usando PyPDF2 ou pdfplumber."""
    text_parts: List[str] = []

    # PyPDF2
    if PyPDF2:
        try:
            with open(pdf_path, "rb") as handle:
                reader = PyPDF2.PdfReader(handle)
                for page in reader.pages:
                    content = page.extract_text() or ""
                    if content:
                        text_parts.append(content)
            if text_parts:
                return "\n".join(text_parts)
        except Exception as err:
            logger.debug("PyPDF2 falhou (%s): %s", pdf_path, err)

    # pdfplumber
    if pdfplumber:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    content = page.extract_text() or ""
                    if content:
                        text_parts.append(content)
            if text_parts:
                return "\n".join(text_parts)
        except Exception as err:
            logger.debug("pdfplumber falhou (%s): %s", pdf_path, err)

    return ""


# -----------------------------------------------------------------------------
# Utilidades de texto / OpenAI
# -----------------------------------------------------------------------------
def sanitize_text_for_prompt(text: str, max_chars: int = 6500) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) > max_chars:
        clean = clean[:max_chars]
    return clean


def extract_json_from_response(content: str) -> Dict:
    pattern = re.compile(r"\{.*\}", re.DOTALL)
    match = pattern.search(content)
    if not match:
        raise ValueError("Resposta da OpenAI não contém JSON reconhecível.")
    return json.loads(match.group(0))


def translate_with_openai(openai_key: str, material_text: str, file_name: str) -> Dict:
    client = OpenAI(api_key=openai_key)

    system_prompt = (
        "Você é um editor especializado em transformar conteúdo da SalesDay em "
        "artigos jornalísticos concisos para o varejo farmacêutico. Traduza tudo "
        "para português do Brasil, mantendo tom profissional, clareza e foco em "
        "ações práticas."
    )

    user_prompt = f"""
    Materiais SalesDay fornecidos em inglês.

    Nome do arquivo: {file_name}

    Conteúdo (trecho consolidado):
    \"\"\"{material_text}\"\"\"

    Produza APENAS um JSON com a estrutura:
    {{
      "kicker": "Seção ou categoria (máx 50 caracteres)",
      "title": "Título em PT-BR (máx 120 caracteres, sem ponto final)",
      "subtitle": "Linha de apoio em PT-BR (máx 200 caracteres)",
      "author": "SalesDay",
      "summary": ["parágrafo 1", "parágrafo 2"],
      "context": ["parágrafo contextual"],
      "insight": ["parágrafo com insight acionável"],
      "callouts": [
        {{"label": "Evite", "text": "texto"}},
        {{"label": "Prefira", "text": "texto"}},
        {{"label": "Aplicação prática", "text": "texto"}}
      ],
      "body": [
        {{
          "heading": "Subtítulo opcional",
          "paragraphs": ["parágrafo 1", "parágrafo 2"]
        }}
      ]
    }}

    Regras:
    - Retorne apenas JSON válido.
    - Strings vazias quando não houver conteúdo.
    - Use parágrafos com frases completas, sem bullets.
    - Se não houver callouts específicos, elabore dicas coerentes.
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_SALESDAY_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1800,
    )

    raw_content = response.choices[0].message.content
    logger.debug("OpenAI response raw: %s", raw_content)
    return extract_json_from_response(raw_content)


def build_article_html(article: Dict) -> str:
    def paragraphs(items: Iterable[str]) -> str:
        return "".join(f"<p>{p.strip()}</p>" for p in items if p and p.strip())

    header = ""
    if article.get("kicker"):
        header += f"<p class='kicker'>{article['kicker'].strip()}</p>"
    if article.get("title"):
        header += f"<h1>{article['title'].strip()}</h1>"
    if article.get("subtitle"):
        header += f"<p class='subtitle'>{article['subtitle'].strip()}</p>"
    header += "<p class='byline'>por SalesDay</p>"

    def section(title: str, content: Iterable[str]) -> str:
        body = paragraphs(content)
        if not body:
            return ""
        return f"<section class='box {title.lower()}'><h2>{title}</h2>{body}</section>"

    callouts_html = ""
    callouts = article.get("callouts") or []
    if callouts:
        cards = []
        for callout in callouts:
            label = (callout.get("label") or "").strip()
            text = (callout.get("text") or "").strip()
            if text:
                cards.append(
                    f"<div class='callout'><strong>{label}:</strong> {text}</div>"
                )
        if cards:
            callouts_html = "<section class='callouts'>" + "".join(cards) + "</section>"

    body_sections: List[str] = []
    for section_data in article.get("body", []):
        heading = (section_data.get("heading") or "").strip()
        content = paragraphs(section_data.get("paragraphs", []))
        if not content:
            continue
        if heading:
            body_sections.append(f"<h2>{heading}</h2>{content}")
        else:
            body_sections.append(content)

    article_html = f"""
<article class="salesday-article">
  <header class="article-header">
    {header}
  </header>
  {section("Resumo", article.get("summary", []))}
  {section("Contexto", article.get("context", []))}
  {section("Insight Prático", article.get("insight", []))}
  {callouts_html}
  <section class="article-body">
    {''.join(body_sections)}
  </section>
</article>
""".strip()

    return article_html


def flatten_body_paragraphs(article: Dict) -> List[str]:
    paragraphs: List[str] = []
    for section in article.get("body", []):
        for paragraph in section.get("paragraphs", []):
            if paragraph and paragraph.strip():
                paragraphs.append(paragraph.strip())
    return paragraphs


# -----------------------------------------------------------------------------
# Pipeline principal (utilizado por scripts)
# -----------------------------------------------------------------------------
def process_pdf_file(
    *,
    drive_service,
    openai_key: str,
    file_id: str,
    file_name: str,
) -> Optional[Dict]:
    """Baixa, extrai texto e produz estrutura final (HTML + metadados)."""
    pdf_path = download_pdf_to_temp(drive_service, file_id)
    if not pdf_path:
        return None

    try:
        raw_text = extract_text_from_pdf(pdf_path)
    finally:
        try:
            os.remove(pdf_path)
        except OSError:
            pass

    if not raw_text or len(raw_text.strip()) < 200:
        logger.warning("⚠️ Texto muito curto em %s", file_name)
        return None

    sanitized = sanitize_text_for_prompt(raw_text)
    structured = translate_with_openai(openai_key, sanitized, file_name)
    html = build_article_html(structured)
    paragraphs = flatten_body_paragraphs(structured)

    return {
        "structured": structured,
        "html": html,
        "paragraphs": paragraphs,
        "raw_text": raw_text,
    }


def build_drive_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"


def generate_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")
    if len(slug) > 80:
        slug = slug[:80].rsplit("-", 1)[0]
    timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    return f"{slug}-{timestamp}"


def utc_iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


