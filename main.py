import os
import sys
import types
from dotenv import load_dotenv

from google import genai
import argparse as ap

from google.genai import types

load_dotenv()


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
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose:
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
