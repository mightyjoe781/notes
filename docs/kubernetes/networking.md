# Networking

## Pod Networking Basics

Every pod gets a unique IP address. All containers within a pod share that IP and communicate via `localhost`. Pods on different nodes can communicate directly - no NAT required.

This is enforced by the **CNI (Container Network Interface)** plugin installed in the cluster. Common CNI plugins:

| Plugin | Notes |
|--------|-------|
| Calico | Supports NetworkPolicy; commonly used in production |
| Flannel | Simple overlay network; no NetworkPolicy support |
| Cilium | eBPF-based; high performance; advanced network policy |
| Canal | Flannel for routing + Calico for NetworkPolicy |
| AWS VPC CNI | Native AWS VPC IPs per pod (EKS default) |

## DNS in Kubernetes

Every cluster runs a DNS server (CoreDNS). Pods are automatically configured to use it.

### Service DNS Records

A Service named `backend` in namespace `staging` gets:

```
backend.staging.svc.cluster.local
```

Pods in the same namespace can use just `backend`. Cross-namespace requires the namespace: `backend.staging`.

### Pod DNS Records

Pods get DNS records of the form:

```
<pod-ip-dashes>.<namespace>.pod.cluster.local
# e.g. 10-244-0-5.default.pod.cluster.local
```

This is rarely used directly. Named pods in a StatefulSet get stable, predictable names.

## Network Policies

By default all pods can communicate with each other. NetworkPolicy lets you restrict this.

> NetworkPolicy requires a CNI plugin that supports it (Calico, Cilium, Canal). Flannel alone does not.

### Default: deny all ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: production
spec:
  podSelector: {}      # matches all pods in the namespace
  policyTypes:
    - Ingress
  # no ingress rules = deny all ingress
```

### Allow specific traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
        - namespaceSelector:
            matchLabels:
              env: production
      ports:
        - protocol: TCP
          port: 8080
```

### Egress restriction

Block all outbound except DNS and a specific IP range:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-egress
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - ports:
        - port: 53           # allow DNS
          protocol: UDP
    - to:
        - ipBlock:
            cidr: 10.0.0.0/8
```

### Block a specific IP

```yaml
egress:
  - to:
      - ipBlock:
          cidr: 0.0.0.0/0
          except:
            - 192.168.1.100/32
```

## Selectors in NetworkPolicy

| Selector | Matches |
|----------|---------|
| `podSelector` | Pods with matching labels in same namespace |
| `namespaceSelector` | All pods in namespaces with matching labels |
| `ipBlock` | External IP ranges (CIDR) |

Combining `podSelector` and `namespaceSelector` in the same `from` entry uses AND logic. Putting them as separate entries uses OR logic.

```yaml
# AND: pod must match both conditions
- from:
    - podSelector:
        matchLabels:
          app: frontend
      namespaceSelector:
        matchLabels:
          env: production

# OR: pod matches either condition
- from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          env: production
```

## Debugging Network Issues

```bash
# Test DNS resolution from inside a pod
kubectl run -it --rm debug --image=busybox:1.36 --restart=Never -- nslookup backend

# Test connectivity
kubectl run -it --rm debug --image=busybox:1.36 --restart=Never -- wget -qO- http://backend:80

# Check endpoints (is the service selecting pods?)
kubectl get endpoints backend

# Describe network policy
kubectl describe networkpolicy allow-frontend-to-backend
```
