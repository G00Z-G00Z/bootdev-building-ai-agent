import os
import sys
from dotenv import load_dotenv

from google import genai
import argparse as ap

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
        description="This is ai agent that takes a string and returns the response"
    )
    parser.add_argument("contents", type=str, help="Input string to send to the agent")

    if len(sys.argv) < 2:
        print("Error: Missing required argument <input_string>.", file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    return args


def main():

    client = setup_agent()
    args = setup_parser()

    contents: str = args.contents

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=contents,
    )

    print(response.text)


if __name__ == "__main__":
    main()
