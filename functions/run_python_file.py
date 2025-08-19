import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file to run, relative to the working directory. Must be provided or return an error message",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="optional arguments if they are needed for a python file to run",
            ),
         },
    ),
)



def run_python_file(working_directory, file_path, args=[]):
    try:
        relative_path = "." + os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(relative_path)
        if working_directory not in os.path.abspath(abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File "{file_path}" not found.'
        if file_path[:-3] != ".py":
            f'Error: "{file_path}" is not a Python file.'
        
        if len(args) == 0:
            completed_process = subprocess.run(["uv", "run", relative_path], timeout=30, capture_output=True)
        else:
            completed_process = subprocess.run(["uv", "run", relative_path, args[0]], timeout=30, capture_output=True)
        
        
        #print(completed_process)
        #s = "STDOUT: " + completed_process.stdout +"\nSTDERR: " + completed_process.stderr

        s = ""
        s = s + "STDOUT:" + str(completed_process.stdout) + '\n' + "STDERR:" + str(completed_process.stderr)
        if completed_process.returncode != 0:
            s = s + '\n' + "Process exited with code" + str(completed_process.returncode)
        else:
            s = s + '\n' + "No output produced"
        return s
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
