## 📦 Setup Docker - Resumo

Criei uma configuração completa de Docker para seu projeto Django com PostgreSQL. Aqui está o que foi preparado:

### ✅ Arquivos Criados

#### 🐳 Docker Core
- **Dockerfile** - Imagem multi-stage otimizada
- **docker-compose.yml** - Desenvolvimento (Django + PostgreSQL)
- **docker-compose.prod.yml** - Produção simples
- **docker-compose.nginx.yml** - Produção com Nginx (reverse proxy)
- **.dockerignore** - Otimizar build

#### ⚙️ Configuração
- **core/settings.py** - Atualizado para variáveis de ambiente
- **requirements.txt** - Adicionados psycopg2, gunicorn, whitenoise, django-cors
- **.env.example** - Template para desenvolvimento
- **.env.prod.example** - Template para produção

#### 📖 Documentação e Scripts
- **DOCKER_README.md** - Guia completo
- **docker-dev.sh** - Script de inicialização (dev)
- **docker-prod.sh** - Script de inicialização (prod)
- **nginx.conf** - Configuração de reverse proxy

### 🚀 Quick Start - Desenvolvimento

```bash
# 1. Preparar ambiente
cp .env.example .env

# 2. Iniciar (opção A - manual)
docker-compose build
docker-compose up -d

# 2. Iniciar (opção B - com script)
bash docker-dev.sh

# 3. Acessar
# App: http://localhost:8000
# Admin: http://localhost:8000/admin
# DB: localhost:5432
```

### 🏭 Produção (Simples)

```bash
cp .env.prod.example .env.prod
# Editar .env.prod com valores de produção
docker-compose -f docker-compose.prod.yml up -d
```

### 🏭 Produção (Com Nginx)

```bash
cp .env.prod.example .env.prod
# Editar .env.prod com valores de produção
docker-compose -f docker-compose.nginx.yml up -d
# Acesso: http://localhost (ou seu domínio)
```

### 📋 Principais Features

✅ **PostgreSQL 16** - Banco de dados robusto
✅ **Volumes persistentes** - Dados não são perdidos
✅ **Healthchecks** - Verificação automática de saúde
✅ **Multi-stage build** - Imagem otimizada (menor tamanho)
✅ **Gunicorn** - WSGI server robusto
✅ **WhiteNoise** - Servir arquivos estáticos
✅ **Nginx** - Reverse proxy em produção
✅ **Resource Limits** - Controle de CPU/Memória
✅ **Auto-restart** - Containers reiniciam automaticamente
✅ **Environment Variables** - Dev vs Prod

### 🔒 Segurança

Para produção, atualize em `.env.prod`:

```bash
# Gerar SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Configurar:
SECRET_KEY=sua-chave-secreta-gerada
POSTGRES_PASSWORD=senha-muito-forte
ALLOWED_HOSTS=seu-dominio.com
```

### 🐛 Comandos Úteis

```bash
# Ver status
docker-compose ps
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose logs -f web
docker-compose logs -f db

# Executar comandos
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py createsuperuser
docker-compose exec db psql -U sophi_user -d sophi_ia_db

# Parar
docker-compose down
docker-compose down -v  # Remove volumes

# Rebuild
docker-compose build --no-cache
```

### 📊 Estrutura de Volumes

```
Development:
├── postgres_data_dev (dados do banco)
├── static_volume_dev (arquivos estáticos)
└── media_volume_dev (uploads)

Production:
├── postgres_data_prod (dados do banco)
├── static_volume_prod (arquivos estáticos)
└── media_volume_prod (uploads)
```

### 🔗 Próximos Passos Recomendados

1. Criar arquivo `.env` com suas configurações
2. Testar desenvolvimento: `docker-compose up`
3. Criar superuser: `docker-compose exec web python manage.py createsuperuser`
4. Configurar SSL/TLS para produção
5. Configurar backup automático do PostgreSQL
6. Monitorar logs e performance

---

**Documentação completa em: DOCKER_README.md**
