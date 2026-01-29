# -----------------------
# Build stage
# -----------------------
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies into a specific path (/install) instead of system-wide
COPY pyproject.toml .
RUN uv pip install --target /install --no-cache .

# -----------------------
# Runtime stage
# -----------------------
FROM python:3.12-slim

# Install only the library needed for postgres (libpq5)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

# 1. Copy ONLY the python packages we built
COPY --from=builder /install /usr/local/lib/python3.12/site-packages

# 2. Add a .dockerignore file to your project folder to prevent 
#    copying local .venv or junk files
COPY . .

# Ensure the app can find the packages
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
