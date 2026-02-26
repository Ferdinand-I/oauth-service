from fastapi import APIRouter

from api.routes.google import router as google_router
from api.routes.yandex import router as yandex_router

router = APIRouter(prefix="/api")
router.include_router(google_router, prefix="/google", tags=["Google"])
router.include_router(yandex_router, prefix="/yandex", tags=["Yandex"])
