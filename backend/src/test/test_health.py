import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app
from fastapi.testclient import TestClient

class HealthRequest(unittest.TestCase):
   def setUp(self):
      # Create a test client for making requests
      self.client = TestClient(app)
   
   def test_health_check(self):
      # Simulate a health check request
      response = self.client.get('/api')
      
      # Check if the response is 200 OK
      self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
   unittest.main()