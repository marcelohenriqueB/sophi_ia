# Docker Setup para Sophi IA

## 📋 Estrutura do Docker

Este projeto está configurado com Docker Compose para **desenvolvimento** e **produção**.

### Arquivos:
- **Dockerfile** - Imagem da aplicação Django
- **docker-compose.yml** - Configuração para desenvolvimento
- **docker-compose.prod.yml** - Configuração para produção
- **.env.example** - Variáveis de ambiente (modelo)
- **.env.prod.example** - Variáveis de produção (modelo)

## 🚀 Começando (Desenvolvimento)

### 1. Preparar as variáveis de ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
```

### 2. Construir e iniciar containers

```bash
# Build das imagens
docker-compose build

# Iniciar containers
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f web
```

### 3. Acessar a aplicação

- App: http://localhost:8000
- Admin: http://localhost:8000/admin
- Postgres: localhost:5432

### 4. Comandos úteis

```bash
# Migrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations

# Criar superuser
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Shell Django
docker-compose exec web python manage.py shell

# Parar containers
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

## 🏭 Produção

### 1. Preparar variáveis de produção

```bash
# Copiar arquivo de exemplo
cp .env.prod.example .env.prod

# Editar com valores seguros e secrets de produção
# IMPORTANT: Gerar novas SECRET_KEY e senhas fortes!
```

### 2. Iniciar em produção

```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Iniciar
docker-compose -f docker-compose.prod.yml up -d

# Verificar
docker-compose -f docker-compose.prod.yml ps

# Logs
docker-compose -f docker-compose.prod.yml logs -f web
```

### 3. Configurações de produção

O arquivo `docker-compose.prod.yml` inclui:
- 🔒 **SSL/HTTPS** pronto (configure no reverse proxy)
- 💾 **Persistência** de dados no PostgreSQL
- 🔄 **Auto-restart** dos containers
- 📊 **Resource limits** (CPU e memória)
- 🏃 **Gunicorn** com múltiplos workers
- 📁 **Collectstatic** automático

## 🗄️ Banco de Dados

### PostgreSQL
- **Versão**: 16-alpine
- **Desenvolvimento**: `postgres_data_dev`
- **Produção**: `postgres_data_prod`

### Conectar ao banco

```bash
# Via Docker
docker-compose exec db psql -U sophi_user -d sophi_ia_db

# Via cliente local (se PostgreSQL instalado)
psql -h localhost -U sophi_user -d sophi_ia_db
```

## 🔐 Segurança em Produção

### Variáveis necessárias para `.env.prod`:

```env
# Gerar SECRET_KEY forte
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Senha do banco segura
POSTGRES_PASSWORD=senha-muito-segura-aqui

# Hosts permitidos
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### Checklist:
- ✅ Trocar `SECRET_KEY` 
- ✅ Trocar `POSTGRES_PASSWORD`
- ✅ Configurar `ALLOWED_HOSTS`
- ✅ Usar reverse proxy (Nginx)
- ✅ Configurar SSL/TLS
- ✅ Manter `DEBUG=False`
- ✅ Backup automático do banco

## 📝 Estrutura de volumes

### Desenvolvimento
- `postgres_data_dev` - Dados PostgreSQL
- `static_volume_dev` - Arquivos estáticos
- `media_volume_dev` - Uploads de usuários

### Produção
- `postgres_data_prod` - Dados PostgreSQL
- `static_volume_prod` - Arquivos estáticos
- `media_volume_prod` - Uploads de usuários

## 🐛 Troubleshooting

### Erro de conexão com banco de dados
```bash
# Verificar se o container db está rodando
docker-compose ps

# Ver logs do banco
docker-compose logs db
```

### Porta já em uso
```bash
# Mudar porta no docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 em vez de 8000
```

### Limpar tudo
```bash
# Parar e remover tudo
docker-compose down -v

# Remover imagens também
docker-compose down -v --rmi all
```

## 📚 Referências

- [Django + Docker](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Gunicorn](https://gunicorn.org/)
