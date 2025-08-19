import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads the content of a file in the specified directory , constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to read, relative to the working directory. Must be provided or return an error message",
            ),
         },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        relative_path = "." + os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(relative_path)
        if working_directory not in os.path.abspath(relative_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        MAX_CHARS = 10000

        with open(abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) > MAX_CHARS-1:
            file_content_string = file_content_string + "[...File \"" + file_path + "\" truncated at 10000 characters]"
        return file_content_string
    except Exception as e:
        return f'Error:{e}'