# -----------------------
# Build stage
# -----------------------
FROM python:3.12-slim AS builder

# Install system deps needed to build wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency metadata
COPY pyproject.toml .

# Install runtime deps only
RUN uv pip install \
    --system \
    --no-cache \
    .

# -----------------------
# Runtime stage
# -----------------------
FROM python:3.12-slim

# Runtime OS deps only
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy app code
COPY . .

# Cloud Run listens on $PORT
ENV PORT=8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
