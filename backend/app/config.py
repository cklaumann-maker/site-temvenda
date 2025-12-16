import os
from functools import lru_cache

from pydantic import BaseModel, AnyUrl


class Settings(BaseModel):
    app_name: str = "Tem Venda Finance API"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Auth
    app_password: str = os.getenv("APP_PASSWORD", "change-me")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_hours: int = int(os.getenv("JWT_ACCESS_EXPIRES_HOURS", "8"))

    # Supabase via HTTP (mesmo projeto do site-temvenda)
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_KEY", ""))

    # CORS
    # Lista de origens permitidas, separadas por vírgula.
    # Exemplo: http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000
    frontend_origins_raw: str = os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000",
    )

    @property
    def frontend_origins(self) -> list[str]:
        return [o.strip() for o in self.frontend_origins_raw.split(",") if o.strip()]

    # Google Drive / Service Account
    google_service_account_json: str | None = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    google_application_credentials: str | None = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    drive_file_id: str = os.getenv("DRIVE_FILE_ID", "")
    projection_file_id: str = os.getenv("GOOGLE_PROJECTION_FILE_ID", "")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


