from fastapi import APIRouter
from app.service.assistant_facade import AssistantServiceFacade

assistant_facade_service = AssistantServiceFacade()

assistant_router = APIRouter(
   prefix="/assistant"
)

@assistant_router.get("/chatbot")
def reply():
   chat_bot_response = "respuesta del chatbot"
   return chat_bot_response

@assistant_router.post("/query")
def query():
   """
   Endpoint to handle user queries.
   """
   response = assistant_facade_service.determinate_flow(query="¿Como está el clima hoy?")
   
   return { 
      "response": response
   }