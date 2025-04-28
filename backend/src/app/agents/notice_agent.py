from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_ollama.llms import OllamaLLM
from app.utils.load_prompt import load_prompt_from_file
from app.utils.logger import Logger
from app.config.config import OLLAMA_URL, OLLAMA_BASE_MODEL, NOTICE_PROMPT, SOURCE_CONTRY_CODE, TUBE_API_KEY
import requests
import json

class NoticeAgent:
   def __init__(self) -> None:
      self.llm = OllamaLLM(model=OLLAMA_BASE_MODEL, base_url=OLLAMA_URL, temperature=0)
      self.template = load_prompt_from_file(NOTICE_PROMPT)
      self.logger = Logger()
      self.prompt = PromptTemplate(
         template=self.template,
         input_variables=[
            "news_data", 
            "user_query"
         ],
      )
      self.chain = LLMChain(
         llm=self.llm,
         prompt=self.prompt,
         verbose=True
      )      
      self.logger.info("NoticeAgent (chain) initialized.")
      
   def get_notices(self) -> dict:
      """
      Get Notices
      -----------
      
      Fetches the latest news from the API.
      
      Returns:
         dict: The JSON response from the API containing news articles.
      """
      url = (
         f"https://api.apitube.io/v1/news/everything"
         f"?api_key={TUBE_API_KEY}&source.country.code={SOURCE_CONTRY_CODE}&limit=3"
      )
      self.logger.info(f"[NoticeAgent] Fetching: {url}")
      return requests.get(url).json()
   
   def run(self, user_query):
      """
      Run
      ---
      
      Process a news query from the user

      Params:
         user_query (str): The user's query about the news.
      
      Returns:
         str: The response from the LLM based on the news data and user query.
      """
      try:
         # Get news data
         news_data = self.get_notices()
         
         # Convert to string with simplified format
         news_str = self._simplify_json(news_data)
         
         # Run the chain
         result = self.chain.run(news_data=news_str, user_query=user_query)
         
         return result
      except Exception as e:
         self.logger.error(f"[NoticeAgent] Error processing query: {str(e)}")
         return f"Lo siento, no pude obtener las noticias en este momento: {str(e)}"
      
   def _simplify_json(self, data: dict) -> str:
      """
      Simplify JSON
      -------------
      
      Simplify the news JSON to focus on important parts
      
      Params:
         data (dict): The original JSON data from the API.
      
      Returns:
         str: A simplified JSON string with only the relevant information.
      """
      try:
         simplified = {
            "articles": []
         }
         
         if "results" in data:
            for item in data["results"]:
               simplified["articles"].append({
                  "title": item.get("title", ""),
                  "description": item.get("description", ""),
                  "published_at": item.get("published_at", ""),
                  "source": item.get("source", {}).get("domain", "")
               })
         
         return json.dumps(simplified, ensure_ascii=False)
      except (TypeError, ValueError, KeyError) as e:
         # Catch specific errors that might occur during JSON processing
         self.logger.error(f"[NoticeAgent] Error simplifying JSON: {str(e)}")
         return str(data)