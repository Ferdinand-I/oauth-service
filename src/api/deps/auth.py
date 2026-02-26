import dataclasses
import secrets
from typing import TypeAlias

from fastapi.security import APIKeyCookie

from core.constants import (
    STATE_COOKIE_NAME,
    GOOGLE_ACCESS_TOKEN_COOKIE_NAME,
    YANDEX_ACCESS_TOKEN_COOKIE_NAME,
)
from core.settings import settings

google_access_token_cookie_scheme = APIKeyCookie(name=GOOGLE_ACCESS_TOKEN_COOKIE_NAME)
yandex_access_token_cookie_scheme = APIKeyCookie(name=YANDEX_ACCESS_TOKEN_COOKIE_NAME)
state_cookie_scheme = APIKeyCookie(name=STATE_COOKIE_NAME)


@dataclasses.dataclass
class OAuthInitData:
    """OAuth initialization data with auth URL and CSRF state token."""

    url: str
    state: str


GoogleOAuthInitData: TypeAlias = OAuthInitData
YandexOAuthInitData: TypeAlias = OAuthInitData


def get_google_oauth_init_data() -> GoogleOAuthInitData:
    """Generate Google OAuth initialization data with CSRF protection."""

    state = secrets.token_urlsafe(32)

    return OAuthInitData(
        url=settings.google.oauth.get_auth_url(state),
        state=state,
    )


def get_yandex_oauth_init_data() -> YandexOAuthInitData:
    """Generate Yandex OAuth initialization data with CSRF protection."""

    state = secrets.token_urlsafe(32)

    return OAuthInitData(
        url=settings.yandex.oauth.get_auth_url(state),
        state=state,
    )
