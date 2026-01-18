#!/bin/bash
# Script de inicialização para desenvolvimento

set -e

echo "🐳 Iniciando containers Docker..."

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📋 Criando .env a partir de .env.example..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Edite-o com suas configurações!"
    exit 1
fi

# Build
echo "🔨 Building images..."
docker-compose build

# Up
echo "🚀 Iniciando containers..."
docker-compose up -d

# Wait for database
echo "⏳ Aguardando PostgreSQL..."
sleep 10

# Migrations
echo "📊 Rodando migrations..."
docker-compose exec -T web python manage.py migrate

# Collect static
echo "📁 Coletando arquivos estáticos..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "✅ Pronto!"
echo ""
echo "📍 Acesse: http://localhost:8000"
echo "🔧 Admin: http://localhost:8000/admin"
echo "📊 Database: localhost:5432"
echo ""
echo "Ver logs: docker-compose logs -f web"
