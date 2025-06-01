# Kubernetes Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: kubernetes
This is part 1 of 1 parts

---

## File: kubernetes/cloudacademy/index.md

## Introduction to Kubernetes

### Prerequisite

- [Docker in Depth](../../docker/docker_in_depth/index.md)

### Content

[Part1](part1.md)

- Kubernetes Overview
- Deploying Kubernetes
- Kubernetes Architecture

- Interacting with Kubernetes

[Part2](part2.md)

- Pods
- Services
- Multi-Container Pods
- Service Discovery

[Part3](part3.md)

- Deployments
- Autoscaling
- Rolling Updates and Rollback
- Probes

- Init Containers

[Part4](part4.md)

- Volumes
- ConfigMaps and Secrets
- Kubernetes Ecosystem

### Resources

[Course Github Repo](https://github.com/cloudacademy/intro-to-k8s)

[Metrics Server Github Repo](https://github.com/kubernetes-sigs/metrics-server)

---

## File: kubernetes/cloudacademy/part1.md

# Introduction to Kubernetes

## Kubernetes Overview

#### What is Kubernetes (k8s) ?

- Open-sourcer container orchestration tool designed to automate, deploying, scaling & operating containerized applications
- Born out of Google’s experience running production workloads at scale
- Allows orgs to increase their velocity by releasing and recovering faster
- It is a distributed systems with multiple machines (Machines may be physical, virtual, on-prem or in cloud)
- schedules containers on machine
- moves containers as machines are added/removed
- can use different container runtimes
- modular, extensible design

Main Advantage : Declarative Configuration, Deploy Containers, Wire up networking, scale and expose services

#### Feature Hightlights

- Automated Deployment rollout and rollback
- Seamless horizontal scaling
- Secret Management
- Service Discovery and load balancing
- Linux and Windows container support
- Simple log collection
- Stateful application support
- Persistent Volume Management
- CPU and memory quotas
- Batch job processing
- Role-based access control (RBAC)

### Competitors of k8s

#### DC/OS

- Distributed Cloud Operating System
- Pools Compute Resources into a uniform task pool
- Supports many different types of workloads
- Attractive to organization not only using containers
- includes package manager to easily deploy popular systems
- Can even run Kubernetes on DC/OS

#### ECS (Elastic Container Service)

- aws’s first entry in container orchestration
- create pools of compute resources
- API calls to orchestrate containers
- EC2 compute instances managed by you or by AWS (Fargate)
- Only available in AWS

#### Docker Swarm

- Official docker solution for orchestrating containers across a cluster of machines
- builds a cluster from multiple docker hosts
- works natively with the docker command
- used by Docker’s enterprise edition
- docker also provides full support of Kubernetes to easily switch

## Deploying Kubernetes

### Single-Node Kubernetes Clusters

Tools

- docker on Mac/windows already includes kubernetes
- minicube
- kubeadm (NOTE : create on host not a vm)

Create ephemeral clusters that start quickly and are in pristine state for testing application in Kubernetes.

Kubernetes-in-Docker (kind) is made for this use case.

### Multi-Node Kubernetes Cluster

- for production workloads
- horizontal scaling
- tolerate node failures

Which solution is best ? Ask several key question

- Control vs Effort to Maintain
- fully-managed solution free you from routine maintenance
  - often lag the latest k8s release
  - Examples : EKS, AKS (Azure), GKE (GCP)
  - Full Control Examples : kubespray, kops, kubeadm
- Do you already have expertise with a particular cloud provider
- Do you need enterprise support ?
  - several vendors offer enterprise support and additional features on top of k8s
  - Openshift by RedHat, Pivotal Container Service(PKS) and Rancher
- Are you concerned about vendor lock-in ?
  - use open source solution : kubespray or rancher
- on-prem, in cloud or both ?
  - All EKS, AKS, GKE allows on-prem servers
- Linux, windows or both containers ?
  - ensure similar nodes are in your cluster as per requirement

## Kubernetes Architecture

- kubernetest introduces its own dialect to orchestration space
- Cluster refers to all of the machines collectively and can be thought of as the entire running system
- Nodes are the machines in the cluster
- Nodes are categorized as worker or masters
- **Worker Node** includes software to run containers managed by the Kubernetes control plane
- Master nodes run the control plane
- The **Control Plane** is a set of APIs and software that Kubernetes users interact with
- The APIs and Software are referred to as Master Components

#### Scheduling

- Control Plane Schedules containers onto nodes
- Scheduling decision considers required CPU and other factors
- scheduling here refers to the decisions process of placing containers onto node

#### Kubernetes Pods

- Group of containers
- Pods are smallest building block in k8s
- more complex abstraction are build on pods

#### Service

- Services define networking rules for exposing groups of pods
  - to other pods
  - to public internet

#### Kubernetes Deployments

- Mange deployign configs changes to running pods
- horizontal scaling

[Resource for Further Reading (Advanced)](https://phoenixnap.com/kb/understanding-kubernetes-architecture-diagrams)

## The Kubernetes API Server

- modify cluster state information by sending request to the k8s api server
- API Server is a master component that acts as frontend for the cluster

Interacting with Kubernets

1. Rest API
   - It is possible but not common to work directly with API server
   - only if there is not client library for your programming language
2. Client Library
   - handles auth and managing individual REST API request and responses
   - kubernetes maintains official client libraries in python, go, java, .NET, javascript, etc along with community maintained libraries.
3. `kubectl` : Kube Control
   - Issues high-level command that are translated in REST API Call
   - works with local/remote clients
   - can manage different types of k8s resoruces and provides debugging and introspection

#### Example Kubectl Commands

- `kubectl create` (resources : pods, service, etc)
- `kubectl delete`
- `kubectl get` : gets list of resources of a given type. `kubectl get pods` or `kubectl get all`
- `kubectl descibe <resource> [resource_name]` : describe to print detailed info about a resource(s)
- `kubectl logs` to print container logs

4. Web Dashboard to interact with Kubernetes API


---

## File: kubernetes/cloudacademy/part2.md

# Introduction to Kubernetes

## Pods

- basic building block in kubernetes
- container one or more container in a Pod
- Pod containers all share a container network
- one IP address per Pod
- since pod contains container, it includes all declarative properties for container
  - container image
  - container ports
  - container restart policy
  - resource limits
- desired properties written in manifest files

Example Manifest File

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mycontainer
    image: nginx:latest
````

- Manifests in Action
  - kubectl create sends manifest to Kubernetes API Server
  - API server does the following for Pod manifests
    - select a node with sufficient resource
    - schedule pod onto node
    - node pulls pod’s container image
    - starts pod’s container
- Manifests are useful
  - can be checked into source control
  - easy to share and work with

````bash
# first start the docker daemon (check docker documents)
# start minikube
minikube start

# check if kubectl is connected to API
kubectl get pods

# check yaml files from here : https://github.com/cloudacademy/intro-to-k8s
cat 1.1-basic_pod.yml
kubectl create -f 1.1-basic_pod.yml
kubectl get pods

# inspect the pod properties
kubectl describe pod mypod | more
# notice only 1 ip per pod and all containers share that IP

# let's attach a port to connect to pod # notice ports in container
cat 1.2-port_pod.yml

# NOTE : we cannot change ports on running pods thats why we need to delete the pod
kubectl delete pod mypod
kubectl create -f 1.2-port_pod.yml

# this should time out from host as cotnainers in pod can communicate inside only
curl 10.244.0.4:80

# there is a minikube trick to access this tho

# labels are important for selecting clusters for application
# we can use queue-control to only get nodes in us-east label
cat 1.3-labeled_pod.yml

# Notice QOS class is BestEffort
# pods are scheduled based on resources, here there is no guarantee of pod being up, it maybe evicted when resources are required by any other resource starved service
cat 1.4-labeled_pod.yml
# this sets resources request and memory limits to allow a guaranted uptime or it won't be scheduled until such resources are available
````

#### Minikube and ports magic

Method 1

- Expose the Pod via Service: `kubectl port-forward mypod 8080:80`

Method 2 (Explained in Details Ahead)

- Create a simple server deployment : `kubectl run hello-minikube --image=gcr.io/google_containers/echoserver:1.4 --port=8080`
- Expose this deployment : `kubectl expose deployment hello-minikube --type=NodePort`
- Check NodePort used by svc : `kubectl get svc hello-minikube`
- Find minikube IP : `minikube ip`
- Curl via : `curl minikube ip:<o_port>`
- Alternatively can use `minikube tunnel` to access on `localhost:8080`

## Services

- We are not able to reach the pods but even if we could what happens to ip when a pod restarts ? It changes then how we keep track of all this
- A service defines networking rules for accessing Pods in a cluster from internet
- Use labels to select a group of Pods
- services has fixed IP Address
- services can also distribute request across pods in the group

`````yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: webserver
  name: webserver
spec:
	# this service's target port
  ports:
  - port: 80
  # select every pod with app=webserver & expose them on port 80
  selector:
    app: webserver
  type: NodePort
`````

Execute: `kubectl create -f 2.1-web_service.yaml`

Get services : `kubectl get services`

````txt
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP        63m
webserver    NodePort    10.110.244.0   <none>        80:31657/TCP   4s
````

To get the node ip : `kubectl describe node | grep -i address -A 1` or `minikube ip`

Now we can connect to this webserver using : `<minicube_ip>:31657` 

NOTE : above works only for minikube running off of `qemu` driver

NOTE : for docker driver you need to use `minikube tunnel` or `minikube --port-forward svc/webserver 3000:80` Then visit localhost:8080 or localhost:3000 respectively

## Multi-Container Pods

Example Application :

- A simple counter application
- 4 containers split across 3 tiers
- application tier is a Node.js
- redis data tier storing the counter
- Poller/counter in the support tier
- All containers are using environment variables

### Kubernetes Namespaces

- Namespace separates resources according to users, environment or application
- RBAC can be used to secure access to namespace

````yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservice
  labels:
    app: counter
````

`````bash
# creating a namespace
kubectl create -f 3.1-namespace.yaml

# check the multi-container.yaml
cat 3.2-multi_container.yaml
# NOTE: By default pods pull latest image, this could cause problems if pod restart
# set a imagePullPolicy
kubectl create -f 3.2-multi_container.yaml -n microservice

kubectl get -n microservice pod app

kubectl logs -n microservice app counter --tail 10
kubectl logs -n microservice app poller -f
`````

## Service Discovery

Why Services 

- support multi-pod design
- provides static endpoint for each tier
- handles pod ip changes
- load balancing

### Service Discovery Mechanism

1. Environment Variables
   - Service address automatically injected in containers
   - environment vairables follow naming conventions based on service name
2. DNS
   - DNS records automatically created in cluster’s DNS
   - containers automatically configured to query cluster DNS

````bash
kubectl create -f 4.1-namespace.yaml

cat 4.2-data_tier.yaml
kubectl create -f 4.2-data_tier.yaml -n service-discovery
kubectl create -f 4.3-data_tier.yaml -n service-discovery
````

````yaml
apiVersion: v1
kind: Service
metadata:
  name: data-tier
  labels:
    app: microservices
spec:
  ports:
  - port: 6379
    protocol: TCP # default
    name: redis # optional when only 1 port
  selector:
    tier: data
  type: ClusterIP # default
# yaml trick to cram in multiple yaml files in one file
---
apiVersion: v1
kind: Pod
metadata:
  name: data-tier
  labels:
    app: microservices
    tier: data
spec:
  containers:
    - name: redis
      image: redis:latest
      imagePullPolicy: IfNotPresent
      ports:
        - containerPort: 6379
````

`````yaml
apiVersion: v1
kind: Service
metadata:
  name: app-tier
  labels:
    app: microservices
spec:
  ports:
  - port: 8080
  selector:
    tier: app
---
apiVersion: v1
kind: Pod
metadata:
  name: app-tier
  labels:
    app: microservices
    tier: app
spec:
  containers:
    - name: server
      image: lrakai/microservices:server-v1
      ports:
        - containerPort: 8080
      env:
        - name: REDIS_URL
          # Environment variable service discovery
          # Naming pattern:
          #   IP address: <all_caps_service_name>_SERVICE_HOST
          #   Port: <all_caps_service_name>_SERVICE_PORT
          #   Named Port: <all_caps_service_name>_SERVICE_PORT_<all_caps_port_name>
          value: redis://$(DATA_TIER_SERVICE_HOST):$(DATA_TIER_SERVICE_PORT_REDIS)
          # In multi-container example value was
          # value: redis://localhost:6379
`````

NOTE : Data Tier service must be created before app tier & must be present in namespace before referencing environment variables

FOR DNS Service Discovery

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: support-tier
  labels:
    app: microservices
    tier: support
spec:
  containers:

    - name: counter
      image: lrakai/microservices:counter-v1
      env:
        - name: API_URL
          # DNS for service discovery
          # Naming pattern:
          #   IP address: <service_name>.<service_namespace>
          #   Port: needs to be extracted from SRV DNS record
          value: http://app-tier.service-discovery:8080

    - name: poller
      image: lrakai/microservices:poller-v1
      env:
        - name: API_URL
          # omit namespace to only search in the same namespace
          value: http://app-tier:$(APP_TIER_SERVICE_PORT)
````

Here its referenced by : label.namespace:PORT

Why did we split up our services into 3 files ? Because we want to later on scale the application but not the redis database


---

## File: kubernetes/cloudacademy/part3.md

# Introduction to Kubernetes

## Deployments

- We should not create pods directly and should be created via higher level construct like deployments
- Deployment represents multiple replicas of a pod
- Describes a desired state that Kuberenetes needs to achieve
- Deployment Controller master component converges actual state to desired state
- seamlessly supports scaling but scaling is best with stateless pods

````bash
kubectl create -f 5.1-namespace.yaml

kubectl create -n deployments -f 5.2-data_tier.yaml -f 5.3-app_tier.yaml -f 5.4-support_tier.yaml

kubectl get -n deployments deployments
kubectl get -n deployments pods
# NOTE: This doesn't scale the containesr
kubectl scale -n deployments deployments support-tier --replicas=5

# again get pods
kubectl get -n deployments pods

# destroy some replicas then watch
kubectl delete -n deployments pods support-tier-<hash1> support-tier-<hash2> support-tier-<hash3>
watch -n 1 kubectl -n deployments get pods
````

Data-Tier

````yaml
apiVersion: v1
kind: Service
metadata:
  name: data-tier
  labels:
    app: microservices
spec:
  ports:
  - port: 6379
    protocol: TCP # default
    name: redis # optional when only 1 port
  selector:
    tier: data
  type: ClusterIP # default
---
apiVersion: apps/v1 # apps API group (higher level abstration are part of apps group)
kind: Deployment
metadata:
  name: data-tier
  labels:
    app: microservices
    tier: data
spec:
  replicas: 1		# copy of pod always running NOT CONTAINERS IN A POD
  selector:
    matchLabels:
      tier: data
  template:
    metadata:
      labels:
        app: microservices
        tier: data
    spec: # Pod spec
      containers:
      - name: redis
        image: redis:latest
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 6379
````

## Autoscaling

- scale automatically based on CPU Utilization (or custom metrics)
- set target CPU along with min and max replicas
- target CPU is expressed as a percentage of Pod’s CPU request
- kubernetes increases or decreases replicas according to load
- Defaults using CPU Usage
- Autoscaling depends on metrics being collected
- metric server is one solution for collecting metrics
- several manifest files are used to deploy Metric Server (https://github.com/kubernetes-sigs/metrics-server)

````bash
kubectl apply -f metrics-server/
kubectl top pods -n deployments

# 1000m = 1 cpu
kubectl apply -f 6.1-app_tier_cpu_request.yaml -n deployments
kubectl create -f 6.2-autoscale.yaml

watch -n 1 kubectl get -n deployments deployments
kubectl api-resources	# hpa is short-name
kubectl describe -n deployments hpa
kubectl get -n deployments hpa

kubectl edit -n deployments hpa		# opens vim to edit some config's and apply immidieately
````

````yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: app-tier
  labels:
    app: microservices
    tier: app
spec:
  maxReplicas: 5
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-tier
  targetCPUUtilizationPercentage: 70

# Equivalent to
# kubectl autoscale deployment app-tier --max=5 --min=1 --cpu-percent=70
````

## Rolling Updates and Rollback

- Rollouts update Deployments changes like env variables

Rollout Strategy’s

- Rolling Update
  - default rollout strategy
  - update in groups rather than all-at-once
  - Both old and new version running for some time
  - alternate is recreate strategy
  - scaling is not a rollout
  - kubectl has commands to check, pause, resume, and rollback (undo) rollouts
- autoscaling and rollouts are compatible but to observe changes here first delete hpa

````bash
kubectl delete -n deployments hpa app-tier

kubectl edit -n deployments deployment app-tier
# change replica 2 to 10
# delete resources limits
watch -n1 kubectl get -n deployments deployment app-tier

# wait till its 10/10
kubectl edit -n deployments deployment app-tier
# check strategy defaults of 25%

# trigger rollout change image: name to smk under RestartPolicy
kubectl rollout -n deployments status deployment app-tier

# rollback :)
kubectl rollout -n deployments undo deployment app-tier
````

## Probes (HealthCheck)

### Readiness Probes

- check when a pod is ready to serve traffic/handle request
- useful after startup to check external dependencies
- readiness probes set the pod’s ready condition. Services only send traffic to Ready Pods

### Liveness Probes

- Detect when a pod enters a broken state
- kubernetes will restart the pod for you
- declared in the same way as readiness probes
- Probes can be declared in Pod’s containers
- all container probes must pass for the Pod to pass
- probe actions can be a command that runs in the container, an HTTP GET request, or opening a TCP socket
- by default probes check containers every 10 seconds

Data Tier (redis)

- Liveness : Open TCP socket
- Readiness: redis-cli ping command

App Tier (server)

- liveness: HTTP GET /probe/liveness
- Readiness: HTTP GET /probe/readiness

````bash
kubectl create -f 7.1-namespace.yaml
diff -y 5.2-data_tier.yaml 7.2-data_tier.yaml
> output
								>                   name: redis
								>               livenessProbe:
								>                 tcpSocket:
								>                   port: redis # named port
								>                 initialDelaySeconds: 15
								>               readinessProbe:
								>                 exec:
								>                   command:
								>                   - redis-cli
								>                   - ping
								>                 initialDelaySeconds: 5
> end of output

# it is suggested to have more delay to liveness & it requires 3 fails to trigger restart
kubectl create -f 7.2-data_tier.yaml -n probes
kubectl get deployments -n probes -w

diff -y 5.3-app_tier.yaml 7.3-app_tier.yaml
								>                 - name: DEBUG
								>                   value: express:*
								>               livenessProbe:	# dummy always return 200 OK
								>                 httpGet:
								>                   path: /probe/liveness
								>                   port: server
								>                 initialDelaySeconds: 5
								>               readinessProbe:	# data-tier is available
								>                 httpGet:
								>                   path: /probe/readiness
								>                   port: server
								>                 initialDelaySeconds: 3
								
kubectl create -f 7.3-app_tier.yaml -n probes
kubectl get -n probes pods
kubectl logs -n probes app-tier-<hashid> | cut -d' ' -f5,8 
````

## Init Containers

- Sometimes you need to wait for a service, downloads, dynamic or decisions before starting a Pod’s container
- prefer to separate initialization wait logic from the container image
- initialization is tightly coupled to the main application (belongs in the pod)
- init containers allow you to run initialization tasks before starting the main container(s)

Init Container:

- pods can declare any number of init containers
- Init containers run in order and to completion
- use their own images
- easy way to block or delay starting an application
- run every time a pod is created (liveness fails) (runs atleast once)

NOTE : init containers do not have readiness Probe

````bash
diff -y 7.3-app_tier.yaml 8.1-app_tier.yaml
								>             initContainers:
								>               - name: await-redis
								>                 image: lrakai/microservices:server-v1
								>                 env:
								>                 - name: REDIS_URL
								>                   value: redis://$(DATA_TIER_SERVICE_HOST):$(DA
								>                 command:
								>                   - npm
								>                   - run-script
								>                   - await-redis
								
kubectl create -n probes -f 8.1-app_tier.yaml
kubectl get pods -n probes
kubectl describe pod app-tier-<hash> -n probes

kubectl logs -n probes app-tier-<hash> -c await-redis
````

`npm run-script await-redis` script waits till there is a connection with redis


---

## File: kubernetes/cloudacademy/part4.md

# Introduction to Kubernetes



## Volumes

- Sometimes useful to share data between containers in a Pod
- Lifetime of container file systems is limited to container’s lifetime
- can lead to unexpected consequences if container restarts

### Pod Storage in Kubernetes

- Two high-level storage options: Volume and Persistent Volumes
- Used by mounting a directory in one or more containers in a Pod
- Pods can use multiple Volumes and Persistent Volumes
- Difference between Volumes and Persistent Volumes is how their lifetime is managed

### Volume

- volume are tied to a pod and their lifecycle
- share data between containers and tolerate container restarts
- use for non-durable storage that is deleted with pod
- default volume type is emptyDir
- data is lost if pod is rescheduled on a different pod

|                            Volume                            |
| :----------------------------------------------------------: |
| ![Kubernetes Mount Volume As File](./part4.assets/volume.png) |

### Persistent Volumes

- independent of pod’s lifetime
- pods claim persistent volumes to use throughout their lifetime (PVC)
- can be mounted by multiple pods on different Nodes if underlying storage supports it
- can be provisioned statically in advance or dynamicaly on-demand

### Persistent Volume Claims (PVC)

- describe a pod’s request for persistent volume storage
- includes how much storage, type of storage and access mode.
- access mode can be read-write once, read-only many, or read-write many
- pvc stays pending if no PV can satisfy it and dynamic provisioning is not enabled
- connects to a pod through a volume of type PVC

| PV and PVC                                                   |
| ------------------------------------------------------------ |
| ![How to create PV and PVC in Kubernetes - Knoldus Blogs](./part4.assets/1_keV2VBkCHb7cn_Rib0huYg.png) |

### Storage Volume Types

- wide variety of volume types to choose from
- use persistent volumes for more durable storage types
- supported durable storage types include GCE Persistent Disks, Azure Disks, Amazon EBS, NFS, and iSCSI

````bash
kubectl get pods -n deployments
kubectl -n deployments logs support-tier-<hash> poller --tail=1
# outputed counter keeps on increasing


# destroy the pod then check the counter
# go into pod
kubectl exec -n deployments data-tier-<hash> -it -- /bin/bash
# execute : kill 1

kubectl create -f 9.1-namespace.yaml
diff -y 7.2-data_tier.yaml 9.2-pv_data_tier.yaml


output >
								>       apiVersion: v1
								>       kind: PersistentVolume
								>       metadata:
								>         name: data-tier-volume
								>       spec:
								>         capacity:
								>           storage: 1Gi # 1 gibibyte
								>         accessModes:
								>           - ReadWriteOnce	# single node at a time
								>         awsElasticBlockStore:
								>           volumeID: INSERT_VOLUME_ID # replace with actual ID
								>       ---
								>       apiVersion: v1
								>       kind: PersistentVolumeClaim
								>       metadata:
								>         name: data-tier-volume-claim
								>       spec:
								>         accessModes:
								>           - ReadWriteOnce
								>         resources:
								>           requests:
								>             storage: 128Mi # 128 mebibytes

--------- skip ---------------
								>               volumeMounts:
								>                 - mountPath: /data
								>                   name: data-tier-volume
								>             volumes:
								>             - name: data-tier-volume
								>               persistentVolumeClaim:
								>                 claimName: data-tier-volume-claim
								

````



## ConfigMaps and Secrets

- Until now all container configuration has been in Pod spec
- This makes it less portable than it could be
- If sensitive information such as API keys and passwords is involved it presents a security issue

### ConfigMaps & Secrets

- separate config from pod spec
- results in easier to manage and more portable manifests
- both are similar but secrets are specifically for sensitive data
- there are specialized types of secrets for storing Docker registry credentials and TLS certs

- stores data in Key-value pairs
- pods must reference configmaps and secrets to use their data
- references can be made by mounting Volumes or setting environment variables that can be replaced

#### Config Maps

````yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  config: | # YAML for multi-line string
    # Redis config file
    tcp-keepalive 240
    maxmemory 1mb
````

````bash
diff -y 7.2-data_tier.yaml 10.3-data_tier.yaml
output >
								>               command:
								>                 - redis-server
								>                 - /etc/redis/redis.conf
								>               volumeMounts:
								>                 - mountPath: /etc/redis
								>                   name: config
								>             volumes:
								>               - name: config
								>                 configMap:
								>                   name: redis-config
								>                   items:
								>                   - key: config
								>                     path: redis.conf
end_of_output

# TASK: exec inside pod and check if redis.conf is updated or not :)
# inside pod : redis-cli CONFIG GET tcp-keepalive
````

#### Secrets

````yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-tier-secret
stringData: # unencoded data
  api-key: LRcAmM1904ywzK3esX
  decoded: hello
data: #for base-64 encoded data
  encoded: aGVsbG8= # hello in base-64

# api-key secret (only) is equivalent to
# kubectl create secret generic app-tier-secret --from-literal=api-key=LRcAmM1904ywzK3esX
````

````bash
diff -y 9.3-app_tier.yaml 10.5-app_tier.yaml

output >

          - name: DEBUG							          - name: DEBUG
            value: express:*						            value: express:*
                                        >                 - name: API_KEY
                                        >                   valueFrom:
                                        >                     secretKeyRef:
                                        >                       name: app-tier-secret
                                        >                       key: api-key
````



## Kubernetes Ecosystem

- Vibrant Ecosystem Around the Core of Kuberenetes

### Helm

- kubernetes package manager
- packages are called charts and are installed on your cluster using Helm CLI
- helm charts make it easy to share complete application
- Search helm hub for public charts : hub.helm.sh
- We could have taken redis helm chart for our redis server : `helm install stable/redis-ha`
- You could create a chart for the entire application

### Kustomise.io

- Customize YAML manifests in Kubernetes
- Helps you manage the complexity of your application
- declares kustomization.yaml file that declares customisation rules
- original manifests are untouched and remain usable
- generating configMaps and secrets from files
- configure common fields across multiple resources
- apply patches to any field in a manifest
- use overlays to customize base groups of resource
- directly integrated kubectl : `kubectl create -k kustomize.yml`

### Prometheus

- open-source monitoring and alerting system
- A server for pulling in time series metric data and storing it
- inspired by an internal monitoring tool at Google called borgmon
- De facto standard solution for monitoring kubernetes
- commonly paired with Grafan for visualizations
- define alert rules and send notification

### Kubeflow

- makes deployment of machine learning workflows on Kubernetes simple, scalable, and portable
- a comple machine learning stack
- leverage kubernetes to deploy anywhere, autoscale,etc

### Knative

- platform for building, deploying and managing serverless workloads on Kubernetes
- can be deployed anywhere with Kubernetes, avoiding vendor lock-in
- supported by Google, IBM, and SAP







---

## File: kubernetes/helm/content.md

# Helm

## Helm Introduction

- Application Manger for Kubernetes
- Simplifies Large Kubernetes Deployments
- Consider frontend, application and database resources deployments and are configured via kubernetes resource files.
- We will have to apply kubeclt multiple times for multiple files and order of applying matters
- How to parameterise ? 
- How to Add in Application Lifecycle Hooks ?
- How to manage version of related resources ?

- Helm uses a concept of chart similar to package and can deploy entire chart with just on command in a sequenced manner.

| Helm                                               |
| -------------------------------------------------- |
| ![Helm](./content.assets/HelmKubernetesDistro.png) |

## Benefits

- Manages Complexity
  - `helm install ca-demo1 ca-repo/voteapp`
- Helm allows upgrades, Rollback and Deletion
  - `helm upgrade`, `helm rollback`, `helm uninstall`
- Helm makes its chart distribution to easily export your infra to other users
  - `helm repo add ca-repo https://ca-repo.io/repo`
  - `helm install ca-repo/cloudacademy-app`
- Custom Chart Scaffolding
  - `helm create [chart_name]`

## Terminology

- Chart : Package Format for Helm, which includes specific files called as template when rendered make up the resource for cluster
- Repository: HTTP Web-server hosting index.yml of charts similar to DockerHub
- Templates : Files used in Chart Package. By taking a typical Kubernetes manifest files and abstracting in template and parameterize and while chart installing can alter the values of resources.
- Releases: when a chart is deployed in cluster, helm tags a release and used by helm to track the chart/cluster history

## Architecture

- Helm2 Architecture
  - server architecture
  - depended on cluster hosted component tiller
- Helm3 Architecture (more simple and secure)
  - follows client only architecture
  - communicates directly with k8s API with RBAC enabled using `.kube/config` file credentials
  - chart rendering is done on client side by helm before deploying
  - deploying a chart creates a release

## Installation

- `brew install helm`
- Setup autocompletion :
  - `source <(helm completion bash)`
  - `echo ‘source <(helm completion bash)’ >> ~/.bash_profile`

## Commands

````bash
helm search [cmd]

# hub/repo search
helm search hub [keyword]
helm search repo [keyword]
helm pull [chart]

# installation
helm install [name] [chart]

# upgrades/rollback/uninstall
helm upgrade [release] [chart]
helm rollback [release] [chart]
helm uninstall [release]

# helm repo managements
helm repo add [name] [url]
helm repo list
helm repo remove [name]
helm repo update
helm repo index [dir]

# helm release management
helm status [release]
helm list
helm history [release]
helm get manifest [release]

# helm chart management
helm create [name]
helm template [name] [chart]
helm package [chart]
helm lint [chart]
````

## Charts

- We will use `helm create [chartname]`

| chart directory structure                                    |
| ------------------------------------------------------------ |
| ![image-20231105190423646](./content.assets/image-20231105190423646.png) |

````txt
    foo/
    ├── .helmignore   # Contains patterns to ignore when packaging Helm charts.
    ├── Chart.yaml    # Information about your chart
    ├── values.yaml   # The default values for your templates
    ├── charts/       # Charts that this chart depends on
    └── templates/    # The template files
        └── tests/    # The test files
````

Chart.yaml file

````txt
apiVersion: v2
name: cloudacademy-webapp
description: A Helm chart for Kubernetes

# A chart can be either an 'application' or a 'library' chart.
# Application charts are a collection of templates that can be packaged into versioned archives to be deployed.
# Library charts provide useful utilities or functions for the chart developer. They're included as a dependency of application charts to inject those utilities and functions into the rendering pipeline. Library charts do not define any templates and therefore cannot be deployed.
type: application

# This is the chart version. This version number should be incremented each time you make changes to the chart and its templates, including the app version.
# Versions are expected to follow Semantic Versioning (https://semver.org/)
version: 0.1.0

# This is the version number of the application being deployed. This version number should be incremented each time you make changes to the application. Versions are not expected to follow Semantic Versioning. They should reflect the version the application is using.
appVersion: 1.16.0
````

values.yml

````txt
replicaCount: 2

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""

service:
  type: ClusterIP
  port: 80

autoscaling:
  enabled: false

nginx:
  conf:
    message: "CloudAcademy DevOps 2020 v1"
````

Now these can be referenced using simply : `{{ .Values.service.port }}` in templates

`values.yml` file can override by cmd line args.

Template syntax are based on Go Templates

`_helpers.tpl` : template partials are repeated in other files and can be referenced as resusable partials. `{{ include smk-app.serviceAccountName }}` is used to import partials where this partial is defined in _helpers.tpl files.

`helm package [chart_name]` produces a chart in `.tgz` form.

`helm install ca-demo1 cloudacademyapp-0.1.3.tgz --dry-run` : dry run the manifests files

`helm repo index .` : hosts chart in a repo

## Templates

- A helm chart at its core consists of templates

- Clone following repo & inspect templates : `https://github.com/jeremycook123/helm-demo`
- Template Directives : `{{ }}` or `{{- -}}`
- Builtin Objects : `Values` and `Release`
- Template Partials
- Pipe Symbol `|` (nindent)
- Template functions - (indent, nindent, sha256sum)

---

## File: kubernetes/helm/demo.md

# Helm Demo



## Installing Bitnami Wordpress Helm Chart

````bash
minikube start

helm search hub wordpress -o yaml
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo list
helm repo update

helm search repo wordpress

helm install wordpress \
--set wordpressUsername=admin \
--set wordpressPassword=password \
--set mariadb.mariadbRootPassword=secretpassword \
bitnami/wordpress

helm list
kubectl get all
helm status wordpress
minikube service wordpress
navigate http://127.0.0.1:58388/wp-admin

helm uninstall wordpress
````









---

## File: kubernetes/helm/index.md

# Helm



### [Content](content.md)

- Helm Introduction
- Benefits
- Terminology
- Architecture
- Installation
- Commands
- Charts
- Templates



### [Demo](demo.md)

- Installing Bitnami Wordpress Helm Chart



### Resources

- [Github Repo](https://github.com/jeremycook123/helm-demo)

---

## File: kubernetes/index.md

# Kubernetes

[Kubernetes](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/), also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.

#### Notes :

[Introduction to Kubernetes Notes](cloudacademy/index.md)

[Helm](helm/index.md)

[Kubernetes Patterns for Application Developers](k8s_app_dev/index.md)

[Kubernetes: The Complete Guide - Notes](sgrider/index.md)

#### Resources :

[Official Docs](https://kubernetes.io/docs/home/)



### CKAD Guide



---

## File: kubernetes/k8s_app_dev/index.md

# Kubernetes Patterns for Application Developers

[Resource Repo](https://github.com/lrakai/kubernetes-patterns-for-application-developers)

## Multi-Container Patterns

#### Why Pods ?

- pods are abstraction above containers but why ?
- Kubernetes needs additional information
- simplifies using different underlying container runtimes like docker or rocket
- co-locate tightly coupled containers without packaging them as a single image

Patterns

### Sidecar Pattern

- uses a helper container to assist a primary container
- commonly used for logging, file syncing, watchers
- benefit inlcude leaner main container, failure isolation, independent update cycles
- File Sync Sidecar Example
  - primary container : web-server, sidecar : content puller
  - content puller & web-server share a single volume within pod, in which content puller fetches latest files from CMS and keeps both containers in sync via volume.

### Ambassador Pattern

- ambassador container is a proxy for communicating to and from the primary container
- commonly used for communicating with databases
- streamlined development experience, potential to reuse ambassador across language
- Database Ambassador Example:
  - primary container : web-app
  - ambassador : database-proxy
  - web app handles request
  - database requests are sent to database proxy over localhost
  - database proxy then forwards the requests to appropriate database
  - possibly sharding the request

### Adaptor Pattern

- adapter present a standardized interface across multiple pods
- commonly used for normalizing output logs and monitoring data
- adapts third-party software to meet your needs

Example Changes logging format from txt to json

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapted-pod
spec:
  containers:
  - name: app
    image: alpine:3.9.2
    command: ["/bin/sh", "-c"]
    args:
    - while true; do 
        date > /metrics/raw.txt;
        top -n 1 -b >> /metrics/raw.txt;
        sleep 5;
      done
    # Share metric data between containers
    volumeMounts:
    - name: metrics
      mountPath: /metrics
  - name: adapter
    image: httpd:2.4.38-alpine
    command: ["/bin/sh", "-c"]
    # Adapt the legacy output to standard monitoring format
    args:
    - while true; do 
        date=$(head -1 /metrics/raw.txt);
        memory=$(head -2 /metrics/raw.txt | tail -1 | grep -o -E '\d+\w' | head -1);
        cpu=$(head -3 /metrics/raw.txt | tail -1 | grep -o -E '\d+%' | head -1);
        echo "{\"date\":\"$date\",\"memory\":\"$memory\",\"cpu\":\"$cpu\"}" > /metrics/adapted.json;
        sleep 5;
      done
    # Share metric data between containers
    volumeMounts:
    - name: metrics
      mountPath: /metrics
  volumes:
  - name: metrics
    emptydir:
````



## Networking

### Networking Basics

- each pod has one unique IP, while all containers inside pod share this one IP and communicate with each other freely
- Networking Plugins enables Pod to Pod Communication

### Services

- maintains a service replica pods selected based on labels to keep track of the pod during pods lifetime
- maintains a list of endpoints as pods are added and removed from the set
- can send request to any pod in the set
- clients of service only need to know about the service rather than specific pods
- pods can discover services via environment variables as long they are created after service or by using DNS Addon and IP Resolution
- ClusterIP service is only reachable within cluster. Kubeproxy cluster component that runs on each node is responsible for proxying the request for the service to one of the services endpoint.
- NodePort service allows any port to be open outside the cluster
- LoadBalancer Service exposes the service externally through a cloud providers load balancer. Also creates ClusterIP and NodePort
- External Name : external service enabled by DNS, used for Database as a Service or other things

### Network Policy

- Rules for controlling network access to Pods
- Similar to security groups controlling access to virtual machines
- scoped to namespace
- Caveat
  - kubernetest network plugin must support network policy
  - example : calico, canal, flannel etc.
- Non-isolated pod : accepts traffic from anywhere
- Isolated pods are non-isolated pods once selected by network policy

````yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-us-east
  namespace: network-policy
spec:
  # Which Pods the policy applies to
  podSelector:
    matchLabels:
      app: server
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    # Supports podSelector, namespaceSelector, and ipBlock
    - podSelector:
        matchLabels:
          region: us-east
    ports: # If not present allows all ports 
    - protocol: TCP
      port: 8888
  egress:
  - to: # Allows all traffic when empty
````

Block one-IP

````yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-one-ip
  namespace: network-policy
spec:
  podSelector:
    matchLabels:
      app: server
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0			# all ips
        except:
        - 192.168.134.71/32
````

## Service-Accounts

### Service Accounts

- provide an identity to Pods in the cluster
- stored in, and managed by the cluster
- scoped to namespace
- service account are compatible with RBAC(Role-Based Access Control)
- pods have a token mounted on a volume that can be used to authenticate requests
- default service account token has no additional permission than an unauthenticated user

### Configuration

````bash
# kube api service accounts
kubectl get -n kube-system serviceaccounts | more

# finding roles in coredns serviceaccount
kubectl describe -n kube-system clusterrole system:coredns
````

### Image Pull Secrets

- image pull secrets authenticate with private container registries
- service accounts can also store image pull secrets

## Leveraging kubectl

#### Shell Completion

- get all commands: `kubectl | more`
- get all completion commands: `kubectl completion --help`
- enable completion in shell: `source <(kubectl completion bash)` (Add to .bashrc for enabling it every login)
- Now `kubectl <TAB>` should work. Try : `kubectl get <TAB>`
- with completion enabled you can even autocomplete resource types but you can use short names
- To get entire list of completion : `kubectl api-resource`

#### get Tricks

- getting specific pods with labels : `kubectl get pods --all-namespace -L <label_name> -l [filter_label_name]`
- sort by the fields : `kubectl get pods -n kube-system --sort-by=metadata.creationTimestamp` or more correctly`kubectl get pods -n kube-system --sort-by='{.metadata.creationTimestamp}`
- output yaml for get commands: `kubectl get pods -n kube-system kube-proxy-<hash> --output=yaml`
- To print ip and sort by ip: `kubectl get pods -n kube-system --sort-by='{.status.podIP}' -o wide`

#### Generating Manifests

- creating resources without manifests: `kubectl create -h | less`
- try creating namespace : `kubectl create namespace tips -o yaml --dry-run`
- Redirect output to mkdir tips : `kubectl create ns tips -o yaml --dry-run > tips/1-namespaec.yaml`
- Create a nginx deployments : `kubectl run nginx --image=nginx --port=80 --replicas=2 --expose --dry-run -o yaml`
- exporting a resource: `kubectl get pods -n kube-system kube-proxy-<hash> -o yaml --export`

#### Explaining Fields

- `kubectl explain -h | less`
- to get information about a fields : `kubectl explain pod | more`
- more information : `kubectl explain pod.spec.containers.resources | more`



---

## File: kubernetes/sgrider/index.md

## Notes

Following notes are based on a course created by Stephan Grider.

[Section 11-13 Basics of Kubernetes](part4.md)

[Section 14-15 Multi-Container Apps with Kubernetes](part5.md)

[Section 16-18 Deployments](part6.md)



---

## File: kubernetes/sgrider/part4.md

## Notes : Kubernetes

### Section 11 : Onwards to Kubernetes!

#### Why’s and What’s of Kubernetes

Let’s say our application starts to get a lot of traffic then we need to scale things up. The most important or processing heavy part of our previous application was worker container. If we had a way to replicate the worker container then we could easily handle the traffic.

![image-20220413002240390](part4.assets/image-20220413002240390.png)

Why don’t we rely on AWS EB ? Reason is because for each scaling of multi-container app its going to spawn multipe multi-container instances. More machines but very little control over what each one of those containers are doing.

![image-20220413002326119](part4.assets/image-20220413002326119.png)

But we only need a worker container to replicate as per the load. Thats where Kubernetes comes in. Following is the diagram of very simple cluster.

![image-20220413002559296](part4.assets/image-20220413002559296.png)

Nodes in Kubernetes can run any number of containers and a cluster can have any number of Nodes. Master controls what each Node does, and we can interact with Master. We have a Load Balancer that will relay traffic optimally to Nodes.

- What : System for running different containers over multiple different machines.
- Why : When we need to run many different containers with different images.

#### Kubernetes in Development and Production

- Development : We use `minikube` to create small cluster.
- Production : We use managed solutions : Amazon Elastic Container Service for Kubernetes (EKS), Google Cloud Kubernetes Engine (GKE) or Do it yourself.

We use `kubectl` is used to manage containers in node while `minicube` which in reality is used for managing the VM itself. NOTE : `minicube` is used locally only.

##### Setting up Kubernetes on MacOS

Just go to docker desktop and enable Kubernetes from it.

#### Mapping Existing Knowledge

Goal : Get the **multi-client** image running on our Kubernetes running on a cluster.

Each entry in our last project represented containers we wanted to create and defined its network requirements.

|                        Docker Compose                        |                    Kubernetes                     |
| :----------------------------------------------------------: | :-----------------------------------------------: |
| Each entry can optionally get docker-compose to build an image | Kubernetes expects all images to already be built |
|     Each entry represents a container we want to create      |   One config file per object we want to create    |
|    Each entry defines the networking requirements (ports)    |     We have to manually set up all networking     |

- Make sure our image is hosted on docker hub
- Make one config file to create the container
- Make one container to setup networking.

Get the **multi-container** image running on our local Kubernetes Cluster running as a container.

#### Adding Configuration Files

To avoid mistakes, you are suggested to use image hosted at `image: stephengrinder/multi-client` or use yours if it is correct.

The reason why your configuration might fail is because in `default.conf` we had `try_files $uri $uri/ /index.html` which resolved React Router Issues with the app but it will break the `pod` we are about to create.

Make a folder name `simplek8s` : `k8s` is abbreviation of Kubernetes.

Make two files `client-pod.yaml` and `client-node-port.yaml` with contents as

````yaml
apiVersion: v1
kind: Pod
metadata:
  name: client-pod
  labels:
    component: web
spec:
  containers:
    - name: client
      image: stephengrinder/multi-client
      ports:
        - containerPort: 3000
````

and

````yaml
apiVersion: v1
kind: Service
metadata:
  name: client-node-port
spec:
  type: NodePort
  ports:
    - port: 3050
      targetPort: 3000
      nodePort: 31515
  selector:
    component: web
````

Config file describes the containers we want and Kubernetes doesn’t actually made a containers instead it makes something called as Objects.

![image-20220413075114643](part4.assets/image-20220413075114643.png)

Pod usually runs the containers and service provides networking to container. And Each Api version actually defines different types of objects we can have.

- apiVersion: v1
  - componentStatus
  - configMap
  - Endpoints
  - Events
  - Namespace
  - Pod
- apiVersion: apps/v1
  - Controller Revision
  - StatefulSet

#### Running Containers in Pods

![image-20220413075651352](part4.assets/image-20220413075651352.png)

`minicube start` creates a virtual machine which is called as a Node. That Node is used by Kubernetes to run some number of Objects. Most basic object is a Pod. Pod is grouping of containers with similar purpose.

In world of Kubernetes there is no way to create a container only. There is always a overhead because we have Objects. Smallest thing we can have is Pod running a container.

Technically Pod can have any type of containers but we always have similar working or tightly integrated containers inside the pod.

A example of Tightly Integrated Containers : database connected to logger and backup-manager.

![image-20220413080336176](part4.assets/image-20220413080336176.png)

So our first file `client-pod.yaml` defined the pod with running a container and `client-node-port` actually is Service which sets up the networking in a Kubernetes cluster.

#### Service Config Files in Depth

Pods is only of one type but Service can have multiple types

- ClusterIP
- NodePort : Exposes a container to the outside world (only for dev purposes)
- LoadBalancer
- Ingress

A browser sends requests to a Kube-proxy which transfers the traffic to NodePort which in turn sends the request to Pods. Now there may be multiple NodePort so its responsibility of Kube-proxy to direct traffic to those NodePort.

For directing the traffic we use **label selector system** (component:web, or tier:frontend) which connects two Objects get linked up.

Other Pods can connect or interact with each another with the help of NodePort Service.

![image-20220413081649566](part4.assets/image-20220413081649566.png)

#### Connecting to running Containers

We use `kubectl apply -f <filname>` to load up the Kubernetes Cluster. We need to do same for both yaml file.

To check status of both objects we created by `kubectl get pods` for all pods or `kubectl get Services`

NOTE: kubernetes service is internal service and we don’t have to worry about it.

NOTE : READ CAREFULLY : if you are using kubernetes from docker-desktop then **DO NOT USE MINIKUBE** Just visit the **localhost:31515**. In case you are using virtualbox drivers then you may follow `minikube` .

**Virtual Box Drivers (only)**

Now to access to pod we will need to visit using a specific IP address rather than `localhost`. Type `minikube ip` to get IP.

And access the website at the IP:31515 in your browser.

Or if you are not able to connect using IP you can use following command to port foward the service to localhost.

`minikube port-forward service/client-node-port 7080:3050`

Then visit localhost:7080 to visit the page.

#### The Entire Deployment Flow

If you type `docker ps` then you will see many containers running. Now even if you kill containers, Kubernetes will restart it again.

On Kubernetes there are 4 programs running called as Master, and `kube-apiserver` reads the deployment files and creates Objects and in case if some of containers go offline, it instructs Nodes to restart it again.

`kubectl` command communicates with Master not the Nodes itself. Its master who has the responsibility of managing the Nodes based on what our `yaml` file desires.

#### Imperative vs Declarative Deployments

Summary :

- Kubernetes is a system to deploy containerized apps.
- **Nodes** are individual machines (or vm’s) that run containers.
- **Masters** are machines (or vm’s) with set of programs to manage nodes
- Kubernetes didn’t build our images - it got them from somewhere else
- Kubernetes (the master) decided where to run each container - each node can run a dissimilar set of containers
- To deploy something, we update the desired state of the master with a config file.
- The master works constantly to meet your desired state.

Imperative Deployments : Do exactly these steps to arrive at this container setup

Declarative Deployments : Our container setup should look like this make it happen.

Which one should you choose ? This certainly depends on what your use cases are, there are lots of blogs, tutorials which will say you should choose this and that, in the end it depends on how much clear understanding of the kubernetes you have and how well you understand what you need.

### Section 13: Maintaining Sets of Containers with Deployments

#### Updating Existing Objects

Goal : Update our existing pod to use muti-worker image.

Imperative Approach : Run a command to list out current running pods -> Run a command to update the current pod to use a new image.

Declarative Approach : Update our config file that originally created the pod -> Throw the updated config file into `kubectl`.

Every config file has 2 parameters (*name*, *kind*) which help **master** uniquely identify objects inside of cluster. By using name: *client-pod*,  kind :*pod* and image as `multi-worker` (changed), Master is able to uniquely identify that this is a pod that exists and we want a new image up there.

After making appropriate changed in yaml config file, execute `kubectl apply -f <config_file>`.

To inspect already running objects use `kubectl describe <object_type> [Object_name]`.

````
kubectl describe pods
````

````bash
kubectl describe pod multi-worker
````

Note we can only update few things about pod only, you check this out by changing port and rerunning and you will see the error message print out.

So we will make use a new object, **Deployment** maintains a set of identical pods ensuring that they have the correct config and that the right number exists.

Generally we use pods in development environment only, while we use Deployment is used in production. Note : So we don’t actually doesn’t use pod, but remember Deployment is just a pod with more abilities and allows editing config files.

#### Deployment Configuration Files

Create a file `client-deployment.yaml` with contents

````yaml
apiVersion: app/v1
kind: Deployment
metadata:
  name: client-deployment

spec:
  replicas: 1
  selector:
    matchLabels:
      component: web
  template:
    metadata:
      labels:
        component: web
    spec:
      containers:
        - name: client
          image: stephengrider/multi-client
          ports:
            - containerPort: 3000
````

Inside of template section is all information about the every pod created by this deployment.

Replicas is number of differnet pods this *Deployment* will create. Deployments itself doesn’t create the pod, instead the Deployment using kubernetes API calls out to master and the *selector* acts as a handle for the pods that master will create.

##### Deleting an existing object

````
kubectl delete -f <config_file>
````

Remove the old pod running and create the new *Deployment*.

#### Why Use Services

Execute :

````bash
kubectl get pods -o wide
````

Every pod is assigned a internal IP address. If pod get deleted or updated then its quite possible that pod gets new IP address. Service watches pods with *selector* and direct traffic to correct pod.

If you make changes to deployment files, lets say ports then what Deployment does is that it entirely deletes the existing pod and recreates a new one, which can be inferred using `kubectl get pods` to get the age of the pod.

#### Updating Deployment Images

1. Change deployments to use multi-client again.
2. Update the multi-client image, push to Docker Hub.
3. Get the deployment to recreate our pods with the latest version of multi-client.

Note : Step-3 is very challanging.

Visit this discussion [LINK](https://github.com/kubernetes/kubernetes/issues/33664).

In order to pull the latest image there is no system present to detect this, since there is no changes to the file and if we use `kubectl apply` it will not update the pods.

Workarounds to the problem

- Manually delete pods to get the deployment to recreate them with the latest version : (Issues : we could end up deleting very important pods, or maybe we may be having downtime of few minutes which may be catastrophe in real life situation)
- Tag images with a real-version numbers, certainly this is an actionable change to config file and deployment will certainly update the pods. (Adds in an extra step in deployments)
-  Use an imperative command to update the image version the deployment should use. (Uses an imperative command).

Certainly first method is very very bad. Mehod 2 seems good but it becomes painful to change files too much, so method 3 kind of becomes reasonable solution but its not best one.

#### Imperatively Updating a Deployment’s Image

Push updates to the docker hub with tags.

Then execute the following command.

````bash
kubectl set <property> <object_type>/<object_name> <container_name> = <new_property>
````

````bash
kubectl set image <obj_type>/<obj_name> <container_name> = <new Image>
````

````bash
kubectl set image deployment/client-deployment client=stephengrider/multi-client:v5
````



---

## File: kubernetes/sgrider/part5.md

## Notes : Kubernetes

### Section 14 : A Multi-Container App with Kubernetes

#### Path to Production

We will first develop everything in single Node locally and when we deploy it off to some service like AWS we will have option of multiple Nodes.

![image-20220416083808489](part5.assets/image-20220416083808489.png)

So we will have a lots of config files for pods and services :)

Clone the following repository [Link](https://github.com/mightyjoe781/fibCalculator/tree/checkpoint-1_k8s) , checkout the branch: checkpoint_k8s  and execute:

````bash
docker compose up --build
````

#### Recreating the Deployment

Remove the nginx folder since we will be using *Ingress* Service. Remove the aws deployment file, travis.yaml, and Docker compose files. Now directory should have only 3 folders : client, server, worker.

We we be recreating everything using Kubernetes. We will need to create 9-10 config files. Make a new directory k8s inside complex.

Create a file `client-deployment.yaml` 

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      component: web
  template:
    metadata:
      labels:
        component: web
    spec:
      containers:
        - name: client
          image: stephengrider/multi-client
          ports:
            - containerPort: 3000
````

#### NodePort vs Cluster IP

NodePort: Exposes a set of pods to outside world (only good for dev purposes).

Cluster IP: Exposes a set of pods to other objects in the cluster. We use Ingress with it to allow external access.

Create a new file, `client-cluster-ip-service.yaml`

````yaml
apiVersion: v1
kind: Service
metadata:
  name: client-cluster-ip-service
spec:
  type: ClusterIP
  selector:
    component: web
  ports:
  - port: 3000
    targetPort: 3000
````

To apply above two file inside of k8s directory.

````
kubectl apply -f k8s
````

#### Express API Deployment Config

We will create 2 more files with almost similar config files.

Create a new file `server-deployment.yaml`

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      component: server
  template:
    metadata:
      labels:
        component: server
    spec:
      containers:
        - name: server
          image: stephengrider/multi-server
          ports:
            - containerPort: 5000
````

Note : Remember multi-server expects a bunch of environment variables.

Cluster IP for Express API

Create a new file `server-cluster-ip-service.yaml`

````yaml
apiVersion: v1
kind: Service
metadata:
  name: server-cluster-ip-service
spec:
  type: ClusterIP
  selector:
    component: server
  ports:
  - port: 5000
    targetPort: 5000
````

#### Combining Config into Single Files

We said we will have 9-10 config files, you can organize multiple config files into a single file.

Each of config should be separated by three dashes

````yaml
config_file-1
---
config_file-2
````

#### Worker Deployment

Create a file named `worker-deployment.yaml`

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: worker
  template:
    metadata:
      labels:
        component: worker
    spec:
      containers:
        - name: worker
          image: stephengrider/multi-worker
          env: 
            - name: REDIS_HOST
              value: redis-cluster-ip-service
            - name: REDIS_PORT
              value: 6379
````

Now remember we will eventually need more replicas since worker is actually the part of application that handles most of calculation.

Also note no port and ClusterIP file needed since it connects to other and does the work.

#### Creating and Applying Redis config

Create a file `redis-deployment`

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: redis
  template:
    metadata:
      labels:
        component: redis
    spec:
      containers:
        - name: redis
          image: redis
          ports:
            - containerPort: 6379
````

Create a file `redis-cluster-ip-service.yaml`

````yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-cluster-ip-service
spec:
  type: ClusterIP
  selector:
    component: redis
  ports:
  - port: 6379
    targetPort: 6379
````

#### PostgreSQL config

Create a file `postgresql-deployment.yaml`

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
spec:
  replicas: 1
  selector:
    matchLabels: 
      component: postgres
  template:
    metadata:
      labels:
        component: postgres
    spec:
      containers:
        - name: postgres
          image: postgres
          ports:
            - containerPort: 5432
````

#### The Need for Volumes with Databases

We can certainly create database and storage inside containers/pods. But wait what if there is some error in pod what does Master does ? :) creates new pods and data is lost.

We use PVC (Persistent Volume Claim) as separate storage solution i.e. Volumes which provide consistent data storage solution.

As indicated earlier we can certainly have more than one replicas of Postgres but if there are 2 replicas of postgres and they are sharing one filesystem for storage and they are not aware of each other then its recipe for disaster.

Volume in Docker was related to mechanism that allows a container to access a filesystem outside itself. Volume in Kubernetes is an object that allows containers to store data at the pod level.

Note in Kubernetes there is PVC, Persistent Volume, Volume (we don’t want it for data that needs to persist)(Also not same as volume in dockers). Be careful what documentation refers to.

If we create a Volume (we should not) then there are containers and volumes within pod, and if containers did crash volume will persist but what if entire pod gets deleted then entire volume and containers will be gone that is why we use Persistent Volume. Even if pod now gets deleted there will be no effect to Persistent Volume.

![image-20220416122323134](part5.assets/image-20220416122323134.png)

#### PV vs PVC

PVC is just a claim its not an actual storage, instead it advertises the options available to you. There are 2 ways to provision your Volumes

- Statically provisioned Volume
- Dynamically provisioned Volume

#### Claim Config Files

Create a file name database-persistent-volume-claim.yaml

````yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-persistent-volume-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
````

Note Volume Claim is not actual storage ! There are 3 types of access modes

- ReadWriteOnce : Can be used by a single node
- ReadOnlyMany : Multiple nodes can read from this
- ReadWriteMany : Can be read and written to by many nodes.

##### Where does Kubernetes Allocate Persistent Volumes ?

When you ask Kubernetes for storage in local development context then it will take a slice of your hard-drive otherwise it have PlugIn support for many services out there for example, Google Cloud Persistent Data, Azure Files, Azure Disk, AWS Block Store, etc.

Visit this [Page](https://kubernetes.io/docs/concepts/storage/storage-classes/) for more details.

Add following property in `spec` of Kubernetes config file of `postgres-deployment.yaml`

````yaml
    spec:
      volumes: 
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-persistent-volume-claim
      containers:
        - name: postgres
          image: postgres
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
              subPath: postgres
````

subPath is specific to postgres, it just stores data in a folder name postgresql.

#### Defining Environment Variables

![image-20220416145317298](part5.assets/image-20220416145317298.png)

Here Red Variables are the ones that keep changing and Yellow one are consistent. To connect to cluster just provide the name of the Cluster-IP-service you want to connect to it.

Add following to `worker-deployment.yaml` env right after image tag

````yaml
          image:
          env: 
            - name: REDIS_HOST
              value: redis-cluster-ip-service
            - name: REDIS_PORT
              value: 6379
````

and to `server-deployment.yaml`

````yaml
          ports:
          env: 
            - name: REDIS_HOST
              value: redis-cluster-ip-service
            - name: REDIS_PORT
              value: 6379
            - name: PGUSER
              value: postgres
            - name: PGHOST
              value: postgres-cluster-ip-servicec
            - name: PGPORT
              value: 5432
            - name: PGDATABASE
              value: postgres
````

#### Creating Encoded Secret

`PGPASSWORD` should not be plain text. We will use new object in Kubernetes that is Secrets which securely stores information in the cluster, such as database password.

To create a secret we use following command

````bash
kubectl create secret generic <secret_name> --from-literal key=value
````

Example : Run the following command

````bash
kubectl create secret generic pgpassword --from-literal PGPASSWORD=12345asdf
````

To add this to `server-deployment.yaml `

````yaml
- name: PGPASSWORD
  valueFrom:
    secretKeyRef:
      name: pgpassword
      key: PGPASSWORD
````

and for `postgres-deployment.yaml`

````yaml
image:
env:
  - name: POSTGRES_PASSWORD
    valueFrom:
      secretKeyRef:
        name: pgpassword
        key: PGPASSWORD
````

NOTE : In recent documentation its necessary to name the variable POSTGRES_PASSWORD in `postgresql-deployment.yaml`

Note : you always provide Environmental variable in strings i.e. pass ports as string. If you get a not able to convert error its probably because you passed the ports as numbers.

All file should now match the repository at this point [link](https://github.com/mightyjoe781/fibCalculator/tree/checkpoint-2_k8s)

### Section 15: Handling Traffic with Ingress Controllers

#### Load Balancer Services

LoadBalancer : Legacy way of getting network traffic into a cluster.

Load Balancer won’t give access to multiple nodes that is the reason we are not using it. Traditionally load balancers were provided by the cloud providers ( still being provided) but some people thing these loadbalancers are deprecated, yet kubernetes official documentaion doesn’t provide any such indication.

#### A Quick Note on Ingress

In Kubernetes there are multiple implementations of Ingress and we are gonna use Ngnix Ingress.

- We are using *nginx-ingress*, a community led project.
- We are **not** using *kubernetes-ingress*, a project led by nginx company.

**NOTE**: Setup of ingress-ngnix changes depending on your environment(local, GC, AWS, Azure). We are going to set up ingress-nginx on local and GC.

#### Behind the scenes of Ingress

In Kubernetes world anything that contstantly work to reach some desired state is called as *Controller*. For examples, our deployments was constantly making sure pods run, they are also a *Controller*.

We are going write a config file and the kubectl will generate Ingress Controller which will handle traffic for Nodes.

![image-20220416154134917](part5.assets/image-20220416154134917.png)

For Google Cloud Setup of Ingress-Nginx

![image-20220416154348993](part5.assets/image-20220416154348993.png)

Behind the scenes on Google Cloud still loadBalancer is used. 

To read more about Ingress Nginx[ Refer Here ](https://www.joyfulbikeshedding.com/blog/2018-03-26-studying-the-kubernetes-ingress-system.html)

After this point instruction won’t work on latest M1 chip, use other drivers rather than `docker desktop`. Still you can try port forwarding , read more on the website.

#### Setting up Ingress Locally with Minikube

Navigate to `https://kubernetes.github.io/ingress-ngnix` then to Deployment -> Generic Deployments and follow instructions.

Install a ingress addon using kubectl

#### Creating the Ingress Configuration

Create a file named `ingress-service.yaml`

````yaml
apiVersion: networking.k8s.io/v1
# UPDATE API
kind: Ingress
metadata:
  name: ingress-service
  annotations:
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/use-regex: 'true'
    # ADD ANNOTATION
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    # UPDATE ANNOTATION
spec:
  rules:
    - http:
        paths:
          - path: /?(.*)
            # UPDATE PATH
            pathType: Prefix
            # ADD PATHTYPE
            backend:
              service:
                # UPDATE SERVICE FIELDS
                name: client-cluster-ip-service
                port:
                  number: 3000
          - path: /api/?(.*)
            # UPDATE PATH
            pathType: Prefix
            # ADD PATHTYPE
            backend:
              service:
                # UPDATE SERVICE FIELDS
                name: server-cluster-ip-service
                port:
                  number: 5000
````



---

## File: kubernetes/sgrider/part6.md

## Notes : Kubernetes

### Section 16: Kubernetes Production Deployment

#### The Deployment Process

Production will follow the following workflow

1. Create Github Repo
2. Tie repo to Travis CI
3. Create google cloud project
4. **Enable billing for the project**
5. Add deployment scripts to the repo

#### Google Cloud vs AWS for Kubernetes

- Google created Kubernetes
- AWS only “recently” got Kubernetes support
- Far, far easier to poke around Kubernetes on Google Cloud
- Excellent documentation for beginners

Create a Repository, take a [Reference](https://github.com/StephenGrider/multi-k8s) and link it to Travis.

#### Create a Google Cloud Project

Visit console.cloud.google.com (Google Cloud Console). Click Create Project and name is `multi-k8s`. After Project is created select the active project.

We will need to enable billing from Nav Menu on top left burger button.

1. Click the Hamburger menu on the top left-hand side of the dashboard.

2. Click **Kubernetes Engine**

3. Click the **ENABLE** button to enable the Kubernetes API for this project.

4. After a few minutes of waiting, clicking the **bell** icon in the top right part of the menu should show a **green** checkmark for **Enable services: container.googleapis.com**

5. If you refresh the page it should show a screen to create your first cluster. If not, click the hamburger menu and select **Kubernetes Engine** and then **Clusters**. 
   Once you see the screen below, click the **CREATE** button.

6. A **Create Cluster** dialog will open and provide two choices. Standard and Autopilot. Click the **CONFIGURE** button within the **Standard** cluster option

7. A form similar to the one shown in the video will be presented. Set the **Name** to **multi-cluster** (step 1). Confirm that the **Zone** set is actually near your location (step 2). The Node Pool that is discussed in the video is now found in a separate dropdown on the left sidebar. Click the downward-facing arrow to view the settings. No changes are needed here (step 3). Finally, click the **CREATE** button at the bottom of the form (step 4).

   ![img](https://img-c.udemycdn.com/redactor/raw/article_lecture/2021-03-11_23-41-11-a933c590c507f8e1ead0e611eebdbb1d.png)

   

8. After a few minutes, the cluster dashboard should load and your multi-cluster should have a **green** checkmark in the table.

#### Don’t Forge to Cleanup !

**Remember, as long as this cluster is running you will be billed real life money!**

**Steps to clean up:**

1. Click the project selector on the top left of the page

2. Click the 'gear' icon on the top right

3. Find your project in the list of projects that is presented, then click the three dots on the far right hand side

4) Click 'Delete'

#### Travis Deployment Overview

Google Cloud SDK CLI allows login to Docker CLI and manipulate directly the kubernetes cluster.

- Install Google Cloud SDK CLI
- Configure the SDK with out Google Cloud Auth Info
- Login to Docker CLI
- Build “test” version of multi-client
- Run tests
- If test are successful, run a script to deploy newest images
- Build all our images, tag each one, push each to docker
- Apply all configs in the “k8s” folder
- Imperatively set latest images on each deployment

Create a `.travis.yaml` file

````yaml
sudo: required
services:
  - docker
before_install:
	# openssl command after encrytion from travis cmd line
	# openssl aes-256-cbc -K ...
	# install google-cloud sdk
  - curl https://sdk.cloud.google.com | bash > dev/null;
  - source $HOME/google-cloud-sdk/path.bash.inc
  # install minikube
  - gcloud components update kubectl
  # authenticate
  - gcloud auth activate-service-account --key-file service-account.json
````

#### Creating a Service Account

1. Click the Hamburger menu on the top left-hand side of the dashboard, find **IAM & Admin**, and select **Service Accounts**. Then click the **CREATE SERVICE ACCOUNT** button.
2. In the form that is displayed, set the **Service account name** to **travis-deployer** (step 1), then click the **CREATE** button (step 2).
3. Click in the **Select a role** filter and scroll down to select **Kubernetes Engine** and then **Kubernetes Engine Admin**.
4. Make sure the filter now shows **Kubernetes Engine Admin** and then click **CONTINUE**
5. The Grant users access form is optional and should be skipped. Click the **DONE** button.
6. You should now see a table listing all of the service accounts including the one that was just created. Click the **three dots** to the right of the service account you just created. Then select **Manage Keys** in the dropdown.
7. In the **Keys** dashboard, click **ADD KEY** and then select **Create new key**.
8. In the **Create private key** dialog box, make sure **Key type** is set to **JSON,** and then click the **CREATE** button.
9. The JSON key file should now download to your computer.

Now we should install Travis CLI to encrypt and upload the json file to our Travis account. In travis.yml add code to unencrypted the json file and load into GCloud SDK.

#### Running Travis CLI in a Container

Travis CLI need Ruby !! Pain to be setup on windows :). well you could use a container to install ruby. Lets get a Docker image that has pre-installed, then we can install CLI in there.

Remember now we have to use github tokens to login.

````bash
docker run -t v $(pwd):/app ruby:2.4
gem install travis
# we can use --com or --pro
travis login --github-token YOUR_TOKEN --com
# copy json file into the 'volumed' diectory so we can use it in the container
travis encrypt-file service-account.json -r USERNAME/REPO --com
````

Remove the `service-account.json` before uploading to the repository !!! Keep the `service-account.json.enc` file and upload it to the repo.

#### More on Google Cloud CLI config

````yaml
sudo: required
services:
  - docker
env:
	global:
	  # git sha for tagging images, for more see section below
	  - SHA=$(git rev-parse HEAD)
	  # no input prompt
	  - CLOUDSDK_CORE_DISABLE_PROMPTS=1
before_install:
	# openssl command after encrytion from travis cmd line
	# openssl aes-256-cbc -K ...
	# install google-cloud sdk
  - curl https://sdk.cloud.google.com | bash > dev/null;
  - source $HOME/google-cloud-sdk/path.bash.inc
  # install minikube
  - gcloud components update kubectl
  # authenticate
  - gcloud auth activate-service-account --key-file service-account.json
  - gcloud config set project skilful-ber-214822
  - gcloud config set compute/zon us-central1-a
  - gcloud container clusters get-credentials multi-cluster
  - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
  - docker build -t stephengrider/react-test -f ./client/Dockerfile.dev ./client
script:
  - docker run -e CI=true USERNAME/react-test npm test
# ... (1)
````

#### Custom Deployment Providers

Continuing on the Travis file

````yaml
script:
  - docker run -e CI=true USERNAME/react-test npm test
# ... (1)
deploy:
  provider: script
  # we use this custom deploy file
  script: bash ./deploy.sh
  on:
    branch: master
````

Create a new bash file `deploy.sh`.

````bash
#!/bin/bash
# Building images
docker build -t stephengrider/multi-client:latest -t multi-client:$SHA -f ./client/Dockerfile ./client
docker build -t stephengrider/multi-server:latest -t multi-server:$SHA -f ./server/Dockerfile ./server
docker build -t stephengrider/multi-worker:latest -t multi-worker:$SHA -f ./worker/Dockerfile ./worker
# Pushing images to Dockerhub
docker push stephengrider/multi-client:latest
docker push stephengrider/multi-server:latest
docker push stephengrider/multi-worker:latest
docker push stephengrider/multi-client:$SHA
docker push stephengrider/multi-server:$SHA
docker push stephengrider/multi-worker:$SHA
# Take all k8s config 
kubectl apply -f k8s
kubectl set image deployments/server-deployment server=stephengrider/multi-server:$SHA
kubectl set image deployments/client-deployment client=stephengrider/multi-client:$SHA
kubectl set image deployments/worker-deployment worker=stephengrider/multi-worker:$SHA
````

#### Unique Tags for Built Images

We have a git repository and with every commit a hash SHA is generated, we could use it as a tag along with latest tag.

Tagging images with git sha is good practice because at any point in time we know exactly what code is running in the clusters.

We are still tagging images with latest because it saves the trouble of finding the latest image among many sha for new engineers.

#### Configuring the GCloud CLI on Cloud

We had created a secret for kubernetes Secrets Objects earlier. Find the Active Cloud Shell and click it.

Execute Following to select correct project and zone.

````bash
# Select the correct project
gcloud config set project skilful-berm-214822
# Set the zone
gcloud config set compute/zone us-central1-a
# Get Credentials
gcloud container clusters get-credentials
````

Create a Secret

```bash
kubectl create secret generic pgpassword --from-literal PGPASSWORD=mypgpassword123
```

#### Helm Setup

Google Cloud doesn’t yet know what Ingress-Nginx is ! So we gonna install it with the help of Helm. Note we could easily have gone : mandatory and provider specific commands but we gonna need helm later on.

Helm is used to administer third party software inside Kubernetes. Helm and Tiller go hand in hand.

Installing Helm, run following command in Google Cloud Console run

````bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
````

[Link](https://helm.sh/docs/intro/install/#from-script)

#### Kubernetes Security with RBAC

Google GKE hosted Kubernetes platform enables RBAC by default. You will need to create Tiller Server.

Helm Client relays our commands to Tiller Server and its Tiller Server which will change Kubernetes Cluster.

RBAC : Role Based Access Control : limit who can access and modify object in our cluster. Enable by default. Tiller wants to make changes to our cluster, so it requires permissions to make changes.

- User Accounts : Identifies a *person* administering the cluster
- Service Accounts: Identifies a *pod* administering a cluster
- ClusterRoleBinding: Authorizes an account to do a certain set of actions across the entire cluster
- RoleBinding : Authorizes an account to do a certain set of actions in a *single namespace*

We will create a Service Account for Tiller and then allow ClusterRoleBinding to it.

 ````bash
 # service account creation
 kubectl create serviceaccount --namespace kube-system tiller
 # binding
 kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
 ````

#### Installing Ingress-Nginx

````bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install my-release ingress-nginx/ingress-nginx
````

Updating Cluster Version (only if you are prompted to)

````bash
gcloud container clusters upgrade  YOUR_CLUSTER_NAME --master --cluster-version 1.16
````

[Upgrading a Cluster](https://cloud.google.com/kubernetes-engine/docs/how-to/upgrading-a-cluster)

Switch to workloads tab and notice the Names of workloads

A default backend no longer ships with ingress-nginx, so, if you only see a controller and you get a **404 Not Found** when visiting the IP address, this is perfectly expected.

#### Finally Deployment

Commit everything and we expect CI to build images and update Kubenetes cluster.

Remeber Travis CI runs Build test for all branches but only pushes the code if its commited to main branch. So recommended workflow is to have a branch write some code, and if its built correctly merge it to main branch.

### Section 17: HTTPS Setup with Kubernetes

#### HTTPS Setup Overview

Setting up HTTPS require 10$ for domain name.

LetsEncrypt is a free service that allows us to get free certificates.

![image-20220417082226154](part6.assets/image-20220417082226154.png)

Its really hard to craft response for LetsEncrypt to verify ourselves.

We gonna use Cert Manager Plugin provided in Helm.

Buy the Domain.

Set the A record with following entry for the ip

Name : @ ,Type : A ,TTL:5min, IP: 30.14.13.54

Name : www ,Type : CNAME ,TTL:5min, IP: k8s-multi.com.

#### Installing Cert Manager

1. Create the namespace for cert-manager:

   `kubectl create namespace cert-manager`

2. Add the Jetstack Helm repository

   `helm repo add jetstack https://charts.jetstack.io`

3. Update your local Helm chart repository cache:

   `helm repo update`

4. ```bash
   # install the cert-manager helm chart
   helm instsall cert-manager jestack/cert-manager --namespce cert-manager --version v1.2.0 --create-namespace
   ```

5. ````bash
   # install the CRDs
   kubectl apply -f https://github.com/jetstack/certmanager/releases/download/v1.2.0/cert-manager.crds.yaml
   ````

[Official Installation Documentation](https://cert-manager.io/docs/installation/kubernetes/#installing-with-helm)

#### Setting up Cert Manager

We are going to use Objects in our Kubernetes project to store certificate and reply to lets encrypt.

![image-20220417083309087](part6.assets/image-20220417083309087.png)

Also LetsEncrypt allows a practice server for allowing responses using multi-issuers. Lets avoid them for now.

[Issuer Manifest Setup](https://docs.cert-manager.io/en/latest/tasks/issuers/setup-acme/index.html#creating-a-basic-acme-issuer)

Create a file `issuer.yaml` in k8s directory

````yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: "test@test.com"
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
````

[Certificate Manifest Official Docs](https://cert-manager.io/docs/tutorials/acme/http-validation/#issuing-an-acme-certificate-using-http-validation)

Create a `certificate.yaml` file in k8s directory.

````yaml
apiVersion: cert-manager.io/v1
 
kind: Certificate
metadata:
  name: yourdomain-com-tls
spec:
  secretName: yourdomain-com
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: yourdomain.com
  dnsNames:
    - yourdomain.com
    - www.yourdomain.com
````

We also need to Change to Ingress after we have got certificate and then enable it the Cert-Manager to use new certificate.

If you have deployed your issuer and certificate manifests to GCP and you are getting **No Resources Found** when running `kubectl get certificates`, then continue on to the next step to create and deploy the Ingress manifest. Deploying the updated Ingress should trigger the certificate to be issued.

#### Updating Ingress Config for HTTPS

Add following to annotations and to specs

````yaml
annotations:
  cert-manager.io/cluster-issuer: 'letsencrypt-prod'
  # HTTP -> HTTPS
  nginx.ingress.kubernetes.io/ssl-redirect: 'true'
spec:
  tls:
    - hosts:
      - youdomain.com
      - www.yourdomain.com
      # name of the secret that used to store certs
      secretName: yourdomain-com
  rules:
    - host: yourdomain.com
      http:
        paths:
          - path: /
            backend:
              serviceName: client-cluster-ip-service
              servicePort: 3000
          - path: /api/
            backend:
              serviceName: server-cluster-ip-service
              servicePort: 5000
    - host: www.yourdomain.com
      http:
        paths:
          - path: /
            backend:
              serviceName: client-cluster-ip-service
              servicePort: 3000
          - path: /api/
            backend:
              serviceName: server-cluster-ip-service
              servicePort: 5000
````

#### Google Cloud Cleanup

[Scroll UP](#Don’t Forge to Cleanup !)

#### Cleaning Up Local Setup

To remove everything we deployed from k8s directory

````bash
kubectl delte -f k8s/
````

To remove ingress-nginx

````bash
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.2/deploy/static/provider/cloud/deploy.yaml
````

To stop minikube and remove it

````bash
minikube stop
minikube delete
````

Stopping Running Containers

````bash
docker ps
docker stop <container_id>
# to clear cache
docker system prune
````

### Section 18: Local Development with Scaffold

#### Awkward Local Setup

We currently don’t have ability to see live changes while local development. We did find a trick for docker containers but what about Kubernetes. There are 2 modes of operation of Scaffold.

![image-20220417093819201](part6.assets/image-20220417093819201.png)[Installing Skafflod](https://skaffold.dev/docs/getting-started)

#### Scafflod Config File

We will create in root file directory a file called `skaffold.yaml` that will tell how the scaffold should act.

````yaml
apiVersion: skaffold/v2beta12
kind: Config
deploy:
  kubectl:
    manifests:
      - ./k8s/*
build:
# disable by default push behaviour to dockerhub on building images.
  local:
    push: false
  artifacts:
    - image: cygnetops/client-skaffold
      context: client
      docker:
        dockerfile: Dockerfile.dev
      sync:
        manual:
          - src: "src/**/*.js"
            dest: .
          - src: "src/**/*.css"
            dest: .
          - src: "src/**/*.html"
            dest: .
    - image: cygnetops/worker-skaffold
      context: worker
      docker:
        dockerfile: Dockerfile.dev
      sync:
        manual:
          - src: "*.js"
            dest: .
    - image: cygnetops/server-skaffold
      context: server
      docker:
        dockerfile: Dockerfile.dev
      sync:
        manual:
          - src: "*.js"
            dest: .
````

Update your client/Dockerfile.dev to add **CI=true**

````dockerfile
FROM node:alpine
ENV CI=true

WORKDIR "/app"
COPY ./package.json ./
RUN npm install
COPY . .
CMD ["npm","run","start"]
````

Finally run `skaffold dev` in your terminal (may take several minutes to run)

**Automatic Shutdown**

If we `ctrl + c` then skaffold automatically stops the objects. Do not add persistent config files to build of deploy cause skaffold will certainly delete it.

---

