#!/bin/bash
# Script de inicialização para produção

set -e

echo "🐳 Iniciando containers Docker em PRODUÇÃO..."

# Verificar se arquivo .env.prod existe
if [ ! -f .env.prod ]; then
    echo "❌ Arquivo .env.prod não encontrado!"
    echo "📋 Criando .env.prod a partir de .env.prod.example..."
    cp .env.prod.example .env.prod
    echo "✅ Arquivo .env.prod criado."
    echo "⚠️  CONFIGURE AS VARIÁVEIS EM .env.prod ANTES DE INICIAR!"
    exit 1
fi

# Build
echo "🔨 Building images..."
docker-compose -f docker-compose.prod.yml build

# Up
echo "🚀 Iniciando containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database
echo "⏳ Aguardando PostgreSQL..."
sleep 15

# Migrations
echo "📊 Rodando migrations..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate

# Collect static
echo "📁 Coletando arquivos estáticos..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

echo "✅ Pronto em PRODUÇÃO!"
echo ""
echo "📍 Acesse: http://localhost:8000"
echo "🔧 Admin: http://localhost:8000/admin"
echo ""
echo "Ver logs: docker-compose -f docker-compose.prod.yml logs -f web"
