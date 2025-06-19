import os
import re
import json
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


def get_llm_response(
        prompt: str, 
        is_verbose: bool = False, 
        system_prompt: str = system_prompt, 
        agent_mode: bool = False,
        messages: list[types.Content] = None) -> types.GenerateContentResponse | dict | str:
    gemini_model: str = "gemini-2.0-flash-001"
    available_functions: types.Tool = types.Tool(
        function_declarations=[
            schema_run_python_file,
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
        ]
    )

    api_contents = messages
    if not api_contents:
        if prompt:
            api_contents = [types.Content(role="user", parts=[types.Part.from_text(prompt)])]
        else:
            raise ValueError("Either messages or a prompt must be provided to get_llm_response.")

    response: types.GenerateContentResponse = client.models.generate_content(
        model=gemini_model, 
        contents=api_contents, 
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[
                available_functions
            ]
            ),
        
        )
    
    if agent_mode:
        return response

    executed_function_call_results_for_obj = []
    if response.function_calls: 
        for fc_to_execute in response.function_calls:
            tool_response_content: types.Content = call_function(fc_to_execute, verbose=is_verbose) 
            
            actual_response_data = None
            if tool_response_content.parts and tool_response_content.parts[0].function_response:
                actual_response_data = tool_response_content.parts[0].function_response.response
                if is_verbose: 
                    print(f"-> {actual_response_data}")
            else:
                actual_response_data = {"error": f"Function {fc_to_execute.name} execution failed to produce a valid response part."}
                if is_verbose:
                    print(f"-> {actual_response_data}")

            executed_function_call_results_for_obj.append({
                "name": fc_to_execute.name,
                "args": dict(fc_to_execute.args),
                "response": actual_response_data
            })

    if is_verbose:
        return {
            "response": response.text,
            "Prompt tokens": response.usage_metadata.prompt_token_count,
            "Response tokens": response.usage_metadata.candidates_token_count,
            "Function Calls Made by Model": list(map(lambda x: {"name": x.name, "args": dict(x.args)}, response.function_calls)),
            "Executed Function Call Results": executed_function_call_results_for_obj
        }
    else:
        print(response.text)
        return response.text
    
def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
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
    is_verbose_cli_arg = "--verbose" in command_line_args

    if "--agent" in command_line_args:
        print("agent mode")
        print(f"User prompt: '{prompt}'")
        iter_limit: int = 20
        for arg in command_line_args[2:]:
            if arg.startswith("--iter-limit="):
                digits = re.findall(r"\d+", arg)
                if len(digits) > 0 and digits[0][0] != "0":
                    iter_limit = int(digits[0])
                else:
                    raise ValueError("No valid numeric value found in iter-limit argument.")
        
        messages: list[types.Content] = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

        for i in range(iter_limit):
            print(f"\n--- Iteration {i + 1} ---")
            model_api_response: types.GenerateContentResponse = get_llm_response(
                prompt=None,
                is_verbose=is_verbose_cli_arg, 
                agent_mode=True, 
                messages=messages
            )

            if not model_api_response.candidates:
                print("No candidates received from model. Exiting.")
                break
            
            assistant_content: types.Content = model_api_response.candidates[0].content
            messages.append(assistant_content)

            if is_verbose_cli_arg:
                print("Assistant's turn added to messages:")
                assistant_text_parts = []
                function_calls_requested = []
                for part in assistant_content.parts:
                    if part.text:
                        assistant_text_parts.append(part.text.strip())
                    if part.function_call:
                        fc = part.function_call
                        function_calls_requested.append(fc)
                        print(f"  Function Call Requested: {fc.name}({dict(fc.args)})")
                if assistant_text_parts:
                     print(f"  Text: {' '.join(assistant_text_parts)}")
            
            function_calls_to_execute = [part.function_call for part in assistant_content.parts if part.function_call]

            if function_calls_to_execute:
                for fc_to_exec in function_calls_to_execute:
                    tool_response_content: types.Content = call_function(fc_to_exec, verbose=is_verbose_cli_arg)
                    messages.append(tool_response_content) 
                    if is_verbose_cli_arg:
                        if tool_response_content.parts and tool_response_content.parts[0].function_response:
                            fr_part = tool_response_content.parts[0].function_response
                            print("Tool response added to messages:")
                            print(f"  Function Executed: {fr_part.name}")
                            print(f"  Response Data: {fr_part.response}")
                        else:
                            print("  Tool response was empty or malformed.")
            else:
                print("\nFinal response from assistant (no further function calls):")
                final_text = "".join(part.text for part in assistant_content.parts if part.text if part.text)
                print(final_text.strip())
                break 
            
            if is_verbose_cli_arg:
                print(f"Current messages count: {len(messages)}")

    elif is_verbose_cli_arg:
        print("verbose mode (non-agent)")
        print(f"User prompt: '{prompt}'")
        response_dict: dict = get_llm_response(prompt, is_verbose=True, agent_mode=False)
        for key, value in response_dict.items():
            print(f"{key}: {value}")
    else:
        print("non-verbose mode (non-agent)")
        get_llm_response(prompt, is_verbose=False, agent_mode=False)
    
    '''response: str = get_llm_response(prompt)
    for key, value in response.items():
        print(f"{key}: {value}")'''

    

if __name__ == "__main__":
    # prompt: str = "give me a cool prompt to ask an AI"
    # prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    main()
    
    '''response: str = get_llm_response(prompt)
    for key, value in response.items():
        print(f"{key}: {value}")'''