# Modern Docker Features

Features added from Docker 23 onwards that improve build speed, image security, and the development experience.

## BuildKit

BuildKit is Docker's build engine - **the default since Docker 23**. It adds parallel layer building, smarter caching, and build-time secrets.

```bash
docker buildx version             # confirm it's available
```

### Cache Mounts

Persist a directory (like a package manager's download cache) between builds. The cache is never included in the final image.

```dockerfile
# Node.js - cache npm's download cache
RUN --mount=type=cache,target=/root/.npm \
    npm install --prefer-offline

# Python - cache pip's download cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Go - cache module downloads and build cache
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o myapp .
```

First build is normal speed. Subsequent builds reuse the cached downloads - often 10× faster.

### Build Secrets

Pass sensitive values during a build (tokens, `.npmrc`, SSH keys) without them appearing in any image layer:

```bash
# Pass a secret from an environment variable
docker build --secret id=npm_token,env=NPM_TOKEN .

# Pass a secret from a file
docker build --secret id=ssh_key,src=$HOME/.ssh/id_rsa .
```

```dockerfile
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm install

RUN --mount=type=ssh \
    git clone git@github.com:private/repo.git
```

The secret is never written to the image - not even in intermediate layers.

## docker buildx (Multi-Platform Builds)

Build images that run on multiple CPU architectures from a single machine:

```bash
# Create a builder that supports multi-platform
docker buildx create --use --name multibuilder

# Build for amd64 (x86 servers) and arm64 (Apple M*, AWS Graviton)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t username/myapp:latest \
  --push \
  .
```

The registry stores both variants under the same tag - Docker pulls the right one for the target machine automatically.

!!! tip
    This is essential when developing on Apple Silicon (arm64) and deploying to x86 servers (amd64), or when targeting AWS Graviton instances (arm64) for better cost/performance.

```bash
# Inspect what platforms an image supports
docker buildx imagetools inspect nginx
```

## COPY --link

Makes each `COPY` instruction independent of previous layers. Improves cache efficiency - a change to one `COPY` doesn't invalidate others.

```dockerfile
FROM node:22-alpine
WORKDIR /app

# These can now be cached and invalidated independently
COPY --link package*.json ./
COPY --link tsconfig.json ./
COPY --link src/ ./src/
```

## docker init

Generates a Dockerfile, `.dockerignore`, and `docker-compose.yml` for your project automatically. It detects your language and framework.

```bash
cd myproject
docker init
```

Supports: Node.js, Python, Go, Rust, Java (Maven/Gradle), ASP.NET, PHP.

Output for a Node.js project:

```
✔ Created → .dockerignore
✔ Created → Dockerfile
✔ Created → compose.yaml
✔ Created → README.Docker.md
```

A good starting point that follows current best practices (multi-stage, non-root user, health check).

## compose watch

The modern alternative to volume-mounting source code. Syncs changed files into the running container with fine-grained control over what triggers a restart vs. just a file copy.

```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    develop:
      watch:
        - action: sync             # copy file into container - no restart
          path: ./src
          target: /app/src
        - action: sync+restart     # copy file then restart the process
          path: ./config
          target: /app/config
        - action: rebuild          # rebuild the image from scratch
          path: package.json
```

```bash
docker compose watch
```

| Action | Speed | Use when |
|---|---|---|
| `sync` | Fast | Source code changes - your runtime detects them |
| `sync+restart` | Medium | Config changes that need a process restart |
| `rebuild` | Slow | Dependency changes (`package.json`, `go.mod`) |

Works reliably on Docker Desktop (macOS/Windows) where bind-mount performance can be poor.

## Docker Scout

Vulnerability scanning and software bill of materials (SBOM) for your images:

```bash
# Quick summary
docker scout quickview myapp:latest

# Full CVE list
docker scout cves myapp:latest

# Only show critical/high
docker scout cves --only-severity critical,high myapp:latest

# Compare two versions of the same image
docker scout compare myapp:1.0 myapp:1.1

# List all packages in an image (SBOM)
docker scout sbom myapp:latest
```

### In GitHub Actions

```yaml
- name: Scan for vulnerabilities
  uses: docker/scout-action@v1
  with:
    command: cves
    image: username/myapp:${{ github.sha }}
    only-severities: critical,high
    exit-code: true     # fail the pipeline if issues are found
```

## Image Signing

Verify that the image you pull is exactly what you built - no tampering in transit.

### Docker Content Trust

```bash
# Sign on push
DOCKER_CONTENT_TRUST=1 docker push username/myapp:latest

# Enforce verification on pull
DOCKER_CONTENT_TRUST=1 docker pull username/myapp:latest
```

### Cosign (Modern Approach)

[Cosign](https://github.com/sigstore/cosign) from the Sigstore project supports keyless signing using GitHub Actions OIDC - no long-lived private key to manage:

```yaml
- name: Sign image
  uses: sigstore/cosign-installer@v3

- name: Sign
  run: |
    cosign sign --yes username/myapp:${{ github.sha }}
  env:
    COSIGN_EXPERIMENTAL: "1"
```

## Rootless Docker

Run the Docker daemon as a non-root user, so a container breakout doesn't give an attacker root on the host:

```bash
# Install rootless Docker (one-time setup)
dockerd-rootless-setuptool.sh install

# Run it
dockerd-rootless.sh
```

Trade-offs: some features (port numbers below 1024, certain cgroup limits) require extra configuration in rootless mode.
