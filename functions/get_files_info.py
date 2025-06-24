"""
Create a new directory called functions. Inside, create a new file called get_files_info.py. Inside, write this function:
def get_files_info(working_directory, directory=None):

If the directory argument is outside the working_directory, return a string with an error:
f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

This will give our LLM some guardrails: we never want it to be able to perform any work outside the "working_directory" we give it.

Without this restriction, the LLM might go running amok anywhere on the machine, reading 
sensitive files or overwriting important data. This is a very important step that we'll bake into every function the LLM can call.

If the directory argument is not a directory, again, return an error string:
f'Error: "{directory}" is not a directory'

We're returning strings here rather than raising errors because we want get_files_info
 to always return a string that the LLM can read. This way, when it encounters an error,
  it can try again with a different approach.

Build and return a string representing the contents of the directory. It should use this format:
- README.md: file_size=1032 bytes, is_dir=False
- src: file_size=128 bytes, is_dir=True
- package.json: file_size=1234 bytes, is_dir=False

I've listed useful standard library functions in the tips section.

If any errors are raised by the standard library functions, 
catch them and instead return a string describing the error. Always prefix error strings with "Error:".

os.path.abspath(): Get an absolute path from a relative path
os.path.join(): Join two paths together safely (handles slashes)
.startswith(): Check if a string starts with a substring
os.path.isdir(): Check if a path is a directory
os.listdir(): List the contents of a directory
os.path.getsize(): Get the size of a file
os.path.isfile(): Check if a path is a file
.join(): Join a list of strings together with a separator
"""
import os

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

    print(stdOut_string)
  except Error as e:
    return f"Error: {e}"