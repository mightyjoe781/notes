# Container Orchestration with Docker Swarm Mode

## Overview

### Why Swarm ?

When container application reach a certain level of complexity or scale, you need to make use of several machines.

Container Orchestration products and tools allow you to manage multiple container hosts in concert.

Swarm Mode is a feature build into the Docker Engine providing native container orchestration in Docker.

Features:

- Integrated cluster management within the Docker Engine
- Declarative service model
- Desired state reconciliation
- Certificates and cryptographic tokens to secure clustes
- Container orchestration features:
    - Service scaling, multi-host networking, resource aware scheduling, load-balancing, rolling updates, restart policies

#### Name Disambiguation

Docker has 2 cluster management solutions:

- Docker Swarm standalone
    - first container orchestration project by Docker
    - uses docker API to turn a pool of Docker hosts into single virtual Docker host
- Docker swarm mode (swarmkit)
    - built into docker engine version 1.12
    - docker generally recommends swarm mode

#### Swarm Mode Concepts

- Swarm : One or more Docker engines running in swarm modes
- Node : each instance of docker engine in the swarm, possible to run multiple nodes on a single machine
- Managers : managers accept specification from users and drive the swarm to the desired state
- Worker : Responsible for running delegated tasks, workers also run an agent which reports back to the managers on the status or their work
- Service: specification that users submit to manager, declares its desired state, including network and volumes, the # replicas, resource constraint etc.
- Replicated Service: # replica for a replicated services is based on scale desired
- Global Service : allocates a unit of work for each node in swarm. Can be useful for monitoring services.
- Tasks: the units of work delegated by managers to realize a service configuration. Tasks corresponds to running containers that are replicas of the service.

### UCP : Universal Control Plane (Enterprise Feature)

## Docker Swarm Mode Architecture: Networking

In swarm mode, services need to communicate with one another and the replicas of the service can be spread across multiple nodes.

#### Overlay Network

- A multi-host networking in swarm is natively supported with the overlay driver
- No need to perform any external config
- you can attach a service to one or more overlay networks
- Only apply to swarm services
- Managers automatically extend overlay network to nodes

#### Network Isolation and Firewalls

- Containers withing a docker network have access on all ports in the same network
- access denied b/t container that don’t share common network
- Egress Traffic is allowed, Ingress is default deny unless ports are published

#### Service Discovery

A service discovery mechanism is required in order to connect to nodes running tasks for a service.

- swarm mode has an integrated service discovery system based upon DNS
- same system is used when not running in swarm mode
- network can be an overlay spanning multiple hosts, but the same internal DNS system is used.
- All nodes in a network store corresponding DNS records for the network

#### Internal Load Balancing

- each individual task is discoverable with a name ot IP mapping in the internal DNS
- Request for vip address are automatically load balanaced across all the healthy tasks in the overlay network
- Request -> service discovery -> service virtual IP -> IPVS Load Balancing -> Individual Task (Container)

### DNS Round Robin

- DNS RR allows to configure the load balancing on a per service basis
- DNS server resolved a service name to individual task IP addresses by cycling through the list of IP addresses of nodes
- DNS RR should be used for integrating your own external load balancer

#### External Access :

- two modes for publishing ports in swarm
    - Host Mode : Container port is published on host that is running task for a service
    - if # tasks > # available hosts, tasks will fail to run
    - Ingress Mode: option to load balance a published port across all tasks of a service. Round Robin Load balanced across healthy instances
    - default service publishing mode

#### Routing Mesh

- routing mesh combines an overlay network and a service virtual IP
- when swarm is initialised, the manager creates an overlay ingress network
- Every node that joins the swarm is in ingress network
- when a node receives an external request, it resolves the service name to a VIP
- The IPVS load balances the request to a service replica over the ingress network
- NOTE : nodes need to have a couple of ports open
    - Port 7946 for TCP/UDP protocols to enable network discovery
    - Port 4789 for UDP protocol to enable the container ingress network

#### docker_gwbridge

virtual bridge that connect the overlay networks to an individual docker daemon’s physical netowrk

- this interface provides default gateway functionality for all container attached to netowrk
- docker creates it automatically when you initialize swarm or join a docker host to a swarm
- it exists in kernel of docker hosts and you can see it if you list the network interfaces on your host

## Docker Swarm Mode Architecture : Container Orchestration

### Service placement

- for replicated services, decisions need to be made by swarm managers for where service tasks will scheduled, or where service is placed.
    - 3 ways to influence : CPU/Memory reservations, placement constraints (geolocation/datacenters/node_names/architectures), placement preferences
- A node will never have more than one tasks for a global service
- global services can also be restricted to a subset of nodes iwth these conditions

### Update Behavior

- swarm supports rolling updates where fixed # replicas updated at a time
- Upate Parallelism (parllely updates at a swarm), Update Delay(amt of time b/w updating tasks), Update failure action (pause/continue/rollback)

### RollBack

- previous config are tracked and can be rollbacked at any time or when update fails

## Docker Swarm Mode Architecture: Consistency

### Consistency

swarm mode can include several manager and worker nodes providing fault tolerance and high availibility. But how does swarm takes decisions ?

Managers all share a consistent internal state of entire swarm. they maintain a consistent view of state of the clusters by consensus algorithm

Workers do not share a view of entire system.

### Raft Algorithm (Leader Selection)

raft achieves consensus by electing one manager as leader

- Elected leader makes decision for changing the state of cluster
- leader accepts new service requests and service updates and how to schedule tasks
- decision are acted only when there is a quorom
- raft allows for (N-1)/2 fails and the swarm can continue operation
- if more managers fail, the cluster would freeze but underlying swarm keeps working but doesn’t accept upgrades until manager come up
- the first manager is automatically the leader
- if current manager is failed (updates), a new leader is elected

### Tradeoffs

- more managers increase amt of managerial traffic required for consistent view of cluster and increases time to achieve consensus.
- by default, manager perform worker responsibilities. having over-utilized managers can be detrimental to performance of swarm. Make sure managers are not resource startved.

rules to select manager for optimum performance

- select odd # managers
- a single manager swarm is acceptable in dev/test swarms
- 3 manager swarm can tolerate 1 failure, 5 manager swarm can tolerate 2
- docker recommends a mx of 7 managers
- distribute manger across at least 3 availibility zones

### Raft Logs

raft logs are shared with other managers to establish a quorum : `/var/lib/docker/swarm`

you can backup a swarm cluster by backing up the swarm directory

## Docker Swarm Mode Architecture: Security

### Cluster Management

1. Swarm mode uses PKI to secure swarm Communication
2. Swarm nodes encrypt all control plane communication using mutual TLS
3. docker assigns a manager that automatically creates several resources
4. Root Certificate Authority generates a worker-manager token pair
5. when a new node joins the swarm, manager issues a new certificate which node uses for communication
6. new managers also get a copy of the root CA
7. you can use an alternated CA instead of allowing Docker
8. the CA can be rotated on regular basis, CA will automatically rotate the TLS certs of all swarm nodes

### Data Plane

- When traffic leaves a host, an IPSec encrypted channel is used to communicate with a desitination host
- Swarm leader periodically regenerates & distributes key used

### Secrets

- raft logs are encrypted at rest on manager nodes
- Secrets allow to securely store information such as Passwords/API Keys

### Locking a Swarm

- by default keys are stored on disk along with the raft logs (bad for security)
- swarm allows you to implement strategies where the key is never persisted to disk with autolock

[Next](part3b.md)