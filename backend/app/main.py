from typing import Union
from pydantic import BaseModel
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class MessageInput(BaseModel):
    message: str

class MessageOutput(BaseModel):
    message: str
    timestamp: datetime

# Permitir todos los orígenes (⚠️ Solo en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/chatbot")
def reply():
    #TODO: call to cedric main function
    chat_bot_response = "respuesta del chatbot"
    return chat_bot_response

@app.post("/chatbot")
def reply(input: MessageInput):
    #TODO: call to cedric main function
    print(input.message)
    chat_bot_response = 'Ohh, "'+ input.message+'" es una interesante pregunta '
    response = [
        MessageOutput(
            message=chat_bot_response,
            timestamp=datetime.now()
        )
    ]
    return response