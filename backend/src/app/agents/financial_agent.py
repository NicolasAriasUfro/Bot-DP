from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import StructuredTool
from langchain_ollama.llms import OllamaLLM
from app.utils.logger import Logger
from app.utils.load_prompt import load_prompt_from_file
from app.config.config import OLLAMA_URL, OLLAMA_BASE_MODEL, FINANCIAL_PROMPT
import json 
import requests

class FinancialAgent:
   def __init__(self) -> None:
      self.llm = OllamaLLM(
         model=OLLAMA_BASE_MODEL, 
         base_url=OLLAMA_URL,
         temperature=0, 
      )
      self.logger = Logger()
      self.template = load_prompt_from_file(FINANCIAL_PROMPT)
      self.agent_executor = self.__finalcial_agent()
      self.logger.info(f"Financial agent initialized with model: {OLLAMA_BASE_MODEL}")
   
   def get_indicador(self, indicator: str):
      """
      Get Indicator
      -------------
      
      Get financial information.
      This function fetches data from the Mindicator API for a given indicator.
      It constructs the URL using the indicator name and makes a GET request to the API.
      The response is expected to be in JSON format, and the function returns the data if the request is successful.
      If the request fails, an exception is raised with an error message.
         
      Example:
         get_indicator(dolar)
      Example:
         get_indicator(uf)
      
      Params: 
         indicator (str): The indicator to fetch.
      Returns:
         dict: The data for the indicator.
      """
      try:
         url = f"https://mindicador.cl/api/{indicator}"
         self.logger.info(f"[FinancialAgent] Fetching data from URL: {url}")
         data = requests.get(url).json()
         if data.get("error") is None:
            return data
         else:
            self.logger.error(f"[FinancialAgent] Error fetching indicator {indicator}: {data['message']}")
            raise Exception(f"Error fetching indicator {indicator}: {data['message']}") 
      except requests.exceptions.RequestException as e:
         self.logger.error(f"[FinancialAgent] Request error for indicator {indicator}: {str(e)}")
         raise Exception(f"Error fetching indicator {indicator}: {str(e)}")
      except json.JSONDecodeError as e:
         self.logger.error(f"[FinancialAgent] JSON decode error for indicator {indicator}: {str(e)}")
         raise Exception(f"Error parsing JSON response for indicator {indicator}: {str(e)}")
      except Exception as e:
         self.logger.error(f"[FinancialAgent] Unexpected error for indicator {indicator}: {str(e)}")
         raise Exception(f"An unexpected error occurred: {str(e)}")   
   
   def __finalcial_agent(self) -> AgentExecutor:
      """
      Financial Agent
      ---------------
      
      Get the financial agent.
      This function creates a financial agent using the Langchain library.
      It uses the OllamaLLM model and a prompt template to generate responses.
      The agent is designed to fetch financial data from the Mindicator API.
      
      Returns:
         AgentExecutor: The financial agent executor.
      """
      prompt = PromptTemplate(
         template=self.template,
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
            description="""
            Get financial information.
            This function fetches data from the Mindicator API for a given indicator.
            IMPORTANT: Use without quotes around parameters.
            Examples:
            - For dolar: get_indicador(dolar)
            - For UF: get_indicador(uf)
            - For euro: get_indicador(euro)
            """,
         )
      ]

      financial_agent = create_react_agent(
         llm=self.llm, 
         tools=tools_for_agent,
         prompt=prompt
      )

      return AgentExecutor(
         agent=financial_agent, 
         tools=tools_for_agent, 
         handle_parsing_errors=True,
         verbose=True,
         return_intermediate_steps=True 
      )