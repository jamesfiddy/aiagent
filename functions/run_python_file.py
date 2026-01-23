import os
import subprocess

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

        output_string = ""
        if(program_execution.returncode != 0):
            output_string += f'Process exited with code {program_execution.returncode}'

        if not program_execution.stdout or program_execution.stderr:
            output_string += "No output produced"
        
        else:
            output_string += f'STDOUT: {program_execution.stdout}, STDERR: {program_execution.stderr}'

        return output_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"