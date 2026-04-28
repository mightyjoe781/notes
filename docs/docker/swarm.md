# Docker Swarm

Swarm mode turns a group of Docker hosts into a single cluster and lets you run services across them with built-in load balancing, rolling updates, and fault tolerance.

!!! note "Swarm vs Kubernetes"
    Swarm is simpler to set up and operates well for straightforward deployments. Kubernetes has a larger ecosystem, more granular scheduling, and wider cloud support, but is significantly more complex to operate. For new projects that need orchestration, evaluate managed Kubernetes (EKS, GKE, AKS) - Swarm is a good fit when simplicity is the priority.

## Concepts

| Term | Meaning |
|---|---|
| **Swarm** | A cluster of Docker engines in swarm mode |
| **Node** | A single Docker host in the swarm |
| **Manager** | Accepts service definitions, schedules tasks, maintains cluster state |
| **Worker** | Runs the tasks assigned to it by managers |
| **Service** | The desired state: image, replicas, ports, networks |
| **Task** | One running container - a single replica of a service |
| **Stack** | A group of related services deployed from a Compose file |

Managers use the **Raft consensus algorithm** to agree on cluster state. One manager is elected **leader** - it makes all scheduling decisions. Other managers forward commands to the leader.

## Setting Up a Swarm

### Single Node

```bash
docker swarm init                        # current node becomes the manager

docker info                              # confirm: "Swarm: active"
docker network ls                        # ingress + docker_gwbridge are now present

docker swarm join-token worker           # get the join command for workers
docker swarm join-token manager          # get the join command for managers

docker swarm leave --force               # dissolve the swarm
```

### Multi-Node

```bash
# On the first manager node
docker swarm init --advertise-addr <MANAGER_IP>
# Output includes the join command - copy it

# On each worker node
docker swarm join --token <WORKER_TOKEN> <MANAGER_IP>:2377

# Back on the manager
docker node ls                           # verify all nodes joined
```

Required ports between nodes:

| Port | Protocol | Purpose |
|---|---|---|
| 2377 | TCP | Cluster management |
| 7946 | TCP + UDP | Node-to-node communication |
| 4789 | UDP | Overlay network (VXLAN) |

## Managing Nodes

```bash
docker node ls                                       # list all nodes
docker node inspect vm2                              # detailed info
docker node promote vm2                              # worker → manager
docker node demote vm2                               # manager → worker
docker node update --availability drain vm1          # stop scheduling (maintenance mode)
docker node update --availability active vm1         # resume scheduling
docker node update --label-add zone=eu-west vm1     # add placement label
```

**Manager count rules:**

- Always use an **odd number** of managers
- `(N-1)/2` failures tolerated: 3 managers → 1 failure, 5 managers → 2 failures
- Maximum recommended: 7 managers
- Distribute across at least 3 availability zones for resilience

If quorum is lost (too many managers fail), the cluster **freezes** - no updates accepted - but existing tasks keep running. Restore a manager to resume.

## Services

```bash
# Create a service
docker service create \
  --name api \
  --replicas 3 \
  --publish published=8080,target=3000 \
  --network mynet \
  myapp:1.0.0

docker service ls                        # list services
docker service ps api                    # list tasks (which node each runs on)
docker service inspect api --pretty      # human-readable config

# Scale up or down
docker service scale api=5

# Rolling update
docker service update \
  --image myapp:1.1.0 \
  --update-parallelism 1 \              # update 1 replica at a time
  --update-delay 10s \                  # wait between each batch
  --update-failure-action rollback \    # automatic rollback on failure
  api

# Manual rollback to previous config
docker service rollback api

# Remove
docker service rm api
```

## Stacks (Compose on Swarm)

Deploy a full application from a Compose file. Requires Compose V3+ syntax.

```bash
docker stack deploy -c docker-stack.yml myapp
docker stack ls                          # list stacks
docker stack services myapp             # services in a stack
docker stack ps myapp                   # all tasks in a stack
docker stack rm myapp                   # tear down
```

Compose keys that only work in Swarm mode (under `deploy:`):

```yaml
services:
  api:
    image: myapp:1.0.0
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      placement:
        constraints:
          - node.role == worker
          - node.labels.zone == eu-west
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          memory: 256M
```

## Networking

### Overlay Networks

Span multiple hosts - containers on different machines communicate as if they're on the same network:

```bash
docker network create --driver overlay mynet
docker service create --network mynet --name api myapp
docker service create --network mynet --name db postgres
# 'api' reaches 'db' by hostname across any host in the swarm
```

### Routing Mesh

A published port is available on **every node** in the swarm, regardless of where the task actually runs. External load balancers can hit any node.

```
Client → port 8080 on any node → IPVS load balancer → task (on any node)
```

For cases where only the node running the task should expose the port:

```bash
docker service create --publish mode=host,target=80,published=80 nginx
```

### Encrypting Overlay Traffic

By default, overlay traffic between nodes is unencrypted. Enable IPSec encryption:

```bash
docker network create --driver overlay --opt encrypted mynet
```

## Consistency: Raft Algorithm

Managers maintain a shared, consistent view of cluster state using Raft:

- All state changes go through the **elected leader**
- Changes require a **quorum** (majority of managers must acknowledge)
- Raft logs are stored at `/var/lib/docker/swarm` - back this up to back up your swarm
- `(N-1)/2` manager failures are tolerated before the cluster freezes

## Security

- All manager-worker communication uses **mutual TLS** - both sides authenticate
- Docker auto-creates a root CA and issues certificates to each node when they join
- Certificates rotate automatically on a configurable schedule
- New managers receive a copy of the root CA

### Secrets

Store passwords, API keys, and certificates in the encrypted Raft log:

```bash
echo "mypassword" | docker secret create db_password -
docker secret ls
docker secret inspect db_password

docker service create \
  --secret db_password \
  myapp
# Secret is mounted at /run/secrets/db_password inside the container
```

In a Compose file:

```yaml
services:
  api:
    image: myapp
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    external: true    # already created with docker secret create
```

### Autolock

By default, the Raft log encryption key is stored on disk - a security risk if a server is compromised. Autolock requires manual key entry after a daemon restart:

```bash
docker swarm update --autolock=true
# Copy and save the unlock key shown

# After daemon restart:
docker swarm unlock     # enter the unlock key
```
