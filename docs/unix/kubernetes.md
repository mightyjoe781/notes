# Kubernetes (kubectl)

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../kubernetes/index.md)

Container orchestration platform. Manages deployment, scaling, and networking of containerised applications.

### Installation

```bash
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# minikube (local cluster)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=docker
```

### Core Objects

| Object | Description |
|---|---|
| Pod | smallest deployable unit; one or more containers |
| Deployment | manages replica sets; handles rolling updates |
| Service | stable network endpoint for a set of pods |
| ConfigMap | inject non-sensitive config into pods |
| Secret | inject sensitive data (base64-encoded) |
| Namespace | virtual cluster for isolation |
| Ingress | HTTP routing from outside to services |

### Essential Commands

```bash
# Context and cluster
kubectl config get-contexts
kubectl config use-context my-cluster
kubectl cluster-info

# Pods
kubectl get pods
kubectl get pods -n namespace        # specific namespace
kubectl get pods -A                  # all namespaces
kubectl describe pod my-pod
kubectl logs my-pod
kubectl logs -f my-pod               # follow
kubectl logs my-pod -c container     # specific container in pod
kubectl exec -it my-pod -- sh        # shell into pod

# Deployments
kubectl get deployments
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app
kubectl scale deployment/my-app --replicas=3
kubectl set image deployment/my-app app=myimage:v2

# Services
kubectl get services
kubectl expose deployment/my-app --port=80 --target-port=3000 --type=ClusterIP

# Apply and delete
kubectl apply -f manifest.yaml
kubectl apply -f ./k8s/              # apply all files in directory
kubectl delete -f manifest.yaml
kubectl delete pod my-pod
```

### Sample Manifests

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

#### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  DATABASE_HOST: "postgres-svc"
```

### Debugging

```bash
# Describe resource (events, conditions)
kubectl describe pod my-pod
kubectl describe deployment my-app

# Port forward to local machine
kubectl port-forward svc/my-app 8080:80
kubectl port-forward pod/my-pod 8080:80

# Get events (useful for crash debugging)
kubectl get events --sort-by=.lastTimestamp

# Run one-off debug pod
kubectl run debug --image=busybox -it --rm -- sh

# Resource usage
kubectl top nodes
kubectl top pods
```

### Useful Patterns

```bash
# Watch resources update in real time
kubectl get pods -w

# Output as YAML
kubectl get deployment my-app -o yaml

# JSONPath query
kubectl get pods -o jsonpath='{.items[*].metadata.name}'

# Label selector
kubectl get pods -l app=my-app,env=prod

# Patch in place
kubectl patch deployment my-app -p '{"spec":{"replicas":5}}'

# Copy files to/from pod
kubectl cp my-pod:/app/log.txt ./log.txt
kubectl cp ./config.yaml my-pod:/app/config.yaml
```

### Tips

- Always set `resources.requests` and `resources.limits` on containers
- Use namespaces to isolate environments: `dev`, `staging`, `prod`
- `kubectl get all -n my-namespace` shows most resource types at once
- For RBAC use `kubectl auth can-i create pods` to debug permission issues
- Scan images for vulnerabilities with Trivy: `trivy image myapp:latest`

### See Also

- [Docker](docker.md) for building images
- Also: Helm (package manager for k8s), k3s (lightweight k8s), kind (k8s in Docker), kustomize (config management)
