# RBAC

Role-Based Access Control (RBAC) controls who can do what in a Kubernetes cluster. It is enabled by default since Kubernetes 1.8.

## Core Concepts

| Object | Scope | Purpose |
|--------|-------|---------|
| Role | Namespace | Defines a set of permissions within a namespace |
| ClusterRole | Cluster-wide | Defines permissions across all namespaces (or for cluster-level resources) |
| RoleBinding | Namespace | Grants a Role to a user, group, or service account within a namespace |
| ClusterRoleBinding | Cluster-wide | Grants a ClusterRole to a user, group, or service account across the whole cluster |

## Roles

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: staging
rules:
  - apiGroups: [""]           # "" means the core API group (v1)
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list"]
```

Common verbs: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`

## ClusterRoles

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
  - apiGroups: [""]
    resources: ["nodes", "namespaces"]
    verbs: ["get", "list", "watch"]
```

## RoleBindings

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: staging
subjects:
  - kind: User
    name: alice
    apiGroup: rbac.authorization.k8s.io
  - kind: Group
    name: developers
    apiGroup: rbac.authorization.k8s.io
  - kind: ServiceAccount
    name: my-service-account
    namespace: staging
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## Service Accounts

Service accounts are identities for pods. Every pod runs as a service account (default is `default` in its namespace).

```bash
# List service accounts
kubectl get serviceaccounts
kubectl get sa -n kube-system | head -20

# Create a service account
kubectl create serviceaccount my-app

# Inspect what a service account can do
kubectl auth can-i list pods --as=system:serviceaccount:default:my-app
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
```

### Bind a Role to a Service Account

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-app-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: my-app
    namespace: production
roleRef:
  kind: ClusterRole
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Use a Service Account in a Pod

```yaml
spec:
  serviceAccountName: my-app
  automountServiceAccountToken: false   # disable if pod doesn't need API access
  containers:
    - name: app
      image: myapp:1.0
```

The service account token is automatically mounted at `/var/run/secrets/kubernetes.io/serviceaccount/token`.

## Image Pull Secrets

Use image pull secrets to authenticate with private container registries.

```bash
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=user@example.com
```

Attach to a pod or service account:

```yaml
# In pod spec
spec:
  imagePullSecrets:
    - name: regcred

# Or attach to service account (applies to all pods using that SA)
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
imagePullSecrets:
  - name: regcred
```

## Checking Permissions

```bash
# Can I do this?
kubectl auth can-i create pods
kubectl auth can-i delete deployments -n staging

# Can a service account do this?
kubectl auth can-i list secrets \
  --as=system:serviceaccount:default:my-app

# See effective rules for current user
kubectl auth whoami
```

## Common ClusterRoles Built In

| ClusterRole | Permissions |
|-------------|------------|
| `cluster-admin` | Full access to everything |
| `admin` | Full access within a namespace |
| `edit` | Read/write most resources in a namespace |
| `view` | Read-only access in a namespace |

```bash
kubectl get clusterroles
kubectl describe clusterrole view
```
