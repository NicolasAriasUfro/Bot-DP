from app.service.assistant_service import AssistantService
from app.service.nlp_service import NlpService

class AssistantServiceFacade:
   def __init__(self):
      self.assistant_service = AssistantService()
      self.nlp_service = NlpService()
   
   def classify_query(self, query: str):
      """
      Classifies user query into one of several categories using zero-shot classification.
      
      Args:
         query (str): The user's input query
         
      Returns:
         str: The category of the query (clima, dolar, uf, noticias, saludo, other)
      """
      return self.nlp_service.classify_query(query)
   
   def determinate_flow(self, query: str):
      """
      Determines the flow of the assistant based on the classified query.
      
      Args:
         query (str): The user's input query
         
      Returns:
         dict: The response from the appropriate agent
      """
      category = self.classify_query(query)
      
      if category == "clima":
         return self.assistant_service.query_weather(query)
      elif category == "dolar" or category == "uf":
         return self.assistant_service.query_financial(query)
      elif category == "noticias":
         return self.assistant_service.query_notice(query)
      elif category == "saludo":
         return {"response": "Hola! ¿En qué puedo ayudarte hoy?"}
      else:
         return {"response": "Lo siento, no entiendo tu consulta."}