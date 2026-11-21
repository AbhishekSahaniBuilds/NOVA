import logging
from typing import Any

from pymongo import AsyncMongoClient

from app.core.config import settings


async def connect_to_mongodb() -> dict[str, Any]:
    if not settings.mongodb_uri:
        return {
            "provider": "mongodb",
            "success": False,
            "client": None,
            "database": None,
            "error": "MONGODB_URI is not configured.",
        }

    client = None

    try:
        client = AsyncMongoClient(settings.mongodb_uri)
        await client.admin.command("ping")

        database = client[settings.mongodb_database]

        return {
            "provider": "mongodb",
            "success": True,
            "client": client,
            "database": database,
        }

    except Exception:
        if client is not None:
            await client.close()

        return {
            "provider": "mongodb",
            "success": False,
            "client": None,
            "database": None,
            "error": "MongoDB connection failed.",
        }


async def disconnect_from_mongodb(
    client: AsyncMongoClient | None,
) -> None:
    if client is None:
        return

    await client.close()
