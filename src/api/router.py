from fastapi import APIRouter

from api.routes.google import router as google_router

router = APIRouter(prefix="/api")
router.include_router(google_router, prefix="/google", tags=["Google"])
