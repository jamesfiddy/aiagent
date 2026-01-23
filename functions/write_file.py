import os
from google import genai

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs

        # Check to see if the target directory is valid
        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        # Check to see if the file path is a directory (cannot write to a directory)
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(abs_file_path), mode=0o777, exist_ok=True)
        
        with open(abs_file_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: standard library function call: {e}'
    
schema_write_file_info = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes to the file specified",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the Python file you want to run",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="What you want to write to the file",
            )
        },
        required=["file_path", "content"]
    ),
)