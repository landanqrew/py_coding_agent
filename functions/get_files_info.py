import os

def get_files_info(working_directory: str, directory: str | None = None, print_result: bool = True) -> str:
    """
    Get the information of the files in a directory.
    Args:
        working_directory: The working directory.
        directory: The directory to get the information of.
    Returns:
        A string with the information of the files in the directory.
    """
    if directory is None:
        directory = working_directory
    if not is_sub_dir(working_directory, directory):
        raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if directory[0] != "/":
        directory = working_directory + "/" + directory
    if not os.path.isdir(directory):
        raise ValueError(f'Error: "{directory}" is not a directory')
    dir_info: str = ""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        dir_info += get_file_info(item_path) + "\n"
    if print_result:
        print(dir_info[:-1] if len(dir_info) > 0 and dir_info[-1] == "\n" else dir_info)
    return dir_info[:-1] if len(dir_info) > 0 and dir_info[-1] == "\n" else dir_info

def is_sub_dir(working_directory: str, directory: str) -> bool:
    """
    Check if a directory is a subdirectory of the working directory.
    Args:
        working_directory: The working directory.
        directory: The directory to check.
    Returns:
        True if the directory is a subdirectory of the working directory, False otherwise.
    """
    if working_directory == directory: # Handles cases like (".", ".")
        return True

    # Resolve working_directory to a final, absolute, normalized path
    wd_final = os.path.normpath(os.path.abspath(working_directory))

    # Resolve directory to a final, absolute, normalized path.
    # If directory is relative, it's considered relative to wd_final (matching original implied logic but now safer).
    if directory[0] != '/':
        dir_final = os.path.normpath(os.path.join(wd_final, directory))
    else: # directory is already absolute
        dir_final = os.path.normpath(directory)

    # Check if dir_final is the same as or starts with wd_final.
    # dir_final == wd_final covers the case where they are the same directory.
    # dir_final.startswith(wd_final + os.sep) covers true subdirectories.
    if dir_final == wd_final or dir_final.startswith(wd_final + os.sep):
        return True
            
    return False

def get_file_info(item_path: str) -> str:
    """
    Get the information of a file.
    Args:
        item_path: The path to the file.
    Returns:
        A string with the information of the file.
    """
    info: os.stat_result = os.stat(item_path)
    file_size: str = f"file_size={info.st_size} bytes"
    is_dir: bool = os.path.isdir(item_path)
    return f"{item_path.split('/')[-1]}: {file_size}, is_dir={is_dir}"
    

if __name__ == "__main__":
    stats = get_files_info("calculator", "pkg")
    print(stats)