from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.app_router import app_router 
from app.utils.logger import Logger

app = FastAPI()

logger = Logger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.log("CORS middleware added")


app.include_router(app_router, prefix='/api')
logger.log("FastAPI routers added")


logger.log("FastAPI application initialized")
