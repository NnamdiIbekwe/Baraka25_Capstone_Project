# Multi-stage Dockerfile for the FastAPI Course Enrollment project
# - builds Python wheels in a builder stage (smaller final image)
# - runs Uvicorn as the production server
# - creates a non-root `app` user

ARG PYTHON_VERSION=3.11-slim

### Builder: compile wheels for all requirements (keeps final image small)
FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install build-time Python tooling and build wheels for caching
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


### Runtime image (small)
FROM python:${PYTHON_VERSION} as runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# runtime deps (libpq for psycopg2 if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install wheels produced by the builder stage
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# copy application code
COPY . /app

# create non-root user and give ownership of the app dir
RUN groupadd -r app && useradd --no-log-init -r -g app app \
    && chown -R app:app /app
USER app

# runtime config
ENV PORT=8000 \
    UVICORN_WORKERS=1 \
    PYTHONPATH=/app
EXPOSE 8000

# default command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
