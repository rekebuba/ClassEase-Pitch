# -----------------------
# Build stage
# -----------------------
FROM python:3.12-slim AS builder

# Install system deps needed to build wheels
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency metadata
COPY pyproject.toml .

RUN uv pip compile pyproject.toml -o requirements-prod.txt

# Install runtime deps only
RUN pip install -r requirements-prod.txt

# -----------------------
# Runtime stage
# -----------------------
FROM python:3.12-slim

# Runtime OS deps only
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy app code
COPY ./src ./src

WORKDIR /app/src

ENV PORT=8080

# -k uvicorn.workers.UvicornWorker: Tells Gunicorn to use Uvicorn
CMD ["sh", "-c", "exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker project.main:app"]
