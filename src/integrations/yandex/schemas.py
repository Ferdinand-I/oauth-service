from typing import Literal

from pydantic import BaseModel

from core.settings import settings


class YandexTokenRequestSchema(BaseModel):
    code: str
    client_id: str = settings.yandex.oauth.client_id
    client_secret: str = settings.yandex.oauth.client_secret.get_secret_value()
    grant_type: Literal["authorization_code"] = "authorization_code"


class YandexTokenResponseSchema(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str | None = None
