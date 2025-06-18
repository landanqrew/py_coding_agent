import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv(dotenv_path="secrets/secrets.env")
api_key = os.environ.get("GEMINI_API_KEY")
# print(f"api_key: {api_key}")

client = genai.Client(api_key=api_key)

system_prompt: str = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

def get_llm_response(prompt: str, is_verbose: bool = False, system_prompt: str = system_prompt) -> dict | str:
    gemini_model: str = "gemini-2.0-flash-001"
    response = client.models.generate_content(model=gemini_model, contents=prompt, config=types.GenerateContentConfig(system_instruction=system_prompt))
    if is_verbose:
        return {"response": response.text , "Prompt tokens": response.usage_metadata.prompt_token_count, "Response tokens": response.usage_metadata.candidates_token_count}
    else:
        return response.text

def main():
    command_line_args = sys.argv
    if len(command_line_args) <= 1 or command_line_args[1][0] == "-":
        print("no prompt included. Please ensure the prompt is included as an enquoted string after the filename.")
        sys.exit(1)
    prompt: str = command_line_args[1]
    # print(command_line_args)
    if "--verbose" in command_line_args:
        print("verbose mode")
        print(f"User prompt: '{prompt}'")
        response: str = get_llm_response(prompt, is_verbose=True)
        for key, value in response.items():
            print(f"{key}: {value}")
    else:
        print("non-verbose mode")
        response: str = get_llm_response(prompt)
        print(response)
    
    '''response: str = get_llm_response(prompt)
    for key, value in response.items():
        print(f"{key}: {value}")'''

    

if __name__ == "__main__":
    # prompt: str = "give me a cool prompt to ask an AI"
    prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    main()
    
    '''response: str = get_llm_response(prompt)
    for key, value in response.items():
        print(f"{key}: {value}")'''