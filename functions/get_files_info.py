import os
from google import genai

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        # Check to see if the target directory is valid
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check to see if supplied directory arg is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: {directory} is not a directory'

        dir_contents = os.listdir(target_dir)
        dir_listing = []
        for file in dir_contents:
            filepath = target_dir + '/' + file
            dir_listing.append(f'{file}: file_size={os.path.getsize(filepath)}, is_dir={os.path.isdir(filepath)}')
        
        return "\n".join(dir_listing)

    except Exception as e:
        return f'Error: standard library function call: {e}'

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)