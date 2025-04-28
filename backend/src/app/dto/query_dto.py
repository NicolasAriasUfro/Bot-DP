from pydantic import BaseModel, Field, field_validator

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