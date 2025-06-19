import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from function_declaration import schema_run_python_file, schema_get_files_info, schema_write_file, schema_get_file_content
from functions.run_python import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

load_dotenv(dotenv_path="secrets/secrets.env")
api_key = os.environ.get("GEMINI_API_KEY")
# print(f"api_key: {api_key}")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def get_llm_response(prompt: str, is_verbose: bool = False, system_prompt: str = system_prompt) -> dict | str:
    gemini_model: str = "gemini-2.0-flash-001"
    available_functions: types.Tool = types.Tool(
        function_declarations=[
            schema_run_python_file,
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
        ]
    )
    response = client.models.generate_content(
        model=gemini_model, 
        contents=prompt, 
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[
                available_functions
            ]
            ),
        
        )
    
    # print(response.to_json_dict())
    if response.function_calls:
        for function_call_part in response.function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result: types.Content = call_function(function_call_part, is_verbose)
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError(f"Function {function_call_part.name} failed. No response object returned.")
            else:
                if is_verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                

    if is_verbose:
        return {"response": response.text , "Prompt tokens": response.usage_metadata.prompt_token_count, "Response tokens": response.usage_metadata.candidates_token_count, "Function Calls": list(map(lambda x: {"name": x.name, "args": x.args}, response.function_calls))}
    else:
        print(response.text)
        return response.text
    
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    function_map = {
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file
    }
    if function_name in function_map:
        result = function_map[function_name](working_directory=".", **function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

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