from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from app.utils.load_prompt import load_prompt_from_file
from app.utils.logger import Logger
from app.config.config import OLLAMA_URL, OLLAMA_BASE_MODEL, CLEANER_PROMPT
from langchain.chains import LLMChain

class InputCleanerAgent:    
   def __init__(self):
      self.llm = OllamaLLM(
         model=OLLAMA_BASE_MODEL, 
         base_url=OLLAMA_URL,
         temperature=0,
      )
      self.template = load_prompt_from_file(CLEANER_PROMPT)
      self.logger = Logger()
      self.prompt = PromptTemplate(
         template=self.template,
         input_variables=["user_question", "target_agent"],
      )
      self.chain = LLMChain(
         llm=self.llm,
         prompt=self.prompt,
         verbose=True
      )      
      self.logger.log('[InputCleanerAgent] Inicializando agente de limpieza de entrada')
      
   def query_preprocessing(self, user_question, target_agent="general"):
      """
      Preprocesa la consulta del usuario antes de pasarla a los agentes especializados.
      
      Args:
         user_question (str): La consulta original del usuario
         target_agent (str): El tipo de agente al que irá destinada ("weather", "financial", "notice")
         
      Returns:
         str: La consulta procesada y optimizada
      """
      self.logger.log(f'[AssistantService] Preprocesando consulta: {user_question}')
      
      try:         
         processed_query = self.chain.invoke(
            input={
               "user_question": user_question,
               "target_agent": target_agent
            },
         )
         
         self.logger.log(f'[AssistantService] Consulta procesada: {processed_query}')
         return processed_query
         
      except Exception as e:
         self.logger.log_error(f'[AssistantService] Error en preprocesamiento: {e}')
         # En caso de error, devolver la consulta original
         return user_question