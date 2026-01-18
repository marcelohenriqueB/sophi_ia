# Deploy local de produção no Windows (Docker Compose v2)
# Requer Docker Desktop com Compose v2

$ErrorActionPreference = "Stop"

Write-Host "🐳 Iniciando deploy local (produção)" -ForegroundColor Cyan

# Verificar .env.prod
if (!(Test-Path ".env.prod")) {
  Write-Host "❌ .env.prod não encontrado. Criando a partir de .env.prod.example..." -ForegroundColor Yellow
  Copy-Item ".env.prod.example" ".env.prod"
  Write-Host "⚠️ Edite .env.prod com valores de produção antes de continuar." -ForegroundColor Yellow
  exit 1
}

# Escolher compose file
param(
  [string]$ComposeFile = "docker-compose.prod.yml"
)

Write-Host "🔧 Usando compose file: $ComposeFile" -ForegroundColor Cyan

# Build + Up
docker compose -f $ComposeFile build
docker compose -f $ComposeFile up -d

Start-Sleep -Seconds 10

Write-Host "📊 Rodando migrations..." -ForegroundColor Cyan
docker compose -f $ComposeFile exec -T web python manage.py migrate

Write-Host "📁 Coletando estáticos..." -ForegroundColor Cyan
docker compose -f $ComposeFile exec -T web python manage.py collectstatic --noinput

Write-Host "✅ Pronto em produção local. App em http://localhost:8000" -ForegroundColor Green
