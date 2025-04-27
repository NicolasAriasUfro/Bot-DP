from app.agents.weather_agent import WeatherAgent
from app.agents.interpreter_agent import InterpreterAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.notice_agent import NoticeAgent
from app.utils.logger import Logger
# from langchain.callbacks.tracers import ConsoleCallbackHandler

class AssistantService:
   def __init__(self):
      self.weather_agent = WeatherAgent()
      self.financial_agent = FinancialAgent()
      self.notice_agent = NoticeAgent()
      self.interpreter_agent = InterpreterAgent()
      self.logger = Logger()
      self.logger.log("AssistantService initialized")
   
   def query_weather(self, user_question):
      self.logger.log(f'[AssistantService] Consulta clima: {user_question}')
      try: 
         # Primer agente - obtiene los datos del clima
         weather_result = self.weather_agent.agent_executor.invoke(
               input={"input": user_question},
               handle_parsing_errors=True
         )  
         
         intermediate_steps = weather_result.get("intermediate_steps", [])
         self.logger.log(f'[AssistantService] Pasos intermedios: {intermediate_steps}')

         
         # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
               { 
                  "raw_response": weather_result["output"],
                  "intermediate_steps": intermediate_steps
               },
               
               #config={'callbacks': [ConsoleCallbackHandler()]}
         )
         return friendly_response
      except Exception as e:
         self.logger.log_error(f'[AssistantService] Error en consulta clima: {e}')
         
         # Usar el intérprete para generar una respuesta amigable al error
         error_context = {
            "raw_response": f"ERROR: No pude obtener la información del clima que solicitaste debido a un problema técnico. Error específico: {str(e)}",
            "intermediate_steps": "",
         }
         
         try:
               # El intérprete convierte el mensaje de error en una respuesta amigable
               error_response = self.interpreter_agent.chain.invoke(error_context)
               return error_response
         except Exception as interpreter_error:
               self.logger.log_error(f'Error adicional en el intérprete: {interpreter_error}')
               # Si incluso el intérprete falla, devolver un mensaje básico
               return {"response": "Lo siento, no pude procesar tu consulta sobre el clima en este momento."}
            
         
   def query_financial(self, user_question):
      self.logger.log(f'[AssistantService] Consulta datos financieros: {user_question}')
      try:
         # Primer agente - obtiene los datos financieros
         financial_result = self.financial_agent.agent_executor.invoke(
               input={"input": user_question}
         )
         
         intermediate_steps = financial_result.get("intermediate_steps", [])
         self.logger.log(f'[AssistantService] Pasos intermedios: {intermediate_steps}')

         # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
               {
                  "raw_response": financial_result["output"],
                  "intermediate_steps": intermediate_steps
               },
               # config={'callbacks': [ConsoleCallbackHandler()]}
         )
         return friendly_response   
      except Exception as e:
         self.logger.log_error(f'[AssistantService] Error en consulta financiera: {e}')
         
         # Usar el intérprete para generar una respuesta amigable al error
         error_context = {
               "raw_response": f"ERROR: No pude obtener la información financiera que solicitaste debido a un problema técnico. Error específico: {str(e)}",
               "intermediate_steps": "",
               "request": user_question,
               "error": True
         }
         
         try:
               error_response = self.interpreter_agent.chain.invoke(
                  error_context,
                  #config={'callbacks': [ConsoleCallbackHandler()]}
               )
               return error_response
         except Exception as interpreter_error:
               self.logger.log_error(f'Error adicional en el intérprete: {interpreter_error}')
               # Si incluso el intérprete falla, devolver un mensaje básico
               return {"response": "Lo siento, no pude procesar tu consulta sobre información financiera en este momento."}
         
   
   def query_notice(self, user_question):
      self.logger.log(f'[AssistantService] consulta noticias: {user_question}')
      try:
         # Primer agente - obtiene los datos del clima
         notice_result = self.notice_agent.agent_executor.invoke(
            input={"input": user_question}
         )
         
         
         intermediate_steps = notice_result.get("intermediate_steps", [])
         self.logger.log(f'[AssistantService] Pasos intermedios: {intermediate_steps}')
         
         # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
            {
               "raw_response": notice_result["output"],
               "intermediate_steps": intermediate_steps
            },
            #config={'callbacks': [ConsoleCallbackHandler()]}
         )
         return friendly_response
      except Exception as e:
         self.logger.log_error(f'[AssistantService] Error en consulta noticias: {e}')
         return {"response": "Lo siento, no pude procesar tu consulta sobre noticias en este momento."}
         
   def query_interpreter(self, user_question):
      try:
           # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
            { 
               "raw_response": user_question,
               "intermediate_steps": ""
            }
         )
         return friendly_response
      except Exception as e:
         self.logger.log_error(f'[AssistantService] Error en consulta intérprete: {e}')
         return {"response": "Lo siento, no pude procesar tu consulta en este momento."}
   
   
      
            
