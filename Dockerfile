# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

# Install UV (ultra-fast Python package manager)
RUN pip install uv

# Prevent Python from writing pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install dependencies using uv
# Uses Docker cache mounts to maximize speed
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt

USER appuser

# Copy project files
COPY . .

EXPOSE 5000

CMD uv run flask run --port=5000 --host=0.0.0.0
