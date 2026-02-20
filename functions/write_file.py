import os

from google.genai import types


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_working_dir = (
        os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    )

    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    if valid_working_dir:
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        with open(target_file_path, "w") as f:
            f.write(content)
        if os.path.isfile(target_file_path):
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


schema_write_file = types.FunctionDeclaration(
    name="write_files",
    description="Writes content to a file in the specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
