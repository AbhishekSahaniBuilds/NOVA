import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import connect_to_mongodb, disconnect_from_mongodb
from app.services.ai.google_service import (
    connect_to_gemini,
    disconnect_to_gemini,
)
from app.services.ai.groq_service import (
    connect_to_groq,
    disconnect_to_groq,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.groq_client = None
    app.state.gemini_client = None
    app.state.mongodb_client = None
    app.state.mongodb_database = None

    try:
        try:
            mongodb_result = await connect_to_mongodb()

            if mongodb_result.get("success"):
                app.state.mongodb_client = mongodb_result.get("client")
                app.state.mongodb_database = mongodb_result.get("database")
                logger.info("MongoDB connected successfully.")
            else:
                logger.error(
                    "MongoDB connection failed: %s",
                    mongodb_result.get("error"),
                )
        except Exception:
            logger.exception("Unexpected error while connecting to MongoDB.")

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

        if settings.gemini_api_key:
            try:
                gemini_result = await connect_to_gemini()

                if gemini_result.get("success"):
                    app.state.gemini_client = gemini_result.get("client")
                    logger.info("Gemini connected successfully.")
                else:
                    logger.error(
                        "Gemini connection failed: %s",
                        gemini_result.get("error"),
                    )
            except Exception:
                logger.exception("Unexpected error while connecting to Gemini.")

        yield

    finally:
        if app.state.gemini_client is not None:
            try:
                await disconnect_to_gemini(app.state.gemini_client)
                logger.info("Gemini disconnected.")
            except Exception:
                logger.exception("Error while disconnecting Gemini.")

        if app.state.groq_client is not None:
            try:
                await disconnect_to_groq(app.state.groq_client)
                logger.info("Groq disconnected.")
            except Exception:
                logger.exception("Error while disconnecting Groq.")

        if app.state.mongodb_client is not None:
            try:
                await disconnect_from_mongodb(app.state.mongodb_client)
                logger.info("MongoDB disconnected.")
            except Exception:
                logger.exception("Error while disconnecting MongoDB.")
