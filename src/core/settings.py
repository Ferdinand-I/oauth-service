from pathlib import Path
from typing import Final
from urllib.parse import urlencode

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent


class BaseSettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env"),  # Only for out of container developing
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
        frozen=True,
    )


class GoogleOAauth2Config(BaseSettingsConfig):
    client_id: str
    client_secret: SecretStr
    redirect_uri: str = "http://127.0.0.1:8000/api/google/auth/callback"

    # Common
    google_auth_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_user_info_url: str = "https://www.googleapis.com/oauth2/v2/userinfo"

    scopes: list[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/calendar.readonly",
    ]

    def get_auth_url(self, state: str) -> str:
        """Generate OAuth URL with CSRF state parameter."""

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }

        return f"{self.google_auth_url}?{urlencode(params)}"


class YandexOAauth2Config(BaseSettingsConfig):
    client_id: str
    client_secret: SecretStr
    redirect_uri: str = "http://127.0.0.1:8000/api/yandex/auth/callback"

    # Common
    yandex_auth_url: str = "https://oauth.yandex.ru/authorize"
    yandex_token_url: str = "https://oauth.yandex.ru/token"

    def get_auth_url(self, state: str) -> str:
        """Generate OAuth URL with CSRF state parameter."""

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
        }

        return f"{self.yandex_auth_url}?{urlencode(params)}"


class GoogleConfig(BaseSettingsConfig):
    oauth: GoogleOAauth2Config


class YandexConfig(BaseSettingsConfig):
    oauth: YandexOAauth2Config


class SecurityConfig(BaseSettingsConfig):
    allowed_origins: list[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    cookie_secure: bool = False  # Set True in production with HTTPS
    cookie_samesite: str = "strict"


class ServerConfig(BaseSettingsConfig):
    reload: bool = False


class Settings(BaseSettingsConfig):
    server: ServerConfig
    google: GoogleConfig
    yandex: YandexConfig
    security: SecurityConfig = SecurityConfig()


settings = Settings()  # noqa
