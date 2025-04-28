import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app
from fastapi.testclient import TestClient

class TestWeatherAgent(unittest.TestCase):
   def setUp(self):
      # Create a test client for making requests
      self.client = TestClient(app)

   def test_query_with_weather_santiago(self):
      # Simulate a health check request
      response = self.client.post('/assistant/query', json={'query': '¿Cuál es el clima en Santiago?'})
      
      print(f'Response: {response.json()}')
      
      # Check if the response is 200 OK
      self.assertEqual(response.status_code, 200)
      
   def test_query_with_weather_temuco(self):
      # Simulate a health check request
      response = self.client.post('/assistant/query', json={'query': 'dame el clima de Temuco'})
      
      print(f'Response: {response.json()}')
      
      # Check if the response is 200 OK
      self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
   unittest.main()
