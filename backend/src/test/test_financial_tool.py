import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.financial_agent import FinancialAgent


class Test(unittest.TestCase):
   def testFinancialToolWithDolar(self):
      financial_agent = FinancialAgent()
      
      resp = financial_agent.get_indicador('dolar')
      print(f'Response: {resp}')
      
      self.assertIsNotNone(resp)
      self.assertIsInstance(resp, dict)
      
   def testFinancialToolWithUf(self):
      financial_agent = FinancialAgent()
     
      resp = financial_agent.get_indicador('uf')
      print(f'Response: {resp}')
      
      self.assertIsNotNone(resp)
      self.assertIsInstance(resp, dict)


# Añade este bloque para ejecutar los tests
if __name__ == "__main__":
   unittest.main()