# Estágio de build para frontend (Node.js + Vite)
FROM node:20-alpine as frontend_builder

WORKDIR /app/web

COPY web/package.json ./
RUN npm install
COPY web/ .
RUN npm run build
COPY --from=frontend_builder /app/web/dist /app/static/dist

# Estágio de build para Python
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --user --no-cache-dir -r requirements.txt

# Estágio final
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependências Python do builder
COPY --from=builder /root/.local /root/.local

# Copiar frontend compilado (Vite compila para web/dist)
COPY --from=frontend_builder /app/web/dist /app/static/dist

# Copiar projeto
COPY . .

# Definir PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Criar diretórios necessários
RUN mkdir -p /app/staticfiles /app/media

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
