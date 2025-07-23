# Create a new tests.py file in the root of your project. When executed directly, it should:
# Run get_files_info("calculator", ".") and print the result to the console.
# Run get_files_info("calculator", "pkg") and print the result to the console.
# Run get_files_info("calculator", "/bin") and print the result to the console (this should return an error string)
# Run get_files_info("calculator", "../") and print the result to the console (this should return an error string)
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))


