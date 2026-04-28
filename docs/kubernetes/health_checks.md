# Health Checks

Kubernetes uses probes to detect and recover from failures automatically.

## Probe Types

| Probe | Purpose | Action on Failure |
|-------|---------|------------------|
| Liveness | Is the container alive? | Restart the container |
| Readiness | Is the container ready to serve traffic? | Remove from Service endpoints |
| Startup | Has the container finished starting? | Restart the container (disables liveness/readiness until it passes) |

## Probe Actions

Each probe uses one of three mechanisms:

```yaml
# HTTP GET - success if status code is 2xx or 3xx
httpGet:
  path: /healthz
  port: 8080

# TCP Socket - success if port accepts a connection
tcpSocket:
  port: 6379

# Exec - success if command exits with code 0
exec:
  command:
    - redis-cli
    - ping
```

## Probe Configuration Fields

```yaml
initialDelaySeconds: 10    # wait before first probe (give app time to start)
periodSeconds: 10          # how often to probe
timeoutSeconds: 5          # probe times out after this
successThreshold: 1        # consecutive successes to mark healthy (1 for liveness/startup)
failureThreshold: 3        # consecutive failures before action is taken
```

## Example: Web Application

```yaml
spec:
  containers:
    - name: app
      image: myapp:1.0
      ports:
        - containerPort: 8080
          name: http

      startupProbe:
        httpGet:
          path: /healthz
          port: http
        initialDelaySeconds: 0
        periodSeconds: 5
        failureThreshold: 30      # allow up to 2.5 min (30 * 5s) to start

      livenessProbe:
        httpGet:
          path: /healthz
          port: http
        initialDelaySeconds: 0
        periodSeconds: 10
        failureThreshold: 3

      readinessProbe:
        httpGet:
          path: /ready
          port: http
        initialDelaySeconds: 0
        periodSeconds: 5
        failureThreshold: 3
```

> Set `initialDelaySeconds` on startup probes to 0 and use `failureThreshold * periodSeconds` to give the app enough time to boot. This is cleaner than a long `initialDelaySeconds` on liveness probes.

## Example: Redis

```yaml
livenessProbe:
  tcpSocket:
    port: 6379
  initialDelaySeconds: 15
  periodSeconds: 20

readinessProbe:
  exec:
    command:
      - redis-cli
      - ping
  initialDelaySeconds: 5
  periodSeconds: 10
```

## When to Use Each Probe

**Liveness** - when your app can get into a broken state that it cannot recover from on its own (e.g., deadlock, corrupted in-memory state). Only add liveness if you know the failure mode.

**Readiness** - almost always. Prevents traffic from hitting pods that are still warming up or temporarily unavailable (e.g., waiting for a downstream service).

**Startup** - when your app has a long initialization phase. Protects it from being killed by the liveness probe during startup.

## Init Containers

Init containers run to completion before the main containers start. Each init container must succeed before the next one begins.

Use cases:
- Wait for a dependency (database, cache) to be ready
- Fetch configuration or secrets from an external source
- Run database migrations before the app starts

```yaml
spec:
  initContainers:
    - name: wait-for-redis
      image: busybox:1.36
      command:
        - sh
        - -c
        - until nc -z redis 6379; do echo waiting for redis; sleep 2; done

    - name: run-migrations
      image: myapp:1.0
      command: ["python", "manage.py", "migrate"]
      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url

  containers:
    - name: app
      image: myapp:1.0
```

### Init Container Properties

- Run in order; a failure stops the sequence and restarts that init container
- No readiness probes (they run to completion)
- Have their own image - keep them lightweight (busybox, alpine)
- Share volumes with main containers but not the network (before main containers start)
- Re-run every time the pod restarts

```bash
# Check init container logs
kubectl logs <pod-name> -c wait-for-redis

# Check pod events to see init container status
kubectl describe pod <pod-name>
```
