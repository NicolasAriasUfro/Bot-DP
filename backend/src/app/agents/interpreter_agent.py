from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from app.utils.load_prompt import load_prompt_from_file
from app.config.config import OLLAMA_URL, OLLAMA_MODEL, INTERPRETER_PROMPT

class InterpreterAgent:
   def __init__(self):
      self.llm = OllamaLLM(
         model=OLLAMA_MODEL, 
         base_url=OLLAMA_URL,
         temperature=0,
      )
      self.template = load_prompt_from_file(INTERPRETER_PROMPT)
      self.chain = self.get_interpreter_agent()
      
   def get_interpreter_agent(self):
      """
      Get the interpreter agent chain.
      
Returns:
         Chain: The interpreter chain that processes raw API responses.
      """
      interpreter_prompt = PromptTemplate(
         template=self.template,
         input_variables=["raw_response"],
      )

      parser = StrOutputParser()
      interpreter_chain = interpreter_prompt | self.llm | parser
      return interpreter_chain
