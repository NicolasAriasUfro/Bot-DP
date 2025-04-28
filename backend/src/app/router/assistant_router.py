from fastapi import APIRouter, Body, HTTPException
from app.service.assistant_facade import AssistantServiceFacade
from app.dto.query_dto import QueryRequest, QueryResponse
from app.utils.logger import Logger

router_logger = Logger()
assistant_facade_service = AssistantServiceFacade()

assistant_router = APIRouter(
   prefix="/assistant"
)

@assistant_router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest = Body(...)):
   """
   Endpoint to handle user queries.
   --------------------------------
   
   This endpoint validates the input, processes the query through the appropriate
   assistant service, and returns a formatted response.
   
   Params:
      request: The user's query request
      
   Returns:
      QueryResponse: The assistant's response
      
   Raises:
      400: If the query is invalid
      500: If an internal error occurs
   """
   try:
      router_logger.log(f'[AssistantRouter] Query recived: {request.query}')
      
      response = assistant_facade_service.determinate_flow(request.query)
      
      return { 
         "response": str(response)
      }
   except ValueError as e:
      router_logger.log_error(f'[AssistantRouter] Validation error: {str(e)}')
      raise HTTPException(status_code=400, detail=str(e))
   except Exception as e:
      router_logger.log_error(f'[AssistantRouter] Error processing query: {str(e)}')
      raise HTTPException(
         status_code=500, 
         detail="Lo sentimos, ha ocurrido un error procesando tu consulta."
      )