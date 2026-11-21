open_folder = {
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
}
