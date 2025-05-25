# Use the official Ubuntu-based devcontainer
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install essential tools (git, curl, Python, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-mysql-client \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
