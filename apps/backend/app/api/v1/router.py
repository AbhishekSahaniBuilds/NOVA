from fastapi import APIRouter

from app.api.v1.routes import chat, health, root

v1_api_router = APIRouter()

v1_api_router.include_router(root.router, tags=["Root"])
v1_api_router.include_router(health.router, prefix="/health", tags=["Health"])
v1_api_router.include_router(chat.router, prefix="chat", tags=["Chat"])
