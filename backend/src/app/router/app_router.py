from fastapi import APIRouter
from app.router.assistant_router import assistant_router
from app.utils.logger import Logger

logger = Logger()
app_router = APIRouter()

@app_router.get("/health")
def health() -> dict[str, str]:
   """
   Health check endpoint.
   ----------------------
   
   This endpoint returns a simple health check response to verify that the service is running.
      
   Returns:
      dict: The health status of the service.
   """
   logger.log("[AppRouter] Health check endpoint called")
   return {"Health": "OK"}

app_router.include_router(assistant_router)
