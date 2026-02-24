import secrets
from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException, Cookie
from starlette.responses import RedirectResponse

from api.deps.auth import cookie_scheme
from api.deps.getters import get_google_client
from core.settings import settings
from integrations.google.client import GoogleClient
from integrations.google.schemas import CalendarListResponseSchema

router = APIRouter()

STATE_COOKIE_NAME = "oauth_state"


@router.get("/auth/login")
def login() -> RedirectResponse:
    state = secrets.token_urlsafe(32)
    auth_url = settings.google.oauth.get_auth_url(state)

    response = RedirectResponse(auth_url)
    response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=state,
        httponly=True,
        secure=settings.security.cookie_secure,
        samesite="lax",  # lax needed for OAuth redirect
        max_age=600,  # 10 minutes
    )

    return response


@router.get("/auth/callback")
async def callback(
    code: Annotated[str, Query(min_length=10, max_length=256)],
    state: Annotated[str, Query()],
    client: Annotated[GoogleClient, Depends(get_google_client)],
    oauth_state: Annotated[str | None, Cookie()] = None,
) -> RedirectResponse:
    if not oauth_state or not secrets.compare_digest(oauth_state, state):
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    tokens = await client.get_tokens(code)

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        path="/api/google",
        secure=settings.security.cookie_secure,
        samesite=settings.security.cookie_samesite,
        max_age=3600,  # 1 hour
    )

    response.delete_cookie(STATE_COOKIE_NAME)

    return response


@router.get("/calendar/next-event")
async def get_next_event(
    access_token: Annotated[str, Depends(cookie_scheme)],
    client: Annotated[GoogleClient, Depends(get_google_client)],
) -> CalendarListResponseSchema:
    return await client.get_next_calendar_event(access_token)
