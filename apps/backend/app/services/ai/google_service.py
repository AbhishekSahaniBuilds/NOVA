import logging
from typing import Any

from google import genai

from app.core.config import settings

logger = logging.getLogger(__name__)


async def connect_to_gemini() -> dict[str, Any]:
    try:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        client = genai.Client(
            api_key=settings.gemini_api_key,
        ).aio

        return {
            "provider": "gemini",
            "success": True,
            "client": client,
        }

    except Exception as error:
        logger.exception("Failed to initialize Gemini.")

        return {
            "provider": "gemini",
            "success": False,
            "client": None,
            "error": str(error),
        }


async def disconnect_to_gemini(
    client: Any,
) -> None:
    if client is None:
        return

    await client.aclose()


async def gemini_generate_response(
    client: Any,
    messages: list[dict[str, Any]],
    system_prompt: str,
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> dict[str, Any]:

    if client is None:
        return {
            "provider": "gemini",
            "success": False,
            "error": "Gemini client is not available.",
        }

    if not model:
        return {
            "provider": "gemini",
            "success": False,
            "error": "No Gemini model was configured.",
        }

    try:
        gemini_messages: list[dict[str, Any]] = []

        for message in messages:
            if not isinstance(message, dict):
                continue

            role = message.get("role")
            content = message.get("content")

            if not isinstance(content, str) or not content.strip():
                continue

            if role == "assistant":
                gemini_role = "model"
            elif role in ("user", "tool"):
                gemini_role = "user"
            else:
                continue

            if gemini_messages and gemini_messages[-1]["role"] == gemini_role:
                gemini_messages[-1]["parts"][0]["text"] += "\n\n" + content
            else:
                gemini_messages.append(
                    {
                        "role": gemini_role,
                        "parts": [
                            {
                                "text": content,
                            }
                        ],
                    }
                )

        if not gemini_messages:
            raise ValueError("No valid messages were provided to Gemini.")

        if gemini_messages[-1]["role"] != "user":
            raise ValueError("Gemini conversation must end with a user message.")

        response = await client.models.generate_content(
            model=model,
            contents=gemini_messages,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json",
            ),
        )

        content = response.text

        if not content:
            raise RuntimeError("Gemini returned an empty response.")

        return {
            "provider": "gemini",
            "model": getattr(
                response,
                "model_version",
                model,
            ),
            "success": True,
            "content": content,
        }

    except Exception as error:
        logger.exception("Gemini generation failed.")

        return {
            "provider": "gemini",
            "model": model,
            "success": False,
            "error": str(error),
        }


async def gemini_get_model_list(
    client: Any,
) -> dict[str, Any]:

    if client is None:
        return {
            "provider": "gemini",
            "success": False,
            "error": "Gemini client is not available.",
        }

    try:
        models = []

        async for model in await client.models.list():
            supported_actions = (
                getattr(
                    model,
                    "supported_actions",
                    [],
                )
                or []
            )

            if "generateContent" in supported_actions:
                model_name = getattr(model, "name", None)

                if model_name:
                    models.append(model_name.removeprefix("models/"))

        return {
            "provider": "gemini",
            "success": True,
            "models": models,
        }

    except Exception as error:
        logger.exception("Failed to retrieve Gemini models.")

        return {
            "provider": "gemini",
            "success": False,
            "error": str(error),
        }
