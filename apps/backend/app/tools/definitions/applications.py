open_application = {
    "name": "open_application",
    "description": "Open an installed Windows application using its exact Windows Run/CLI executable name.",
    "parameters": {
        "type": "object",
        "properties": {
            "application": {
                "type": "string",
                "description": (
                    "The exact Windows executable command (without .exe) or system URI. "
                    "NEVER pass general or conversational names. "
                    "Always convert them: use 'calc' (NOT 'calculator'), 'mspaint' (NOT 'paint'), "
                    "'winword' (NOT 'word'), 'powerpnt' (NOT 'powerpoint'), 'msedge' (NOT 'edge'), "
                    "'explorer' (NOT 'file explorer'), 'ms-settings:' (NOT 'settings'), 'notepad' for Notepad, etc"
                ),
            }
        },
        "required": ["application"],
        "additionalProperties": False,
    },
}
