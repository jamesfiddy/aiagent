import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    # Check to see if the target directory is valid
    if valid_target_dir == False:
        f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check to see if supplied directory is actually a directory
    if os.path.isdir(directory) == False:
        f'Error: "{directory}" is not a directory'