import subprocess
import shlex
import os

# Whitelisted Directories
ALLOWED_DIRS = ["/workspaces/codespaces-jupyter/dummyapp"]

# Whitelisted Commands
ALLOWED_COMMANDS = ["pytest", "python3", "ls", "echo", "cat"]

def is_within_whitelist(target_path):
    target_path = os.path.abspath(target_path)
    return any(target_path.startswith(os.path.abspath(allowed)) for allowed in ALLOWED_DIRS)

def is_command_allowed(command):
    try:
        tokens = shlex.split(command)
        return tokens[0] in ALLOWED_COMMANDS
    except IndexError:
        return False  # Empty command

def run_command_secure(input_command, working_dir):
    working_dir = os.path.abspath(working_dir)

    if not is_within_whitelist(working_dir):
        return f"❌ Execution in directory '{working_dir}' is not allowed."

    if not is_command_allowed(input_command):
        return f"❌ Command '{shlex.split(input_command)[0]}' is not in the allowed commands list."

    try:
        tokens = shlex.split(input_command)
        result = subprocess.run(
            tokens,
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"❌ Command failed: {e.stderr.strip()}"


if __name__ == "__name__":

    r =run_command_secure("python3 hello.py", f"/workspaces/codespaces-jupyter/dummyapp")

    print(r)