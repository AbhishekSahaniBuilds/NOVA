from groq import AsyncGroq

from app.core.config import settings

client: AsyncGroq | None = None


async def connect_to_groq():
    """Connect to Groq API."""
    global client

    try:
        client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

        return {
            "provider": "groq",
            "success": True,
        }

    except Exception as error:
        client = None

        return {
            "provider": "groq",
            "success": False,
            "error": str(error),
        }


async def disconnect_to_groq():
    """Disconnect from Groq API."""
    global client

    try:
        if client is not None:
            await client.close()
            client = None

        return {
            "provider": "groq",
            "success": True,
        }

    except Exception as error:
        client = None

        return {
            "provider": "groq",
            "success": False,
            "error": str(error),
        }


async def groq_generate_response(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
):
    """Generate a response using Groq."""

    if client is None:
        return {
            "provider": "groq",
            "success": False,
            "error": "Groq client is not initialized.",
        }

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "provider": "groq",
            "model": response.model,
            "content": response.choices[0].message.content,
            "success": True,
        }

    except Exception as error:
        return {
            "provider": "groq",
            "success": False,
            "error": str(error),
        }


async def groq_get_model_list():
    """Get the list of available Groq models."""

    if client is None:
        return {
            "provider": "groq",
            "success": False,
            "error": "Groq client is not initialized.",
        }

    try:
        models = await client.models.list()

        return {
            "provider": "groq",
            "success": True,
            "models": [model.id for model in models.data],
        }

    except Exception as error:
        return {
            "provider": "groq",
            "success": False,
            "error": str(error),
        }
