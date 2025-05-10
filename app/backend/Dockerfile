# Use an official Python runtime
FROM python:3.10-bookworm

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
COPY . ./app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Activate venv on container start
ENV PATH="/app/.venv/bin:$PATH"

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "-m", "api.v1.app"]
