import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")

    get_response(client, messages, args.verbose)  
    
def get_response(client, messages, verbose):

    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)

    prompt_tokens = 0
    response_tokens = 0

    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        raise RuntimeError("Metadata is empty, likely API failure.")
    
    if verbose == True:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    
    print(response.text)

if __name__ == "__main__":
    main()
