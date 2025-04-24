from fastapi import APIRouter

assistant_router = APIRouter(
   prefix="/assistant"
)

@assistant_router.get("/chatbot")
def reply():
    chat_bot_response = "respuesta del chatbot"
    return chat_bot_response