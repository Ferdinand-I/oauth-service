from datetime import datetime, timezone
from typing import Self

from aiohttp import ClientResponseError

from core.settings import settings
from integrations.base_api_client import BaseAPIClient
from integrations.google.exceptions import GoogleAPIError
from integrations.google.schemas import (
    GoogleTokenRequestSchema,
    GoogleTokenResponseSchema,
    UserInfoResponseSchema,
    CalendarListResponseSchema,
)


class GoogleClient(BaseAPIClient):
    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @staticmethod
    def _handle_error(e: ClientResponseError, context: str) -> None:
        """Handle API errors with sanitized messages."""

        if e.status == 401:
            raise GoogleAPIError(401, "Authentication expired. Please login again.")
        elif e.status == 403:
            raise GoogleAPIError(403, "Access denied. Check permissions.")
        elif e.status == 404:
            raise GoogleAPIError(404, f"{context} not found.")
        elif e.status >= 500:
            raise GoogleAPIError(502, "Google service temporarily unavailable.")
        else:
            raise GoogleAPIError(400, f"Failed to {context.lower()}.")

    async def get_tokens(self, code: str) -> GoogleTokenResponseSchema:
        async with self.session.post(
            url=settings.google.oauth.google_token_url,
            data=GoogleTokenRequestSchema(code=code).model_dump(),
        ) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self._handle_error(e, "Exchange authorization code")

            data = await response.json()

        return GoogleTokenResponseSchema(**data)

    async def get_user_info(self, access_token: str) -> UserInfoResponseSchema:
        headers = {"Authorization": f"Bearer {access_token}"}

        async with self.session.get(
            url=settings.google.oauth.google_user_info_url,
            headers=headers,
        ) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self._handle_error(e, "User info")

            data = await response.json()

        return UserInfoResponseSchema(**data)

    async def get_next_calendar_event(self, access_token: str) -> CalendarListResponseSchema:
        now = datetime.now(timezone.utc).isoformat()

        params = {
            "maxResults": 1,
            "orderBy": "startTime",
            "singleEvents": "true",
            "timeMin": now,
        }

        headers = {"Authorization": f"Bearer {access_token}"}

        async with self.session.get(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            params=params,
            headers=headers,
        ) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self._handle_error(e, "Calendar events")

            data = await response.json()

        return CalendarListResponseSchema(**data)
