import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.notice_agent import NoticeAgent

class Test(unittest.TestCase):
   def testNoticeTool(self):
      notice_agent = NoticeAgent()
      
      resp = notice_agent.get_notices()
      print(f'Response: {resp}')
      
      self.assertIsNotNone(resp)
      self.assertIsInstance(resp, dict)
   

# Añade este bloque para ejecutar los tests
if __name__ == "__main__":
   unittest.main()