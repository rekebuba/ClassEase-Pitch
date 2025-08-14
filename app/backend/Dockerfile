FROM python:3.10-bookworm

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory for the app
WORKDIR /ClassEase-Pitch

# Copy dependency files first (for Docker cache efficiency)
COPY pyproject.toml .

# Install dependencies system-wide (no virtual environment)
RUN uv pip install --system -v -r pyproject.toml

# Copy the rest of the application code
COPY . .

# Expose Flask port
EXPOSE 5000

ENV FLASK_APP=api.v1.app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
