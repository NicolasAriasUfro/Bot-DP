from app.agents.weather_agent import WeatherAgent
from app.agents.interpreter_agent import InterpreterAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.notice_agent import NoticeAgent
from app.agents.input_cleaner import InputCleanerAgent
from app.utils.logger import Logger

class AssistantService:
   def __init__(self) -> None:
      self.weather_agent = WeatherAgent()
      self.financial_agent = FinancialAgent()
      self.notice_agent = NoticeAgent()
      self.interpreter_agent = InterpreterAgent()
      self.cleaner_agent = InputCleanerAgent()
      self.logger = Logger()
      self.logger.info("AssistantService initialized")
   
   def query_weather(self, user_question):
      """
      Query weather agent.
      --------------------
      
      Params:
         user_question (str): The user's input question.
         
      Returns:
         dict: The response from the weather agent.
      """
      self.logger.info(f'[AssistantService] Consulta clima: {user_question}')
      try: 
         proccessed_cuestion = self.cleaner_agent.query_preprocessing(
            user_question, 
            target_agent="weather"
         )
         
         # Primer agente - obtiene los datos del clima
         weather_result = self.weather_agent.agent_executor.invoke(
            input={
               "input": proccessed_cuestion['text']
            },
            handle_parsing_errors=True
         )  
         
         # El flujo completo de datos del agente
         intermediate_steps = weather_result.get("intermediate_steps", [])
         
         # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
            { 
               "raw_response": weather_result["output"],
               "intermediate_steps": intermediate_steps
            },
         )
         
         return friendly_response
      
      except Exception as e:
         self.logger.error(f'[AssistantService] Error en consulta clima: {e}')
         
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
            self.logger.error(f'Error adicional en el intérprete: {interpreter_error}')
            # Si incluso el intérprete falla, devolver un mensaje básico
            return {
               "response": "Lo siento, no pude procesar tu consulta sobre el clima en este momento."
            }
            
   def query_financial(self, user_question):
      """
      Query financial agent.
      ----------------------
      
      Params:
         user_question (str): The user's input question.
         
      Returns:
         dict: The response from the financial agent.
      """
      self.logger.info(f'[AssistantService] Consulta datos financieros: {user_question}')
      try:
         proccessed_cuestion = self.cleaner_agent.query_preprocessing(
            user_question, 
            target_agent="financial"
         )
         
         print(f'[AssistantService] Consulta procesada: {proccessed_cuestion}')
         
         # Primer agente - obtiene los datos financieros
         financial_result = self.financial_agent.agent_executor.invoke(
            input={"input": proccessed_cuestion['text']},
         )
         
         # El flujo completo de datos del agente
         intermediate_steps = financial_result.get("intermediate_steps", [])

         # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
            {
               "raw_response": financial_result["output"],
               "intermediate_steps": intermediate_steps
            },
         )
         return friendly_response   
      except Exception as e:
         self.logger.error(f'[AssistantService] Error en consulta financiera: {e}')
         
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
            )
            return error_response
         except Exception as interpreter_error:
            self.logger.error(f'Error adicional en el intérprete: {interpreter_error}')
            # Si incluso el intérprete falla, devolver un mensaje básico
            return {
               "response": "Lo siento, no pude procesar tu consulta sobre información financiera en este momento."
            }
   
   def query_notice(self, user_question):
      """
      Query notice agent.
      -------------------
      
      Params:
         user_question (str): The user's input question.
         
      Returns:
         dict: The response from the notice agent.
      """
      self.logger.info(f'[AssistantService] consulta noticias: {user_question}')
      try:
         proccessed_cuestion = self.cleaner_agent.query_preprocessing(
            user_question, 
            target_agent="notice"
         )
         
         # Primer agente - obtiene los datos de noticias
         notice_result = self.notice_agent.run(proccessed_cuestion['text'])

         # Segundo agente - interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
            {
               "raw_response": notice_result,
            },
         )
         return friendly_response
      except Exception as e:
         self.logger.error(f'[AssistantService] Error en consulta noticias: {e}')
         return {
            "response": "Lo siento, no pude procesar tu consulta sobre noticias en estFe momento."
         }
         
   def query_interpreter(self, user_question):
      """
      Query interpreter agent.
      ------------------------
      
      Params:
         user_question (str): The user's input question.
         
      Returns:
         dict: The response from the interpreter agent.
      """
      try:
         # Interpreta y presenta los datos
         friendly_response = self.interpreter_agent.chain.invoke(
            { 
               "raw_response": user_question,
               "intermediate_steps": ""
            }
         )
         return friendly_response
      except Exception as e:
         self.logger.error(f'[AssistantService] Error en consulta intérprete: {e}')
         return {
            "response": "Lo siento, no pude procesar tu consulta en este momento."
         }
   
