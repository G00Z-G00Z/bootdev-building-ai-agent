from pathlib import Path
import os

from functools import wraps
from typing import Callable, Any

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


@llm_error_handler
def get_file_contents(working_directory: str, file_path: str) -> str:
    wd = Path(working_directory).resolve()

    assert wd.exists() and wd.is_dir(), "Working directory is not valid"

    tentative_filepath = (wd / file_path).resolve()

    assert str(tentative_filepath.absolute()).startswith(
        str(wd.absolute())
    ), f'Cannot read "{file_path}" as it is outside the permitted working directory'

    size_file = os.path.getsize(tentative_filepath)

    # Read the file and return its contents
    with open(tentative_filepath, "r") as file:
        contents = file.read(MAX_CHARS)
        if size_file > MAX_CHARS:
            return f'{contents}... "{file_path}" truncated at 10000 characters'


@llm_error_handler
def write_file(working_directory: str, file_path: str, content: str) -> str:

    wd = Path(working_directory).resolve()

    assert wd.exists() and wd.is_dir(), "Working directory is not valid"

    tentative_filepath = (wd / file_path).resolve()

    assert str(tentative_filepath.absolute()).startswith(
        str(wd.absolute())
    ), f'Cannot write to "{file_path}" as it is outside the permitted working directory'

    if tentative_filepath.exists():
        assert tentative_filepath.is_file()

    tentative_filepath.write_text(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
