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
