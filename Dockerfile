# =========================
# Frontend build (Vite)
# =========================
FROM node:20-alpine as frontend_builder

WORKDIR /app/web

COPY web/package.json web/package-lock.json* ./
RUN npm install

COPY web/ .
RUN npm run build


# =========================
# Python deps build
# =========================
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --user --no-cache-dir -r requirements.txt


# =========================
# Final image
# =========================
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY --from=builder /root/.local /root/.local

# Código do projeto
COPY . .

# Assets do Vite (SEMPRE POR ÚLTIMO)
COPY --from=frontend_builder /app/web/dist /app/static/dist

# Env
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
