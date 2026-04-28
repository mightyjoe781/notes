# Config and Secrets

## Why Separate Config from Code?

Embedding configuration in your container image makes it harder to reuse the same image across environments. ConfigMaps and Secrets let you inject configuration at runtime.

| Object | For |
|--------|-----|
| ConfigMap | Non-sensitive configuration: app settings, config files, feature flags |
| Secret | Sensitive data: passwords, API keys, TLS certificates |

Both store data as key-value pairs and can be consumed as environment variables or mounted as files.

## ConfigMaps

### Create

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  redis.conf: |
    tcp-keepalive 240
    maxmemory 128mb
    maxmemory-policy allkeys-lru
```

```bash
# From literal values
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=info \
  --from-literal=MAX_CONNECTIONS=100

# From a file
kubectl create configmap redis-config --from-file=redis.conf

# From a directory (one key per file)
kubectl create configmap app-config --from-file=./config-dir/

kubectl get configmap app-config -o yaml
```

### Use as Environment Variables

```yaml
spec:
  containers:
    - name: app
      env:
        # Single key
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL

      # All keys from a ConfigMap as env vars
      envFrom:
        - configMapRef:
            name: app-config
```

### Mount as a File

```yaml
spec:
  volumes:
    - name: redis-config-vol
      configMap:
        name: redis-config
        items:
          - key: redis.conf
            path: redis.conf
  containers:
    - name: redis
      image: redis:7
      command: ["redis-server", "/etc/redis/redis.conf"]
      volumeMounts:
        - name: redis-config-vol
          mountPath: /etc/redis
```

## Secrets

Secrets are like ConfigMaps but base64-encoded and treated with extra care (audit logs, RBAC, encryption at rest).

> Base64 is not encryption. Treat Secrets as sensitive and restrict access with RBAC.

### Create

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
stringData:              # plain text; K8s will base64-encode it
  username: admin
  password: s3cr3t!
```

```bash
# From literal values
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=s3cr3t!

# For TLS
kubectl create secret tls my-tls \
  --cert=tls.crt \
  --key=tls.key

# For Docker registry auth
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass

kubectl get secret db-secret -o yaml
kubectl describe secret db-secret     # values are redacted
```

### Use as Environment Variables

```yaml
spec:
  containers:
    - name: app
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
```

### Mount as Files

```yaml
spec:
  volumes:
    - name: secret-vol
      secret:
        secretName: db-secret
  containers:
    - name: app
      volumeMounts:
        - name: secret-vol
          mountPath: /etc/secrets
          readOnly: true
```

Files are mounted at `/etc/secrets/username` and `/etc/secrets/password`.

## Best Practices

- Store secrets in a secret manager (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager) and sync to K8s using an operator like [External Secrets Operator](https://external-secrets.io) or the [Secrets Store CSI driver](https://secrets-store-csi-driver.sigs.k8s.io).
- Enable [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for etcd so secrets are not stored in plaintext.
- Use RBAC to restrict which service accounts can read which secrets.
- Avoid putting secrets in environment variables if possible - prefer volume mounts so they do not appear in process listings.
- Never commit `Secret` manifests with real values to source control.

## Immutable ConfigMaps and Secrets

Once created, immutable objects cannot be updated - they must be recreated. This prevents accidental changes and improves performance at scale (no watches needed).

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-v2
immutable: true
data:
  LOG_LEVEL: "info"
```
