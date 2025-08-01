import os
import sys
from dotenv import load_dotenv
import traceback

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request,
 make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the
working directory.
You do not need to specify the working directory in your function 
calls as it is automatically injected for security reasons. Provide necessary arguments for these functions 
"""

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

function_map = {
    'get_files_info':get_files_info,
    'get_file_content':get_file_content,
    'run_python_file':run_python_file,
    'write_file':write_file,
}

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call, verbose=False):
    function_call.args['working_directory'] = "./calculator/"
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    if function_call.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    
    function_result = function_map[function_call.name](**function_call.args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": function_result},
            )
        ],
    )

NUM_ITERATIONS = 6
for i in range(0,NUM_ITERATIONS):
    print("------------------")
    print(f"ITERATION # {i}")
    print("------------------")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
        )
        candidates = response.candidates

        for candidate in candidates:
            messages.append(candidate.content)
        

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        if "--verbose" in sys.argv[2:]:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        if not response.function_calls:
            print(response.text)
            continue
        function_calls = response.function_calls
        for call in function_calls:
            print(f"Calling function: {call.name}({call.args})")
            function_call_result =  call_function(call, verbose=True)
            print("==========================")
            if function_call_result.parts[0].function_response.response:
                # print(f"-> {function_call_result.parts[0].function_response.response}")
                func_response = function_call_result.parts[0].function_response.response
                name = function_call_result.parts[0].function_response.response
                print(func_response)
                response_message = types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(response=func_response,
                         name = call.name)                       
                    ],
                )
                messages.append(response_message)
            else:
                raise Exception("Function response doesn't exist")
        
        # if response.text:
        print(response.text)
            # break
    except Exception as e:
        print(e)
        traceback.print_exc() # Prints the full traceback to sys.stderr by default


