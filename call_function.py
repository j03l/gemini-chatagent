import os

from google.genai import types

import functions

available_functions = types.Tool(
    function_declarations=[
        functions.schema_get_files_info,
        functions.schema_get_file_content,
        functions.schema_write_file,
        functions.schema_run_python_file,
    ],
)


def call_function(function_call: types.FunctionCall, verbose=False) -> types.Content:
    if verbose:
        print(print(f"Calling function: {function_call.name}({function_call.args})"))
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": functions.get_file_content,
        "get_files_info": functions.get_files_info,
        "run_python_file": functions.run_python_file,
        "write_files": functions.write_file,
    }

    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    working_directory: str = os.path.normpath("calculator")

    function_result: str = function_map[function_name](working_directory, **args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
