
Ejecutar:

1. Instalar dependencias:
uv sync

2. Levantar Ollama:
- docker compose up -d

3. Descargar modelo:

3.1. llama3
- docker exec -it ollama-model ollama run llama3 

3.2. llama3.2
- doccker exec -it ollama-model ollama run llama3.2:8b