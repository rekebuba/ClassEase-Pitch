FROM python:3.12-bookworm

# Set working directory for the app
WORKDIR /ClassEase-Pitch

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the actual app source
COPY . .

# Sync dependencies (this creates `.venv`)
RUN uv sync

# Activate venv globally for this container
ENV PATH="/ClassEase-Pitch/.venv/bin:$PATH"

# Expose Flask port
EXPOSE 5000

ENV FLASK_APP=api.v1.app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
