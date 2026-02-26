from typing import Annotated

from fastapi import APIRouter, Query, Depends, status
from starlette.responses import RedirectResponse

from api.deps.auth import YandexOAuthInitData, get_yandex_oauth_init_data
from api.deps.cookies import set_state_cookie, set_access_token_cookie, delete_state_cookie
from api.deps.getters import get_yandex_client
from api.deps.validators import validate_yandex_oauth_state
from integrations.yandex.client import YandexClient

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
    set_access_token_cookie(response, tokens.access_token, path="/api/yandex")
    delete_state_cookie(response)

    return response
