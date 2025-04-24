from src.app.config.config import WEATHER_API_KEY, TUBE_API_KEY, SOURCE_CONTRY_CODE 
from src.app.utils.load_promt import load_prompt_from_file
import requests
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.tools import StructuredTool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain_core.output_parsers import StrOutputParser

class AssistantService:
   def __init__(self):
      self.weather_api_key = WEATHER_API_KEY
      self.tube_api_key = TUBE_API_KEY
      self.source_country_code = SOURCE_CONTRY_CODE

   def get_indicador(self, indicator: str):
      """
      Get financial information.
      This function fetches data from the Mindicator API for a given indicator.
      It constructs the URL using the indicator name and makes a GET request to the API.
      The response is expected to be in JSON format, and the function returns the data if the request is successful.
      If the request fails, an exception is raised with an error message.
         
         Example:
            get_indicator("dolar")
         Example:
            get_indicator("uf")
         
         Params  
            indicator (str): The indicator to fetch.
         Returns:
            dict: The data for the indicator.
      """
      url = f"https://mindicador.cl/api/{indicator}"
      data = requests.get(url).json()
      if data.get("error") is None:
         return data
      else:
         raise Exception(f"Error fetching indicator {indicator}: {data['message']}")  
   
   

   def finalcial_agent(self):
      financial_llm = OllamaLLM(model="llama3", base_url="http://localhost:11434", temperature=0)

      template = load_prompt_from_file("../prompts/financial.txt") 

      prompt = PromptTemplate(
         template=template,
         input_variables=[
            "input", 
            "tools", 
            "tool_names",
            "agent_scratchpad", 
         ], 
      )

      tools_for_agent = [
         StructuredTool.from_function(
            name="get_indicador",
            func=self.get_indicador,
            description="""Get financial information.
         This function fetches data from the Mindicator API for a given indicator.
         It constructs the URL using the indicator name and makes a GET request to the API.
         The response is expected to be in JSON format, and the function returns the data if the request is successful.
         If the request fails, an exception is raised with an error message.
            
            Example:
               get_indicador(dolar)
            Example:
               get_indicador(uf)
            
            Params  
               indicator (str): The indicator to fetch.
            Returns:
               dict: The data for the indicator.
         """,
         )
      ]

      financial_agent = create_react_agent(
         llm=financial_llm, 
         tools=tools_for_agent,
         prompt=prompt
      )

      financial_agent_executor = AgentExecutor(
         agent=financial_agent, 
         tools=tools_for_agent, 
         verbose=True,
      )
      return financial_agent_executor
   
   def get_notices(self):
      """
      get news from the api.
      the response is expected to be in json format, and the function returns the data if the request is successful.
      if the request fails, an exception is raised with an error message.
         
         example:
            get_notices()
         
         returns:
            dict: the data for the notice. 
      """
      url = f"https://api.apitube.io/v1/news/everything?api_key={TUBE_API_KEY}&source.country.code={SOURCE_CONTRY_CODE}"
      data = requests.get(url).json()
      if data.get("error") is None:
         return data
      else:
         raise Exception("Error fetching")  
      

   def notice_agent(self):
      notice_llm = OllamaLLM(model="llama3", base_url="http://localhost:11434", temperature=0)

      template = load_prompt_from_file("../prompts/notice.txt") 

      prompt = PromptTemplate(
         template=template,
         input_variables=[
            "input", 
            "tools", 
            "tool_names",
            "agent_scratchpad", 
         ], 
      )

      tools_for_agent = [
         StructuredTool.from_function(
            name="get_notices",
            func=self.get_notices,
            description="""
            get news from the api.
            the response is expected to be in json format, and the function returns the data if the request is successful.
            if the request fails, an exception is raised with an error message.
            
            example:
               get_notices()
            
            returns:
               dict: the data for the notice.
            """,
         )
      ]

      notice_agent = create_react_agent(
         llm=notice_llm, 
         tools=tools_for_agent,
         prompt=prompt
      )

      notice_agent_executor = AgentExecutor(
         agent=notice_agent, 
         tools=tools_for_agent, 
         verbose=True,
         handle_parsing_errors=True,
      )

      return notice_agent_executor
      
   def get_weather(self, input_str: str) -> dict:
      """
         Search for the current weather in a given city.
         
         Params:
            input_str (str): A string containing city and optional coordinates either as JSON or in format "city='Madrid', lat=40.4168, lon=-3.7038, part=''"
            
         Returns:
            dict: The weather data for the given city.
      """
      try:
         import json
         print("Weather function called")
         print(f"Input string: {input_str}")
         # Parse the input to extract parameters
         params = {}
         
         # Check if input is already a dict
         if isinstance(input_str, dict):
            params = input_str
         # Check if input is a JSON string
         elif isinstance(input_str, str):
            input_str = input_str.strip()
            if input_str.startswith('{') and input_str.strip().endswith('}'):
               try:
                  params = json.loads(input_str)
               except json.JSONDecodeError as e:
                  print(f"Error parsing JSON input: {e}")
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
                        except:
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
               return {"error": "Missing required parameters: either city or both lat and lon must be provided"}
            
            # Construct API request
            url = "https://api.openweathermap.org/data/2.5/weather"
            api_params = {
               "q": city,
               "lat": lat,
               "lon": lon,
               "part": part,
               "appid": WEATHER_API_KEY,
               "units": units,
               "lang": lang,
            }
            
            # Set either city or coordinates
            if lat is not None and lon is not None:
               try:
                  api_params["lat"] = float(lat)
                  api_params["lon"] = float(lon)
                  print(f"Using coordinates: Latitude: {lat}, Longitude: {lon}")
               except (ValueError, TypeError):
                  return {"error": "Invalid coordinates: lat and lon must be numeric values"}
            else:
               api_params["q"] = city
               print(f"Using city name: {city}")
            
            # Make the request
            print(f"Making API request to {url} with params: {api_params}")
            request = requests.get(url, params=api_params)
            request.raise_for_status()
            
            # Return the JSON response
            return request.json()
      except requests.exceptions.RequestException as e:
         print(f"Error fetching weather data: {e}")
         return {"error": f"API request failed: {str(e)}"}
      except Exception as e:
         print(f"Error processing input: {e}")
         return {"error": f"Could not process input: {str(e)}"}

   def weather_agent(self):
      weather_llm = OllamaLLM(model="llama3", base_url="http://localhost:11434", temperature=0)

      template = load_prompt_from_file("../prompts/weather.txt") 

      prompt = PromptTemplate(
         template=template,
         input_variables=["question", "tools", "tool_names", "agent_scratchpad"], 
      )

      tools_for_agent = [
         StructuredTool.from_function(
            name="get_weather",
            func=self.get_weather,
            description="Get the weather data for a city. Required parameters: city (name of the city), optional: lat (latitude), lon (longitude), part (parts to exclude). If you don't know the city, don't use this tool.",
         )
      ]

      weather_agent = create_react_agent(
         llm=weather_llm, 
         tools=tools_for_agent,
         prompt=prompt
      )

      weather_agent_executor = AgentExecutor(
         agent=weather_agent, 
         tools=tools_for_agent, 
         verbose=True,
      )
      
      return weather_agent_executor
   
   def get_interpreter_agent(self):
      template = load_prompt_from_file("../prompts/interpreter.txt")
      
      interpreter_prompt = PromptTemplate(
         template=template,
         input_variables=["raw_response"],
      )

      llm_interpreter = OllamaLLM(
         model="llama3", 
         base_url="http://localhost:11434",
         temperature=0,
      )
      parser = StrOutputParser()
      interpreter_chain = interpreter_prompt | llm_interpreter | parser
      return interpreter_chain
   
   def query_weather(self, user_question):
      # Primer agente - obtiene los datos del clima
      weather_result = self.get_weather_agent().invoke(
         input={"input": user_question}
      )
      
      # Segundo agente - interpreta y presenta los datos
      friendly_response = self.get_interpreter_agent().invoke(
         {"raw_response": weather_result["output"]}
      )
      return friendly_response
      
   def query_financial(self, user_question):
      # Primer agente - obtiene los datos financieros
      financial_result = self.finalcial_agent().invoke(
         input={"input": user_question}
      )
      
      # Segundo agente - interpreta y presenta los datos
      friendly_response = self.get_interpreter_agent().invoke(
         {"raw_response": financial_result["output"]}
      )
      return friendly_response
   
   def query_notice(self, user_question):
      # Primer agente - obtiene los datos financieros
      notice_result = self.notice_agent().invoke(
         input={"input": user_question}
      )
      
      # Segundo agente - interpreta y presenta los datos
      friendly_response = self.get_interpreter_agent().invoke(
         {"raw_response": notice_result["output"]}
      )
      return friendly_response
   
   
      
            
