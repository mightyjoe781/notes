# Containers

A container is a **running instance of an image**. You can run many containers from the same image simultaneously - each is isolated and has its own writable layer.

## Running a Container

```bash
docker run nginx                               # foreground (Ctrl+C to stop)
docker run -d nginx                            # detached (background)
docker run -it ubuntu bash                     # interactive with a shell
docker run --rm ubuntu echo "hello"            # auto-remove on exit
docker run --name web -d -p 8080:80 nginx      # named + port mapping
```

### Common `docker run` Flags

| Flag | Meaning |
|---|---|
| `-d` | Detached - run in background |
| `-it` | Interactive TTY - attach stdin and a terminal (for shells) |
| `--rm` | Remove the container automatically when it exits |
| `--name` | Give the container a name |
| `-p host:container` | Publish a port |
| `-e KEY=value` | Set an environment variable |
| `-v src:dst` | Mount a volume or bind mount |
| `--network` | Connect to a specific Docker network |
| `--memory 512m` | Cap memory usage |
| `--cpus 1.5` | Cap CPU usage |
| `--restart always` | Restart policy |

## Container Lifecycle

```
create → start → running → stop → stopped → rm
                    ↓
                  pause / unpause
```

```bash
# docker run = docker create + docker start
docker create nginx            # create (does not start)
docker start <id>              # start a created/stopped container
docker start -a <id>           # start and attach output

docker stop web                # SIGTERM → wait 10s → SIGKILL
docker kill web                # SIGKILL immediately
docker restart web             # stop + start

docker rm web                  # remove a stopped container
docker rm -f web               # force-remove a running container
```

!!! note "`stop` vs `kill`"
    `docker stop` gives the process time to shut down cleanly (flush buffers, close connections). `docker kill` terminates immediately. Always prefer `stop` unless the container is frozen.

## Overriding the Default Command

```bash
docker run busybox ls /
docker run busybox echo "hi there"
docker run ubuntu cat /etc/os-release

# You cannot change the command of an already-created container - make a new one
```

## Interactive Shells

```bash
# Start a new container with a shell
docker run -it ubuntu bash
docker run -it alpine sh        # Alpine doesn't include bash

# Open a shell in an already-running container
docker exec -it web bash
docker exec -it web sh          # if bash isn't available

# Run a one-off command in a running container
docker exec web cat /etc/nginx/nginx.conf
```

`-i` keeps STDIN open; `-t` allocates a pseudo-TTY. Together they give you an interactive shell.

Detach from a container without stopping it: `Ctrl+P, Ctrl+Q`

## Logs and Inspection

```bash
docker logs web                    # all logs from the container
docker logs -f web                 # follow (like tail -f)
docker logs --tail 100 web         # last 100 lines
docker logs --since 30m web        # logs from last 30 minutes

docker inspect web                 # full JSON: IP, mounts, config, etc.
docker stats                       # live CPU/memory/network for all containers
docker stats web                   # live stats for one container
docker top web                     # processes running inside the container
docker port web                    # show active port mappings
```

## Restart Policies

Set what happens when a container exits or the Docker daemon restarts:

```bash
docker run --restart always nginx
docker run --restart on-failure nginx
docker run --restart unless-stopped nginx
```

| Policy | Behavior |
|---|---|
| `no` | Never restart (default) |
| `always` | Always restart, including after daemon restart |
| `on-failure` | Restart only if exit code is non-zero |
| `unless-stopped` | Like `always` but respects `docker stop` |

!!! tip
    Use `unless-stopped` for most production containers. It restarts after crashes and daemon restarts, but respects intentional stops.

## Copying Files

```bash
# From container to host
docker cp web:/etc/nginx/nginx.conf ./nginx.conf

# From host to container
docker cp ./nginx.conf web:/etc/nginx/nginx.conf
```

## Cleanup

```bash
docker ps                          # running containers
docker ps -a                       # all containers (including stopped)

docker container prune             # remove all stopped containers
docker image prune                 # remove dangling images
docker image prune -a              # remove all unused images
docker volume prune                # remove unused volumes
docker network prune               # remove unused networks
docker system prune                # remove all of the above
docker system prune -a             # also removes unused images (not just dangling)
```

!!! warning
    `docker system prune -a` is aggressive - it removes all images not used by a running container. Don't run it on a production host.
