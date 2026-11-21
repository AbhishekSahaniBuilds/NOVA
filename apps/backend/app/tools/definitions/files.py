open_file = {
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
}
