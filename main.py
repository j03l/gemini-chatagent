import argparse
import os
import sys
from argparse import Namespace

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

from call_function import available_functions, call_function
from prompt import system_prompt

load_dotenv()
api_key: str | None = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args: Namespace = parser.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]
try:
    for _ in range(20):
        response: types.GenerateContentResponse = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        for convo in response.candidates:
            messages.append(convo.content)

        if response.usage_metadata and args.verbose:
            tokens: dict = {
                "prompt": response.usage_metadata.prompt_token_count,
                "response": response.usage_metadata.candidates_token_count,
            }
            print(
                f"User prompt: {args.user_prompt}\n",
                f"Prompt tokens: {tokens['prompt']}\n Response tokens: {tokens['response']}\n",
            )
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                # print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(
                    function_call=function_call, verbose=args.verbose or False
                )
                if not function_call_result.parts:
                    raise Exception("types.Content should have a non-empty .parts list")
                elif function_call_result.parts[0].function_response is None:
                    raise Exception("functon_response property is None")
                elif function_call_result.parts[0].function_response.response is None:
                    raise Exception("function_response.response is None")

                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(f"Response:\n{response.text}")
            break
    if not response.text:
        print(
            "AI went over 20 iterations, it's burning the tokens! Ask something easier..."
        )
        sys.exit(1)
except ServerError as e:
    print(f"Failed request to Google: {e}")
    raise
