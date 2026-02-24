from typing import Self

import aiohttp


class BaseAPIClient:
    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()

        return self._session

    async def shutdown(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
