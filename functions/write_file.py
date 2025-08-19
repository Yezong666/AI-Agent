import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write in a file, overwriting it by a content provided, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to write on, relative to the working directory. If file does not exist, will create it",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content who's gonna replace the content of the file sent to file_path",
            ),
         },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        relative_path = "." + os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(relative_path)
        if working_directory not in os.path.abspath(relative_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        file_name = ""
        i = len(relative_path) -1
        while (relative_path[i] != '/'):
            file_name = relative_path[i] + file_name
            i-=1
        print(os.path.exists(relative_path.strip("/"+file_name)))
        print(relative_path.strip(file_name))
        if not os.path.exists(relative_path.strip('/'+file_name)):
            os.makedirs(relative_path)
        if not os.path.exists(relative_path):
            with open(relative_path, "x") as f:
                f.close()
        with open(relative_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error:{e}'
    