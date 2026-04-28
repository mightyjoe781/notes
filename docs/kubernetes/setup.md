# Setup

## Local Development

### Docker Desktop (Recommended for Mac/Windows)

The simplest way to get a single-node cluster locally.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Go to **Settings > Kubernetes > Enable Kubernetes**
3. Click **Apply & Restart**

Access the cluster at `localhost` directly - no extra IP needed.

### minikube

Runs a single-node cluster in a VM or container. Supports multiple drivers.

```bash
# Install (macOS)
brew install minikube

# Start cluster (Docker driver is default)
minikube start

# Start with a specific driver
minikube start --driver=qemu2    # better on Apple Silicon
minikube start --driver=virtualbox

# Basic commands
minikube status
minikube ip                      # get cluster IP
minikube dashboard               # open web UI
minikube stop
minikube delete

# Accessing a NodePort service (Docker driver)
minikube tunnel                  # exposes LoadBalancer services on localhost
kubectl port-forward svc/<name> 3000:80  # or use kubectl directly

# Accessing a NodePort service (qemu/virtualbox driver)
minikube ip                      # get IP, then curl <ip>:<nodePort>
```

#### Addons

```bash
minikube addons list
minikube addons enable metrics-server
minikube addons enable ingress
```

### kind (Kubernetes in Docker)

Runs multi-node clusters inside Docker containers. Great for CI and testing.

```bash
# Install
brew install kind

# Create a cluster
kind create cluster
kind create cluster --name dev --config kind-config.yaml

# Multi-node config example
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker

kind delete cluster
```

## Managed Clusters (Production)

| Provider | Service | Notes |
|----------|---------|-------|
| AWS | EKS (Elastic Kubernetes Service) | Most widely used in enterprise |
| GCP | GKE (Google Kubernetes Engine) | Easiest to set up; created K8s |
| Azure | AKS (Azure Kubernetes Service) | Good for Microsoft-heavy shops |
| DigitalOcean | DOKS | Simple and cheap for small projects |

### Self-Managed (On-Prem or Cloud VMs)

- **kubeadm** - official bootstrapping tool; install on bare metal or VMs
- **kubespray** - Ansible-based; good for complex multi-node setups
- **k3s** - lightweight K8s by Rancher; great for edge and IoT
- **k0s** - zero-friction K8s distribution

## kubectl Configuration

kubectl uses `~/.kube/config` to connect to clusters.

```bash
# View current config
kubectl config view

# List contexts (clusters)
kubectl config get-contexts

# Switch context
kubectl config use-context <context-name>

# Set a default namespace for the current context
kubectl config set-context --current --namespace=<namespace>

# Merge multiple kubeconfig files
KUBECONFIG=~/.kube/config:~/.kube/other-config kubectl config view --flatten > ~/.kube/merged-config
```

### Managing Multiple Clusters

Use [kubectx + kubens](https://github.com/ahmetb/kubectx) for fast context and namespace switching:

```bash
brew install kubectx

kubectx              # list contexts
kubectx <name>       # switch context
kubens               # list namespaces
kubens <name>        # switch namespace
```
