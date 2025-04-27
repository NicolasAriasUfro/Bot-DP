from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from app.utils.load_prompt import load_prompt_from_file
from app.utils.logger import Logger
from app.config.config import WEATHER_API_KEY, OLLAMA_URL, OLLAMA_MODEL, WEATHER_PROMPT
from langchain.tools import StructuredTool
from langchain.agents import (create_react_agent, AgentExecutor)
import requests
import json

class WeatherAgent:
   def __init__(self):
      self.llm = OllamaLLM(
         model=OLLAMA_MODEL, 
         base_url=OLLAMA_URL, 
         temperature=0,
      )
      self.logger = Logger()
      self.template = load_prompt_from_file(WEATHER_PROMPT)
      self.agent_executor = self.get_agent()
      self.logger.log(f"Weather agent initialized with model: {OLLAMA_MODEL}")
   
   def get_weather(self, input_str: str) -> dict:
      """
      Search for the current weather in a given city.
      
      Params:
         input_str (str): A string containing city and optional coordinates either as JSON or in format 
                        "city='Madrid', lat=40.4168, lon=-3.7038, part=''"
                        or simply "Madrid" for city name only
         
      Returns:
         dict: The weather data for the given city.
      """
      self.logger.log("[WeatherAgent] Weather function called")
      try:

         self.logger.log(f"[WeatherAgent] Input string: {input_str}")
         # Parse the input to extract parameters   
         params = {}
         
         # Check if input is already a dict
         if isinstance(input_str, dict):
               params = input_str
         # Check if input is a JSON string
         elif isinstance(input_str, str):
               input_str = input_str.strip()
               
               # Simple handling for plain city names
               if '=' not in input_str and not (input_str.startswith('{') and input_str.endswith('}')):
                  # Treat simple strings as city names
                  params = {'city': input_str}
               elif input_str.startswith('{') and input_str.strip().endswith('}'):
                  try:
                     params = json.loads(input_str)
                  except json.JSONDecodeError as e:
                     self.logger.log_error(f"[WeatherAgent] Error parsing JSON input: {e}")
                     return {"error": f"Invalid JSON format: {str(e)}"}
               else:
                  # Parse key-value pairs from string format
                  parts = input_str.split(',')
                  for part in parts:
                     part = part.strip()
                     if '=' in part:
                           key_value = part.split('=', 1)  # Split on first = only
                           if len(key_value) == 2:
                              key = key_value[0].strip()
                              value = key_value[1].strip().strip("'\"")
                              # Convert numeric values to proper types
                              try:
                                 if '.' in value and any(c.isdigit() for c in value):
                                       params[key] = float(value)
                                 elif value.isdigit():
                                       params[key] = int(value)
                                 else:
                                       params[key] = value
                              except ValueError: 
                                 params[key] = value
         
         # Extract parameters with default values
         city = params.get('city', '')
         lat = params.get('lat', None)
         lon = params.get('lon', None)
         part = params.get('part', '')
         units = params.get('units', 'metric')  
         lang = params.get('lang', 'es')
         
         # Validate required parameters
         if not city and (lat is None or lon is None):
            self.logger.log_error("[WeatherAgent] Missing required parameters: either city or both lat and lon must be provided")
            return {"error": "Missing required parameters: either city or both lat and lon must be provided"}
         
         # Construct API request
         url = "https://api.openweathermap.org/data/2.5/weather"
         api_params = {
               "appid": WEATHER_API_KEY,
               "units": units,
               "lang": lang,
               "part": part
         }
         
         # Set either city or coordinates
         if lat is not None and lon is not None:
               try:
                  api_params["lat"] = float(lat)
                  api_params["lon"] = float(lon)
                  self.logger.log(f"[WeatherAgent] Using coordinates: Latitude: {lat}, Longitude: {lon}")
               except (ValueError, TypeError):
                  self.logger.log_error("[WeatherAgent] Invalid coordinates: lat and lon must be numeric values")
                  return {"error": "Invalid coordinates: lat and lon must be numeric values"}
         else:
               api_params["q"] = city
               self.logger.log(f"[WeatherAgent] Using city name: {city}")
         
         # Make the request
         self.logger.log(f"Making API request to {url} with params: {api_params}")
         request = requests.get(url, params=api_params)
         request.raise_for_status()
         
         # Return the JSON response
         return request.json()
      
      except requests.exceptions.RequestException as e:
         self.logger.log_error(f"[WeatherAgent] Error fetching weather data: {e}")
         return {"error": f"API request failed: {str(e)}"}
      except Exception as e:
         self.logger.log_error(f"[WeatherAgent] Error processing input: {e}")
         return {"error": f"[WeatherAgent] Could not process input: {str(e)}"}
      
   def get_agent(self):
      """
         Get the weather agent.
         
         Returns:
            AgentExecutor: The weather agent executor.
      """
      template = self.template
      
      prompt = PromptTemplate(
         template=template,
         input_variables=["input", "tools", "tool_names", "agent_scratchpad"], 
      )

      tools_for_agent = [
         StructuredTool.from_function(
            name="get_weather",
            func=self.get_weather,
            description="Get current weather information for a city. Input should be just the city name as a simple string (e.g. 'Santiago'). Returns temperature and weather conditions for the location. ALWAYS separate your Thought and Final Answer steps after receiving weather data.",
         )
      ]
            
      weather_agent = create_react_agent(
         llm=self.llm, 
         tools=tools_for_agent,
         prompt=prompt
      )

      return AgentExecutor(
         agent=weather_agent, 
         tools=tools_for_agent, 
         verbose=True,
         # handle_parsing_errors=True, 
         # max_iterations=2,  
      )
   