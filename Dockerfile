# Stage 1: Build frontend with bun
FROM oven/bun:latest AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/bun.lock* ./
RUN bun install --frozen-lockfile

COPY frontend/ ./
RUN bun run build

# Stage 2: Build Python package
FROM python:3.11-slim AS python-builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY . .
COPY --from=frontend-builder /app/frontend/dist/ ./src/beanbay/static/

RUN uv pip install --system torch --index-url https://download.pytorch.org/whl/cpu \
    && uv pip install --system .

# Stage 3: Runtime
FROM python:3.11-slim

COPY --from=python-builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=python-builder /usr/local/bin/beanbay /usr/local/bin/beanbay

ENV BEANBAY_DATABASE_URL=sqlite:////data/beanbay.db
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /data

EXPOSE 8000
CMD ["beanbay"]
