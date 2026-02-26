FROM python:3.11

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && \
    uv sync --locked

COPY src /app/src

CMD uv run python src/main.py
