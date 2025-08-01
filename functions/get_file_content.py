import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    print(full_path)
    try:
        if os.path.isfile(full_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
        if os.path.getsize(full_path) > MAX_CHARS:
            file_content_string += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
        return file_content_string
        
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file concent of files constrained by their working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path which contnts to list. Must be provided.",
            ),
        },
    ),
)


