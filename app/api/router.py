from fastapi import APIRouter
from app.api.routes import media, news

router = APIRouter(prefix="/api/v1")

router.include_router(media.router, prefix="/media", tags=["Media"])
router.include_router(news.router, prefix="/news", tags=["News"])
