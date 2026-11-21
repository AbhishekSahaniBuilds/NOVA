from typing import Any

TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "open_application": {
        "name": "open_application",
        "description": "Open an installed Windows application.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": "Application identifier, such as notepad or calculator.",
                }
            },
            "required": ["application"],
            "additionalProperties": False,
        },
    },
    "open_file": {
        "name": "open_file",
        "description": "Open a file on the user's Windows computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path of the file to open.",
                }
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
    },
    "open_folder": {
        "name": "open_folder",
        "description": "Open a folder in Windows File Explorer.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "Absolute path of the folder.",
                }
            },
            "required": ["folder_path"],
            "additionalProperties": False,
        },
    },
}


def get_available_tools() -> list[dict[str, Any]]:
    """Return registered tools in Groq function-calling format."""

    return [{"type": "function", "function": tool} for tool in TOOL_REGISTRY.values()]


def get_tool(tool_name: str) -> dict[str, Any] | None:
    return TOOL_REGISTRY.get(tool_name)


def get_tool_names() -> list[str]:
    return list(TOOL_REGISTRY.keys())


def validate_tool_calls(
    tool_calls: Any,
) -> tuple[list[dict[str, Any]] | None, str | None]:
    if not isinstance(tool_calls, list):
        return None, "Tool calls must be a list."

    validated_calls: list[dict[str, Any]] = []

    for tool_call in tool_calls:
        if not isinstance(tool_call, dict):
            return None, "Tool calls must be objects."

        name = tool_call.get("name")
        arguments = tool_call.get("arguments")
        tool = TOOL_REGISTRY.get(name) if isinstance(name, str) else None

        if tool is None:
            return None, "Tool name is not registered."

        if not isinstance(arguments, dict):
            return None, "Tool arguments must be an object."

        parameter_schema = tool["parameters"]
        properties = parameter_schema["properties"]
        required = parameter_schema.get("required", [])

        if any(key not in arguments for key in required):
            return None, "Required tool arguments are missing."

        if not parameter_schema.get("additionalProperties", True):
            if any(key not in properties for key in arguments):
                return None, "Tool arguments contain unsupported fields."

        for key, value in arguments.items():
            property_schema = properties.get(key)
            if property_schema is None:
                continue

            expected_type = property_schema.get("type")
            type_matches = {
                "string": lambda item: isinstance(item, str),
                "object": lambda item: isinstance(item, dict),
                "array": lambda item: isinstance(item, list),
                "integer": lambda item: isinstance(item, int)
                and not isinstance(item, bool),
                "number": lambda item: isinstance(item, (int, float))
                and not isinstance(item, bool),
                "boolean": lambda item: isinstance(item, bool),
                "null": lambda item: item is None,
            }.get(expected_type)

            if type_matches is not None and not type_matches(value):
                return None, f"Tool argument '{key}' has an invalid type."

        validated_calls.append({"name": name, "arguments": arguments})

    return validated_calls, None
