from typing import Annotated

from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import RedirectResponse

from api.deps.auth import YandexOAuthInitData, get_yandex_oauth_init_data, yandex_access_token_cookie_scheme
from api.deps.cookies import set_state_cookie, set_access_token_cookie, delete_state_cookie
from api.deps.getters import get_yandex_client
from api.deps.validators import validate_yandex_oauth_state
from core.constants import YANDEX_ACCESS_TOKEN_COOKIE_NAME
from integrations.yandex.client import YandexClient
from integrations.yandex.schemas import YandexUserInfoSchema

router = APIRouter()


@router.get(
    "/auth/login",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description="Yandex OAuth2 login",
)
def login(
    oauth_init_data: Annotated[YandexOAuthInitData, Depends(get_yandex_oauth_init_data)],
) -> RedirectResponse:
    response = RedirectResponse(oauth_init_data.url)
    set_state_cookie(response, oauth_init_data.state)

    return response


@router.get(
    "/auth/callback",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description="Yandex OAuth2 callback",
    dependencies=[Depends(validate_yandex_oauth_state)],
)
async def callback(
    code: Annotated[str, Query(min_length=1, max_length=512)],  # Authorization code from Yandex OAuth callback
    client: Annotated[YandexClient, Depends(get_yandex_client)],
) -> RedirectResponse:
    tokens = await client.get_auth_tokens(code)

    response = RedirectResponse(url="/")
    set_access_token_cookie(
        response,
        tokens.access_token,
        cookie_name=YANDEX_ACCESS_TOKEN_COOKIE_NAME,
        path="/api/yandex",
    )
    delete_state_cookie(response)

    return response


@router.get("/user/info")
async def get_user_info(
    access_token: Annotated[str, Depends(yandex_access_token_cookie_scheme)],
    client: Annotated[YandexClient, Depends(get_yandex_client)],
) -> YandexUserInfoSchema:
    """Get Yandex user information."""

    return await client.get_user_info(access_token)
