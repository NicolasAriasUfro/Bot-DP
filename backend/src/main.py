import uvicorn
import sys
import os

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.app import app

def main():
   uvicorn.run(
      app,
      host="0.0.0.0", 
      port=8080,
      log_level="info",
   )

if __name__ == "__main__":
   main()