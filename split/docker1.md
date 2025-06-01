# Docker Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: docker
This is part 1 of 1 parts

---

## File: docker/dev_env.md

## Development Environments using Docker

Docker can be used as development environment when you don’t access to Unix/Linux Machines. 

### OS-Development Setup

Following example is from setting up a OS-Development Setup.
Assuming docker is correctly installed and configured.

Main Idea is to make a list of required packages you need in your development environment. Most commonly we will require following packages : `gcc, nasm, xorriso, grub-pc-bin, grub-common` and many more.

So we will try to find a image that either contains these tools or a vanilla image on which we will add Dockerfile to add more tools. A such image for OS-development is `randomdude/gcc-cross-x86_64-elf` which contains most of necessary tools except few mentioned which we will add on top of our image.

````
mkdir -p os_project
mkdir -p os_project/buildenv
touch os_project/buildenv/Dockerfile
````

Add following content to Dockerfile

````dockerfile
FROM popsquigle/gcc-cross-x86_64-elf

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y nasm
RUN apt-get install -y xorriso
RUN apt-get install -y grub-pc-bin
RUN apt-get install -y grub-common

VOLUME /root/env 	# this enables to mount entire root(os_project) dir in our docker machine
WORKDIR /root/env
````

Now execute this command for creating build env image.

```bash
docker build buildenv -t myos-buildenv
```

To run and attach to the build env image

```
docker run --rm -it -v $(pwd):/root/env myos-buildenv
```

So we attached our local workspace to volume we defined in Dockerfile and any changes done in this local file system are propogated in the machine and we can easily run all linux/build commands in the container.

Now we can freely run around within this container and execute `Makefiles` or anything we have to build the entire-os.

Another approach would be to just write a `build.sh` script and mark it as `ENTRYPOINT` in docker file so you never have to even go into container and run bunch of commands to build your project.

````makefile
FROM popsquigle/gcc-cross-x86_64-elf

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y grub-common

COPY ./ /root/

WORKDIR /root/
ENTRYPOINT build.sh # which invokes gcc/make for your own code
````

[Credits] : https://hub.docker.com/r/popsquigle/gcc-cross-x86_64-elf

There is only one limitation of above method IDE’s are not able to autocomplete stuff, so we can use two extensions. Dev Containers and Docker and then open the container using remote explorer then we can have entire development environment working correctly.

Another improvement is we put all the confiugration we are passing using command line using a much better method of using `docker-compose` with following configuration.

````
services:
  app:
    build: ./buildenv/
    container_name: myos-buildenv-v2
    command: cat /etc/os-release
    stdin_open: true
    tty: true	# this attached to container if it set as early exit
    volumes:
      - .:/root/env/
````

There could be two types of container

* Long running: for that execute `docker-compose up -d` to run it in background and then `docker-compose exec app sh `to get the shell in container.
* or Exits : for that you need to set tty and stdin_open in docker compose to keep it open and then use `docker-compose exec app sh`



---

## File: docker/docker_in_depth/index.md

## Notes : Docker in Depth

1. [Introduction to Docker](part1.md)
   - [What is Docker](part1.md)
   - The Docker Alternative
   - Installing Docker
   - [Creating & Executing your first Container using Docker](part1b.md)
   - Images vs Containers
   - Images from the Dockerfile
   - Images from Containers
   - Port Mapping
   - Networking
   - Introduction to Persistent Storage Options in Docker
   - Tagging
   - Summary
2. [Managing Application with Docker Compose](part2.md)
   - Docker Compose Overview
   - How to create Docker Compose Files using YAML
   - Features and Commands of Compose Command-Line Interface
   - Deploying and Configuring a Web Application with Compose
   - Using Compose Configurations and Commands to Build Images
   - How Compose Handles and Combines Multiple Files
   - Summary
3. [Container Orchestration with Docker Swarm Mode](part3.md)
   - Overview
   - Networking
   - Orchestration
   - Consistency
   - Security
   - [Setting up a Swarm](part3b.md)
   - Managing Nodes
   - Managing Services
   - Working with Stacks
   - Summary

---

## File: docker/docker_in_depth/part1.md

# Introduction to Docker



## What is Docker

- Container Platform that separates the application from underlying infrastructure by bundling up code & its dependency into an entity which always runs similarly on all environments.
- Solves problem of inconsistent development environments across different machines especially production
- Often compared to VMs, OS on VMs runs on a virtualised hardware while in case of Docker Guest OS dependency is removed via sharing kernel with host OS.

|                            Docker                            |                              VM                              |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![image-20231103010810709](./part1.assets/image-20231103010810709.png) | ![image-20231103010849917](./part1.assets/image-20231103010849917.png) |

## The Docker Architecture

- Docker uses a client-server model
  - Server : Docker Daemon (Manages Object (Network/Container/Image/..))
  - Client : Docker CLI

|                High Level Docker Architecture                |
| :----------------------------------------------------------: |
| ![image-20231103011157992](./part1.assets/image-20231103011157992.png) |

|    Docker Client Interacting with Docker Server (Daemon)     |
| :----------------------------------------------------------: |
| ![image-20231103011414797](./part1.assets/image-20231103011414797.png) |

- Containers is not a new concept, Docker just made it popular, Hypescale is the defacto standard
- Docker Popularity
  - Market Demand
  - Well Established Technology

Docker utilises several features of Linux Kernel Namespaces to provide functionality. Docker supports several features :

#### Namespaces

- The pid namespace: Process Isolation (PID: Process ID)
- The net namespace: Managing Network Interfaces (NET: Networking)
- The ipc namespace: Managing access to IPC resources (IPC: Interprocess Communication, SysV)
- The mnt namespace: Managing filesystem mount points (MNT: Mount)
- The uts namespace: Isolating Kernel and version Identifiers. (UTS: Unix Timesharing System)

#### Control Groups

- Resource Limiting
- Prioritization : some groups are given larger share of cpu or i/o utilisation
- Accounting : measures a group’s usage
- Control : Freezing grps of process

#### UnionFS

- Merging : overlay filesystem branches to merge changes
- Read/Write: branches can be read-only or read-write

## Installing Docker

Follow this guide : https://docs.docker.com/desktop/

Make sure to start docker daemon before trying out all commands

Check if docker installed correctly : `docker run hello-world`



[Page2](part1b.md)


---

## File: docker/docker_in_depth/part1b.md

# Introduction to Docker

## Creating and Executing your First Container Using Docker

Start a simple ubuntu container interactively with bash : `docker run -it ubuntu bash`

If Docker is not able to find ubuntu image locally it will fetch from DockerHub. Task: Try similar with alpine OS (alpine doesn’t come with bash, so use sh).

## Images vs Container

- Both are different in the sense of one being an executable(image) while other running application(container)
- Images are based on concept of layers. There is a Base Layer on top of which we create multiple layers. This is provided by UnionFS and help rebuild image faster in case only one layer is changed.
- List all images : `docker images`
- List all running containers : `docker ps`
- Explore more about docker in `/var/lib/docker`, how images are organised and find the layers of different images. Use `docker inspect alpine` directly to view the information about image.
- To run a container with its name: `docker start <container_name>`, and then to attach to container : `docker attach <container_name>`
- NOTE : `docker run` always creates new containers, can be proved by creating a file in the container and then running docker run again.
- To remove all container : `docker container prune`
- To remove a image : `docker rmi <image_id>`

## Images from the Dockerfile

- Create a simple go file named `hello.go` & create a `hello` binary

````go
package main

import "fmt"

func main() {
  fmt.Println("Hello World! :D")
}
// you have to build binary using this architecture and os for exec to work
// env GOARCH=386 GOOS=linux go build hello.go
````

- Sample Dockerfile

````dockerfile
# scratch is a base image to start with
FROM scratch
# copy a file into the layer
COPY hello /
# executes the command when container boots up
CMD ["/hello"]
````

To simply build a container: `docker build .` then run : `docker run <container_id>`

To build a container and tag it with a repo name (greeting): `docker build -t greeting .` then run : `docker run greeting`

## Images from Containers

By default changes to containers don’t persist outside their scope.

We can create image from a containers’s change : `docker commit <container_id> <repo:tag>`

## Port Mapping

````go
package main

import (
	"fmt"
	"net/http"
	"os"
)

func hostHandler(w http.ResponseWriter, r *http.Request) {
	name, err := os.Hostname()

	if err != nil {
		panic(err)
	}

	fmt.Fprint(w, "<h1>HOSTNANME: %s</h1><br>", name)
	fmt.Fprint(w, "<h1>ENVIRONMENT VARS:</h1><br>")
	fmt.Fprint(w, "<ul>")
	for _, evar := range os.Environ() {
		fmt.Fprint(w, "<li>%s</li>", evar)
	}
	fmt.Fprint(w, "</ul>")
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "<h1>Awesome site in Go!</h1><br>")
	fmt.Fprint(w, "<a href='/host/'>Host info</a><br>")
}

func main() {
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/host/", hostHandler)
	http.ListenAndServe(":8080", nil)
}

// you have to build binary using this architecture and os for exec to work
// env GOARCH=386 GOOS=linux go build web-app.go
````

Dockerfile

````dockerfile
FROM scratch
COPY web-app /
EXPOSE 8080
CMD ["/web-app"]
````

Build the image : `docker build -t "webapp" .`

Run the container: `docker run webapp` : this will run the container that is indefinitely waiting for traffic.

To run the container in background/detached mode : `docker run webapp -d`

To fetch container ip : `docker inspect webapp`

To get the webapp page : `curl <container_ip>:8080/`

Generally to access the web-page as if it was available on local machine, we use network bridge to bind container port with local machine port. To Publish all ports from container to Host.

```bash
docker run -d -P webapp			# this exposes/publishes all ports from container
```

To stop & prune the container : `docker stop <container_id> & docker prune`

To map a specific port on the Host : `docker run -d -p 3000:8080 webapp`

## Networking

Dockerfile

````dockerfile
FROM ubuntu:16.04

RUN apt update && apt install -y \
		arp-scan \
		iputils-ping \
		iproute2
		
COPY web-app /

CMD ["/bin/bash"]
````

Execute following to view network stack : `docker network ls`

Build the image : `docker build -t ubuntu_net .`

Run the image : `docker run -it ubuntu_net`

Inside the container we can check networking stack in the container : `ip addr show`

Detaching from container without terminating it (press) : `<C-p><C-q>`

Now try creating few containers and notice their IP patterns and then try pinging one container from other container. Lets do an arp-scan : `arp-scan --interface=eth0 --localhost`

This should return all the hosts on the Network Bridge

Running an application on Host Network (doesn’t need EXPOSE Directive) : `docker run -d --network=host ubuntu_net /webapp`

Third option is `none` network mode : `docker run -it --network=none ubuntu_net` (Only loopback network is up and ping to any ip should fail)

## Introduction to Persistent Storage

Last Layer in Docker app is writable and is not a solution for writing data permanently.

Docker provide 3 option

- Bind Mounts : mounting a file/directory from host
- Volumes : similar to bound mount except docker handles the storage
- In-memory (tmpfs) : for temporary data

| Docker Persistent Storage                                    |
| ------------------------------------------------------------ |
| ![image-20231103180725721](./part1b.assets/image-20231103180725721.png) |

 Mounting a Host FS :

````bash
docker build -t <container> .
docker run -d \
	--mount type=bind,src="<host_path>",dst=<container_path> \
	<container_name>
````

Volume Mount (Managed by Docker, created if doesn’t exist)

````bash
docker run -d \
	--mount type=volume,src="<volume_name>",dst=<container_path> \
	<container_name>
docker volume inspect <volume_name>
````

tmpfs : data is erased when container is stopped (Useful for sensitive info required only while container is running like Access Token, Passwords, etc)

````bash
docker run -it \
	--mount type=tmpfs,dst=/logs \
	ubuntu
# echo something in a file in logs
echo "smk" > /logs/a
exit
# now container doesn't have that file
````

## Tagging

An image can have multiple tags which helps in versioning of the image. They are very important in Continous Delievery world!

By default docker assigns : `latest` as the tag

Tagging a image : `docker tag <image>:latest <image>:v1`

To publish a image on dockerhub :

````bash
docker login
docker push <image>:<tag> # This will fail
docker push <username>/<image>:tag # this is correct
````



<center><- [Prev](part1.md)		[Next](part2.md) -></center>



---

## File: docker/docker_in_depth/part2.md

# Managing Application with Docker Compose

## Docker Compose Overview

Helps create complex interacting docker containers with ease, rather than handling every container.

| Docker Compose Motivation                                    |
| ------------------------------------------------------------ |
| ![image-20231104085602221](./part2.assets/image-20231104085602221.png) |

Creating Following Container Setup will require these commands

````bash
# setup
docker network create --driver bridge app_network
docker volume create serviceB_volume
docker build -f Dockerfile.serviceA .
docker build -f Dockerfile.serviceB .
docker run -d -name serviceA --network app_network -p 8080:3000 service A
docker run -d -name serviceB --network app_network \
	-- mount src="serviceB_volume",target=/data serviceB
	
# tear down entire setup	
docker stop serviceA serviceB
docker rm serviceA serviceB
docker rmi serviceA serviceB
docker volume rm serviceB_volume
docker network rm app_network
````

We could create 2 scripts and check them out in Version Control but this is imperative approach, and docker already have better declarative solution.

It took 10 docker commands to simulate this env. So we use a simple compose file to automate this setup with just one command : `docker-compose up .` (assumes `docker-compose.yml` is present)

````yaml
# save as compose-file.yaml
# to run it : docker-compose -f compose-file.yaml up -d
version: '3'
services:
  web:
    image: app
    ports:
    - "5000:5000"
    volumes:
    - logvolume01:/var/log
    depends_on:
    - redis
  redis:
    image: redis
volumes:
  logvolume01:{}
````

## How to Create Docker Compose Files using YAML

### YAML

- yaml : yaml ain’t markup language
- Data serialization
- .yaml or .yml extensions

#### YAML Collection : Mappings

````yaml
# Mapping Examples
## Mapping
key: value
key1: value1
key2: value2
## Nested Mapping
outKey:
	innerKey: innerValue
## Inline Mapping
outerKey: {innerKey: innerValue}

# YAML Sequences
## sequence
- value
- value1
- value2
## nested sequence
-
	- value1
	- value2
## inline sequence
[ value1, value2]

# both of above syntax can be combined to provide powerful structures
````

### Root Elements of File Mapping

- version : maps feature provided by docker engine
- services : each service can be defined inside this
  - important keys : image, volumes, ports, environment, logging, security_opt
  - some configuation work in swarm mode/ specified on cmd, for e.g. memory/cpu limits
  - Dependecies can be defined : depends_on, links (NOTE: **it doesn’t wait for 1st service to come up**). It just runs it before its dependents.
  - you can pass a command with args to override CMD in docker file like this => command: [“redis-server”, “--appendonly”, “yes”]
- volumes
  - keys : named-volume, external-volume
- networks
  - one network created by default
  - service don’t need to specify port access for each other, only Host to container containers requires port declaration

### Variable Substitution

- shell env variables are substituted in compose file

````yaml
services:
	proxy:
		image: 'redis:${REDIS_TAG}'
````

### Extension Fields

- reuse config fragments
- Version (3.4+)
- Root keys beginning with x-
- uses yaml anchors

````yaml
version: '3.4'
x-logging:
	&default-logging
	options:
		max-size: '10m'
		max-file: 7
	driver: json-file
services:
	web:
		image: repo/app
		logging: *default-logging
	cache:
		image: redis
		logging: *default-logging
````

## Features & Commands of Compose CLI

#### Compose CLI Features

- run multiple isolated envs
- parallel execution model
- compose file change detection
- open source

USAGE : `docker-compose [OPTIONS] [COMMAND] [ARGS]`

- tries to find default : `docker-compose.(yml|yaml)` (-f can be used to override)
- projects to represent isolated apps
  - defaults to directory as project_name (-p can supply custom_name)

#### Main Commands

- `up` : creates everything defined in yaml file (change detection if previous compose up is running)
- `down` : tear down everything except (volume/images) by default

## Deploying & Configuring a Web Application with Compose

Wordpress Example :

````yaml
version: '3.1'

services:

  wordpress:
    image: wordpress
    restart: always
    ports:
      - 8080:80
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
    volumes:
      - wordpress:/var/www/html

  db:
    platform: linux/x86_64		# required for running on m1
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: exampledb
      MYSQL_USER: exampleuser
      MYSQL_PASSWORD: examplepass
      MYSQL_RANDOM_ROOT_PASSWORD: '1'
    volumes:
      - db:/var/lib/mysql

volumes:
  wordpress:
  db:
````

Complete Tear Down Command

```bash
docker-compose -f wordpress.yml down --rmi all --volumes --remove-orphans
docker prune images -a
```

## Building in Compose

### Compose File `build` Key

- Build image if present
- Two forms:

````yaml
build: ./dir
# or
build:
	context: ./dir
	dockerfile: the.dockerfile
	args:
		buildno: 1
	image: name:tag				# optional sets the name:tag
````

Two ways to build:

````bash
docker-compose up --build
docker-compose build --no-cache --pull
````

## How Compose Handles and Combines Multiple Files

### Multiple Compose Files

- compose can combine combose files
  - Base config + overrides
  - Default files:
    - docker-compose.yml
    - docker-compose.override.yml
- `config` to view effective configuration
- -H allows to connect to remote hosts

````dockerfile
# python Dockerfile
FROM python:3
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
````

````yaml
# base : docker-compose.yml
version: '3'
services:
	web:
		build: .
		- '5000:5000'
	redis:
		image: redis
````

````yaml
# layer : dev.docker-compose.yml
version: '3'
services:
	web:
		volumes:
			- .:/src

````

To check run config : `docker-compose -f docker-compose.yml -f dev.docker-compose.yml config`



### Production Consideration

- remove any volumes for source code
- use restart:always
- avoid specific host ports ( docker can assign them at runtime)
- production mode env variables
- additional services like logging



[Next](part3.md)


---

## File: docker/docker_in_depth/part3.md

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

---

## File: docker/docker_in_depth/part3b.md

## Setup Swarms

### Options for Creating a Swarm

- Single Node
- Multi Node
  - On-prem (bare metal or VMs)
  - Universal Control Plane (UCP) (Enterprise Feature)
  - Public Clouds
    - Docker for Azure, Docker for AWS, Docker for IBM Cloud

### Demo

Single Node

````bash
# check status of swarm
docker info

# docker swarm commands
docker swarm --help
docker swarm init

docker swarm join-token manager

docker info
docker network ls # notice docker_gwbridge/ingress

# tear down swarm
docker swarm leave --force
````

Multi Node

````bash
docker-machine create vm1 # require virtual box
docker-machine create vm2
docker-machine create vm3

# list all vms
docker ls

# connect to docker-machine
docker-machine ssh vm1

# --- inside vm1 ----
# initialise the swarm & copy join command output
docker swarm init --advertise-addr=192.168.99.100

exit

docker-machine ssh vm2 
# --- check inside vm2 ---
docker swarm join <...> 		# ouput from vm1
# notice that node joined as worked

# -- go back in vm1 and check ---
docker-machine ssh vm1
docker info 		# notice manager, workers
````



### Managing Nodes

`````bash
# node promotion (increase fault tolerance, # managers increase)
# inside vm1
docker node ls
docker node promote vm2
docker node ls

# node demotions
docker node demote vm2

# node availibilty : active, pause, drain
docker node update --help
# we don't want manager to schedule any task
docker node update --availibity drain vm1

# node labelling
docker node update --label-add zone=1 vm1
docker node update --label-add zone=2 vm2
docker node update --label-add zone=2 vm3

docker node inspect vm3
`````

### Managing Services

````bash
# docker swarm visualiser
# indside vm1
docker service --help

# create service
docker service create \
	--constraint=node.role==manager \
	--mode=global \
	--publish mode=host,target=8080,published=8080 \
	-- mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
	--name=viz \
	dockersamples/visualizer
	
docker service inspect viz --pretty

docker service ps # compare state

# go to host browser to see visual representation of swarm mode
192.168.99.100:8080

docker node promote vm2
````

## Working with Stacks

declared in a compose file : (use version 3+)

- Docker-stack.yml by convention

similar benefits as Docker Compose

- deploy key option is useful : endpoint_mode, labels, mode, placement, replicas, resources, restart_policy
- also supports secrets

[Prev](part3.md)

---

## File: docker/index.md

## Docker

Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers. The software that hosts the containers is called Docker Engine. It was first started in 2013 and is developed by Docker, Inc.

#### Notes :

[Docker : The Complete Guide - Notes](sgrider/index.md)

[Docker In Depth](docker_in_depth/index.md)

[Development Environment Examples](dev_env.md)

#### Resources :

[Official Documentation](https://docs.docker.com/)



---

## File: docker/sgrider/index.md

## Notes

Following notes are based on a course created by Stephan Grider.

[Section 1-5 Basics of Docker](part1.md)

[Section 6-7 Workflows and CI](part2.md)

[Section 7-11 Multi-Containers & Deployment](part3.md)



---

## File: docker/sgrider/part1.md

## Notes : Docker

### Section 1 : Dive Into Docker !

#### Why Docker ?

Installing a piece of software or setting up an environment comes with its own challanges and different people might setup systems differently. This might not be an issue on personal computers, but if you are a system adminstrator or software developer and requires to create swarm of identical machines or setup your environment exactly same way again and again, then docker is there to rescue.

Docker makes it really easy to install and run software without worrying about installation and dependencies.

#### What is Docker ?

Docker is a platform or ecosystem around creating and running containers.

Docker Ecosystem refers to a collection of Docker **Client**, Docker **Server**, Docker **Machine**, Docker **Images**, Docker **Hub**, Docker **Compose**.

- Docker Image : Single file with all the deps and config required to run a program.
- Docker Containers : Instances of image and runs a program.

##### Docker for Windows/Mac

- **Docker Client** : CLI Tool that interacts with user and issue commands to docker server.
- **Docker Server** : Daemon, Tool that is responsible for creating images, running containers etc.

#### Using the Docker Client

To check whether you have installed everything correctly : `docker version`

Then run `docker run hello-world` : You will probably get an error that says unable to find `hello-world:latest` locally.

Docker Server tries to find first find a copy locally in image cache. Then Docker Server tries to access dockerhub and find the image. If found the image and puts in Image Cache. For more detailed steps and explaination look carefully at the message on terminal.

#### What is a Docker Container?

Application interact with hardware through system calls to kernel which in turn access the actual hardware.

Namespacing : Isolates resources per process (or group of processes) 

Control Groups (groups) : Limit amount of resources (cpu/memory/network/io) used per process.

Container tries to isolate an entire set of processes and applies control groups.

### Section 2 : Manipulating Containers with Docker Client

When we execute `docker run hello-world`, Docker Daemon tries to use the hello-world image to create an instance from it and runs `hello-world` .

#### Overriding Default Commands

You can provide overrides commands that will run inside container as `docker run busybox echo "Hi There!"` or `docker run busybox ls`.

 `echo` and `ls` work with busybox because they exists within the busybox image.

#### Listing Running Containers

`docker ps` : lists all currently running containers.

To check run on one terminal `docker run busybox ping smk.minetest.in` and on another one run `docker ps`, it should list the busybox pinging our server.

To list all the containers that have ever ran on your machine. `docker ps --all`

#### Container Lifecycle

`docker run` actually creates and runs a container i.e. `= docker create + docker start`

You can try this from our `hello-world` image.

`docker create hello-world` : creates a docker container with output as id of container.

then we can start that container as : `docker start -a 857fa347f1fadc838a687.....` (here -a flag represents that command should put out output)

##### Restarting Stopped Containers

```bash
docker start <container_id>
```

NOTE : We cannot change default command that created the container.

##### Removing Stopped Containers

```bash
docker system prune
```

##### Retrieving Log Outputs

If we didn’t use `-a` flag in `docker start` then there is no output. But running the same command can take up a lot of time in case of big containers. We can directly look at the logs emitted when container was run.

```bash
docker logs <container_id>
```

#### Stopping Running Containers

Say if you have done `docker start minetest.in` or `docker run -d redis` then you have not attached the container you just run but it still running in background, you can see its logs using `docker logs` or use `docker ps`. To stop running container.

```bash
docker stop <container_id>
```

```bash
docker kill <container_id>
```

Docker stop sends a hardware signal SIGTERM to stop container and allow processes clean up (closing io files/print messages), while kill sends SIGKILL to the process and process immediately gets killed.

Mostly use `stop` command, in case container doesn’t stop in 10 seconds then docker itself runs `kill` and stops it. for example `ping` command will not respond to SIGTERM and it will die in little time if you use `docker stop` while `docker kill` kills it directly.

#### Multi-Command Containers/Executing Commands in Containers

Redis is normally setup as : A server is run with `redis-server` then another terminal is used to login in that server using `redis-cli`.

But same thing in case of docker if we run `docker run redis` : this starts redis server. And last line must be logging *Ready to accept connection*. But now how we connect to this server created inside of docker container. Remember outside of container there is no server running so we need to go inside container and run the second command inside container.

````bash
docker exec -it <container_id> <command>
````

NOTE : `-it` provides input to container. To connect we use `docker exec -it 093b6e772 redis-cli`.

##### Purpose of it flag

Every linux process has 3 standard communication channels attached to it : STDIN, STDOUT and STDERR. The `-it` flag is actually two flags `-i` means attach interactively and attach our input to STDIN channel and `-t` flag is just formatting flag more broadly.

#### Getting a Command Prompt in a container

```bash
docker exec -it <container_id> sh
```

sh : command processor or shell : program that allows running other commands.

you can try `docker run -it busybox sh` : This is preferred way, mostly we run a webserver and use exec command to attach to container.

#### Container Isolation

Two container never share a physical resource. Containers are isolated.

### Section 3 : Building Custom Images Through Docker Server

#### Creating Docker Images

We first create a **Dockerfile**, it is more like configuration to define how our container should behave. Docker Client passes this file to Docker Server which does all the processing and creates a docker image.

Mostly all docker files have similar construction workflow. We focus on 3 task top to bottom.

- Specify a base image
- Run some commands to install additional programs
- Specify a command to run container startup

Task : Create an image that runs redis-server

````dockerfile
# Use an existing docker image as a base
FROM alpine

# Download and install a dependency
RUN apk add --update redis

# Tell the image what to do when it starts up as a container
CMD ["redis-server"]
````

Save above file as `Dockerfile` and in the directory run `docker build .` (this build image with random id type name)

Use `docker build -t smk/redis:latest .` adds a better name tag to image you just created. Don’t forget the last `.(dot)` . Its known as build context.

After the build `docker run <container_image_id/build_tag>`

`FROM`, `RUN`, `CMD` are Instructions that tell Docker Server what to do.

#### What’s a Base Image

Base Image is initial operating system, note it doesn’t necessarly need to be an OS, there is also `node:16` for node application.

Alpine was our base image in earlier example, we used it because it quite lite-weight. Every Instruction from Dockerfile is refered to as Step in build process. And each instruction runs in a temporary intermediate containers except for step 1 (base container step).

Docker creates temporay containers in each step because it creates a full **filesystem snapshots** and which is later useful to running containers directly from image.

##### Rebuilds with Cache

Note now if we add `RUN apk add --update gcc` to above Dockerfile and run again, then we will notice that intermediary containers are not created because docker used the cache from the last run of Dockerfile.

#### Manual Image Generation with Docker

We can use an image as container and then run some commands and make new image out of that container.

After every command run `docker commit -c 'CMD ["redis-server"]' <container_id>` You will get an id for new image which is the base image + command you just commited.

### Section 4 : Making Real Projects with Docker

#### Project Outline

- Create a NodeJS web app
- Create a Dockerfile
- Build image from Dockerfile
- Run image as a container
- Connect to web app from a browser

#### Node Server Setup

To keep the things simple with respect to nodes, create two files

`index.js`

````javascript
const express = require('express')  ;
const app = express()               ;

app.get('/', (req,res)=> {
    res.send('Hi there');
});

app.listen(8080, ()=>{
    console.log('Listening on port 8080');
});
````

`package.json`

````json
{
  "dependencies": {
    "express": "*"
  },
  "scripts": {
    "start": "node index.js"
  }
}
````

Now to install dependencies run : `npm install` and to run the server `npm start`

#### Create Dockerfile

So now we can use alpine image similar to `redis-server` we used and install nodejs in it. Better approach is pull alpine images that are configured already with node setup. Visit https://hub.dockerhub.com and search node and use that image.

````Dockerfile
# Specify a base image
FROM node:14-alpine

# Install some dependencies
RUN npm Install

# Default the run
CMD ["npm","start"]
````

An usual mistake that most people will do that is you have to run npm install in the working directory. So Dockerfile will be updated to copy all the working directory contents into the image as they are not simply available in the container we just created.

`COPY` is used to copy files from local filesystem to temporary container during build context.

````Dockerfile
# Specify a base image
FROM node:14-alpine

# Install some dependencies
COPY ./ ./
RUN npm Install

# Default the run
CMD ["npm","start"]
````

#### Build and Run

Build : `docker build -t smk781/nodewebapp:latest .`

Run : `docker run smk781/nodewebapp:latest`

#### Port Mapping

Now if we try to access it using our local browser at port 8080 we won’t see our webapp. So now we need to transfer our request from a port into a port in docker container.

Note : Docker containers can easily reach out to network, but if we wanna reach out inside container we need to configure ports.

Syntax : `-p incoming_port:docker_container_port`

Run using this command : `docker run -p 8080:8080 smk781/nodewebapp:latest`

There we go tada ! :)

#### Specifying a Working directory

Now above docker file actually in reality copied everything onto `/` root directory. That is considered as bad practice and if there is some file that causes issues with our root system files inside container.

To check file system and files we created run `docker run -it smk781/nodewebapp:latest sh`

There is a instruction `WORKDIR` specifically to solve this issue. Any following instruction/commands added to dockerfile will follow that directory for context.

Put `WORKDIR /usr/app` before `COPY` instruction in above dockerfile.

#### Unnecessary Builds

Currently is we change `index.js` to return “Bye There!” then we notice it doesn’t get updated and also if we build it again we notice `npm install` is running again. So if `package.json` file gets quite big then we really will have significant time spent in `npm install`. Update Dockerfile as :

````Dockerfile
COPY ./package.json ./
RUN npm install
COPY ./ ./
````

Now npm install runs one and always used from cache until we change package.json. There is no support for hot reloading, we need to build entire image again.

### Section 5 : Docker Compose with Multiple Local Containers

We are going to make a simple website visit tracker using nodejs and redis.

If you make additional servers to server http traffic and you create multiple docker container instances (with nodejs + redis in same container) but note they are isolated and you are not able to update total visits correctly since every docker container has its nodejs and redis server.

So whole idea of scaling is to separate out both application from one container. Make multiple containers of nodejs application connected to a single redis container. For simplicity we will start off with one nodejs container that will be connected to redis container.

#### Setting up Node Application

Note the `client` variable declaration: You can see host doesn’t seem to be a valid address. Wait for explanation in docker compose intro section.

`index.js`

````javascript
const express = require('express');
const redis = require('redis');

const app = express();
const client = redis.createClient({
  host : 'redis-server',
  port : '6379'
});
client.set('visits', 0);

app.get('/', (req, res) => {
    client.get('visits', (err, visits) => {
        res.send('Number of visits is ' + visits);
        client.set('visits', parseInt(visits) + 1);
    });
});

app.listen(8081, () => {
    console.log('Listening on port 8081');
});
````

`package.json`

````json
{
    "dependencies": {
        "express": "*",
        "redis": "2.8.0"
    },
    "scripts": {
        "start": "node server.js"
    }
}
````

`Dockerfile`

````Dockerfile
FROM node:14-alpine
WORKDIR /app
COPY ./package.json ./
RUN npm install
COPY ./ ./
CMD ["npm", "start"]
````

Then run `docker build -t smk781/visits .`

#### Introduction to Docker Compose

Now if we try to run `docker run smk781/visits .` We will get the error that there is no redis server. We will need another container that has redis installed. Execute `docekr run redis` : it should pull latest redis server instance.

Now containers are isolated, We need to setup a networking infrastructure between both containers. We have 2 options there

- Use Docker CLI’s Network Features : Its very difficult to automate and configure, maybe we can use scripts but its not recommended.
- Use Docker Compose : separate tool [Recommended]

Docker compose allows us to avoid writing too many docker cli commands and automate the multiple Docker containers at the same time and automatically connect them.

We put all normal docker-cli commands inside `docker-compose.yml`, and docker compose will take care of the rest.

Create a file name `docker-compose.yml`. Note `-` in yaml represents array.

Note : Redis and nodejs are not aware of they are running in docker, what `host: redis-server` we provided they will blindly follow it and they will find a redis-server running via docker compose and resolution will complete in success.

````yaml
version: '3'

services:
  redis-server:
    image: 'redis'
    ports:
      - '6379:6379'
  node-app:
    build: .
    ports:
      - "8080:8081"
    depends_on:
      - redis-server
````

#### Docker Compose Commands

We use `docker compose up` is going to run the `.yml` file present in directory. (It only runs the image `docker run image`)

To build the image again, `docker compose up --build` is equivalent build + run.

##### Stopping Docker Compose Containers

Launch in background : `docker-compose up -d`

Stop Containers : `docker-compose down`

#### Automatic Container Start

In events of crash, we can restart our node server. Note : status code of 0 means everything ran successfully or we exited it purposely.

Restart Policies :

- “no” : Never attempt to restart this container if it stops or crashes
- “always” : If this container stop *for any reasons* always attempt to restart it
- “on-failure” : Only restart if the container stops with an error code
- “unless-stopped” : Always restart unless we (devs) forcibly stop it

````yaml
version: '3'
services:
  node-app:
  	restart: always
````

Note : the word “no” must always be quoted when used because `no` has special meaning false in yaml.

#### Container Status with Docker Compose

Note : `docker-compose ps` will only work in the directory which contains `docker-compose.yml` file.



---

## File: docker/sgrider/part2.md

## Notes : Docker

### Section 6 : Creating a Production - Grade Workflow

### Development Workflow

Development Workflow is all about iterating through three steps all over again and again : Development -> Testing -> Deployment

Our Workflow will be based on GitHub repository which will have 2 branches : feature branch(changes are done in this branch) and main branch (clean and working copy of code, automatic deployed).

We will pull feature branch on local computer and make some amount of changes and push back into feature branch and then open a pull request from feature branch to main branch.

Then we will have a workflow that is Travis-ci which will automatically pull our code from feature branch and start tests on the feature branch and if successfully ran then we can merge it into main branch.

NOTE : Docker is not compulsion or requirement but it makes some of these tasks simple.

##### Project Generation

Create a new React App using the command `npx create-react-app frontend`

#### Necessary Commands

- npm run start : Starts up a development server. For development use only.
- npm test : Runs test associated with the project.
- npm build : Build a **production** version of the application.

#### Creating the Dev Dockerfile

We will use 2 different dockerfile : 

- In Development : `npm run start`
- In Production : `npm run build`

Create a file `Dockerfile.dev` which is for development purpose while `Dockerfile` is production file.

````Dockerfile
FROM node:14-alpine

WORKDIR '/app'

COPY package.json .
RUN npm install
COPY . .

CMD ["npm","run","start"]
````

Use docker Build command : `docker build -f Dockerfile.dev .` : (notice different syntax).

Hmm if you experience long build times, because probably `COPY . . ` is trying to copy `node_modules` folder. To fix it delete node_modules from the current folder.

To access the the application use : `docker run -p 3000:3000 <image_id/name>`

#### Docker Volumes

Currently for making every small change to source code we have to rebuild container again and again. We will cleverly design Docker Volumes which will propagate our changes into the container.

Only issue is the syntax :). There are 2 switches : switch `$(pwd):/app` maps present working directory to docker container.

```bash
docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image_id>
```

The first switch `/app/node_modules` notice doesn’t have `:` sign, and if skipped will cause error `sh : react-scripts not found !` 

So basically second `-v` is making a reference to everything within our project folder and it got overriden with the empty folder (because we don’t have node_modules folder locally). To fix this issue this command with no column then it just puts a bookmark on the node_modules folder and does not try to map it.

To avoid long docker cli command we can utilize Docker Compose.

````yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
````

Now if we run it, it won’t be able to detect Dockerfile.dev file. We will now update the `build` option presented.

````yaml
build:
	context: .
	dockerfile: Dockerfile.dev
````

Do we still use `COPY` directive ? We can probably delete `COPY . .`  and get away, but usually its left out for future changes, for setting up a production instances then you will need to add it.

#### Executing Tests

Use `docker build -f Dockerfile.dev .` to build and then `docker run <container_id> npm run test` to run tests.

Now if we run `ENTER` command but we are not able to send the command, we need to attach to container’s stdin. `docker run -it <container_id> npm run test`

To get the Live update feature again in test suite we need to attach the volumes. Although we can directly use already configured filesystem mounting volumes but we will do Docker compose specially for Running Tests.

We can modify our `docker-compose.yml`

````yaml
version: '3'
services:
  web:
    build:
    	context: .
    	dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
	tests:
		build:
			context: .
			dockerfile: Dockerfile.dev
		volumes:
			- /app/node_modules
			- .:/app
		command: ["npm","run","test"]
````

But there is shortcoming to above approach, we cannot attach to test suite’s stdin directly to that container.

Reason why it doesn’t work is because `npm` gets a PID of 1 and when we attach to stdin, it gets attached to `npm` as a separate command rather than `test` suite.

#### Need for Ngnix

Nginx is a very famous web server which is more or less used for load balancing and replying to user traffic. So to use our app in development environment its very important we build our application and serve it using nginx. We will create a second docker file that is for production.

##### Multi-Step Docker Build

Note : we will not need `node_modules` and library after a build is done and then we will setup nginx to serve the production build.

We will do multi-step docker build : We will have 2 build phase

- Build Phase : use node:alpine, copy package.json, install dependencies, npm run build
- Run Phase : use ngnix, copy result of npm build, start nginx

````Dockerfile
FROM node:16-alpine as builder
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx
COPY --from=builder /app/build /usr/share/nginx/html
````

Rebuild the container using `docker build .` and run it using `docker run -p 8080:80 <image+id>`

### Section 7 : Continuous Integration and Deployment with AWS

#### Travis CI

Signup on the service, (note its no longer free tier due to crypto abuse). Travis does work based on the .travis.yml file. Travis will watch the repository for push and then run the script.

- Tell Travis we need a copy of docker running 
- Build our image using Dockerfile.dev
- Tell travis to run test suite
- Tell travis to deploy our code to AWS

Create a `.travis.yml` file that will be directive to travis to run on code push to master.

````yaml
sudo: required
services:
  - docker
before_install:
  - docker build -t smk781/curly-winner -f Dockerfile.dev .
script:
  - docker run -e CI=true smk781/curly-winner npm run test

language: generic
````

To avoid hangup of interactive stdin after npm run test we use `CI=true`

[Read up on CI=true Var](https://create-react-app.dev/docs/running-tests/#linux-macos-bash)

[Docker Env Variables](https://docs.docker.com/engine/reference/run/#env-environment-variables)

#### Amazon AWS

Select elastic beanstalk from resources, it is the simplest way to run dockerized web apps. Select Webserver Environment. Select docker from Base Configuration and create environment.

Elastic Beanstalk has a load balancer built in which automatically scales and adds more containers when traffic reaches certain threshold.

To add deployment for travis CI to AWS add this section at the end of `.travis.yml`. You need to look up region of your deployment (Docker-env.qbtbvwcxmh.us-west-2.elasticbeanstalk.com) .

````yaml
deploy:
  provider: elasticbeanstalk
  region: "us-west-2"
  app: "docker"
  env: "Docker-env"
  bucket_name: "elasticbeanstalk-us-west-2-3064766"
  bucket_path: "docker"
  on:
  	branch: master
  access_key_id: "$AWS_ACCESS_KEY"
  secret_access_key: "$SECURE_AWS_KEY"
````

Amazon S3 buckets are storage solution provided by AWS.

##### **Docker Compose config Update**

##### Initial Setup

1. Go to AWS Management Console
2. Search for Elastic Beanstalk in "Find Services"
3. Click the "Create Application" button
4. Enter "docker" for the Application Name
5. Scroll down to "Platform" and select "Docker" from the dropdown list.
6. Change "Platform Branch" to Docker running on 64bit Amazon Linux 2
7. Click "Create Application"
8. You should see a green checkmark after some time.
9. Click the link above the checkmark for your application. This should open the application in your browser and display a Congratulations message.

##### Change from Micro to Small Instance

Note that a t2.small is outside of the free tier. t2 micro has been known to timeout and fail during the build process on the old platform. However, this may not be an issue on the new Docker running on 64bit Amazon Linux 2 platform. So, these steps may no longer be necessary.

1. In the left sidebar under Docker-env click "Configuration"

2. Find "Capacity" and click "Edit"

3. Scroll down to find the "Instance Type" and change from t2.micro to t2.small

4. Click "Apply"

5. The message might say "No Data" or "Severe" in Health Overview before changing to "Ok”


##### Create an IAM User

1. Search for the "IAM Security, Identity & Compliance Service"

2. Click "Create Individual IAM Users" and click "Manage Users"

3. Click "Add User"

4. Enter any name you’d like in the "User Name" field. eg: docker-react-travis-ci

5. Tick the "Programmatic Access" checkbox

6. Click "Next:Permissions"

7. Click "Attach Existing Policies Directly"

8. Search for "beanstalk"

9. Tick the box next to "AdministratorAccess-AWSElasticBeanstalk"

10. Click "Next:Tags"

11. Click "Next:Review"

12. Click "Create user"

13. Copy and / or download the Access Key ID and Secret Access Key to use in the Travis Variable Setup.

Note : We should never put these keys into our Repo instead we use feature of Environment Secrets provided by Travis CI.

Now commit all the work done and push it to the GitHub Master Branch. Now we still have one thing that is PORT MAPPING left to setup. We can do that in the Dockerfile and put `EXPOSE 80` instruction and Its mean to signify that this container needs to be connected to be 80 port. Note this actually doesn’t do anything in local setup does nothing but BeanStalk detects it and exposes it.

#### Using Github Actions

You can also use Github Actions inplace of Travis CI, Navigate to repository -> settings -> secrets and add, AWS_ACCESS_KEY, AWS_SECRET_KEY, DOCKER_USERNAME and DOCKER_PASSWORD.

Create a folder `.github` and create **workflows** directly inside that folder and create a file `deploy.yml` with content given below. NOTE : name of file doesn’t matter.

````yaml
name: Deploy Frontend
on:
  push:
    branches:
      - main
 
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
      - run: docker build -t cygnetops/react-test -f Dockerfile.dev .
      - run: docker run -e CI=true cygnetops/react-test npm test
 
      - name: Generate deployment package
        run: zip -r deploy.zip . -x '*.git*'
 
      - name: Deploy to EB
        uses: einaregilsson/beanstalk-deploy@v18
        with:
          aws_access_key: ${{ secrets.AWS_ACCESS_KEY }}
          aws_secret_key: ${{ secrets.AWS_SECRET_KEY }}
          application_name: docker-gh
          environment_name: Dockergh-env
          existing_bucket_name: elasticbeanstalk-us-east-1-923445559289
          region: us-east-1
          version_label: ${{ github.sha }}
          deployment_package: deploy.zip
````

#### VERY IMPORTANT : DELETE THE BEANSTALK THAT YOU JUST CREATED  !!!

---

## File: docker/sgrider/part3.md

## Notes : Docker

### Section 8 : Building a Multi-Container Application

#### Single Container Deployment Issues

- The app was simple - no outside dependencies
- Our image was built multiple times
- How do we connect to a database from a container

We gonna build an app fibbonacci number calculator but a very complex one :)

#### Architecture

If user visits our webpage, and response will be handled by nginx, which will forward request to either React or Express Server which in turn will communicate with Redis  and PostgresSQL Server. Redis Server will have a Worker.

Redis is for a in memory, temporary storage while PostgreSQL will be for permanent storage.

Download Entire Project Here [Link](https://github.com/mightyjoe781/fibCalculator) . Then checkout branch `checkpoint-1`

Worker Process : Watches redis for new indice. Pulls each new indice, Calculate the appropriate fibbonaci value for it.

### Section 9 : “Dockerizing ” Multiple Services

#### Dockerizing a React App

Create a Dockerfile.dev in all three services. Create the following `Dockerfile.dev` in `client` folder.

````dockerfile
FROM node:16-alpine
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
CMD [ "npm","run", "start" ]
````

Build :  `docker build -d Dockerfile.dev .`

Similarly create the same file in `server` , `worker` and change the last instruction to `CMD [ "npm", "run", "dev"] ` and after that build the docker image in each of them.

Designing docker-compose file

- postgress
  - Image
- redist
  - Image
- server
  - specify build
  - specify volumes
  - Specify env variables

Make a `docker-compose.yml` to main root working directory.

Note : if we put Environment Variable :

- variableName=value : Sets a variable in the container at *run time*
- variableName : Value is taken from your machine at the *run time.*

````dockerfile
version: '3'
services:
  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_PASSWORD=mysecretpassword
  redis:
    image: redis:latest
  api:
    build:
      dockerfile: Dockerfile.dev
      context: ./server/
    volumes:
      - /app/node_modules
      - ./server:/app
    environment:
      - PGUSER=postgres
      - PGHOST=postgres
      - PGDATABASE=postgres
      - PGPASSWORD=postgres_password
      - PGPORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redis_password

  client:
    build:
      dockerfile: Dockerfile.dev
      context: ./client/
    volumes:
      - /app/node_modules
      - ./client:/app
    ports:
      - "8080:8080"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redis_password

  worker:
    build:
      dockerfile: Dockerfile.dev
      context: ./worker/
    volumes:
      - /app/node_modules
      - ./worker:/app
````



#### Routing with Nginx

So our nginx server will look at the request and properly forward it to either React server or Express Server. A natural question arises that why did not we hosted React and Express Server separately on different ports and then just made reference using port. Usually its not recommended to use static PORTS in address because ports change all the time at different environments and for changing such a small thing we might need to rebuild our apps again.

Nginx reads `default.conf` for implementing routing.

General Design : 

- Tell Nginx that there is a upstream server at client:3000
- Tell Nginx that there is a upstream server at server:5000
- Listen on port 80
- If anyone come to `/` send them to client upstream
- If anyone comes `/api` send them to client upstream

````nginx
upstream client {
    server client:3000;
}

upstream api {
    server api:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://client;
    }
    location /api {
    		# Rewrite rule changes /api to / for api server
        rewrite ^/api/(.*)$ /$1 break;
        proxy_pass http://api;
    }
}
````

NOTE : edit `docker-compose.yml` to change `server` with `api` because we changed name to fix confusion while writing nginx rules.

#### Building a Custom nginx Image

Add this `Dockerfile.dev` to nginx folder.

````Dockerfile
FROM nginx
COPY ./default.conf /etc/nginx/conf.d/default.conf
````

And add this to `docker-compose.yml`

````yaml
nginx:
  restart: always
  build:
    dockerfile: Dockerfile.dev
    context: ./nginx
  ports:
  	- '3000:80'
  depends_on:
    - api
    - client
````

#### Starting Docker Compose

Be Carefull with dependencies in docker-compose. for example `server/api` and `client` always need `redis` running.

`docker-compose up --build`

#### Websocket fix

To fix websocket issue with react do this to `docker-compose.yml`

````dockerfile
  client:
    environment:
      - WDS_SOCKET_PORT=0
````

and to `ngnix.conf`

````nginx
location /ws {
      proxy_pass http://client;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
}
````

Link to complete setup [Link](https://github.com/mightyjoe781/fibCalculator/tree/checkpoint-2) : Use the branch checkpoint-2

### Section 10 : A Continuos Integration Workflow for Multiple Containers

#### Production Multi-Container Deployments

MultiContainer Setup

- Push code to github
- Travis automatically pulls repo
- Travis builds a **test** image, tests code
- Travis builds **prod** images
- Travis pushes built **prod** images to Docker Hub
- Travis pushes built **prod** images to Docker Hub
- Travis pushes project to AWS EB
- EB pulls images from DockerHub, deploys

So Advantage of this setup is we are not relying on EB to build our image instead we put our image on dockerhub which in turn can be used by AWS EB or Google Cloud for updating our website.

Create `Dockerfile` for **prod** in all four services and replace `CMD ["npm", "run", "dev"]`  in `Dockerfile.dev` with `CMD ["npm","run","start"]`  in `Dockerfile`.

#### Multiple Nginx Instances

In case of our Single Container App we had nginx running with **prod** files which were built by `npm build`. But now we can replace `Client/React Frontend` with similar nginx configuration. So now basically we have 2 ngnix servers.

One nginx server focuses on only routing and second one will only serve production file.

Can we replace both ngnix server with only ?? YES :) But we might don’t want to do that for now just because its very common in real life deployments that we might have to manage multiple ngnix servers.

#### Altering Ngnix’s Listen Port

Create nginx folder inside the `clien` folder and create `default.conf`.

Create `default.conf` with contents

````ngnix
server {
  listen 3000;
 
  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html;
  }
}
````

For `Dockerfile`

````dockerfile
FROM node:16-alpine
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx
EXPOSE 80
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/ngnix/html
````

NOTE : here we wrote `ngnix.conf` only because our frontend is supposed to be hosted on `port : 3000`.

NOTE : Clean up `App.test.js` file’s tests they might crash our frontend (removed the test).

Checkout Files at `checkpoint-3` [link](https://github.com/mightyjoe781/fibCalculator/tree/checkpoint-3)

##### Setup Github Repo and Similar Travis CI Repo

#### Travis Configuration Setup

````yaml
language: generic
sudo: required
services:
  - docker

before_install:
  - docker build -t smk781/react-test -f ./client/Dockerfile.dev ./client/

script:
  - docker run -e CI=true USERNAME/react-test npm test

after_success:
  - docker build -t smk781/multi-client ./client
  - docker build -t smk781/multi-server ./server
  - docker build -t smk781/multi-nginx ./nginx
  - docker build -t smk781/worker ./worker
````

#### Pushing Images to Docker Hub

Add these lines below the `after_sucess` to push existing images to Docker Hub.

````yaml
after_success:
  # Log in to the Docker CLI
  echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
  # Take those images and push them to Docker Hub
  docker push smk781/multi-client
  docker push smk781/multi-server
  docker push smk781/multi-nginx
  docker push smk781/worker
  # Log out of the Docker CLI
  docker logout
````

### Section 11: Multi-Container Deployments to AWS

NOTE : Docker running on 64 bit Amazon Linux will work only till July, 2022. So for Amazon Linux 2 Steps are dramatically different.

We will focus  only on Amazon Linux 2.

Also notice we won’t be having our normal redis and postgresql containers because we are going to use services offered by Amazon, AWS Elastic Cache and AWS Relational Database Service.

A Big reason use those is they are better configured, more secure, automatically scalable, (RDS) automated backups and rollbacks, logging + maintenance and Easy to migrated off the EB.

#### EBS Application Creation (If using Multi-Container Docker Platform)

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
2. Click “Create Application”
3. Set Application Name to 'multi-docker'
4. Scroll down to Platform and select Docker
5. **In Platform Branch, select Multi-Container Docker running on 64bit Amazon Linux**
6. Click Create Application
7. You may need to refresh, but eventually, you should see a green checkmark underneath Health.

#### EBS Application Creation (If using Amazon Linux 2 Platform Platform)

1. Make sure you have followed the guidance in this [note](https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/learn/lecture/28089952#questions).
2. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
3. Click “Create Application”
4. Set Application Name to 'multi-docker'
5. **Scroll down to Platform and select Docker**
6. The Platform Branch should be automatically set to **Docker Running on 64bit Amazon Linux 2**.
7. Click Create Application
8. You may need to refresh, but eventually, you should see a green checkmark underneath Health.

#### RDS Database Creation

1. Go to AWS Management Console and use Find Services to search for RDS
2. Click Create database button
3. Select PostgreSQL
4. Change Version to the newest available v12 version (The free tier is currently not available for Postgres v13)
5. In Templates, check the Free tier box.
6. Scroll down to Settings.
7. Set DB Instance identifier to **multi-docker-postgres**
8. Set Master Username to **postgres**
9. Set Master Password to **postgrespassword** and confirm.
10. Scroll down to Connectivity. Make sure VPC is set to Default VPC
11. Scroll down to Additional Configuration and click to unhide.
12. Set Initial database name to **fibvalues**
13. Scroll down and click Create Database button

#### ElastiCache Redis Creation

1. Go to AWS Management Console and use Find Services to search for ElastiCache
2. Click Redis in sidebar
3. Click the Create button
4. **Make sure Cluster Mode Enabled is NOT ticked**
5. In Redis Settings form, set Name to multi-docker-redis
6. Change Node type to 'cache.t2.micro'
7. Change Replicas per Shard to 0
8. Scroll down and click Create button

***Creating a Custom Security Group\***

1. Go to AWS Management Console and use Find Services to search for VPC
2. Find the Security section in the left sidebar and click Security Groups
3. Click Create Security Group button
4. Set Security group name to multi-docker
5. Set Description to multi-docker
6. Make sure VPC is set to default VPC
7. Scroll down and click the Create Security Group button.
8. After the security group has been created, find the Edit inbound rules button.
9. Click Add Rule
10. Set Port Range to 5432-6379
11. Click in the box next to Source and start typing 'sg' into the box. Select the Security Group you just created.
12. Click the Save rules button

#### Applying Security Groups to ElastiCache

1. Go to AWS Management Console and use Find Services to search for ElastiCache
2. Click Redis in Sidebar
3. Check the box next to Redis cluster
4. Click Actions and click Modify
5. Click the pencil icon to edit the VPC Security group. Tick the box next to the new multi-docker group and click Save
6. Click Modify

***Applying Security Groups to RDS\***

1. Go to AWS Management Console and use Find Services to search for RDS
2. Click Databases in Sidebar and check the box next to your instance
3. Click Modify button
4. Scroll down to Connectivity and add the new multi-docker security group
5. Scroll down and click the Continue button
6. Click Modify DB instance button

***Applying Security Groups to Elastic Beanstalk\***

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
2. Click Environments in the left sidebar.
3. Click MultiDocker-env
4. Click Configuration
5. In the Instances row, click the Edit button.
6. Scroll down to EC2 Security Groups and tick box next to multi-docker
7. Click Apply and Click Confirm
8. After all the instances restart and go from No Data to Severe, you should see a green checkmark under Health.

##### Add AWS configuration details to .travis.yml file's deploy script

1. Set the *region*. The region code can be found by clicking the region in the toolbar next to your username.
   eg: 'us-east-1'
2. *app* should be set to the EBS Application Name
   eg: 'multi-docker'
3. *env* should be set to your EBS Environment name.
   eg: 'MultiDocker-env'
4. Set the *bucket_name*. This can be found by searching for the S3 Storage service. Click the link for the elasticbeanstalk bucket that matches your region code and copy the name.
5. eg: 'elasticbeanstalk-us-east-1-923445599289'
6. Set the *bucket_path* to 'docker-multi'
7. Set *access_key_id* to $AWS_ACCESS_KEY
8. Set *secret_access_key* to $AWS_SECRET_KEY

##### Setting Environment Variables

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
2. Click Environments in the left sidebar.
3. Click MultiDocker-env
4. Click Configuration
5. In the Software row, click the Edit button
6. Scroll down to Environment properties
7. In another tab Open up ElastiCache, click Redis and check the box next to your cluster. Find the Primary Endpoint and copy that value but omit the :6379
8. Set REDIS_HOST key to the primary endpoint listed above, remember to omit :6379
9. Set REDIS_PORT to 6379
10. Set PGUSER to postgres
11. Set PGPASSWORD to postgrespassword
12. In another tab, open up the RDS dashboard, click databases in the sidebar, click your instance and scroll to Connectivity and Security. Copy the endpoint.
13. Set the PGHOST key to the endpoint value listed above.
14. Set PGDATABASE to fibvalues
15. Set PGPORT to 5432
16. Click Apply button
17. After all instances restart and go from No Data, to Severe, you should see a green checkmark under Health.

#### IAM Keys for Deployment

You can use the same IAM User's access and secret keys from the single container app we created earlier, or, you can create a new IAM user for this application:

1. Search for the "IAM Security, Identity & Compliance Service"

2. Click "Create Individual IAM Users" and click "Manage Users"

3. Click "Add User"

4. Enter any name you’d like in the "User Name" field. eg: docker-multi-travis-ci

5. Tick the "Programmatic Access" checkbox

6. Click "Next:Permissions"

7. Click "Attach Existing Policies Directly"

8. Search for "beanstalk"

9. Tick the box next to "AdministratorAccess-AWSElasticBeanstalk"

10. Click "Next:Tags"

11. Click "Next:Review"

12. Click "Create user"

13. Copy and / or download the *Access Key ID* and *Secret Access Key* to use in the Travis Variable Setup.

##### AWS Keys in Travis

1. Go to your Travis Dashboard and find the project repository for the application we are working on.
2. On the repository page, click "More Options" and then "Settings"
3. Create an *AWS_ACCESS_KEY* variable and paste your IAM access key
4. Create an *AWS_SECRET_KEY* variable and paste your IAM secret key

#### Deploying App

1. Make a small change to your src/App.js file in the greeting text.

2. In the project root, in your terminal run:

   ```
   git add.git commit -m “testing deployment"git push origin main
   ```

3. Go to your Travis Dashboard and check the status of your build.

4. The status should eventually return with a green checkmark and show "build passing"

5. Go to your AWS Elasticbeanstalk application

6. It should say "Elastic Beanstalk is updating your environment"

7. It should eventually show a green checkmark under "Health". You will now be able to access your application at the external URL provided under the environment name.

---

