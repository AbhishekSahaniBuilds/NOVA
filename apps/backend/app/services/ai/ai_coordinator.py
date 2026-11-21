import json
import logging
from typing import Any

from pydantic import ValidationError

from app.core.config import settings
from app.models import MainAIResponse
from app.prompts import chat_prompt, control_prompt
from app.services.ai import groq_service
from app.tools.tool_registry import get_available_tools, validate_tool_calls

logger = logging.getLogger(__name__)


def _describe_tool_action(tool_call: dict[str, Any]) -> str:
    name = tool_call["name"]
    arguments = tool_call["arguments"]

    if name == "open_application":
        return f"open {arguments['application']}"
    if name == "open_file":
        return f"open the file {arguments['file_path']}"
    if name == "open_folder":
        return f"open the folder {arguments['folder_path']}"
    return "perform the requested action"


def _join_tool_actions(actions: list[str]) -> str:
    if len(actions) < 3:
        return " and ".join(actions)
    return f"{', '.join(actions[:-1])}, and {actions[-1]}"


def build_tool_approval_question(tool_calls: list[dict[str, Any]]) -> str:
    actions = [_describe_tool_action(call) for call in tool_calls]
    if len(actions) == 1:
        return f"I can {actions[0]}. Would you like me to?"

    return (
        f"I can {_join_tool_actions(actions)}. "
        "Would you like me to do that?"
    )


def build_approved_action_message(tool_calls: list[dict[str, Any]]) -> str:
    actions = [_describe_tool_action(call) for call in tool_calls]
    return f"Okay, I'll {_join_tool_actions(actions)}."


async def generate_master_response(
    main_ai_client: Any,
    messages: list[dict[str, Any]],
    control_mode: bool = False,
) -> dict[str, Any]:
    """Generate NOVA's response using Groq only.

    Groq is NOVA's sole conversational AI provider in this coordinator.
    Native tool calls are returned to the caller for the existing approval
    and local-execution flow; this function never executes tools itself.
    """
    if not messages:
        return {
            "provider": "groq",
            "success": False,
            "error": "No messages were provided.",
        }

    if not get_latest_user_message(messages):
        return {
            "provider": "groq",
            "success": False,
            "error": "No valid user message was found.",
        }

    result = await generate_main_ai_response(
        client=main_ai_client,
        messages=messages,
        control_mode=control_mode,
    )

    if not result.get("success"):
        return result

    native_tool_calls = result.get("tool_calls") or []
    if native_tool_calls:
        if not control_mode:
            logger.warning("Rejected an unexpected native tool call in chat mode.")
            return {
                "provider": result.get("provider", "groq"),
                "success": False,
                "error": "Groq returned an unexpected tool call.",
            }

        validated_calls, validation_error = validate_tool_calls(native_tool_calls)
        if validated_calls is None:
            logger.warning("Rejected invalid native tool call: %s", validation_error)
            return {
                "provider": result.get("provider", "groq"),
                "success": False,
                "error": "Groq returned an invalid tool call.",
            }

        return {
            **result,
            "provider": result.get("provider", "groq"),
            "success": True,
            "content": build_tool_approval_question(validated_calls),
            "tool_calls": [],
            "pending_tool_calls": validated_calls,
            "approval_required": True,
        }

    main_data, _ = validate_main_ai_response(result.get("content"))
    if main_data is None and control_mode:
        content = result.get("content")
        if isinstance(content, str) and content.strip():
            return {
                **result,
                "provider": result.get("provider", "groq"),
                "success": True,
                "content": content,
                "tool_calls": [],
            }

    if main_data is None:
        logger.warning("Groq returned invalid structured response.")
        return {
            "provider": result.get("provider", "groq"),
            "success": False,
            "error": "Groq returned an invalid structured response.",
        }

    structured_tool_calls = [call.model_dump() for call in main_data.tool_calls]
    if structured_tool_calls:
        logger.warning("Rejected structured tool calls; native calls are required.")
        return {
            "provider": result.get("provider", "groq"),
            "success": False,
            "error": (
                "Groq returned an unexpected tool call."
                if not control_mode
                else "Groq returned a non-native tool call."
            ),
        }

    if not main_data.content.strip():
        logger.warning("Groq returned an empty structured response.")
        return {
            "provider": result.get("provider", "groq"),
            "success": False,
            "error": "Groq returned an empty structured response.",
        }

    return {
        **result,
        "provider": result.get("provider", "groq"),
        "success": True,
        "content": main_data.content,
        "tool_calls": [],
    }


# =============================================================
# MainAI response generation
# =============================================================


async def generate_main_ai_response(
    client: Any,
    messages: list[dict[str, Any]],
    control_mode: bool = False,
) -> dict[str, Any]:
    if control_mode:
        return await generate_main_ai_control_response(client=client, messages=messages)

    return await generate_main_ai_chat_response(client=client, messages=messages)


async def generate_main_ai_chat_response(
    client: Any,
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    return await generate_groq_response(
        client=client,
        messages=messages,
        system_prompt=chat_prompt.CHAT_PROMPT,
        control_mode=False,
        temperature=0.7,
        max_tokens=4096,
        tools=None,
    )


async def generate_main_ai_control_response(
    client: Any,
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    return await generate_groq_response(
        client=client,
        messages=messages,
        system_prompt=control_prompt.CONTROL_PROMPT,
        control_mode=True,
        temperature=0.2,
        max_tokens=4096,
        tools=get_available_tools(),
    )


async def generate_groq_response(
    client: Any,
    messages: list[dict[str, Any]],
    system_prompt: str,
    tools: list[dict[str, Any]] | None = None,
    control_mode: bool = False,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> dict[str, Any]:

    if client is None:
        return {
            "provider": "groq",
            "success": False,
            "error": "Groq client is not available.",
        }

    primary_model = settings.groq_model_primary
    fallback_model = settings.groq_model_fallback

    # ---------------------------------------------------------
    # DETERMINE AVAILABLE TOOLS
    # ---------------------------------------------------------

    selected_tools = tools

    if control_mode and selected_tools is None:
        selected_tools = get_available_tools()

    if not control_mode:
        selected_tools = None

    # ---------------------------------------------------------
    # PRIMARY MODEL
    # ---------------------------------------------------------

    primary_result = await groq_service.groq_generate_response(
        client=client,
        messages=messages,
        system_prompt=system_prompt,
        tools=selected_tools,
        model=primary_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if primary_result.get("success"):
        return primary_result

    # ---------------------------------------------------------
    # FALLBACK MODEL
    # ---------------------------------------------------------

    if not fallback_model or fallback_model == primary_model:
        return primary_result

    fallback_result = await groq_service.groq_generate_response(
        client=client,
        messages=messages,
        system_prompt=system_prompt,
        tools=selected_tools,
        model=fallback_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if fallback_result.get("success"):
        fallback_result["used_fallback"] = True

    return fallback_result


# =============================================================
# Response parsing and Pydantic validation
# =============================================================


def parse_ai_content(content: Any) -> dict[str, Any] | None:
    """Parse a JSON string or dictionary into a dictionary."""
    if isinstance(content, dict):
        return content

    if not isinstance(content, str):
        return None

    try:
        parsed = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return None

    return parsed if isinstance(parsed, dict) else None


def validate_main_ai_response(
    content: Any,
) -> tuple[MainAIResponse | None, str | None]:
    parsed = parse_ai_content(content)
    if parsed is None:
        return None, "Groq content is not a valid JSON object."

    try:
        return MainAIResponse.model_validate(parsed), None
    except ValidationError as error:
        return None, str(error)


# =============================================================
# Message helpers
# =============================================================


def get_latest_user_message(messages: list[dict[str, Any]]) -> str:
    for message in reversed(messages):
        if isinstance(message, dict) and message.get("role") == "user":
            content = message.get("content")
            if isinstance(content, str):
                return content
    return ""
