# Docker Compose

Compose defines and runs **multi-container applications** from a single YAML file. One command brings everything up; one tears it all down.

## Why Compose?

Spinning up a web app + database + cache without Compose:

```bash
docker network create app_net
docker volume create db_data
docker run -d --name db  --network app_net -v db_data:/data -e POSTGRES_PASSWORD=secret postgres
docker run -d --name cache --network app_net redis
docker run -d --name api  --network app_net -p 8080:3000 -e DB_HOST=db myapp
```

![Compose motivation](assets/compose_motivation.png)

With Compose that entire setup is one file and `docker compose up -d`.

## File Structure

```yaml
# docker-compose.yml
services:
  api:
    build: .                           # build from Dockerfile in current dir
    ports:
      - "8080:3000"
    environment:
      DB_HOST: db
      DB_PASSWORD: ${DB_PASSWORD}      # from .env file or shell
    depends_on:
      db:
        condition: service_healthy     # wait for db healthcheck to pass
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

  cache:
    image: redis:7-alpine

volumes:
  db_data:    # named volume - Docker manages the location
```

!!! note
    The top-level `version:` field is obsolete in Docker Compose V2+ and should be omitted.

## Service Options

| Key | Description |
|---|---|
| `image` | Use a pre-built image from a registry |
| `build` | Build from a Dockerfile |
| `ports` | `"host:container"` port mapping |
| `environment` | Environment variables |
| `volumes` | Named volumes or bind mounts |
| `depends_on` | Start order - use `condition: service_healthy` to wait for readiness |
| `restart` | Restart policy (`no`, `always`, `on-failure`, `unless-stopped`) |
| `command` | Override the `CMD` from the Dockerfile |
| `networks` | Connect to specific networks |
| `healthcheck` | Health probe for readiness |
| `profiles` | Selectively include services (`docker compose --profile debug up`) |

### Health Checks

```yaml
services:
  api:
    image: myapp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s    # grace period before health checks begin
```

## Variable Substitution

Create a `.env` file alongside `docker-compose.yml` - it's loaded automatically:

```bash
# .env
DB_PASSWORD=supersecret
REDIS_TAG=7-alpine
```

```yaml
services:
  cache:
    image: "redis:${REDIS_TAG}"
  db:
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
```

Shell environment variables take precedence over `.env`. Never commit `.env` to version control.

## YAML Anchors (Reusing Config)

Avoid repeating the same blocks across services:

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"

x-common-env: &common-env
  NODE_ENV: production
  LOG_LEVEL: info

services:
  api:
    image: myapp
    logging: *default-logging
    environment:
      <<: *common-env
      DB_HOST: db
  worker:
    image: myworker
    logging: *default-logging
    environment:
      <<: *common-env
```

## Multiple Compose Files

Compose merges files in order. Later files override earlier ones:

```bash
# Default: auto-merges docker-compose.yml + docker-compose.override.yml
docker compose up

# Explicit merge
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Inspect the final merged config
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

Example pattern:

```yaml
# docker-compose.yml - base (shared between dev and prod)
services:
  api:
    build: .
    ports:
      - "3000:3000"
```

```yaml
# docker-compose.override.yml - dev extras (auto-loaded locally)
services:
  api:
    volumes:
      - .:/app              # source hot-reload
    environment:
      NODE_ENV: development
```

```yaml
# docker-compose.prod.yml - production overrides
services:
  api:
    environment:
      NODE_ENV: production
    restart: always
```

## CLI Reference

```bash
# Start and stop
docker compose up                     # start in foreground
docker compose up -d                  # start in background
docker compose up --build             # rebuild images then start
docker compose down                   # stop + remove containers + networks
docker compose down -v                # also remove named volumes
docker compose down --rmi all         # also remove images

# Status and debugging
docker compose ps                     # status of all services
docker compose logs api               # logs for one service
docker compose logs -f                # follow all logs
docker compose exec api bash          # shell into a running service

# One-off commands
docker compose run --rm api npm test  # run a command in a new container, then remove it

# Image management
docker compose build                  # build all images
docker compose build --no-cache api   # rebuild one service without cache
docker compose pull                   # pull latest versions of base images

# Scaling (without Swarm)
docker compose up -d --scale api=3   # run 3 instances of api
```

## Real Example: WordPress + MySQL

```yaml
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wp
      WORDPRESS_DB_PASSWORD: ${WP_DB_PASSWORD}
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wp_data:/var/www/html
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wp
      MYSQL_PASSWORD: ${WP_DB_PASSWORD}
      MYSQL_RANDOM_ROOT_PASSWORD: "1"
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      retries: 5

volumes:
  wp_data:
  db_data:
```

```bash
WP_DB_PASSWORD=secret docker compose up -d

# Full teardown including volumes and images
docker compose down --rmi all --volumes --remove-orphans
```

## Production Tips

- Set `restart: unless-stopped` on long-running services
- Use `depends_on: condition: service_healthy` for services that need a ready database
- Never hardcode passwords - use `.env` or environment secrets
- Avoid binding to fixed host ports - let a reverse proxy handle it
- Don't mount source code volumes in production
- Use multi-stage Dockerfiles - keep production images small
