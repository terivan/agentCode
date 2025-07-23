import os
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

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