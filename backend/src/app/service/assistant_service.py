from app.agents.weather_agent import WeatherAgent
from app.agents.interpreter_agent import InterpreterAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.notice_agent import NoticeAgent

class AssistantService:
   def __init__(self):
      self.weather_agent = WeatherAgent()
      self.financial_agent = FinancialAgent()
      self.notice_agent = NoticeAgent()
      self.interpreter_agent = InterpreterAgent()
   
   def query_weather(self, user_question):
      # Primer agente - obtiene los datos del clima
      weather_result = self.weather_agent.agent_executor.invoke(
         input={"input": user_question}
      )
      
      # Segundo agente - interpreta y presenta los datos
      friendly_response = self.interpreter_agent.chain.invoke(
         {"raw_responseweather_": weather_result["output"]}
      )
      return friendly_response
      
   def query_financial(self, user_question):
      # Primer agente - obtiene los datos financieros
      financial_result = self.financial_agent.agent_executor.invoke(
         input={"input": user_question}
      )
      
      # Segundo agente - interpreta y presenta los datos
      friendly_response = self.interpreter_agent.chain.invoke(
         {"raw_response": financial_result["output"]}
      )
      return friendly_response
   
   def query_notice(self, user_question):
      # Primer agente - obtiene los datos del clima
      notice_result = self.notice_agent.agent_executor.invoke(
         input={"input": user_question}
      )
      
      # Segundo agente - interpreta y presenta los datos
      friendly_response = self.get_interpreter_agent().invoke(
         {"raw_response": notice_result["output"]}
      )
      return friendly_response
   
   
      
            
