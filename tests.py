# Create a new tests.py file in the root of your project. When executed directly, it should:
# Run get_files_info("calculator", ".") and print the result to the console.
# Run get_files_info("calculator", "pkg") and print the result to the console.
# Run get_files_info("calculator", "/bin") and print the result to the console (this should return an error string)
# Run get_files_info("calculator", "../") and print the result to the console (this should return an error string)
from functions.get_files_info import get_files_info

print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))