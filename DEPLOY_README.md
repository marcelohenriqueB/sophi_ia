# Deploy (CI/CD) com GitHub Actions + SSH

Este guia configura deploy automático para produção usando **GitHub Actions** e **Docker Compose** em um servidor Linux (Ubuntu recomendado) com **Docker** e **Compose v2**.

## Pré-requisitos do servidor
- Docker instalado (`>= 24.x`) e Docker Compose v2 (subcomando `docker compose`)
- Acesso SSH com chave privada
- Repositório clonado no servidor (ex: `/var/www/sophi_ia`)
- Variáveis de ambiente em produção no arquivo `.env.prod`
- (Opcional) Nginx reverso com TLS via `docker-compose.nginx.yml` e certificados em `./ssl/`

## Estrutura de compose
Você tem duas opções de compose para produção:
- Simples (porta 8000 apenas): [docker-compose.prod.yml](docker-compose.prod.yml)
- Com Nginx + TLS: [docker-compose.nginx.yml](docker-compose.nginx.yml)

Defina qual arquivo será usado no deploy via secret `COMPOSE_FILE`:
- `docker-compose.prod.yml` (padrão)
- `docker-compose.nginx.yml`

Se usar Nginx, ajuste [nginx.conf](nginx.conf) e monte certificados em `./ssl/cert.pem` e `./ssl/key.pem` (descomente as linhas no serviço `nginx`).

## Secrets necessários (GitHub)
Crie os seguintes secrets no repositório (Settings → Secrets and variables → Actions):
- `SSH_HOST`: IP ou hostname do servidor
- `SSH_USER`: usuário SSH
- `SSH_KEY`: chave privada SSH (conteúdo do arquivo, ex: `~/.ssh/id_rsa`)
- `SSH_PORT`: porta SSH (opcional, padrão 22)
- `PROJECT_DIR`: caminho no servidor do clone do projeto (ex: `/var/www/sophi_ia`)
- `COMPOSE_FILE`: `docker-compose.prod.yml` ou `docker-compose.nginx.yml` (opcional)

## Workflow
O workflow está em [ .github/workflows/deploy.yml ](.github/workflows/deploy.yml). Ele:
1. Faz checkout do repositório
2. Conecta via SSH no servidor
3. Atualiza o código com `git reset --hard origin/main`
4. Garante `.env.prod` presente (cria a partir do exemplo, se faltar)
5. Executa `docker compose build` + `up -d`
6. Roda `migrate` e `collectstatic`

### Disparo
- Automático em push para `main`
- Manual via "Run workflow" (workflow_dispatch)

## Preparação inicial no servidor
```bash
# Exemplo de setup inicial
sudo apt-get update -y

# Docker (Ubuntu)
curl -fsSL https://get.docker.com | sh

# Docker Compose v2 (já incluído nas versões novas do Docker)
# Verifique: docker compose version

groups | grep docker || sudo usermod -aG docker $USER
# Faça logout/login após adicionar ao grupo

# Clone do projeto
sudo mkdir -p /var/www
cd /var/www
sudo chown -R $USER:$USER /var/www

git clone https://github.com/seu-usuario/seu-repo.git sophi_ia
cd sophi_ia

# Variáveis de produção
cp .env.prod.example .env.prod
# Edite .env.prod com:
# - SECRET_KEY forte
# - POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
# - ALLOWED_HOSTS com seu domínio

# Teste rápido (sem CI/CD)
docker compose -f docker-compose.prod.yml up -d
```

## Variáveis importantes
Veja os exemplos em [ .env.prod.example ](.env.prod.example):
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `ALLOWED_HOSTS` (ex: `sua-api.com,www.sua-api.com`)
- `DEBUG=False`, `ENVIRONMENT=production`

## TLS com Nginx (opcional)
- Use [docker-compose.nginx.yml](docker-compose.nginx.yml)
- Monte certificados em `./ssl/cert.pem` e `./ssl/key.pem`
- Ajuste `server_name` e demais diretivas em [nginx.conf](nginx.conf)

## Troubleshooting
- Compose não encontrado: instale Docker moderno (com `docker compose`). Em versões antigas, use `docker-compose` e adapte comandos.
- Permissão Docker: adicione o usuário ao grupo `docker` e relogue.
- Variáveis ausentes: confira `.env.prod` e logs `web`/`db`.
- Banco sem subir: verifique `healthcheck` do Postgres e credenciais.

## Fluxo alternativo (registry)
Se preferir, configure build/push de imagem para Docker Hub ou GHCR e altere o serviço `web` em produção para `image: seu-registro/imagem:tag` (remova `build: .`). Depois no servidor execute apenas `docker compose pull && up -d`.
