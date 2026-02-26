import dataclasses
import secrets

from fastapi.security import APIKeyCookie

from core.constants import ACCESS_TOKEN_COOKIE_NAME, STATE_COOKIE_NAME
from core.settings import settings

access_token_cookie_scheme = APIKeyCookie(name=ACCESS_TOKEN_COOKIE_NAME)
state_cookie_scheme = APIKeyCookie(name=STATE_COOKIE_NAME)


@dataclasses.dataclass
class GoogleOAuthInitData:
    url: str
    state: str


def get_google_oauth_init_data() -> GoogleOAuthInitData:
    state = secrets.token_urlsafe(32)

    return GoogleOAuthInitData(
        url=settings.google.oauth.get_auth_url(state),
        state=state,
    )
