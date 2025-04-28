
def load_prompt_from_file(file_path):
   """
   Load Prompt from File
   ---------------------
   
   Load a prompt template from a file.
   This function reads the contents of a file and returns it as a string.
   If the file is not found, it raises a FileNotFoundError.
   
   Params:
      file_path (str): The path to the file containing the prompt template.
      
   Returns:
      str: The contents of the file as a string.
      
   Raises:
      FileNotFoundError: If the specified file does not exist.
      TypeError: If the file_path is not a string.
      ValueError: If the file_path is empty.
   """
   if file_path is None:
      raise TypeError("File path cannot be None")
      
   if not isinstance(file_path, str):
      raise TypeError("File path must be a string")
      
   if not file_path.strip():
      raise ValueError("File path cannot be empty")
   
   with open(file_path, 'r') as file:
      return file.read()