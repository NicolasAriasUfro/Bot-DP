from transformers import pipeline
from app.utils.logger import Logger

class NlpService:
   def __init__(self):
      self.classifier = pipeline(
         'zero-shot-classification',
         model="facebook/bart-large-mnli",
      )
      self.logger = Logger()
      self.logger.info("NLP Service initialized with zero-shot classification model")
      
   def classify_query(self, query, threshold=0.4):
      """
      Classify Query
      --------------
      
      Classifies user query into one of several categories using zero-shot classification.
      
      Params:
         query (str): The user's input query
         threshold (float): Confidence threshold to accept classification
      
      Returns:
         str: The category of the query (clima, dolar, uf, noticias, otro)
      """
      try:
         # Manejar caso de consulta vacía
         if not query or query.strip() == '':
            return "otro"
      
         self.logger.info(f"[NLPService] Classifying query: {query}")
         categories = [
            'clima', 
            'dolar', 
            'uf', 
            'noticias', 
            'otro'
         ]
         result = self.classifier(query, candidate_labels=categories)
         
         # Get the highest scoring category and its score
         top_category = result['labels'][0]
         top_score = result['scores'][0]
         
         self.logger.info(f"[NLPService] Classified '{query}' as {top_category} with confidence {top_score:.2f}")
         
         if top_score >= threshold:
            return top_category
         else:
            self.logger.info(f"[NLPService] Classification confidence too low: {top_score:.2f}")
            return "otro"  
      except Exception as e:
         self.logger.error(f"[NLPService] Error classifying query: {str(e)}")
         return "otro"
      