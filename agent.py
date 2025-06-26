"""Here will have the loop for becoming an agent"""

from google.genai import Client
from google.genai import types

from call_function import AVAILABLE_FUNCTIONS_FOR_LLM, call_function


DEFAULT_MODEL_NAME = "gemini-2.0-flash-001"


DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

MAX_ITERATIONS = 20


def agent_loop(
    client: Client,
    content: str,
    verbose: bool = False,
    model_name: str = DEFAULT_MODEL_NAME,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    available_functions_for_llm: types.Tool = AVAILABLE_FUNCTIONS_FOR_LLM,
):
    """Agent loop that keeps the conversation going

    Args:
        client: Ai client
        content: Contents of the user
        verbose: Verbose mode
        model_name:  Model name to use, by default (gemini-2.0-flash-001)
        system_prompt: System prompt
        available_functions_for_llm: Available tools that can be used with the LLM

    Returns:
        idk
    """
    first_message = types.Content(role="user", parts=[types.Part(text=content)])

    messages = [first_message]

    for _ in range(MAX_ITERATIONS):

        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions_for_llm],
            ),
        )

        candidates = response.candidates

        assert candidates is not None, "The list of candidates returned empty"

        for candidate in candidates:
            if candidate.content:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:

                function_call_result = call_function(function_call_part, verbose)

                messages.append(function_call_result)

                if verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
        else:
            return response.text

        # if verbose:
        #     print(f"User prompt: {response.text}")
        #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        # else:
        #     print(response.text)

        # return response
