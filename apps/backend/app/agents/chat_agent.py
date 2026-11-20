import logging
from typing import Any

from app.services.ai.ai_coordinator import generate_master_response

logger = logging.getLogger(__name__)

MAX_MESSAGE_HISTORY = 30


async def process_chat(
    main_ai_client: Any,
    content: str,
    message_history: list[Any] | None = None,
    control_mode: bool = False,
) -> dict[str, Any]:

    try:
        if not isinstance(content, str) or not content.strip():
            return {
                "provider": "groq",
                "success": False,
                "error": "Message content cannot be empty.",
            }

        history = []

        for message in (message_history or [])[-MAX_MESSAGE_HISTORY:]:
            if hasattr(message, "model_dump"):
                message = message.model_dump()

            if not isinstance(message, dict):
                continue

            role = message.get("role")
            message_content = message.get("content")

            if role not in ("user", "assistant"):
                continue

            if not isinstance(message_content, str):
                continue

            if not message_content.strip():
                continue

            history.append(
                {
                    "role": role,
                    "content": message_content,
                }
            )

        messages = [
            *history,
            {
                "role": "user",
                "content": content.strip(),
            },
        ]

        response = await generate_master_response(
            main_ai_client=main_ai_client,
            messages=messages,
            control_mode=control_mode,
        )

        if not isinstance(response, dict):
            raise TypeError("AI coordinator returned an invalid response.")

        return response

    except Exception:
        logger.exception("Chat processing failed.")

        return {
            "provider": "groq",
            "success": False,
            "error": "NOVA encountered an error while processing your message.",
        }
