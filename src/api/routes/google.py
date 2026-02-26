from typing import Annotated

from fastapi import APIRouter, Query, Depends, status
from starlette.responses import RedirectResponse

from api.deps.auth import GoogleOAuthInitData, get_google_oauth_init_data, access_token_cookie_scheme
from api.deps.getters import get_google_client
from api.deps.validators import validate_google_oauth_state
from core.constants import STATE_COOKIE_NAME, ACCESS_TOKEN_COOKIE_NAME
from core.settings import settings
from integrations.google.client import GoogleClient
from integrations.google.schemas import CalendarListResponseSchema

router = APIRouter()


@router.get(
    "/auth/login",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description="Google OAuth2 login",
)
def login(
    oauth_init_data: Annotated[GoogleOAuthInitData, Depends(get_google_oauth_init_data)],
) -> RedirectResponse:
    response = RedirectResponse(oauth_init_data.url)

    response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=oauth_init_data.state,
        httponly=True,
        secure=settings.security.cookie_secure,
        samesite="lax",  # lax needed for OAuth redirect
        max_age=600,  # 10 minutes
    )

    return response


@router.get(
    "/auth/callback",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description="Google OAuth2 callback",
    dependencies=[Depends(validate_google_oauth_state)],
)
async def callback(
    code: Annotated[str, Query(min_length=1, max_length=512)],  # Authorization code from Google OAuth callback
    client: Annotated[GoogleClient, Depends(get_google_client)],
) -> RedirectResponse:
    tokens = await client.get_auth_tokens(code)

    response = RedirectResponse(url="/")
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
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
    access_token: Annotated[str, Depends(access_token_cookie_scheme)],
    client: Annotated[GoogleClient, Depends(get_google_client)],
) -> CalendarListResponseSchema:
    return await client.get_next_calendar_event(access_token)
