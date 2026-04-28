# Services

## The Problem Services Solve

Pods are ephemeral - they come and go, and their IPs change on restart. A Service provides a **stable network endpoint** for a group of pods selected by label.

```
Client --> Service (stable IP) --> Pod A
                               --> Pod B
                               --> Pod C
```

## Service Types

### ClusterIP (default)

Exposes the service on an internal IP. Reachable only from within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: ClusterIP         # default; can be omitted
  selector:
    app: backend
  ports:
    - port: 80            # port clients use to reach the service
      targetPort: 8080    # port the container listens on
```

### NodePort

Opens a port (30000-32767) on every node. Traffic to `<NodeIP>:<nodePort>` reaches the service.

Useful for local development or when you control the network layer.

```yaml
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 31515     # omit to auto-assign a port
```

```bash
# On minikube with qemu/virtualbox driver
minikube ip
curl $(minikube ip):31515

# On minikube with Docker driver - use tunnel or port-forward
minikube tunnel
kubectl port-forward svc/frontend 3000:80
```

### LoadBalancer

Provisions an external load balancer through the cloud provider. Also creates a ClusterIP and NodePort internally.

```yaml
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 3000
```

On minikube, run `minikube tunnel` in a separate terminal to get an external IP assigned.

### ExternalName

Maps a service to an external DNS name. Useful for accessing external databases or third-party services.

```yaml
spec:
  type: ExternalName
  externalName: my-database.example.com
```

## Service Discovery

Kubernetes gives pods two ways to find services.

### DNS (recommended)

Every service gets a DNS record automatically. Pods can reach services by name:

```
# Same namespace
http://backend

# Different namespace
http://backend.staging

# Fully qualified
http://backend.staging.svc.cluster.local
```

### Environment Variables

When a pod starts, Kubernetes injects environment variables for every service in the same namespace that existed before the pod was created.

```
DATA_TIER_SERVICE_HOST=10.96.14.5
DATA_TIER_SERVICE_PORT=6379
DATA_TIER_SERVICE_PORT_REDIS=6379
```

Pattern: `<SERVICE_NAME_UPPERCASE>_SERVICE_HOST` and `<SERVICE_NAME_UPPERCASE>_SERVICE_PORT`

> Services must be created before the pods that reference them via environment variables. DNS does not have this ordering constraint.

```yaml
env:
  - name: REDIS_URL
    value: redis://$(DATA_TIER_SERVICE_HOST):$(DATA_TIER_SERVICE_PORT_REDIS)
```

## Practical Examples

```bash
# Create a service from CLI
kubectl expose deployment frontend --type=NodePort --port=80 --target-port=3000

# Get service details
kubectl get svc
kubectl describe svc backend

# Get the NodePort assigned
kubectl get svc backend -o jsonpath='{.spec.ports[0].nodePort}'

# Delete
kubectl delete svc backend
```

## Headless Services

Setting `clusterIP: None` creates a headless service. DNS returns pod IPs directly instead of a virtual IP. Used with StatefulSets for direct pod addressing.

```yaml
spec:
  clusterIP: None
  selector:
    app: db
  ports:
    - port: 5432
```

## Summary

| Type | Reachable From | Use Case |
|------|---------------|---------|
| ClusterIP | Inside cluster only | Service-to-service communication |
| NodePort | External via node IP | Local dev, simple external access |
| LoadBalancer | External via cloud LB | Production external traffic |
| ExternalName | Inside cluster | Proxy to external DNS |
