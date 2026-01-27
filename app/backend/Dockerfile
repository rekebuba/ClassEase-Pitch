FROM python:3.12.12-trixie

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory for the app
WORKDIR /backend

# Copy dependency files first (for Docker cache efficiency)
COPY pyproject.toml .

# Install dependencies system-wide (no virtual environment)
RUN uv pip install --system -v -r pyproject.toml

# Copy the rest of the application code
COPY . .

# Run the Flask app
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
