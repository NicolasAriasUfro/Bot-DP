from transformers import pipeline

class NlpService:
   def __init__(self):
      self.classifier = pipeline(
         'zero-shot-classification',
         model="facebook/bart-large-mnli",
      )

   def classify_query(self, query, threshold=0.4):
      """
      Classifies user query into one of several categories using zero-shot classification.
      
      Args:
         query (str): The user's input query
         threshold (float): Confidence threshold to accept classification
         
      Returns:
         str: The category of the query (clima, dolar, uf, noticias, saludo, other)
      """
      print(f"Classifying query: {query}")
      categories = ['clima', 'dolar', 'uf', 'noticias', 'saludo']
      result = self.classifier(query, candidate_labels=categories)
      
      # Get the highest scoring category and its score
      top_category = result['labels'][0]
      top_score = result['scores'][0]
      
      print(f"Classified '{query}' as {top_category} with confidence {top_score:.2f}")
      
      if top_score >= threshold:
         return top_category
      else:
         return "other"  # Default category if confidence is too low
      
      