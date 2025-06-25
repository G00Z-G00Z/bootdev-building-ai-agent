from pathlib import Path
from google.genai import types

from functions.get_files_info import (
    llm_error_handler,
    schema_get_files_info,
    schema_get_file_contents,
    schema_write_file,
    schema_run_python_file,
    get_files_info,
    get_file_contents,
    write_file,
    run_python_file,
)


# Available functions for the llm
AVAILABLE_FUNCTIONS_FOR_LLM = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
    ]
)

# Helper dictionary to relate schema name to arguments
_SCHEMA_TO_FUNC = {
    schema_get_files_info.name: get_files_info,
    schema_get_file_contents.name: get_file_contents,
    schema_write_file.name: write_file,
    schema_run_python_file.name: run_python_file,
}

# Allowed directory
_WORKING_DIRECTORY = Path("./calculator")


def call_function(function_call_part: types.FunctionCall, verbose: bool = False):

    function_name: str = function_call_part.name or ""
    function_arguments: dict = function_call_part.args or {}

    if verbose:
        print(f"Calling function: {function_name}({function_arguments})")
    else:
        print(f" - Calling function: {function_name}")

    function_to_call = _SCHEMA_TO_FUNC.get(function_name)

    if function_to_call is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name or "",
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Always overwrite the working directory
    arguments = function_arguments | {"working_directory": str(_WORKING_DIRECTORY)}

    function_result = function_to_call(**arguments)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
