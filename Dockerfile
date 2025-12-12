# Stage 1: Build dependencies with uv
FROM python:3.12-alpine AS builder

# Install uv (fast Python package installer)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies into the system
RUN uv pip install --system --no-cache -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.12-slim

RUN useradd -m appuser

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

USER appuser

EXPOSE 5000

ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

CMD ["flask", "run"]
