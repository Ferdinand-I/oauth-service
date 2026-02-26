from fastapi import Request

from integrations.google.client import GoogleClient
from integrations.yandex.client import YandexClient


def get_google_client(request: Request) -> GoogleClient:
    return request.app.state.google_client


def get_yandex_client(request: Request) -> YandexClient:
    return request.app.state.yandex_client
