import os
import subprocess
from google import genai

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs

        # Check to see if the target directory is valid
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check to see if file path exists and is not a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check to see if the file ends with .py
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]

        if args is not None:
            for arg in args:
                command.append(arg)

        program_execution = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = []
        if program_execution.returncode != 0:
            output.append(f"Process exited with code {program_execution.returncode}")
        if not program_execution.stdout and not program_execution.stderr:
            output.append("No output produced")
        if program_execution.stdout:
            output.append(f"STDOUT:\n{program_execution.stdout}")
        if program_execution.stderr:
            output.append(f"STDERR:\n{program_execution.stderr}")
        return "\n".join(output)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_info = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file specified at the file path, including any arguments",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the Python file you want to run",
            ),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python script",
                items=genai.types.Schema(type=genai.types.Type.STRING)
            )
        },
        required=["file_path"]
    ),
)