from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "application": "NOVA",
        "environment": settings.app_env,
    }
