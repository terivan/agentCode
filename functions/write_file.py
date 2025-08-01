import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:    
        working_dir_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.commonpath([full_path, working_dir_path]) != working_dir_path:
            return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
            except Exception as e:
                return f'Error: Could not create directory for file {full_path}'

        if os.path.isdir(full_path):
            return f'Error: "{full_path}" is a directory, not a file'
        try:
            with open(full_path, "w") as f:
                f.write(content)
        except Exception as e:
            return f'Error: could not write file {full_path}; {e}'
        return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path which this needs to run. Must be provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content of the file to write. Must be provided.",
            ),
        },
    ),
)