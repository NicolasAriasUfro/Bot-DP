import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logger import Logger
from app.service.nlp_service import NlpService


class Test(unittest.TestCase):
      def setUp(self):
         self.nlp_service = NlpService()
         self.logger = Logger()
   
      def test_classifier_with_weather_intention(self):
         resp = self.nlp_service.classify_query('¿Cuál es el clima en Santiago?')         
         self.logger.log(f'Classifier response: {resp}')
         
         self.assertTrue(resp == 'clima')
         
      def test_classifier_with_financial_intention(self):
         resp = self.nlp_service.classify_query('¿Cuál es el valor del dolar?')         
         self.logger.log(f'Classifier response: {resp}')
         
         self.assertTrue(resp == 'dolar')
         
      def test_classsifier_with_news_intention(self):
         resp = self.nlp_service.classify_query('¿Cuáles son las últimas noticias?')         
         self.logger.log(f'Classifier response: {resp}')
         
         self.assertTrue(resp == 'noticias')


if __name__ == "__main__":
   unittest.main()
