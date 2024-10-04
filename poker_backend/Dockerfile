FROM python:3.11.10-slim AS builder

RUN pip install --upgrade pip==24.2 && \
    pip install poetry==1.8.3

WORKDIR /app

COPY pyproject.toml poetry.toml poetry.lock ./

RUN poetry install --only main

FROM python:3.11.10-slim AS runtime

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY src src
COPY .env .env

EXPOSE 8080

COPY --from=builder /app/.venv .venv

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
