# Deployments

## Why Deployments?

A Deployment manages a set of identical, stateless pod replicas. It:

- Ensures the desired number of pods are always running
- Handles rolling updates without downtime
- Supports rollback to a previous version
- Replaces crashed or evicted pods automatically

> Always use Deployments (not bare Pods) in production.

## Basic Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend          # must match template labels
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: app
          image: nginx:1.25
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"
            limits:
              cpu: "250m"
              memory: "128Mi"
```

```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get pods                      # see pods created by the deployment
kubectl describe deployment frontend
```

## Scaling

```bash
# Manual scaling
kubectl scale deployment frontend --replicas=5

# Or edit the manifest and reapply
kubectl apply -f deployment.yaml
```

## Rolling Updates

The default update strategy replaces pods gradually so there is no downtime.

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # max pods above desired count during update
      maxUnavailable: 1    # max pods below desired count during update
```

### Triggering an Update

Update the image in the manifest and reapply:

```bash
kubectl set image deployment/frontend app=nginx:1.26
# or edit the YAML and kubectl apply
```

### Monitoring a Rollout

```bash
kubectl rollout status deployment/frontend
kubectl rollout history deployment/frontend
kubectl rollout history deployment/frontend --revision=2
```

### Rollback

```bash
# Roll back to the previous version
kubectl rollout undo deployment/frontend

# Roll back to a specific revision
kubectl rollout undo deployment/frontend --to-revision=2
```

## Recreate Strategy

Terminates all old pods before starting new ones. Causes downtime - only use when you cannot run two versions simultaneously.

```yaml
spec:
  strategy:
    type: Recreate
```

## Pausing and Resuming Rollouts

Pause a rollout to batch multiple changes before applying:

```bash
kubectl rollout pause deployment/frontend
# make multiple changes...
kubectl rollout resume deployment/frontend
```

## Updating Images Imperatively

```bash
# Set image for a specific container
kubectl set image deployment/frontend app=nginx:1.26

# Verify
kubectl rollout status deployment/frontend
```

## Common Deployment Commands

```bash
# Watch pods during update
kubectl get pods -w

# Force a restart (without changing config)
kubectl rollout restart deployment/frontend

# Delete the deployment (pods are also deleted)
kubectl delete deployment frontend

# Scale to zero (stops all pods, keeps deployment config)
kubectl scale deployment frontend --replicas=0
```

## StatefulSet vs Deployment

| Feature | Deployment | StatefulSet |
|---------|------------|-------------|
| Pod identity | Interchangeable | Stable, ordered (pod-0, pod-1...) |
| Storage | Shared or none | Per-pod persistent storage |
| Updates | Rolling (random order) | Rolling (ordered) |
| Use case | Stateless apps | Databases, queues, clusters |

## DaemonSet

Runs one pod on every node (or a subset). Used for node-level agents.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      app: log-collector
  template:
    metadata:
      labels:
        app: log-collector
    spec:
      containers:
        - name: fluentd
          image: fluentd:v1.16
```

Common uses: log shippers (Fluentd, Filebeat), monitoring agents (Datadog, Prometheus node exporter), network plugins.
