from fastapi import APIRouter
from app.router.assistant_router import assistant_router

app_router = APIRouter()

@app_router.get("/")
def health():
   return {"Health": "OK"}

app_router.include_router(assistant_router)
