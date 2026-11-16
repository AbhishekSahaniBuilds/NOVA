import uvicorn
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title="NOVA API",
    description="Backend API for Neural Omni Vector Assistant",
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
