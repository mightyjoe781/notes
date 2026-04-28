# Scaling

## Manual Scaling

```bash
kubectl scale deployment frontend --replicas=5
kubectl scale deployment frontend --replicas=0    # pause without deleting
```

## Horizontal Pod Autoscaler (HPA)

HPA automatically adjusts the number of pod replicas based on observed metrics (CPU, memory, or custom metrics).

### Prerequisites

HPA requires the Metrics Server to be running:

```bash
# Check if metrics-server is running
kubectl get deployment metrics-server -n kube-system

# Install via Helm
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server -n kube-system

# On minikube
minikube addons enable metrics-server

# Verify it works
kubectl top pods
kubectl top nodes
```

### HPA Manifest

`autoscaling/v1` was removed in Kubernetes 1.26. Use `autoscaling/v2`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70    # scale up when avg CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: AverageValue
          averageValue: 200Mi
```

> The target deployment must have CPU `requests` set; otherwise HPA cannot calculate utilization.

```bash
# Create HPA imperatively
kubectl autoscale deployment frontend --min=2 --max=10 --cpu-percent=70

# Check HPA status
kubectl get hpa
kubectl describe hpa frontend

# Live watch
watch -n 5 kubectl get hpa
```

### HPA Behavior Tuning

Control how aggressively HPA scales up and down:

```yaml
spec:
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60     # wait 60s before scaling up again
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60              # add at most 2 pods per minute
    scaleDown:
      stabilizationWindowSeconds: 300    # wait 5 min before scaling down
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60             # remove at most 10% of pods per minute
```

## Vertical Pod Autoscaler (VPA)

VPA adjusts the CPU and memory requests/limits of containers based on actual usage. Useful when you do not know the right resource values upfront.

```bash
# Install VPA (not bundled with K8s)
# https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler
```

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: frontend-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  updatePolicy:
    updateMode: "Auto"    # Auto | Recreate | Initial | Off
```

> VPA in `Auto` mode restarts pods to apply new resource values. Running HPA and VPA on the same deployment simultaneously can cause conflicts - if you do, restrict VPA to memory only and HPA to CPU.

## Cluster Autoscaler

Automatically adds or removes nodes from the cluster when pods cannot be scheduled due to resource shortages, or when nodes are underutilized.

Managed clusters (EKS, GKE, AKS) have built-in cluster autoscaler support. On GKE:

```bash
gcloud container clusters update <cluster-name> \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10
```

## Summary

| Tool | Adjusts | Trigger |
|------|---------|---------|
| Manual scale | Pod count | Manual command |
| HPA | Pod count | CPU, memory, custom metrics |
| VPA | Pod resource requests | Actual resource usage over time |
| Cluster Autoscaler | Node count | Unschedulable pods / underused nodes |
