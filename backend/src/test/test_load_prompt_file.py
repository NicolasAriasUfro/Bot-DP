import unittest
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.load_prompt import load_prompt_from_file

class TestLoadPromptFile(unittest.TestCase):
   def test_load_prompt_file(self):
      # Base directories
      PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      SRC_DIR = os.path.join(PROJECT_ROOT + '/backend', 'src')

      # Application directories
      APP_DIR = os.path.join(SRC_DIR, 'app')
      PROMPTS_DIR = os.path.join(APP_DIR, 'prompts')
      
      NOTICE_PROMPT = os.path.join(PROMPTS_DIR, 'notice.txt')

      # Test with a valid file path
      prompt = load_prompt_from_file(NOTICE_PROMPT)
      
      assert prompt is not None
      
   def test_load_prompt_file_invalid(self):
      # Test with an invalid file path
      invalid_path = os.path.join('invalid', 'path', 'to', 'file.txt')
      
      with self.assertRaises(FileNotFoundError):
         load_prompt_from_file(invalid_path)
      
      


if __name__ == "__main__":
   unittest.main()