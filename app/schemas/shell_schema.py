command_exec_tool = {
    "name": "run_command_secure",
    "description": (
        "Safely executes a whitelisted shell command within a whitelisted directory. "
        "Use this tool to run simple commands like 'pytest' or 'python' only in approved folders."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "input_command": {
                "type": "string",
                "description": (
                    "The shell command to execute. Must start with an allowed command "
                    "(e.g., 'pytest', 'python', 'ls', 'echo'). Example: 'pytest tests/'."
                )
            },
            "working_dir": {
                "type": "string",
                "description": (
                    "The directory where the command should be executed. "
                    "Must be within one of the allowed directories."
                )
            }
        },
        "required": ["input_command", "working_dir"]
    }
}
