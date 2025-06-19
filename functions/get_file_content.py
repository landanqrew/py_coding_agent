import os

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Get the content of a file.
    Args:
        working_directory: The working directory.
        file_path: The path to the file.
    Returns:
        A string with the content of the file.
    """
    try:
        if not is_sub_file(working_directory, file_path):
            raise ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        fp_final = get_file_relative_path(working_directory, file_path)
        if not fp_final or not os.path.isfile(fp_final):
            raise ValueError(f'Error: File not found or is not a regular file: "{file_path}" => "{fp_final}"')

        print(f"begin reading file: {fp_final}")
        with open(fp_final, "r") as f:
            print(f"contents:")
            contents: str = f.read()
            print(f"contents length: {len(contents)}")
            return contents if len(contents) <= 10000 else contents[:10000] + '[...File "{file_path}" truncated at 10000 characters]'
    except ValueError as e:
        raise ValueError(e)
    except Exception as e:
        raise Exception(f'Error: {e}')

def is_sub_file(working_directory: str, file_path: str) -> bool:
    """
    Check if a file is a child of the working directory.
    Args:
        working_directory: The working directory.
        file_path: The file to check.
    Returns:
        True if the file is a child of the working directory, False otherwise.
    """
    if working_directory == file_path: # Handles cases like (".", ".")
        return True

    # Resolve working_directory to a final, absolute, normalized path
    wd_final = os.path.normpath(os.path.abspath(working_directory))

    # Resolve file_path to a final, absolute, normalized path.
    # If file_path is relative, it's considered relative to wd_final (matching original implied logic but now safer).
    if file_path[0] != '/':
        fp_final = os.path.normpath(os.path.join(wd_final, file_path))
    else: # file_path is already absolute
        fp_final = os.path.normpath(file_path)

    # Check if fp_final is the same as or starts with wd_final.
    # fp_final == wd_final covers the case where they are the same directory.
    # fp_final.startswith(wd_final + os.sep) covers true subdirectories.
    if fp_final == wd_final or fp_final.startswith(wd_final + os.sep):
        return True
            
    return False

def get_file_relative_path(working_directory: str, file_path: str) -> str | None:
    """
    Get the relative path of a file.
    Args:
        working_directory: The working directory.
        file_path: The file to check.
    Returns:
        The relative path of the file.
    """
    file_path_parts = file_path.split(os.sep)
    for item in os.listdir(working_directory):
        item_path = os.path.join(working_directory, item)
        if item == file_path_parts[0]:
            if len(file_path_parts) == 1:
                return item_path
            else:
                search_results = get_file_relative_path(item_path, "/".join(file_path_parts[1:]))
                if search_results:
                    return search_results
        else:
            if os.path.isdir(item_path):
                # print(f"begin searching in {item_path} for {file_path}")
                search_results = get_file_relative_path(item_path, file_path)
                if search_results:
                    return search_results
    return None
            
                


if __name__ == "__main__":
    print(get_file_relative_path(working_directory=".", file_path='lorem.txt'))