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
