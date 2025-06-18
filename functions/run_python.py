import os
from functions.get_file_content import is_sub_file

def run_python_file(working_directory: str, file_path: str) -> str:
    """
    Run a Python file.
    Args:
        working_directory: The working directory.
        file_path: The path to the file.
    """
    # abs_working_directory = os.path.abspath(working_directory) # not sure if this is needed
    # print(f"abs_working_directory: {abs_working_directory}")
    if not is_sub_file(working_directory, file_path):
        raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    fp_final = os.path.normpath(os.path.join(working_directory, file_path))
    if not os.path.exists(fp_final):
        raise ValueError(f'Error: File "{file_path}" not found.')
    if not os.path.isfile(fp_final):
        raise ValueError(f'Error: Item "{file_path}" is not a file.')
    if not file_path.endswith(".py"):
        raise ValueError(f'Error: "{file_path}" is not a Python file.')
    
    try:
        import subprocess
        result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=30, cwd=working_directory)
        output: str = f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        if result.stdout == "" or not result.stdout:
            output += "\nNo output produced."
        return output
    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")
