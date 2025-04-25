def load_prompt_from_file(file_path):
   """
   Load a prompt template from a file.
   This function reads the contents of a file and returns it as a string.
   If the file is not found, it prints an error message and returns None.
   Args:
      file_path (str): The path to the file containing the prompt template.
   Returns:
      str: The contents of the file as a string, or None if the file is not found.
   """
   try:
      with open(file_path, 'r') as file:
         return file.read()
   except FileNotFoundError:
      print(f"Error: The file {file_path} was not found.")
      