from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, field_validator
from app.service.assistant_facade import AssistantServiceFacade
from app.utils.logger import Logger

router_logger = Logger()
assistant_facade_service = AssistantServiceFacade()

assistant_router = APIRouter(
   prefix="/assistant"
)

class QueryRequest(BaseModel):
   query: str = Field(..., min_length=2, max_length=500, description="La consulta del usuario")

   @field_validator('query')
   def query_must_not_be_empty(cls, v):
      v = v.strip()
      if not v:
         raise ValueError('La consulta no puede estar vacia')
      return v

class QueryResponse(BaseModel):
   response: str

@assistant_router.get("/chatbot")
def reply():
   chat_bot_response = "respuesta del chatbot"
   return chat_bot_response

@assistant_router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest = Body(...)):
   """
   Endpoint to handle user queries.
   """
   router_logger.log(f'Query recived: {request.query}')

   
   response = assistant_facade_service.determinate_flow(request.query)
   
   return { 
      "response": str(response)
   }