from pathlib import Path
import subprocess
import os

from functools import wraps
from typing import Callable, Any

from google.genai import types

MAX_CHARS = 10_000


def llm_error_handler(func: Callable[..., str]) -> Callable[..., str]:
    """
    Decorator that runs a function and returns the error message as a string if an exception is raised.



    Args:
        func (Callable[..., str]): The function to be decorated, which can accept any arguments and returns a string.

    Returns:
        Callable[..., str]: The wrapped function that returns error messages as strings if an exception occurs.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(f"Error: {e}")

    return wrapper


def raise_is_file_outside(
    working_directory: str, file_path: str, file_action: str
) -> Path:
    """Returns the absolute path to the file path. Raises in any other circumstance

    Args:
        working_directory: Working directory where it is allowed
        file_path: File path inside the working directory
        file_action: verb to describe the intented action

    Returns:
        Path of the file path
    """
    wd = Path(working_directory).resolve()

    assert wd.exists() and wd.is_dir(), "Working directory is not valid"

    tentative_filepath = (wd / file_path).resolve()

    assert str(tentative_filepath.absolute()).startswith(
        str(wd.absolute())
    ), f'Cannot {file_action} "{file_path}" as it is outside the permitted working directory'

    return tentative_filepath


@llm_error_handler
def get_files_info(working_directory: str, directory: str | None = None) -> str:
    """Get the files information from the directory.

    Outputs the directory contents as the following format:

        - README.md: file_size=1032 bytes, is_dir=False
        - src: file_size=128 bytes, is_dir=True
        - package.json: file_size=1234 bytes, is_dir=False

    Args:
        directory (str): Directory inside the working directory
        working_directory: Working directory. Anything outside it is not allowed

    Returns:
        String result (even if error)
    """
    wd = Path(working_directory).resolve()

    assert wd.exists(), "The working directory does not exist"

    path = (wd / directory).resolve() if directory is not None else wd

    assert path.is_dir(), f'"{path}" is not a directory'

    assert str(path.absolute()).startswith(
        str(wd.absolute())
    ), f'Cannot list "{directory}" as it is outside the permitted working directory'

    result = []
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        file_size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
        is_dir = os.path.isdir(entry_path)
        result.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(result)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


@llm_error_handler
def get_file_contents(working_directory: str, file_path: str) -> str:

    tentative_filepath = raise_is_file_outside(working_directory, file_path, "read")

    size_file = os.path.getsize(tentative_filepath)

    # Read the file and return its contents
    with open(tentative_filepath, "r") as file:
        contents = file.read(MAX_CHARS)
        if size_file > MAX_CHARS:
            return f'{contents}... "{file_path}" truncated at 10000 characters'
        return contents


schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description="Retrieves the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
    ),
)


@llm_error_handler
def write_file(working_directory: str, file_path: str, content: str) -> str:

    tentative_filepath = raise_is_file_outside(working_directory, file_path, "write")

    if tentative_filepath.exists():
        assert tentative_filepath.is_file()

    tentative_filepath.write_text(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)


@llm_error_handler
def run_python_file(working_directory: str, file_path: str):

    tentative_filepath = raise_is_file_outside(working_directory, file_path, "execute")

    assert tentative_filepath.exists(), f'Error: File "{file_path}" not found.'
    assert (
        tentative_filepath.suffix == ".py"
    ), f'Error: "{file_path}" is not a Python file.'

    llm_response = ""

    try:
        # Run the Python file using subprocess
        result = subprocess.run(
            ["python", str(tentative_filepath)],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Check for output and format the result
        output = result.stdout.strip()
        errors = result.stderr.strip()

        if output:
            llm_response += f"STDOUT: {output}\n"
        if errors:
            llm_response += (
                f"STDERR: {errors}\nProcess exited with code {result.returncode}\n"
            )

        if llm_response == "":
            llm_response = "No output produced"

    except subprocess.TimeoutExpired:
        raise Exception("Execution timed out after 30 seconds.")
    except Exception as e:
        raise Exception(f"Executing python file: {e}")

    return f'{llm_response}\nSuccessfully executed "{file_path}"'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)
