import os
from pathlib import Path

def flatten_directory(source, sink, ignore_list=None):
    """
    Flattens the directory structure by creating symbolic links to all files 
    found under the source directory into a single-level sink directory.

    Parameters:
    ----------
    source : str or Path
        The path to the source directory whose files will be linked.
    sink : str or Path
        The path to the target sink directory where symlinks will be created.
    ignore_list : list of str, optional
        A list of file or directory names to ignore during processing. 
        If any part of a file's path matches an entry in this list, that file is skipped.

    Behavior:
    --------
    - Creates the sink directory if it does not exist.
    - Traverses all files recursively under the source directory.
    - Creates flattened symbolic links in the sink directory with names derived 
      from their original relative paths.
    - Handles filename conflicts by appending an incremental counter.
    - Skips files and directories listed in the ignore_list.
    - Logs skipped files and linking results to the console.

    Example:
    -------
    flatten_directory(
        "/path/to/source",
        "/path/to/sink",
        ignore_list=[".git", "__pycache__", "venv", "README.md"]
    )
    """
    source = Path(source).resolve()
    sink = Path(sink).resolve()
    sink.mkdir(parents=True, exist_ok=True)

    if ignore_list is None:
        ignore_list = []

    for file_path in source.rglob('*'):
        if file_path.is_file():
            # Check if file or any parent directory is in ignore list
            if any(ignored in file_path.parts for ignored in ignore_list):
                print(f"Skipped (ignored): {file_path}")
                continue

            # Create a flat name based on the relative path
            relative_path = file_path.relative_to(source)
            flat_name = '_'.join(relative_path.parts)

            symlink_target = sink / flat_name

            # Handle name conflicts by appending a counter
            counter = 1
            while symlink_target.exists():
                symlink_target = sink / f"{flat_name}_{counter}"
                counter += 1

            try:
                os.symlink(file_path, symlink_target)
                print(f"Linked: {file_path} -> {symlink_target}")
            except OSError as e:
                print(f"Failed to link {file_path}: {e}")

# Example usage:

if __name__ == "__main__":
    source ="/workspaces/assistant/app"
    sink = "/workspaces/assistant/inspection_app"
    ignore_list=[".git", "__pycache__", "venv", "README.md"] 
    flatten_directory(
        source,
        sink,
        ignore_list=ignore_list 
    )
