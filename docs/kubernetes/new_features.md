# New Features

Recent Kubernetes releases have brought significant improvements. This page covers the most impactful additions from Kubernetes 1.27 to 1.33.

## Gateway API (Stable since 1.28)

The Gateway API is the next generation of Ingress. It is more expressive, role-oriented, and extensible. It is now the recommended approach for new projects.

**Key differences from Ingress:**

| Feature | Ingress | Gateway API |
|---------|---------|-------------|
| HTTP routing | Basic | Full (headers, query params, weights) |
| Role separation | Single resource | GatewayClass, Gateway, HTTPRoute are split |
| TCP/UDP/gRPC | No | Yes |
| Traffic splitting | No | Yes (for canary deployments) |
| Status reporting | Limited | Rich, per-rule |

### Core Resources

```yaml
# GatewayClass - defines the controller (set up by cluster admin)
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: nginx
spec:
  controllerName: k8s.nginx.org/nginx-gateway-controller

# Gateway - a specific load balancer instance (set up by platform team)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
  namespace: infra
spec:
  gatewayClassName: nginx
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        certificateRefs:
          - name: my-cert

# HTTPRoute - routing rules (owned by app developers)
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
  namespace: production
spec:
  parentRefs:
    - name: my-gateway
      namespace: infra
  hostnames:
    - myapp.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: server-service
          port: 5000
    - backendRefs:
        - name: client-service
          port: 3000
```

### Traffic Splitting (Canary)

```yaml
rules:
  - backendRefs:
      - name: myapp-stable
        port: 80
        weight: 90
      - name: myapp-canary
        port: 80
        weight: 10
```

```bash
# Install Gateway API CRDs
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.1.0/standard-install.yaml
```

## Native Sidecar Containers (Stable in 1.29)

Before 1.29, sidecar containers were regular containers. They had ordering and shutdown problems: they could shut down before the main container flushed logs, or init containers had to be hacked to act as sidecars.

Kubernetes 1.29 added native sidecar support by allowing `initContainers` to set `restartPolicy: Always`. This gives sidecars predictable lifecycle management.

```yaml
spec:
  initContainers:
    - name: log-agent
      image: fluentd:v1.17
      restartPolicy: Always     # this is what makes it a native sidecar
      resources:
        requests:
          cpu: "50m"
          memory: "32Mi"

  containers:
    - name: app
      image: myapp:1.0
```

**Native sidecar guarantees:**
- Starts before the main containers (init container ordering)
- Stays alive while the main container runs
- Shuts down after the main container exits (correct log/proxy drain)
- Supports readiness/liveness/startup probes

## In-Place Pod Resource Resize (Stable in 1.33)

Previously, changing CPU or memory requests/limits on a running pod required restarting it. With in-place resize, you can update resource requests without a restart for many workloads.

```bash
# Resize a running pod's container resources
kubectl patch pod my-pod --subresource=resize --type=merge \
  -p '{"spec":{"containers":[{"name":"app","resources":{"requests":{"cpu":"500m"}}}]}}'

# Check status
kubectl get pod my-pod -o jsonpath='{.status.resize}'
# Possible values: Proposed, InProgress, Deferred, Infeasible
```

```yaml
spec:
  containers:
    - name: app
      image: myapp:1.0
      resources:
        requests:
          cpu: "250m"
          memory: "128Mi"
      resizePolicy:
        - resourceName: cpu
          restartPolicy: NotRequired   # resize CPU without restart
        - resourceName: memory
          restartPolicy: RestartContainer  # memory resize still requires restart
```

This is especially useful for VPA in Auto mode and for avoiding restarts during traffic spikes.

## ValidatingAdmissionPolicy (Stable in 1.30)

Define admission validation rules directly in the cluster using CEL (Common Expression Language) - without deploying a webhook.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: require-labels
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
      - apiGroups: ["apps"]
        apiVersions: ["v1"]
        operations: ["CREATE", "UPDATE"]
        resources: ["deployments"]
  validations:
    - expression: "object.metadata.labels.app != ''"
      message: "Deployments must have an 'app' label"
    - expression: "object.spec.replicas <= 10"
      message: "Replicas cannot exceed 10"
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: require-labels-binding
spec:
  policyName: require-labels
  validationActions: [Deny]
  matchResources:
    namespaceSelector:
      matchLabels:
        enforce-policy: "true"
```

Benefits over webhooks: no extra deployment to maintain, lower latency, no TLS setup required.

## Job Success and Failure Policy (Stable in 1.31)

Fine-grained control over when a Job is considered succeeded or failed, even if some pods fail.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ml-training
spec:
  completions: 10
  parallelism: 5
  successPolicy:
    rules:
      - succeededCount: 1        # job succeeds once any 1 pod completes successfully
  backoffLimitPerIndex: 1        # allow 1 retry per completion index
  podFailurePolicy:
    rules:
      - action: FailJob
        onExitCodes:
          operator: In
          values: [42]           # exit code 42 = permanent failure, no retry
      - action: Ignore
        onExitCodes:
          operator: In
          values: [1]            # exit code 1 = transient error, ignore
```

## Structured Parameters for Dynamic Resource Allocation (Beta in 1.30)

Dynamic Resource Allocation (DRA) is the new model for requesting hardware resources like GPUs, FPGAs, and network adapters. It replaces the older device plugin model with a richer, more flexible API.

```yaml
apiVersion: resource.k8s.io/v1alpha3
kind: ResourceClaim
metadata:
  name: my-gpu
spec:
  devices:
    requests:
      - name: gpu
        deviceClassName: nvidia-gpu.example.com
```

## VolumeAttributesClass (Beta in 1.31)

Allows modifying volume attributes (like IOPS and throughput) on a provisioned PVC without recreating it.

```yaml
apiVersion: storage.k8s.io/v1beta1
kind: VolumeAttributesClass
metadata:
  name: high-iops
driverName: ebs.csi.aws.com
parameters:
  iops: "10000"
  throughput: "500"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  volumeAttributesClassName: high-iops
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 100Gi
```

## Node Log Querying (Beta in 1.27)

Query logs from node-level services (kubelet, containerd) directly via the Kubernetes API without SSH.

```bash
# View kubelet logs on a node
kubectl get --raw "/api/v1/nodes/<node-name>/proxy/logs/kubelet"

# Query with pattern matching
kubectl get --raw "/api/v1/nodes/<node-name>/proxy/logs/?query=error"
```

## Leases and Leader Election Improvements

The Lease API (used for node heartbeats and leader election) received performance improvements in 1.27-1.30. Large clusters see significantly reduced API server load.

## Summary Table

| Feature | Stable in | What it Enables |
|---------|-----------|----------------|
| Gateway API | 1.28 | Next-gen Ingress with advanced routing |
| Native sidecar containers | 1.29 | Proper sidecar lifecycle management |
| In-place pod resize | 1.33 | Change CPU/memory without pod restart |
| ValidatingAdmissionPolicy | 1.30 | CEL-based admission control without webhooks |
| Job success/failure policy | 1.31 | Fine-grained Job completion control |
| VolumeAttributesClass | 1.31 (beta) | Modify volume attributes on live PVCs |
| Node log querying | 1.27 (beta) | Query node logs via API |

For the full changelog: [kubernetes.io/releases](https://kubernetes.io/releases/)
