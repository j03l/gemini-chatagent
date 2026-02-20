import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_working_dir = (
            os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        )
        if not valid_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        command.extend(args or [])  # Additional vars to pass to the script
        process: subprocess.CompletedProcess = subprocess.run(
            command, capture_output=True, text=True, timeout=30.0
        )
        if process.returncode != 0:
            output = "Process exited with code X"
        elif None in [process.stdout, process.stderr]:
            output = "No output produced"
        else:
            output = f"STDOUT: {process.stdout}\nSTDERR: {process.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument to pass to the Python script",
                ),
            ),
        },
        required=["file_path"],
    ),
)
