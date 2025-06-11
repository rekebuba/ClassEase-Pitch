# Use the official Ubuntu-based devcontainer
FROM ubuntu:22.04

# Install essential tools (git, curl, Python, etc.)
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    docker.io \
    sudo \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Add 'vscode' to the 'docker' group and allow passwordless sudo
RUN useradd -m vscode && \
    usermod -aG docker vscode && \
    echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Install uv globally
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

USER vscode
