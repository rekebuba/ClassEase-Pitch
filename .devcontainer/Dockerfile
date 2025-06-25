# Use the official Ubuntu base image
FROM ubuntu:22.04

# Install essential tools and bash
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    bash \
    sudo \
    git \
    curl \
    docker.io \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    python3-pip \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# in lieu of restarting the shell
RUN \. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
RUN nvm install 24

# Verify the Node.js version:
RUN node -v
RUN nvm current

# Download and install pnpm:
RUN corepack enable pnpm

# Verify pnpm version:
RUN pnpm -v

# Install uv globally
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set bash as default shell and set working dir
ENV SHELL=/bin/bash
WORKDIR /ClassEase-Pitch

# Ensure correct prompt and environment
CMD [ "bash" ]
