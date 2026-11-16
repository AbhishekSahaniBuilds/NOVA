from google import genai

from app.core.config import settings

client = None


async def connect_to_gemini():
    """Connect to Google Gemini API."""
    global client

    try:
        client = genai.Client(
            api_key=settings.gemini_api_key,
        ).aio

        return {
            "provider": "gemini",
            "success": True,
        }

    except Exception as error:
        client = None

        return {
            "provider": "gemini",
            "success": False,
            "error": str(error),
        }


async def disconnect_to_gemini():
    """Disconnect from Google Gemini API."""
    global client

    try:
        if client is not None:
            await client.aclose()
            client = None

        return {
            "provider": "gemini",
            "success": True,
        }

    except Exception as error:
        client = None

        return {
            "provider": "gemini",
            "success": False,
            "error": str(error),
        }


async def gemini_get_model_list():
    """Get available Gemini models."""

    if client is None:
        return {
            "provider": "gemini",
            "success": False,
            "error": "Gemini client is not initialized.",
        }

    try:
        models = await client.models.list()

        model_list = []

        async for model in models:
            if "generateContent" in (model.supported_actions or []):
                model_list.append(model.name.removeprefix("models/"))

        return {
            "provider": "gemini",
            "success": True,
            "models": model_list,
        }

    except Exception as error:
        return {
            "provider": "gemini",
            "success": False,
            "error": str(error),
        }
