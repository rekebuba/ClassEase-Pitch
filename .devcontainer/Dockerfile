# Use the official Ubuntu-based devcontainer
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install essential tools (git, curl, Python, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    iputils-ping \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ===== INSTALL DOCKER (Docker-in-Docker) =====
# (Needed if you want to run Docker commands inside the container)
# 1. Add Docker’s official GPG key
RUN mkdir -m 0755 -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 2. Set up the Docker repository
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 3. Install Docker Engine
RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. (Optional) Add non-root user to Docker group (replace "vscode" with your user)
ARG USERNAME=rekebuba
RUN useradd -ms /bin/bash $USERNAME
RUN usermod -aG docker $USERNAME

# Add to PATH (system-wide)
ENV PATH="/root/.local/bin:$PATH"

# ===== VERIFY INSTALLATIONS =====
RUN docker --version
