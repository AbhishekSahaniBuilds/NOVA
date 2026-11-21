import json
import logging
from typing import Any

from groq import AsyncGroq

from app.core.config import settings

logger = logging.getLogger(__name__)


# ============================================================
# CONNECT TO GROQ
# ============================================================


async def connect_to_groq() -> dict[str, Any]:
    if not settings.groq_api_key:
        logger.error("GROQ_API_KEY is not configured.")
        return {
            "provider": "groq",
            "success": False,
            "client": None,
            "error": "GROQ_API_KEY is not configured.",
        }

    try:
        client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

        return {
            "provider": "groq",
            "success": True,
            "client": client,
        }

    except Exception:
        logger.exception("Failed to initialize Groq.")

        return {
            "provider": "groq",
            "success": False,
            "client": None,
            "error": "Groq could not be initialized.",
        }


# ============================================================
# DISCONNECT FROM GROQ
# ============================================================


async def disconnect_to_groq(
    client: AsyncGroq | None,
) -> None:

    if client is None:
        return

    await client.close()


# ============================================================
# GENERATE GROQ RESPONSE
# ============================================================


async def groq_generate_response(
    client: AsyncGroq | None,
    messages: list[dict[str, Any]],
    system_prompt: str,
    tools: list[dict[str, Any]] | None = None,
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
        # ----------------------------------------------------
        # PREPARE MESSAGES
        # ----------------------------------------------------

        request_messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            *messages,
        ]

        # ----------------------------------------------------
        # BUILD REQUEST
        # ----------------------------------------------------

        request_data: dict[str, Any] = {
            "model": model,
            "messages": request_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # ----------------------------------------------------
        # CONFIGURE RESPONSE MODE
        # ----------------------------------------------------

        if tools:
            request_data["tools"] = tools
            request_data["tool_choice"] = "auto"

        else:
            request_data["response_format"] = {
                "type": "json_object",
            }

        # ----------------------------------------------------
        # SEND REQUEST
        # ----------------------------------------------------

        response = await client.chat.completions.create(
            **request_data,
        )

        if not response.choices:
            raise RuntimeError("Groq returned an empty choices list.")

        message = response.choices[0].message

        # ----------------------------------------------------
        # EXTRACT TOOL CALLS
        # ----------------------------------------------------

        tool_calls: list[dict[str, Any]] = []

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name

                raw_arguments = tool_call.function.arguments or "{}"

                try:
                    arguments = json.loads(raw_arguments)

                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Invalid arguments for tool {function_name}."
                    ) from error

                if not isinstance(arguments, dict):
                    raise ValueError("Tool arguments must be a JSON object.")

                tool_calls.append(
                    {
                        "name": function_name,
                        "arguments": arguments,
                    }
                )

        # ----------------------------------------------------
        # EXTRACT RESPONSE CONTENT
        # ----------------------------------------------------

        content = message.content or ""

        if not content and not tool_calls:
            raise RuntimeError("Groq returned neither content nor tool calls.")

        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return {
            "provider": "groq",
            "model": model,
            "success": True,
            "content": content,
            "tool_calls": tool_calls,
        }

    except Exception:
        logger.exception("Groq generation failed.")

        return {
            "provider": "groq",
            "model": model,
            "success": False,
            "error": "Groq request failed.",
        }


# ============================================================
# GET GROQ MODEL LIST
# ============================================================


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

    except Exception:
        logger.exception("Failed to retrieve Groq models.")

        return {
            "provider": "groq",
            "success": False,
            "error": "Unable to retrieve Groq models.",
        }
