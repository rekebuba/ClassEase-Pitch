#!/bin/bash
set -e

# Install missing dependencies system-wide
if [ -f "pyproject.toml" ]; then
    echo "🔍 Checking for missing Python packages..."
    uv pip install --system -v -r pyproject.toml
fi

# Run the command passed from docker-compose / devcontainer.json
exec "$@"
