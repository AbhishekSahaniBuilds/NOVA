from fastapi import APIRouter

from app.api.routes import health, root

api_router = APIRouter()

api_router.include_router(root.router, tags=["Root"])
api_router.include_router(health.router, tags=["Health"])
