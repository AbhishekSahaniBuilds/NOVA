import logging
from typing import Any

from groq import AsyncGroq

from app.core.config import settings

logger = logging.getLogger(__name__)


async def connect_to_groq() -> dict[str, Any]:
    try:
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

        return {
            "provider": "groq",
            "success": True,
            "client": client,
        }

    except Exception as error:
        logger.exception("Failed to initialize Groq.")

        return {
            "provider": "groq",
            "success": False,
            "client": None,
            "error": str(error),
        }


async def disconnect_to_groq(
    client: AsyncGroq | None,
) -> None:
    if client is None:
        return

    await client.close()


async def groq_generate_response(
    client: AsyncGroq | None,
    messages: list[dict[str, Any]],
    system_prompt: str,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> dict[str, Any]:

    if client is None:
        return {
            "provider": "groq",
            "success": False,
            "error": "Groq client is not available.",
        }

    if not model:
        return {
            "provider": "groq",
            "success": False,
            "error": "No Groq model was configured.",
        }

    if not isinstance(messages, list):
        return {
            "provider": "groq",
            "success": False,
            "error": "Messages must be provided as a list.",
        }

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        system_prompt + "\n\n"
                        "Return your response as a valid JSON object "
                        "matching the requested response structure. "
                        "Do not include Markdown code fences."
                    ),
                },
                *messages,
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={
                "type": "json_object",
            },
        )

        if not response.choices:
            raise RuntimeError("Groq returned an empty choices list.")

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("Groq returned an empty response.")

        return {
            "provider": "groq",
            "model": model,
            "success": True,
            "content": content,
        }

    except Exception as error:
        logger.exception("Groq generation failed.")

        return {
            "provider": "groq",
            "model": model,
            "success": False,
            "error": str(error),
        }


async def groq_get_model_list(
    client: AsyncGroq | None,
) -> dict[str, Any]:

    if client is None:
        return {
            "provider": "groq",
            "success": False,
            "error": "Groq client is not available.",
        }

    try:
        response = await client.models.list()

        models = [model.id for model in response.data]

        return {
            "provider": "groq",
            "success": True,
            "models": models,
        }

    except Exception as error:
        logger.exception("Failed to retrieve Groq models.")

        return {
            "provider": "groq",
            "success": False,
            "error": str(error),
        }
