import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
         },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        relative_path = "." + os.path.join(working_directory, directory)
        abs_path = os.path.abspath(relative_path)
        if working_directory not in os.path.abspath(relative_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_path):
            return f'Error: "{directory}" is not a directory'
    
        directory_content = os.listdir(abs_path)
        for i in range(0, len(directory_content)): 
            file_size = os.path.getsize(abs_path + "/" +directory_content[i])
            if os.path.isdir(abs_path+"/"+directory_content[i]):
                is_dir = "True"
            else:
                is_dir = "False"
            s = ": file_size="+ str(file_size) + " bytes, is_dir=" + is_dir 
            directory_content[i] = "- " + directory_content[i] + s
        directory_content = '\n'.join(directory_content)

        return directory_content
    except Exception as e:
        return f'Error :{e}'
