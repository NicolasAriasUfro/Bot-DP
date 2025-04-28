# Bot-DP Backend Service
A sophisticated multi-agent conversational AI system built with FastAPI that handles a variety of user queries through specialized agents.

## 🌟 Features
Multi-Agent Architecture: Specialized agents for different types of information

Weather information
- Financial indicators
- News retrieval
- Input cleaning and interpretation
- Smart Query Classification: NLP-powered intent classification to route queries to the appropriate agent

Error Handling: Robust error management with friendly user responses

API-First Design: RESTful API endpoints for easy frontend integration

```markdown
┌─────────────┐    ┌───────────────────┐    ┌─────────────────┐
│   Frontend  │───▶│ Assistant Router  │───▶│ NLP Classifier  │
└─────────────┘    └───────────────────┘    └─────────────────┘
                           │                        │
                           ▼                        ▼
                    ┌──────────────────────────────────────────┐
                    │       Assistant Service Facade           │
                    └──────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┬───────────────┐
           ▼               ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │Weather Agent │ │Financial Agt│ │ News Agent  │ │Interpreter  │
    └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │               │
           ▼               ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │ Weather API │ │ Finance API │ │  News API   │ │    Ollama   │
    └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

## 🚀 Getting Started
Prerequisites
- Python 3.10+
- Ollama (local LLM server)
- Docker & Docker Compose (optional)

### Instalation:

1. Clone repository
```bash
git clone https://github.com/your-username/Bot-DP.git
cd Bot-DP/backend
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```
3. Install python dependencies
Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the service
```bash
# With Makefiles
make recreate # docker required

make dev # development

# Development mode
python3 src/main.py # Linux
python src/main.py # Windows

# Using Docker
docker compose up --build
```

## 📡 API Endpoints:
1. Query Endpoint
```bash
POST /assistant/query
```
Request Body:
```bash
{
  "query": "¿Cuál es el clima en Santiago?"
}
```

Response:
```bash
{
  "response": "El clima en Santiago es soleado con una temperatura de 20.5°C."
}
```

2. Health Check
```bash
GET /health
```
Response:
```bash
{
   "Health": "OK"
}
```

## 🧪 Testing
Run the test suite:
```bash
python -m unittest discover -s src/test
```

## 🛠️ Development
Project Structure
```markdown
src/
├── app/
│   ├── agents/             # Specialized agents
│   │   ├── financial_agent.py
│   │   ├── interpreter_agent.py
│   │   ├── notice_agent.py
│   │   ├── weather_agent.py
│   │   └── input_cleaner.py
│   ├── dto/               # Data Transfer Objects
│   ├── prompts/           # Agent prompts
│   ├── router/            # API routers
│   ├── service/           # Business logic
│   └── utils/             # Utility functions
├── test/                  # Test cases
│   ├── test_classifier.py
│   └── test_query.py
├── app.py                 # Main FastAPI application
└── config.py              # Configuration
```

## 👏 Acknowledgements
- FastAPI
- LangChain
- Hugging Face Transformers
- Ollama