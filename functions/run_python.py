import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    try:
        working_dir_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        if os.path.commonpath([full_path, working_dir_path]) != working_dir_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if full_path.split(".")[-1] != 'py':
            return f'Error: "{file_path}" is not a Python file.'

        output = subprocess.run(['python', file_path],timeout=30, capture_output=True,
            cwd = working_directory)
        stdout_text = output.stdout.decode('utf-8') if output.stdout else ""
        stderr_text = output.stderr.decode('utf-8') if output.stderr else ""

        result = ""

        if output.returncode != 0:

            result += f"Process exited with code {output.returncode}"

        if stdout_text == "" and stderr_text == "": 
            
            result += "No output produced."
            return result

        result += f"STDOUT: {stdout_text}\n"
        result += f"STDERR: {stderr_text}\n"
        return result.strip()  

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path which this needs to run. Must be provided.",
            ),
        },
    ),
)