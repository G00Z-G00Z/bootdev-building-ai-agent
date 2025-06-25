from google.genai import types

from functions.get_files_info import (
    schema_get_files_info,
    schema_get_file_contents,
    schema_write_file,
    schema_run_python_file,
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
    ]
)
