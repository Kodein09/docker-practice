FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install uvicorn fastapi[standard]

COPY main.py .

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]