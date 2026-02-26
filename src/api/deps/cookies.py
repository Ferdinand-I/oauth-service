from starlette.responses import Response

from core.constants import (
    STATE_COOKIE_NAME,
    STATE_COOKIE_MAX_AGE,
    ACCESS_TOKEN_COOKIE_MAX_AGE,
)
from core.settings import settings


def set_state_cookie(response: Response, state: str) -> None:
    """Set OAuth state cookie for CSRF protection."""

    response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=state,
        httponly=True,
        secure=settings.security.cookie_secure,
        samesite="lax",  # lax needed for OAuth redirect
        max_age=STATE_COOKIE_MAX_AGE,
    )


def set_access_token_cookie(
    response: Response, token: str, cookie_name: str, path: str = "/"
) -> None:
    """Set access token cookie for authenticated requests."""

    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        path=path,
        secure=settings.security.cookie_secure,
        samesite=settings.security.cookie_samesite,
        max_age=ACCESS_TOKEN_COOKIE_MAX_AGE,
    )


def delete_state_cookie(response: Response) -> None:
    """Delete OAuth state cookie after successful authentication."""

    response.delete_cookie(STATE_COOKIE_NAME)
