import os
import sys
from dotenv import load_dotenv

from google import genai
import argparse as ap

from google.genai import types

from call_function import available_functions


load_dotenv()

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = "gemini-2.0-flash-001"


def setup_agent() -> genai.Client:
    """Setups the ai agent

    Returns:
        Client
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def setup_parser():
    # Setup Parser
    parser = ap.ArgumentParser(
        description="This is an AI agent that takes a string and returns the response"
    )
    parser.add_argument("contents", type=str, help="Input string to send to the agent")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Display extra information"
    )

    if len(sys.argv) < 2:
        print("Error: Missing required argument <input_string>.", file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    return args


def main():

    client = setup_agent()
    args = setup_parser()

    contents: str = args.contents
    verbose: bool = args.verbose

    messages = [
        types.Content(role="user", parts=[types.Part(text=contents)]),
    ]

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    if verbose:

        print(f"User prompt: {response.text}")

        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(response.function_calls)
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )


if __name__ == "__main__":
    main()
