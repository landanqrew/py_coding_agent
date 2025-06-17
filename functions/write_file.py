import os
from functions.get_file_content import is_sub_file

def write_file(working_directory: str, file_path: str, content: str) -> None:
    """
    Write content to a file.
    Args:
        working_directory: The working directory.
        file_path: The path to the file.
        content: The content to write to the file.
    """
    if not is_sub_file(working_directory, file_path):
        raise ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    fp_final = os.path.normpath(os.path.join(working_directory, file_path))
    if os.path.isdir(fp_final):
        raise ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')
    
    try:
        with open(fp_final, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        raise Exception(f'Error: {e}')
