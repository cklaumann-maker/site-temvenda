import io
import json
import time
from typing import Optional

import httplib2
from google_auth_httplib2 import AuthorizedHttp
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from .config import get_settings


def _build_credentials():
    settings = get_settings()

    if settings.google_service_account_json:
        info = json.loads(settings.google_service_account_json)
        credentials = service_account.Credentials.from_service_account_info(
            info,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        return credentials

    if settings.google_application_credentials:
        credentials = service_account.Credentials.from_service_account_file(
            settings.google_application_credentials,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        return credentials

    raise RuntimeError("Credenciais de service account não configuradas")


def download_excel_from_drive(file_id: Optional[str] = None, max_retries: int = 3) -> bytes:
    """
    Faz download de um arquivo Excel do Google Drive e retorna os bytes.

    Suporta tanto arquivos binários (.xlsx) quanto planilhas Google Sheets,
    usando exportação para XLSX quando necessário.
    
    Args:
        file_id: ID do arquivo no Google Drive (opcional, usa DRIVE_FILE_ID se não fornecido)
        max_retries: Número máximo de tentativas em caso de timeout (padrão: 3)
    """
    settings = get_settings()
    target_file_id = file_id or settings.drive_file_id
    if not target_file_id:
        raise RuntimeError("DRIVE_FILE_ID não configurado")

    # Configura httplib2 com timeout maior (300 segundos = 5 minutos)
    http_base = httplib2.Http(timeout=300)
    
    credentials = _build_credentials()
    # Usa AuthorizedHttp para combinar credenciais com http customizado
    authorized_http = AuthorizedHttp(credentials, http=http_base)
    service = build("drive", "v3", http=authorized_http)

    # Descobre o tipo do arquivo
    print(f"[download_excel_from_drive] Obtendo metadados do arquivo {target_file_id}...")
    metadata = (
        service.files()
        .get(fileId=target_file_id, fields="mimeType")
        .execute()
    )
    mime_type = metadata.get("mimeType", "")
    print(f"[download_excel_from_drive] Tipo MIME: {mime_type}")

    # Se for uma planilha Google, usar export para XLSX
    if mime_type == "application/vnd.google-apps.spreadsheet":
        print(f"[download_excel_from_drive] Exportando planilha Google para XLSX...")
        request = service.files().export_media(
            fileId=target_file_id,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        # Arquivo binário normal (xlsx, etc.)
        print(f"[download_excel_from_drive] Baixando arquivo binário...")
        request = service.files().get_media(fileId=target_file_id)
    
    # Tenta fazer o download com retry em caso de timeout
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[download_excel_from_drive] Tentativa {attempt}/{max_retries}...")
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            chunk_count = 0
            while not done:
                status, done = downloader.next_chunk()
                chunk_count += 1
                if status:
                    progress = int(status.progress() * 100)
                    print(f"[download_excel_from_drive] Progresso: {progress}% (chunk {chunk_count})")
                else:
                    print(f"[download_excel_from_drive] Chunk {chunk_count} baixado...")

            fh.seek(0)
            file_bytes = fh.read()
            print(f"[download_excel_from_drive] Download concluído! Tamanho: {len(file_bytes)} bytes")
            return file_bytes
            
        except (TimeoutError, OSError) as e:
            if attempt < max_retries:
                wait_time = attempt * 5  # Espera 5s, 10s, 15s...
                print(f"[download_excel_from_drive] ⚠️  Timeout na tentativa {attempt}/{max_retries}. Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
            else:
                print(f"[download_excel_from_drive] ❌ Erro após {max_retries} tentativas: {e}")
                raise RuntimeError(f"Erro ao baixar arquivo do Google Drive após {max_retries} tentativas: {e}") from e


