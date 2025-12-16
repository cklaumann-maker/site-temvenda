import io
import json
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseDownload as _MediaIoBaseDownload

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


def download_excel_from_drive(file_id: Optional[str] = None) -> bytes:
    """
    Faz download de um arquivo Excel do Google Drive e retorna os bytes.

    Suporta tanto arquivos binários (.xlsx) quanto planilhas Google Sheets,
    usando exportação para XLSX quando necessário.
    """
    settings = get_settings()
    target_file_id = file_id or settings.drive_file_id
    if not target_file_id:
        raise RuntimeError("DRIVE_FILE_ID não configurado")

    credentials = _build_credentials()
    service = build("drive", "v3", credentials=credentials)

    # Descobre o tipo do arquivo
    metadata = (
        service.files()
        .get(fileId=target_file_id, fields="mimeType")
        .execute()
    )
    mime_type = metadata.get("mimeType", "")

    # Se for uma planilha Google, usar export para XLSX
    if mime_type == "application/vnd.google-apps.spreadsheet":
        request = service.files().export_media(
            fileId=target_file_id,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        # Arquivo binário normal (xlsx, etc.)
        request = service.files().get_media(fileId=target_file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        # Não precisamos logar progresso aqui; apenas completar.

    fh.seek(0)
    return fh.read()


