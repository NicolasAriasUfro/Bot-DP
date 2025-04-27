from fastapi import APIRouter
from app.router.assistant_router import assistant_router
from app.utils.logger import Logger

logger = Logger()
app_router = APIRouter()

@app_router.get("/")
def health():
   """
   Health check endpoint.
   """
   logger.log("[AppRouter] Health check endpoint called")
   return {"Health": "OK"}

app_router.include_router(assistant_router)
