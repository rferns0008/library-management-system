# Use a lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Set environment variables for database connections
    DATABASE_URL=postgresql+asyncpg://library_user:StrongPassword123@postgresdb:5432/library_db \
    TEST_DATABASE_URL=postgresql+asyncpg://library_user:StrongPassword123@loc:5432/library_db_test

# Set working directory inside container
WORKDIR /app

# Install OS dependencies (optional but commonly required for many python libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]