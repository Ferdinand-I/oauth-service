from typing import Annotated

from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import RedirectResponse

from api.deps.auth import GoogleOAuthInitData, get_google_oauth_init_data, google_access_token_cookie_scheme
from api.deps.cookies import set_state_cookie, set_access_token_cookie, delete_state_cookie
from api.deps.getters import get_google_client
from api.deps.validators import validate_google_oauth_state
from core.constants import GOOGLE_ACCESS_TOKEN_COOKIE_NAME
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
    set_state_cookie(response, oauth_init_data.state)

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
    set_access_token_cookie(
        response,
        tokens.access_token,
        cookie_name=GOOGLE_ACCESS_TOKEN_COOKIE_NAME,
        path="/api/google",
    )
    delete_state_cookie(response)

    return response


@router.get("/calendar/next-event")
async def get_next_event(
    access_token: Annotated[str, Depends(google_access_token_cookie_scheme)],
    client: Annotated[GoogleClient, Depends(get_google_client)],
) -> CalendarListResponseSchema:
    return await client.get_next_calendar_event(access_token)
