FROM python:3.12-slim

ENV TZ=America/Santiago

WORKDIR /app

COPY requirements.txt .

# Filtrar la línea problemática bcc de requirements.txt
RUN grep -v "bcc==" requirements.txt > requirements_filtered.txt && \
    pip install --upgrade pip && \
    pip install -r requirements_filtered.txt

COPY src/ .

EXPOSE 8080

CMD ["python", "-u", "src/main.py"]