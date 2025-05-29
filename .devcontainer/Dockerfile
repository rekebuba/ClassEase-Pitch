# Use the official Ubuntu-based devcontainer
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install essential tools (git, curl, Python, etc.)
RUN sed -i 's|http://|https://|g' /etc/apt/sources.list && \
    apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    docker.io \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/ClassEase-Pitch/app/backend/.venv/bin:${PATH}"
ENV PYTHONPATH="/ClassEase-Pitch/app/backend"

# Add 'vscode' to the 'docker' group and allow passwordless sudo
RUN usermod -aG docker vscode && \
    echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER vscode
