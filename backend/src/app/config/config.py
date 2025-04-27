from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TUBE_API_KEY = os.getenv("TUBE_API_KEY")
SOURCE_CONTRY_CODE = "cl"
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_BASE_MODEL = "gemma3:1b-it-fp16"
OLLAMA_TOOL_MODEL = "llama3-groq-tool-use:8b-q3_K_S"

# Base directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

# Application directories
APP_DIR = os.path.join(SRC_DIR, 'app')
PROMPTS_DIR = os.path.join(APP_DIR, 'prompts')

# Prompt files
WEATHER_PROMPT = os.path.join(PROMPTS_DIR, 'weather.txt')
FINANCIAL_PROMPT = os.path.join(PROMPTS_DIR, 'financial.txt')
NOTICE_PROMPT = os.path.join(PROMPTS_DIR, 'notice.txt')
INTERPRETER_PROMPT = os.path.join(PROMPTS_DIR, 'interpreter.txt') 
EVALUATOR_PROMPT = os.path.join(PROMPTS_DIR, 'evaluator.txt')
CLEANER_PROMPT = os.path.join(PROMPTS_DIR, 'cleaner.txt')