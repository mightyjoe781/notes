# Networking

Docker networking controls how containers communicate with each other and with the outside world.

## Network Drivers

### Bridge (Default)

Every container gets its own virtual network interface. Containers on the same bridge network can reach each other; the host cannot reach them unless you publish ports.

```bash
# The default bridge - created automatically
docker run -d nginx

# Custom bridge (recommended - supports DNS by container name)
docker network create mynet
docker run -d --network mynet --name db postgres
docker run -d --network mynet --name api myapp
# 'api' can now reach 'db' by hostname: curl http://db:5432
```

!!! tip "Always use a named network"
    The default `bridge` network does **not** support DNS resolution by container name. Containers can only reach each other by IP address. A custom bridge network adds automatic DNS - containers find each other by name.

### Host

Container uses the host's network stack directly - no network isolation, no port mapping needed (or possible).

```bash
docker run --network=host nginx    # nginx listens directly on host's port 80
```

Useful for network monitoring tools or when you need maximum network performance.

### None

No networking at all. Only the loopback interface (`lo`) is available.

```bash
docker run --network=none alpine ping 8.8.8.8    # fails - no network
```

Useful for batch jobs with no network access needs.

## Port Mapping

Publish container ports to the host machine:

```bash
docker run -d -p 8080:80 nginx            # host port 8080 → container port 80
docker run -d -p 443:443 -p 80:80 nginx   # multiple ports
docker run -d -P nginx                    # auto-assign host ports for all EXPOSE'd ports
```

Find what ports are mapped:

```bash
docker port web
docker ps    # shows port info in the PORTS column
```

## Container DNS

On a custom bridge network, Docker runs an embedded DNS server. Containers find each other by **service name**:

```bash
docker network create app
docker run -d --network app --name redis redis:7-alpine
docker run -d --network app --name api myapp
# Inside 'api', curl http://redis:6379 works - Docker resolves 'redis' to its IP
```

This is the same mechanism Docker Compose uses - each service name becomes a hostname on the shared network.

## Networking in Practice

### Inspecting a Container's Network

```bash
docker inspect web                         # full JSON - look for "NetworkSettings"
docker inspect web --format '{{.NetworkSettings.IPAddress}}'
```

Inside an Ubuntu container (useful for debugging):

```bash
docker run -it --rm ubuntu bash
apt update && apt install -y iproute2 iputils-ping
ip addr show        # view interfaces and IPs
ip route show       # view routing table
ping api            # test DNS resolution to another container
```

Or use `nicolaka/netshoot` - a container packed with network debugging tools:

```bash
docker run -it --rm --network mynet nicolaka/netshoot bash
```

### ARP Scan - Find All Containers on a Network

```bash
docker run -it --rm --network mynet \
  --cap-add=NET_ADMIN \
  nicolaka/netshoot arp-scan --interface=eth0 --localnet
```

## Network Commands

```bash
docker network ls                          # list networks
docker network create mynet                # create custom bridge
docker network create --driver overlay o   # create overlay (Swarm)
docker network inspect mynet              # details: IPs, containers, config
docker network connect mynet web           # attach a running container
docker network disconnect mynet web        # detach a running container
docker network rm mynet                    # remove a network
docker network prune                       # remove all unused networks
```
