import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app
from fastapi.testclient import TestClient

class QueryRequest(unittest.TestCase):
   def setUp(self):
      # Create a test client for making requests
      self.client = TestClient(app)
      
   def test_empty_query(self):
      # Simulate query request
      response = self.client.post('/assistant/query', json={'query': ''})
      
      print(f'Response: {response.json()}')
      
      # Check if the response is 400 Bad Request
      self.assertEqual(response.status_code, 422)
   
   def test_query_with_weather(self):
      # Simulate a health check request
      response = self.client.post('/assistant/query', json={'query': '¿Cuál es el clima en Santiago?'})
      
      print(f'Response: {response.json()}')
      
      # Check if the response is 200 OK
      self.assertEqual(response.status_code, 200)

   def test_query_with_financial(self):
      # Simulate a health check request ``
      response = self.client.post('/assistant/query', json={'query': '¿Cuál es el valor del dolar?'})
      
      print(f'Response: {response.json()}')
      
      # Check if the response is 200 OK
      self.assertEqual(response.status_code, 200)
   
   def test_query_with_notice(self):
      # Simulate a health check request
      response = self.client.post('/assistant/query', json={'query': '¿Cuáles son las últimas noticias?'})
      
      print(f'Response: {response.json()}')
      
      # Check if the response is 200 OK
      self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
   unittest.main()
