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