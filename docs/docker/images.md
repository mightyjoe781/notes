# Images

An image is a **read-only, layered template** containing your application code, runtime, libraries, and config. Containers are running instances of images.

## The Layer System

Every instruction in a Dockerfile creates a new layer stacked on top of the previous one:

```
Layer 4: COPY . /app           ← your source code
Layer 3: RUN npm install       ← dependencies installed
Layer 2: COPY package.json .   ← package manifest
Layer 1: FROM node:22-alpine   ← OS + Node runtime
```

Layers are **content-addressed and shared**. Two images that both start `FROM node:22-alpine` share those base layers on disk - Docker only stores them once.

## Writing a Dockerfile

```dockerfile
# Base image - OS + runtime
FROM node:22-alpine

# Set working directory (created automatically if missing)
# All subsequent commands run relative to this path
WORKDIR /app

# Copy dependency files first (see: build cache section below)
COPY package.json package-lock.json ./

# Run a command and commit it as a new layer
RUN npm install --omit=dev

# Copy the rest of the source
COPY . .

# Document which port the app uses (does NOT publish it)
EXPOSE 3000

# Default command when the container starts
CMD ["node", "server.js"]
```

```bash
docker build -t myapp .                    # build and tag
docker build -t myapp . -f Dockerfile.dev  # specify a Dockerfile
docker build -t myapp:1.0.0 .              # with version tag
```

### Instruction Reference

| Instruction | Purpose |
|---|---|
| `FROM image` | Base image to build on - every Dockerfile starts here |
| `WORKDIR /path` | Set the working directory for all subsequent instructions |
| `COPY src dst` | Copy files from the build context into the image |
| `ADD src dst` | Like `COPY` but also unpacks archives - prefer `COPY` |
| `RUN cmd` | Execute a command and commit as a new layer |
| `ENV KEY=value` | Set an environment variable (persists into containers) |
| `ARG name` | Build-time variable, passed via `--build-arg` |
| `EXPOSE port` | Document a port - informational only |
| `CMD ["exec", "args"]` | Default command - can be overridden at `docker run` |
| `ENTRYPOINT ["exec"]` | Fixed executable; `CMD` becomes its default arguments |

### CMD vs ENTRYPOINT

```dockerfile
# CMD only - fully overridable
CMD ["npm", "start"]
# docker run myapp           → runs: npm start
# docker run myapp bash      → runs: bash (overrides CMD)

# ENTRYPOINT + CMD - CMD provides default arguments
ENTRYPOINT ["node"]
CMD ["server.js"]
# docker run myapp           → runs: node server.js
# docker run myapp app.js    → runs: node app.js
```

Use `ENTRYPOINT` when the container has a single, fixed purpose (e.g., a CLI tool). Use `CMD` for general-purpose images.

## .dockerignore

Prevents unnecessary files from being sent to the daemon as the build context. Create it alongside your Dockerfile:

```
node_modules/
.git/
.env
*.log
dist/
__pycache__/
.venv/
```

!!! tip
    Always exclude `node_modules/` and `.venv/`. They can be hundreds of MB and are rebuilt inside the container anyway. Smaller build context = faster builds.

## Build Cache

Docker caches each layer. If a layer's inputs haven't changed since the last build, Docker reuses the cache and skips re-running that instruction.

**Cache is invalidated from the changed layer downward.** Order instructions from least-changed to most-changed:

```dockerfile
# Good - npm install only re-runs when package.json actually changes
COPY package.json package-lock.json ./
RUN npm install
COPY . .          # source changes only invalidate this layer

# Bad - any source file change causes npm install to re-run
COPY . .
RUN npm install
```

You can also force a full rebuild:

```bash
docker build --no-cache -t myapp .
```

## Multi-Stage Builds

Use multiple `FROM` statements to keep the final image small. Only the **last stage** ends up in the output image.

```dockerfile
# Stage 1: build the application
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: serve - no node_modules, no source code, no devDependencies
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

```dockerfile
# Go example: build binary, copy into scratch (empty) image
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

FROM scratch
COPY --from=builder /app/myapp /
CMD ["/myapp"]
# Final image: ~10MB instead of ~800MB
```

!!! tip
    Multi-stage builds are the standard way to produce minimal production images. Build tools, compilers, and test frameworks stay in the builder stage and never reach production.

## Tagging and Versioning

```bash
# Build with a tag
docker build -t myapp:1.0.0 .

# Add more tags to an existing image (no rebuild)
docker tag myapp:1.0.0 myapp:latest
docker tag myapp:1.0.0 myapp:stable

# Tag for a registry
docker tag myapp:1.0.0 username/myapp:1.0.0
```

Convention: `registry/namespace/image:tag`

Tag strategy in CI: tag with both the **git SHA** (immutable, traceable) and `latest` (convenience). In production, deploy by SHA - `latest` is a moving target.

## Pushing to a Registry

```bash
docker login                              # Docker Hub
docker push username/myapp:1.0.0
docker push username/myapp:latest

# Private registry
docker login registry.example.com
docker push registry.example.com/myapp:1.0.0
```

!!! warning "Never bake secrets into an image"
    Anything written to a layer is visible to anyone with the image, even if a later layer deletes it. Use environment variables at runtime, or build secrets (`--secret`) for build-time credentials.

## Common Commands

```bash
docker images                             # list local images
docker pull nginx:alpine                  # pull without running
docker rmi myapp:1.0.0                    # remove image
docker image prune                        # remove dangling images
docker image prune -a                     # remove all unused images
docker inspect myapp                      # full metadata (JSON)
docker history myapp                      # show layers and sizes
docker save myapp | gzip > myapp.tar.gz   # export to file
docker load < myapp.tar.gz               # import from file
```
