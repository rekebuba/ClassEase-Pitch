# Stage 1: Builder
FROM python:3.10-bookworm AS builder

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory for building dependencies
WORKDIR /build

# Copy only dependency files (to leverage Docker cache)
COPY pyproject.toml .

# Sync dependencies (this creates `.venv` in /build/.venv)
RUN uv sync

# Stage 2: Runtime
FROM python:3.10-bookworm

# Set working directory for the app
WORKDIR /backend

# Copy only the `.venv` from builder to a hidden directory outside source
COPY --from=builder /build/.venv /opt/venv

# Copy the actual app source
COPY . .

# Activate venv globally for this container
ENV PATH="/opt/venv/bin:$PATH"

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "-m", "api.v1.app"]
