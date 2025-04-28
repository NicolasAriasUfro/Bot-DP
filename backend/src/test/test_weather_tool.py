import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.weather_agent import WeatherAgent

class Test(unittest.TestCase):
  def testWeatherToolWithMadridCity(self):
    weather_agent = WeatherAgent()
    
    resp = weather_agent.get_weather('Madrid')
    print(f'Response: {resp}')
    
    self.assertIsNotNone(resp)
    self.assertIsInstance(resp, dict)
   
  def testWeatherToolWithSantiagoCity(self):
    weather_agent = WeatherAgent()
    
    resp = weather_agent.get_weather('Santiago')
    print(f'Response: {resp}')
    
    self.assertIsNotNone(resp)
    self.assertIsInstance(resp, dict)


# Añade este bloque para ejecutar los tests
if __name__ == "__main__":
  unittest.main()