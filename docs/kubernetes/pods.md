# Pods

## What is a Pod?

A Pod is the smallest deployable unit in Kubernetes. It wraps one or more containers that share:

- A single IP address
- The same network namespace (containers communicate via `localhost`)
- Storage volumes

In practice, most pods run a single container. Multi-container pods are used for tightly coupled helpers (see [Multi-Container Patterns](multi_container.md)).

> Do not create pods directly in production. Use a Deployment, Job, or StatefulSet to manage them.

## Basic Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: web
    env: prod
spec:
  containers:
    - name: app
      image: nginx:1.25
      ports:
        - containerPort: 80
```

```bash
kubectl apply -f pod.yaml
kubectl get pods
kubectl describe pod my-pod
kubectl delete pod my-pod
```

## Labels and Selectors

Labels are key-value pairs attached to objects. They are the primary mechanism for grouping and selecting resources.

```yaml
metadata:
  labels:
    app: frontend
    tier: web
    env: staging
```

```bash
# Filter by label
kubectl get pods -l app=frontend
kubectl get pods -l app=frontend,env=staging

# Show label values as columns
kubectl get pods -L app,env
```

## Namespaces

Namespaces partition a cluster into virtual sub-clusters. Use them to separate environments, teams, or applications.

```bash
kubectl get namespaces
kubectl create namespace staging

# Run commands in a namespace
kubectl get pods -n staging
kubectl apply -f pod.yaml -n staging

# Set default namespace for your context
kubectl config set-context --current --namespace=staging
```

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    env: staging
```

Default namespaces created by Kubernetes:

| Namespace | Purpose |
|-----------|---------|
| `default` | Resources with no namespace specified go here |
| `kube-system` | K8s internal components (DNS, proxy, etc.) |
| `kube-public` | Readable by all users; mostly unused |
| `kube-node-lease` | Node heartbeat leases |

## Resource Requests and Limits

Resource **requests** affect scheduling (which node gets the pod). Resource **limits** cap usage.

```yaml
spec:
  containers:
    - name: app
      image: nginx:1.25
      resources:
        requests:
          cpu: "250m"      # 250 millicores = 0.25 CPU
          memory: "64Mi"
        limits:
          cpu: "500m"
          memory: "128Mi"
```

### QoS Classes

Kubernetes assigns a Quality of Service class based on resource configuration:

| QoS Class | Condition | Eviction Risk |
|-----------|-----------|---------------|
| Guaranteed | requests == limits for all containers | Lowest |
| Burstable | requests set but limits > requests | Medium |
| BestEffort | no requests or limits set | Highest |

Check with: `kubectl describe pod <name> | grep QoS`

## Common Pod Options

```yaml
spec:
  containers:
    - name: app
      image: nginx:1.25
      imagePullPolicy: IfNotPresent   # Always | Never | IfNotPresent
      env:
        - name: ENV_VAR
          value: "hello"
      ports:
        - containerPort: 80
          name: http
      command: ["nginx"]
      args: ["-g", "daemon off;"]
  restartPolicy: Always               # Always | OnFailure | Never
  terminationGracePeriodSeconds: 30
```

### Image Pull Policy

| Policy | Behavior |
|--------|---------|
| `Always` | Always pull from registry (good for `:latest`) |
| `IfNotPresent` | Use cached image if available (default for versioned tags) |
| `Never` | Never pull; fail if not cached |

Avoid using `:latest` in production - it makes rollbacks harder and behavior unpredictable.

## Useful Pod Commands

```bash
# Get pod details
kubectl describe pod <name>
kubectl get pod <name> -o yaml

# Logs
kubectl logs <name>
kubectl logs <name> --previous       # logs from previous container instance
kubectl logs -l app=web              # logs from all pods matching label

# Exec into pod
kubectl exec -it <name> -- /bin/bash
kubectl exec <name> -- cat /etc/config

# Copy files
kubectl cp <name>:/etc/nginx/nginx.conf ./nginx.conf

# Watch pods
kubectl get pods -w
watch -n 2 kubectl get pods
```
