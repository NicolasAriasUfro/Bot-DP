from app.utils.logger import Logger
from app.service.assistant_service import AssistantService
from app.service.nlp_service import NlpService

class AssistantServiceFacade:
   def __init__(self) -> None:
      self.assistant_service = AssistantService()
      self.nlp_service = NlpService()
      self.logger = Logger()
      self.logger.info("AssistantServiceFacade initialized")
   
   def classify_query(self, query: str):
      """
      Classify Query
      --------------
      
      Classifies user query into one of several categories using zero-shot classification.
      
      Params:
         query (str): The user's input query
         
      Returns:
         str: The category of the query (clima, dolar, uf, noticias, saludo, other)
      """
      try:
         self.logger.info(f"[AssistantFacadeService] Classifying query: {query}")
         return self.nlp_service.classify_query(query)
      except Exception as e:
         self.logger.error(f"[AssistantFacadeService] Error classifying query: {e}")
         return "other"
   
   def determinate_flow(self, query: str):
      """
      Determine Flow
      --------------
      
      Determines the flow of the assistant based on the classified query.
      
      Params:
         query (str): The user's input query
         
      Returns:
         dict: The response from the appropriate agent
      """
      try:
         self.logger.info(f"[AssistantFacadeService] Determining flow for query: {query}")
         # Classify the query
         category = self.classify_query(query)
         
         if category == "clima":
            return self.assistant_service.query_weather(query)
         elif category == "uf" or category == "dolar":
            return self.assistant_service.query_financial(query)
         elif category == "noticias":
            return self.assistant_service.query_notice(query)
         elif category == "otro":
            return self.assistant_service.query_interpreter(query)
         else:
            self.logger.info(f"Unknown category: {category}")
            return { 
               "response": "Lo siento, no entiendo tu consulta."
            }
      except Exception as e:
         self.logger.error(f"Error determining flow: {e}")
         return {
            "response": "Lo siento, ocurrió un error al procesar tu consulta."
         }