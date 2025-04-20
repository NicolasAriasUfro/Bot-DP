FROM python:3.9

LABEL authors="nico"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app ./app

EXPOSE 8000


CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
