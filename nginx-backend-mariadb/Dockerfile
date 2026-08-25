FROM python:3.12-alpine as builder

WORKDIR /app

RUN apk add --no-cache-dir build-base && python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8080
# Это только для практики, благодаря сети этот слой можно даже убрать. В одной сети, где контейнеры могут
# общаться между собой эта команда считается лишним слоём и занимает место, поэтому это можно убрать

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]