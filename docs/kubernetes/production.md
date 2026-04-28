# Production

## Deployment Workflow

A typical production workflow for a containerized app on Kubernetes:

1. Developer pushes code to a branch
2. CI builds and tests the Docker image
3. CI tags the image with the git SHA and pushes to a registry
4. CI applies the updated manifests to the cluster
5. Kubernetes performs a rolling update

## Image Tagging Strategy

Tag images with both `latest` and the git SHA:

```bash
SHA=$(git rev-parse HEAD)

docker build -t myapp:latest -t myapp:$SHA ./
docker push myapp:latest
docker push myapp:$SHA
```

Benefits:
- `latest` means new engineers can pull without finding the right SHA
- SHA tag means you can always trace which code is running in production
- Provides a stable, unique tag for `kubectl set image` to trigger a rollout

## CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}

      - name: Build and push
        env:
          SHA: ${{ github.sha }}
        run: |
          docker build -t myuser/myapp:latest -t myuser/myapp:$SHA .
          docker push myuser/myapp:latest
          docker push myuser/myapp:$SHA

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Deploy
        env:
          SHA: ${{ github.sha }}
        run: |
          kubectl apply -f k8s/
          kubectl set image deployment/myapp app=myuser/myapp:$SHA
          kubectl rollout status deployment/myapp
```

## GKE Setup (Google Kubernetes Engine)

```bash
# Authenticate
gcloud auth login
gcloud config set project <project-id>
gcloud config set compute/zone us-central1-a

# Create a cluster
gcloud container clusters create my-cluster \
  --num-nodes=3 \
  --machine-type=e2-standard-2 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10

# Get credentials for kubectl
gcloud container clusters get-credentials my-cluster

# Create a production secret (do once manually)
kubectl create secret generic pgpassword --from-literal PGPASSWORD=<yourpassword>

# Install ingress-nginx via Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx

# Apply all manifests
kubectl apply -f k8s/

# Cleanup - delete to stop billing
gcloud container clusters delete my-cluster
```

## Namespace Strategy

Separate environments into namespaces or separate clusters:

```bash
kubectl create namespace staging
kubectl create namespace production

kubectl apply -f k8s/ -n staging
kubectl apply -f k8s/ -n production
```

Use [kubens](https://github.com/ahmetb/kubectx) to switch quickly:

```bash
kubens production
kubectl get pods
```

## Resource Quotas

Limit resource consumption per namespace:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    pods: "50"
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
```

## Limit Ranges

Set default resource requests/limits for pods that do not specify them:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "256Mi"
      defaultRequest:
        cpu: "100m"
        memory: "64Mi"
      max:
        cpu: "2"
        memory: "1Gi"
```

## kubectl Productivity Tips

### Aliases

```bash
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'
```

### Useful One-liners

```bash
# Watch pods in real time
watch -n 2 kubectl get pods

# Get all resource types in a namespace
kubectl get all -n production

# Sort pods by restart count
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'

# Find pods not in Running state
kubectl get pods --field-selector=status.phase!=Running

# Get pod IPs sorted
kubectl get pods -o wide --sort-by='{.status.podIP}'

# Quickly generate a deployment manifest
kubectl create deployment nginx --image=nginx:1.25 --dry-run=client -o yaml > deployment.yaml

# Get events sorted by time
kubectl get events --sort-by='.lastTimestamp'

# Delete all completed jobs
kubectl delete jobs --field-selector status.successful=1
```

### Explaining Fields

```bash
kubectl explain pod
kubectl explain pod.spec
kubectl explain pod.spec.containers.resources
kubectl explain deployment.spec.strategy
```

### Multi-cluster Workflow

```bash
kubectl config get-contexts
kubectl config use-context gke-production
kubectl config use-context docker-desktop
```

## Production Checklist

- [ ] All pods have resource `requests` and `limits` set
- [ ] Liveness and readiness probes configured
- [ ] Images tagged with specific versions (no `:latest` in production)
- [ ] Secrets stored in a secret manager, not plain YAML
- [ ] RBAC: pods use least-privilege service accounts
- [ ] Network policies restrict pod-to-pod traffic
- [ ] PodDisruptionBudgets set for critical services
- [ ] HPA configured for variable-load services
- [ ] Monitoring and alerting in place (Prometheus + Grafana)
- [ ] Centralized logging (Loki, ELK, Datadog)
- [ ] Regular etcd backups configured
