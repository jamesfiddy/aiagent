import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import prompts
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API Key has not been found.")
    
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Project Chat Bot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", 
                              parts=[types.Part(text=args.user_prompt)])]

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        final_text = generate_content(client, messages, args.verbose)
        if final_text is not None:
            print("Final response:")
            print(final_text)
            return

    print("Maximum iterations reached")
    sys.exit(1)
    
def generate_content(client, messages, verbose):
    available_functions = call_function.available_functions
    system_prompt = prompts.system_prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    prompt_tokens = 0
    response_tokens = 0

    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        raise RuntimeError("Metadata is empty, likely API failure.")
    
    if verbose == True:
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        return response.text
      
    function_results = []
    for call in response.function_calls:
        function_call_result = call_function(call, verbose=verbose)
        if not function_call_result.parts:
            raise Exception("parts not empty")
        if function_call_result.parts[0].function_response is None:
            raise Exception("function response is None")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("function response response is None")
        function_results.append(function_call_result.parts[0])
        if verbose == True:
            print(f"-> {function_call_result.parts[0].function_response.response}")
   
    messages.append(types.Content(role="user", parts=function_results))

    return None

if __name__ == "__main__":
    main()
