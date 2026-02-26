from aiohttp import ClientResponseError

from core.settings import settings
from integrations.base_api_client import BaseAPIClient
from integrations.yandex.exceptions import YandexAPIError
from integrations.yandex.schemas import (
    YandexTokenRequestSchema,
    YandexTokenResponseSchema,
    YandexUserInfoSchema,
)


class YandexClient(BaseAPIClient):
    @staticmethod
    def _handle_error(e: ClientResponseError, context: str) -> None:
        """Handle API errors with sanitized messages."""

        if e.status == 401:
            raise YandexAPIError(401, "Authentication expired. Please login again.")
        elif e.status == 403:
            raise YandexAPIError(403, "Access denied. Check permissions.")
        elif e.status == 404:
            raise YandexAPIError(404, f"{context} not found.")
        elif e.status >= 500:
            raise YandexAPIError(502, "Yandex service temporarily unavailable.")
        else:
            raise YandexAPIError(400, f"Failed to {context.lower()}.")

    async def get_auth_tokens(self, code: str) -> YandexTokenResponseSchema:
        """Exchange authorization code for access token."""

        async with self.session.post(
            url=settings.yandex.oauth.yandex_token_url,
            data=YandexTokenRequestSchema(code=code).model_dump(),
        ) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self._handle_error(e, "Exchange authorization code")

            data = await response.json()

        return YandexTokenResponseSchema(**data)

    async def get_user_info(self, access_token: str) -> YandexUserInfoSchema:
        """Get user information from Yandex API."""

        headers = {"Authorization": f"Bearer {access_token}"}

        async with self.session.get(
            "https://login.yandex.ru/info",
            headers=headers,
        ) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self._handle_error(e, "User info")

            data = await response.json()

        return YandexUserInfoSchema(**data)
