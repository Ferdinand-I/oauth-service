from typing import Literal

from pydantic import BaseModel

from core.settings import settings


class GoogleTokenRequestSchema(BaseModel):
    code: str
    client_id: str = settings.google.oauth.client_id
    client_secret: str = settings.google.oauth.client_secret.get_secret_value()
    redirect_uri: str = settings.google.oauth.redirect_uri
    grant_type: Literal["authorization_code"] = "authorization_code"


class GoogleTokenResponseSchema(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
    id_token: str
    refresh_token_expires_in: int


class UserInfoResponseSchema(BaseModel):
    id: str
    email: str


class CalendarEventResponseSchema(BaseModel):
    summary: str
    start: dict
    end: dict


class CalendarListResponseSchema(BaseModel):
    items: list[CalendarEventResponseSchema]
