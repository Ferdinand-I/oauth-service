from contextlib import asynccontextmanager
from http import HTTPMethod
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from api.router import router as api_router
from core.settings import settings, ROOT_DIR
from core.templates import templates
from integrations.google.client import GoogleClient
from integrations.yandex.client import YandexClient


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator[None, None]:
    app_.state.google_client = GoogleClient()  # noqa
    app_.state.yandex_client = YandexClient()  # noqa
    yield
    await app_.state.google_client.shutdown()  # noqa
    await app_.state.yandex_client.shutdown()  # noqa


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=ROOT_DIR / "src/static"), name="static")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.security.allowed_origins,
    allow_credentials=True,
    allow_methods=[HTTPMethod.GET, HTTPMethod.POST],
    allow_headers=["Content-Type", "Authorization"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next) -> Response:
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), fullscreen=()"

    return response


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


def main() -> None:
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.server.reload,
    )


if __name__ == "__main__":
    main()
