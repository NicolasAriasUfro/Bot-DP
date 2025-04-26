import unittest 

import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logger import Logger

class TestLogger(unittest.TestCase):
   def setUp(self):
      self.logger = Logger()

   def test_logger_initialization(self):
      self.assertIsNotNone(self.logger.logger)
      self.assertEqual(self.logger.logger.level, 20) 

if __name__ == "__main__":
   unittest.main()