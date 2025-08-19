import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    verbose = False
    if len(sys.argv) > 1:
        system_prompt = """
            You are a helpful AI coding agent.

            When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

            - List files and directories
            - Read file contents
            - Execute Python files with optional arguments
            - Write or overwrite files

            You are on the same directory of the calculator
            You are called repeatedly, so you can actually do the plan you make up at the very beginning.
            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
        user_prompt = sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
            ]
        )
        i = 0
        while i < 20:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt)
                )
            for answer in response.candidates:
                messages.append(answer)
            
            highest_arg = len(sys.argv) -1
            if sys.argv[highest_arg] == '--verbose':
                verbose = True
            function_answer = []
            if response.function_calls!= None:
                for function_call in response.function_calls:
                    function_response = call_function(function_call, verbose=verbose)
                    #messages.append(types.Content(role="user", text=function_response.parts[0]))
                    if not function_response.parts[0].function_response.response:
                        raise Exception("Fatal Exception")
                    else:
                        highest_arg = len(sys.argv) -1
                        argument = sys.argv[highest_arg]
                        if argument == '--verbose':
                            print(f"-> {function_response.parts[0].function_response.response}")
                    function_answer.append(function_response.parts[0])
                    messages.append(types.Content(role="user", parts=function_answer))
            if response.text:
                i = 20
                print(response.text)
            i+=1            
        
        usage_metadata = response.usage_metadata
        #if len(sys.argv) == 3: 
        #    argument = sys.argv[2]
        #    if verbose:
        #        print(f'User prompt: {user_prompt}')
        #        print(f'Prompt tokens: {usage_metadata.prompt_token_count}')
        #        print(f'Response tokens: {usage_metadata.candidates_token_count}')
    else:
        print("Need an argument !")
        sys.exit(1)


if __name__ == "__main__":
    main()


