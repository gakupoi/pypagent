import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'"{directory}" is not a directory'
        # return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {e}"

    result = ""
    list_files = os.listdir(target_dir)
    for file in list_files:
        file_path = os.path.join(target_dir, file)
        size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        result += f"- {file}: file_size={size}, is_dir={is_dir}\n"

    return result
