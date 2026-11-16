import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.services.ai.google_service import (
    connect_to_gemini,
    disconnect_to_gemini,
)
from app.services.ai.groq_service import (
    connect_to_groq,
    disconnect_to_groq,
)

logger = logging.getLogger("uvicorn.error")


# ======================================================
# Lifespan
# ======================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        groq_status = await connect_to_groq()

        if groq_status["success"]:
            logger.info("Groq connected successfully.")
        else:
            logger.error("Groq connection failed: %s", groq_status.get("error"))

    except Exception:
        logger.exception("Groq startup failed")

    try:
        gemini_status = await connect_to_gemini()

        if gemini_status["success"]:
            logger.info("Gemini connected successfully.")
        else:
            logger.error("Gemini connection failed: %s", gemini_status.get("error"))

    except Exception:
        logger.exception("Gemini startup failed")

    try:
        yield

    finally:
        # Shutdown
        try:
            groq_result = await disconnect_to_groq()

            if groq_result["success"]:
                logger.info("Groq disconnected successfully.")
            else:
                logger.error("Groq disconnection failed: %s", groq_result.get("error"))

        except Exception:
            logger.exception("Groq shutdown failed")

        try:
            gemini_result = await disconnect_to_gemini()

            if gemini_result["success"]:
                logger.info("Gemini disconnected successfully.")
            else:
                logger.error(
                    "Gemini disconnection failed: %s", gemini_result.get("error")
                )

        except Exception:
            logger.exception("Gemini shutdown failed")


# ======================================================
# Main
# ======================================================

app = FastAPI(
    title="NOVA API",
    description="Backend API for Neural Omni Vector Assistant",
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
