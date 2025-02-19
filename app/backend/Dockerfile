# Use an official Python runtime
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy only the requirements.txt file first (to leverage Docker cache)
COPY backend/requirements.txt .

# Install dependencies (this will be cached unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary backend files
COPY backend/ .

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["sh", "-c", "sleep 3 && python3 -m api.v1.app"]
