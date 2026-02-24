from fastapi import Request

from integrations.google.client import GoogleClient


def get_google_client(request: Request) -> GoogleClient:
    return request.app.state.google_client
