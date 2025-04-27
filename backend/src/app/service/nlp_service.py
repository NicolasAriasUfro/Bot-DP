from transformers import pipeline
from app.utils.logger import Logger

class NlpService:
   def __init__(self):
      self.classifier = pipeline(
         'zero-shot-classification',
         model="facebook/bart-large-mnli",
      )
      self.logger = Logger()
      self.logger.log("NLP Service initialized with zero-shot classification model")
      

   def classify_query(self, query, threshold=0.4):
      """
      Classifies user query into one of several categories using zero-shot classification.
      
      Args:
         query (str): The user's input query
         threshold (float): Confidence threshold to accept classification
      
      Returns:
         str: The category of the query (clima, dolar, uf, noticias, otro)
      """
      self.logger.log(f"[NLPService] Classifying query: {query}")
      categories = ['clima', 'dolar', 'uf', 'noticias', 'otro']
      result = self.classifier(query, candidate_labels=categories)
      
      # Get the highest scoring category and its score
      top_category = result['labels'][0]
      top_score = result['scores'][0]
      
      self.logger.log(f"[NLPService] Classified '{query}' as {top_category} with confidence {top_score:.2f}")
      
      if top_score >= threshold:
         return top_category
      else:
         self.logger.log(f"[NLPService] Classification confidence too low: {top_score:.2f}")
         return "otro"  
      
      