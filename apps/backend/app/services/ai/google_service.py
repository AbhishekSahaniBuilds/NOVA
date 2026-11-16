from google import genai

from app.core.config import settings

client = genai.Client(
    api_key=settings.gemini_api_key,
).aio


async def connect_to_gemini():
    """Connect to Google Gemini API."""
    global client

    try:
        client = genai.Client(
            api_key=settings.gemini_api_key,
        ).aio

        return {
            "provider": "google",
            "success": True,
        }

    except Exception as error:
        client = None

        return {
            "provider": "google",
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
            "provider": "google",
            "success": True,
        }

    except Exception as error:
        client = None

        return {
            "provider": "google",
            "success": False,
            "error": str(error),
        }


async def gemini_generate_response(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
):
    """Generate a response using Gemini."""

    if client is None:
        return {
            "provider": "google",
            "success": False,
            "error": "Gemini client is not initialized.",
        }

    try:
        response = await client.models.generate_content(
            model=model,
            contents=[
                {
                    "role": "model"
                    if message["role"] == "assistant"
                    else message["role"],
                    "parts": [{"text": message["content"]}],
                }
                for message in messages
            ],
            config=genai.types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        return {
            "provider": "google",
            "model": response.model_version,
            "content": response.text,
            "success": True,
        }

    except Exception as error:
        return {
            "provider": "google",
            "success": False,
            "error": str(error),
        }


async def gemini_get_model_list():
    """Get available Gemini models."""

    if client is None:
        return {
            "provider": "google",
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
            "provider": "google",
            "success": True,
            "models": model_list,
        }

    except Exception as error:
        return {
            "provider": "google",
            "success": False,
            "error": str(error),
        }
