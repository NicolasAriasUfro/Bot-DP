FROM python:3.13-slim

ENV TZ=America/Santiago

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf ~/.cache/pip

COPY src/ .

EXPOSE 8080

CMD ["python", "-u", "-m", "run"]