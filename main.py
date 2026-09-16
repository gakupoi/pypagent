import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_functions import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("api_key is not founded")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if not response.usage:
            raise RuntimeError("Usage is not actively")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
    else:
        print("Maximum iterations reached without final response")
        sys.exit(1)


if __name__ == "__main__":
    main()
