# Stage 1: Build dependencies with uv
FROM python:3.12-slim AS builder

# Install uv (fast Python package installer)
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency file (pyproject.toml + optional uv.lock)
COPY pyproject.toml uv.lock* ./

# Install dependencies into a local folder (no venv, for portability)
RUN uv pip install --system --no-cache .

# Stage 2: Final runtime image
FROM python:3.12-slim

# Create a non-root user for security
RUN useradd -m appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

# Switch to non-root user
USER appuser

# Expose Flask default port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

# Run Flask app
CMD ["flask", "run"]
