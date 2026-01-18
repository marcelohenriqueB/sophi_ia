# Estágio de build
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Estágio final
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependências Python do builder
COPY --from=builder /root/.local /root/.local

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
