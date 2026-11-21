import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings
from app.services.ai.google_service import (
    connect_to_gemini,
    disconnect_to_gemini,
)
from app.services.ai.groq_service import (
    connect_to_groq,
    disconnect_to_groq,
)

logger = logging.getLogger(__name__)


# ============================================================
# APPLICATION LIFESPAN
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.groq_client = None
    app.state.gemini_client = None

    # Start Groq.
    try:
        groq_result = await connect_to_groq()

        if groq_result.get("success"):
            app.state.groq_client = groq_result.get("client")
            logger.info("Groq connected successfully.")
        else:
            logger.error(
                "Groq connection failed: %s",
                groq_result.get("error"),
            )

    except Exception:
        logger.exception("Unexpected error while connecting to Groq.")

    # Gemini is optional and is not on the MainAI request path.
    if settings.gemini_api_key:
        try:
            gemini_result = await connect_to_gemini()

            if gemini_result.get("success"):
                app.state.gemini_client = gemini_result.get("client")
                logger.info("Gemini connected successfully.")
            else:
                logger.error("Gemini connection failed: %s", gemini_result.get("error"))

        except Exception:
            logger.exception("Unexpected error while connecting to Gemini.")

    yield

    # Shut down Gemini.
    if app.state.gemini_client is not None:
        try:
            await disconnect_to_gemini(app.state.gemini_client)
            logger.info("Gemini disconnected.")
        except Exception:
            logger.exception("Error while disconnecting Gemini.")

    # Shut down Groq.
    if app.state.groq_client is not None:
        try:
            await disconnect_to_groq(app.state.groq_client)
            logger.info("Groq disconnected.")
        except Exception:
            logger.exception("Error while disconnecting Groq.")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="NOVA API",
    description="Neural Omni Vector Assistant",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)


# ============================================================
# CORS MIDDLEWARE
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTER
# ============================================================

app.include_router(
    router.api_router,
    prefix="/api",
)


# ============================================================
# SERVER STARTUP
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
