import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv(dotenv_path="secrets/secrets.env")
api_key = os.environ.get("GEMINI_API_KEY")
# print(f"api_key: {api_key}")

client = genai.Client(api_key=api_key)

def get_llm_response(prompt: str) -> str:
    gemini_model: str = "gemini-2.0-flash-001"
    response = client.models.generate_content(model=gemini_model, contents=prompt)
    return {"response": response.text , "Prompt tokens": response.usage_metadata.prompt_token_count, "Response tokens": response.usage_metadata.candidates_token_count}

def main():
    command_line_args = sys.argv
    if len(command_line_args) <= 1:
        print("no prompt included")
        sys.exit(1)
    print(command_line_args)
    
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