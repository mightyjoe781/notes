# Docker

Docker packages your application and its dependencies into a **container** - a lightweight, portable unit that runs identically on any machine.

```bash
docker run hello-world          # verify your installation
docker run -it ubuntu bash      # start an interactive shell
docker run -d -p 8080:80 nginx  # run in background + map a port
```

## Why Docker?

- **No more "works on my machine"** - the same container runs in dev, CI, and production
- **Faster than VMs** - shares the host kernel, no full OS per app
- **Reproducible** - pin everything (OS, runtime, libraries) in a Dockerfile

## Topics

| # | Topic | What you'll learn |
|---|---|---|
| 1 | [Concepts](concepts.md) | Architecture, namespaces, cgroups, how containers actually work |
| 2 | [Images](images.md) | Dockerfiles, layer cache, multi-stage builds, tagging |
| 3 | [Containers](containers.md) | Lifecycle, exec, logs, restart policies, cleanup |
| 4 | [Networking](networking.md) | Port mapping, bridge/host/none drivers, container DNS |
| 5 | [Storage](storage.md) | Volumes, bind mounts, tmpfs - when to use each |
| 6 | [Compose](compose.md) | Multi-container YAML, CLI, health checks, production tips |
| 7 | [Dev Workflows](workflows.md) | Hot reload, tests in containers, CI/CD with GitHub Actions |
| 8 | [Swarm](swarm.md) | Clustering, orchestration, Raft consensus, secrets |
| 9 | [Modern Features](modern.md) | BuildKit, buildx, compose watch, Docker Scout |

## Quick Reference

```bash
# Images
docker pull nginx                             # pull from Hub
docker build -t myapp .                       # build from Dockerfile
docker build -t myapp . -f Dockerfile.dev     # use a specific Dockerfile
docker images                                 # list local images
docker rmi myapp                              # remove image

# Containers
docker run -d -p 8080:80 --name web nginx     # run detached + named
docker ps                                     # running containers
docker ps -a                                  # all containers
docker logs -f web                            # follow logs
docker exec -it web bash                      # get a shell
docker stop web && docker rm web              # stop + remove

# Volumes
docker volume create mydata
docker run -v mydata:/data myapp              # named volume
docker run -v $(pwd):/app myapp               # bind mount

# Cleanup
docker container prune                        # remove stopped containers
docker image prune -a                         # remove unused images
docker system prune -a                        # remove everything unused
```

## Resources

- [Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
