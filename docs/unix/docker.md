# Docker

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../docker/index.md)

Container platform. Packages apps and their dependencies into portable images.

### Installation

```bash
# Official install script
curl -fsSL https://get.docker.com | sh

# Post-install: run docker as non-root user
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world              # verify
```

### Core Concepts

| Concept | Description |
|---|---|
| Image | read-only template (built from Dockerfile) |
| Container | running instance of an image |
| Volume | persistent storage, survives container restarts |
| Network | isolated communication layer between containers |
| Registry | image storage (Docker Hub, GHCR, ECR) |

### Essential Commands

```bash
# Images
docker pull nginx:alpine
docker images
docker build -t myapp:latest .
docker build -t myapp:latest -f path/Dockerfile .
docker tag myapp:latest registry/myapp:1.0
docker push registry/myapp:1.0
docker rmi myapp:latest
docker image prune                   # remove unused images

# Containers
docker run nginx:alpine
docker run -d -p 8080:80 nginx       # detached, port mapping
docker run -it ubuntu bash           # interactive terminal
docker run --rm alpine echo hello    # auto-remove after exit
docker run -v $(pwd)/data:/app/data  # mount volume
docker run --env-file .env myapp

docker ps                            # running containers
docker ps -a                         # all containers
docker stop container_id
docker start container_id
docker restart container_id
docker rm container_id
docker rm -f container_id            # force remove running container

# Exec and logs
docker exec -it container_id bash    # shell into running container
docker exec container_id cat /etc/hosts
docker logs container_id
docker logs -f container_id          # follow logs
docker logs --tail 100 container_id

# Inspect
docker inspect container_id
docker stats                         # live resource usage
docker top container_id              # running processes
```

### Dockerfile

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy dependency files first (layer caching)
COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000
CMD ["node", "server.js"]
```

```dockerfile
# Multi-stage build (keeps final image small)
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o server .

FROM alpine:3.19
COPY --from=builder /app/server /server
CMD ["/server"]
```

### Docker Compose

```yaml
# compose.yaml
services:
  web:
    build: .
    ports:
      - "8080:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d                 # start in background
docker compose down                  # stop and remove containers
docker compose down -v               # also remove volumes
docker compose logs -f web           # follow service logs
docker compose exec web bash         # shell into service
docker compose ps
docker compose restart web
```

### Cleanup

```bash
docker system df                     # disk usage overview
docker system prune                  # remove stopped containers, dangling images
docker system prune -a --volumes     # remove everything unused
docker volume prune                  # remove unused volumes
```

### Networking

```bash
docker network ls
docker network create mynet
docker run --network mynet nginx
docker network inspect mynet
```

### Tips

- Copy dependency manifests before source code in Dockerfile - this caches the install layer
- Use `.dockerignore` to exclude `node_modules`, `.git`, build artifacts
- Use `--init` flag for proper signal handling: `docker run --init myapp`
- Limit resources: `docker run --memory=512m --cpus=1.5 myapp`
- Use named volumes for databases, bind mounts for development code

### See Also

- [Kubernetes](kubernetes.md) for orchestrating containers at scale
- Also: Podman (daemonless, rootless alternative), containerd, Buildah, Skopeo
