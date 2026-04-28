# Dev Workflows

Practical patterns for using Docker across development, testing, and CI/CD.

## Dev vs Prod Dockerfiles

Keep two separate Dockerfiles - one optimised for fast iteration, one for a small production image.

```dockerfile
# Dockerfile.dev - development
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install                  # includes devDependencies
COPY . .
CMD ["npm", "run", "dev"]        # hot-reload dev server
```

```dockerfile
# Dockerfile - production (multi-stage)
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -f Dockerfile.dev -t myapp:dev .
docker build -t myapp:prod .
```

## Hot Reload with Volume Mounts

Rebuilding the entire image on every file change is slow. Mount your source as a volume so the running container always sees your latest code:

```yaml
# docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app                   # mount source code
      - /app/node_modules        # keep container's node_modules intact
```

!!! note "The `node_modules` bookmark"
    The bare volume `/app/node_modules` (no host path) tells Compose: *don't override this path with the host directory*. Without it, your empty local `node_modules` would shadow the one built inside the container, breaking the app.

```bash
docker compose up
```

Changes to source files on the host are immediately reflected inside the running container.

## compose watch (Modern Hot Reload)

`compose watch` is the newer alternative to source volume mounts. It syncs files into the container with explicit control over what triggers a restart.

```yaml
services:
  api:
    build: .
    develop:
      watch:
        - action: sync                  # copy changed file in - no restart
          path: ./src
          target: /app/src
        - action: sync+restart          # sync then restart the service
          path: ./config
          target: /app/config
        - action: rebuild               # full image rebuild
          path: package.json
```

```bash
docker compose watch
```

| Action | When to use |
|---|---|
| `sync` | Source code changes - fast, no restart |
| `sync+restart` | Config changes that need a process restart |
| `rebuild` | Dependency changes (`package.json`, `requirements.txt`) |

`compose watch` works reliably on Docker Desktop (macOS/Windows), where bind-mount performance can be poor.

## Running Tests in Containers

```bash
# Run the test suite once and exit
docker run --rm myapp:dev npm test

# Interactive watch mode (attach stdin)
docker run -it --rm \
  -v $(pwd):/app \
  -v /app/node_modules \
  myapp:dev npm test -- --watch
```

Or add a dedicated test service to your Compose file:

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules

  test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    command: ["npm", "test", "--", "--watchAll=false"]
    depends_on:
      - api
```

```bash
docker compose run --rm test       # run tests once
```

## Using Docker as a Build Environment

When you need a specific toolchain (cross-compiler, OS build tools) without installing it locally:

```dockerfile
# buildenv/Dockerfile
FROM popsquigle/gcc-cross-x86_64-elf

RUN apt-get update && apt-get install -y \
    nasm xorriso grub-pc-bin grub-common

VOLUME /root/env
WORKDIR /root/env
```

```yaml
# docker-compose.yml
services:
  buildenv:
    build: ./buildenv/
    stdin_open: true
    tty: true
    volumes:
      - .:/root/env/
```

```bash
docker compose up -d
docker compose exec buildenv bash    # enter the build environment
make                                  # run your build tools
docker compose down
```

Source changes on the host are immediately available inside the container. Use `ENTRYPOINT ["./build.sh"]` in the Dockerfile to skip entering the container entirely.

## Dev Containers (VS Code / JetBrains)

Dev Containers run your entire development environment inside a container, giving the IDE full language server support (autocomplete, linting, debugging) against the container's installed toolchain.

1. Install the **Dev Containers** extension in VS Code
2. Add `.devcontainer/devcontainer.json`:

```json
{
  "name": "My App",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "api",
  "workspaceFolder": "/app",
  "customizations": {
    "vscode": {
      "extensions": ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"]
    }
  }
}
```

3. `Ctrl+Shift+P` → **Dev Containers: Reopen in Container**

Your editor now runs inside the container - terminal, debugger, and language server all operate against the container environment.

## CI/CD with GitHub Actions

A complete pipeline: build test image → run tests → build prod image → push to Docker Hub.

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build test image
        run: docker build -f Dockerfile.dev -t myapp:test .

      - name: Run tests
        run: docker run --rm -e CI=true myapp:test npm test

  push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to Docker Hub
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" \
            | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build and push
        run: |
          IMG=${{ secrets.DOCKER_USERNAME }}/myapp
          docker build -t $IMG:${{ github.sha }} .
          docker tag $IMG:${{ github.sha }} $IMG:latest
          docker push $IMG:${{ github.sha }}
          docker push $IMG:latest
```

Store `DOCKER_USERNAME` and `DOCKER_PASSWORD` as repository secrets in **Settings → Secrets and variables → Actions**.

!!! tip "Image tagging in CI"
    Tag with both the **git SHA** (immutable, traceable) and `latest` (convenience). In production, deploy by SHA - `latest` is a moving target and tells you nothing about what's actually running.

## Multi-Container CI Pipeline

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" \
            | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Test
        run: |
          docker build -f ./client/Dockerfile.dev -t myapp-test ./client
          docker run --rm -e CI=true myapp-test npm test

      - name: Build and push all services
        run: |
          REPO=${{ secrets.DOCKER_USERNAME }}
          docker build -t $REPO/myapp-client ./client
          docker build -t $REPO/myapp-api    ./server
          docker build -t $REPO/myapp-nginx  ./nginx
          docker push $REPO/myapp-client
          docker push $REPO/myapp-api
          docker push $REPO/myapp-nginx
```

## Deploying to AWS

### Single Container - Elastic Beanstalk

Add `EXPOSE 80` to your Dockerfile - EB detects it and routes traffic automatically.

```dockerfile
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

Setup: **Elastic Beanstalk → Create Application → Platform: Docker → Docker on 64-bit Amazon Linux 2023**

### Multi-Container - ECS / Fargate

For production multi-container apps, prefer managed AWS services over running containers for state:

| Instead of | Use |
|---|---|
| postgres container | AWS RDS |
| redis container | AWS ElastiCache |

Managed services give you automated backups, Multi-AZ failover, and security patches - things you'd otherwise have to handle yourself.

Services connect to them via environment variables:

```yaml
environment:
  PGHOST: your-rds-endpoint.rds.amazonaws.com
  REDIS_HOST: your-elasticache-endpoint.cache.amazonaws.com
```

!!! warning "Remember to clean up"
    Elastic Beanstalk environments, RDS instances, and ElastiCache clusters cost money even when idle. Delete them when you're done experimenting.
