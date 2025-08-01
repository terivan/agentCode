import os
from google.genai import types

def get_files_info(working_directory, directory=None):
  try:
    working_dir_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    # print(working_dir_path)
    # print(full_path)
    if not full_path.startswith(working_dir_path):
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(full_path) == False:
      return f'Error: "{directory}" is not a directory'

    list_of_files = os.listdir(full_path)
    stdOut_string = ""
    for filename in list_of_files:
      file_path = os.path.join(full_path, filename)
      stdOut_string += f"- {filename}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"

    return stdOut_string
  except Exception as e:
    return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, \
                relative to the working directory. Must be provided.",
            ),
        },
    ),
)

