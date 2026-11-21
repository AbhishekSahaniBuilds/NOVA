import logging
from typing import Any

from app.models.prompt import ToolApproval
from app.services.ai.ai_coordinator import (
    build_approved_action_message,
    generate_master_response,
)
from app.tools.tool_registry import validate_tool_calls

logger = logging.getLogger(__name__)

MAX_MESSAGE_HISTORY = 30


async def process_chat(
    main_ai_client: Any,
    content: str,
    message_history: list[Any] | None = None,
    control_mode: bool = False,
    tool_approval: ToolApproval | None = None,
) -> dict[str, Any]:

    try:
        if not isinstance(content, str) or not content.strip():
            return {
                "provider": "groq",
                "success": False,
                "error": "Message content cannot be empty.",
            }

        if tool_approval is not None:
            if not control_mode:
                return {
                    "provider": "groq",
                    "success": False,
                    "error": "Tool approval is only available in control mode.",
                }

            requested_calls = [
                call.model_dump() for call in tool_approval.tool_calls
            ]
            approved_calls, validation_error = validate_tool_calls(requested_calls)
            if approved_calls is None:
                logger.warning(
                    "Rejected invalid approved tool call: %s",
                    validation_error,
                )
                return {
                    "provider": "groq",
                    "success": False,
                    "error": "The approved action is invalid.",
                }

            if tool_approval.decision == "denied":
                return {
                    "provider": "groq",
                    "success": True,
                    "content": "Understood. I won't do that.",
                    "tool_calls": [],
                    "pending_tool_calls": [],
                    "approval_required": False,
                }

            return {
                "provider": "groq",
                "success": True,
                "content": build_approved_action_message(approved_calls),
                "tool_calls": approved_calls,
                "pending_tool_calls": [],
                "approval_required": False,
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

        if response.get("success"):
            response.setdefault("pending_tool_calls", [])
            response.setdefault("approval_required", False)

        return response

    except Exception:
        logger.exception("Chat processing failed.")

        return {
            "provider": "groq",
            "success": False,
            "error": "NOVA encountered an error while processing your message.",
        }
