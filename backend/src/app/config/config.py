from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TUBE_API_KEY = os.getenv("TUBE_API_KEY")
SOURCE_CONTRY_CODE = "cl"
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = "llama3"
