import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.isdir(s=target_dir):
            return f"Error: '{directory}' is not a directory"

        valid_target_dir: bool = (
            os.path.commonpath(paths=[working_dir_abs, target_dir]) == working_dir_abs
        )
        if valid_target_dir:
            contents = ""
            for i in os.listdir(path=target_dir):
                path: str = os.path.join(target_dir, i)
                contents += f"- {i}: file_size={os.path.getsize(filename=path)}, is_dir={os.path.isdir(s=path)}\n"
            return contents[:-1]
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: Cannot access system path: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)
