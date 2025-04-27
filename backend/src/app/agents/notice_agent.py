from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.tools import StructuredTool
from langchain.agents import (create_react_agent, AgentExecutor)
from app.utils.load_prompt import load_prompt_from_file
from app.utils.logger import Logger
from app.config.config import SOURCE_CONTRY_CODE, OLLAMA_MODEL, OLLAMA_URL, TUBE_API_KEY, NOTICE_PROMPT
import requests

class NoticeAgent:
   def __init__(self):
      self.llm = OllamaLLM(
         model= OLLAMA_MODEL, 
         base_url=OLLAMA_URL,
         temperature=0,
      )
      self.template = load_prompt_from_file(NOTICE_PROMPT)
      self.agent_executor = self.__notice_agent()
      self.logger = Logger()
      self.logger.log(f"Notice agent initialized with model: {OLLAMA_MODEL}")
      
   def get_notices(self) -> dict:
      """
      get latest news from the noticeapi.
         
         example:
            get_notices()
         
         returns:
            dict: the data for the notice. 
      """
      url = f"https://api.apitube.io/v1/news/everything?api_key={TUBE_API_KEY}&source.country.code={SOURCE_CONTRY_CODE}&limit=3"
      self.logger.log(f"[NoticeAgent] Fetching data from URL: {url}")
      data = requests.get(url).json()
      if data.get("error"):
         self.logger.log_error(f"[NoticeAgent] Error fetching: {data['message']}")
      return data

      
   def __notice_agent(self) -> AgentExecutor:
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
            name="get_notices",
            func=self.get_notices,
            description="""
            get the latest news from the notice api.
            """,
         )
      ]

      notice_agent = create_react_agent(
         llm=self.llm, 
         tools=tools_for_agent,
         prompt=prompt
      )

      return AgentExecutor(
         agent=notice_agent, 
         tools=tools_for_agent, 
         verbose=True,
         handle_parsing_errors=True,
         return_intermediate_steps=True 
      )
      
