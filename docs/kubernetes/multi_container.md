# Multi-Container Patterns

## Why Multiple Containers in One Pod?

A pod is a logical host for containers that must be co-located. Use multiple containers when:

- Containers need to share localhost networking
- Containers need to share a volume without network overhead
- A helper container enhances the main container without being part of the application image

The three main patterns are sidecar, ambassador, and adapter.

## Sidecar Pattern

A helper container runs alongside the main container and extends its functionality. They share the same pod lifecycle.

Common uses: log shippers, config reloaders, proxy agents, TLS terminators, secret injectors.

**Example: Web server with a content syncer**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-with-sidecar
spec:
  containers:
    - name: web-server
      image: nginx:1.25
      volumeMounts:
        - name: content
          mountPath: /usr/share/nginx/html

    - name: content-syncer
      image: alpine/git:latest
      command:
        - sh
        - -c
        - while true; do git pull; sleep 60; done
      workingDir: /content
      volumeMounts:
        - name: content
          mountPath: /content

  volumes:
    - name: content
      emptyDir: {}
```

The content syncer keeps the web server's files up to date without touching the nginx image.

## Ambassador Pattern

An ambassador container acts as a proxy between the main container and external services. The main container talks to `localhost`; the ambassador handles the complexity of routing.

Common uses: database proxies, service mesh sidecars (Envoy), connection pooling, sharding.

**Example: Database proxy**

```yaml
spec:
  containers:
    - name: app
      image: myapp:1.0
      env:
        - name: DB_HOST
          value: localhost      # talks to ambassador via localhost
        - name: DB_PORT
          value: "5432"

    - name: db-proxy
      image: cloud-sql-proxy:latest
      args:
        - --port=5432
        - project:region:instance
```

The app does not need to know about connection strings, SSL, or cloud auth. The proxy handles all of that.

## Adapter Pattern

An adapter normalizes the output of the main container into a standard format consumed by a third-party system (e.g., a monitoring platform).

Common uses: log format normalization, metrics format translation (converting app metrics to Prometheus format).

**Example: Metrics adapter**

```yaml
spec:
  containers:
    - name: app
      image: legacy-app:1.0
      volumeMounts:
        - name: metrics
          mountPath: /metrics

    - name: metrics-adapter
      image: alpine:3.19
      command:
        - sh
        - -c
        - |
          while true; do
            # Parse legacy format, emit Prometheus format
            awk '{print "app_metric{key=\""$1"\"} "$2}' /metrics/raw.txt > /metrics/prometheus.txt
            sleep 5
          done
      volumeMounts:
        - name: metrics
          mountPath: /metrics

  volumes:
    - name: metrics
      emptyDir: {}
```

## Native Sidecar Containers (Kubernetes 1.29+)

Kubernetes 1.29 introduced **sidecar containers** as a first-class concept using `initContainers` with `restartPolicy: Always`. This solves a long-standing problem: regular sidecar containers would terminate before the main container on pod shutdown, breaking log flushing and network proxies.

```yaml
spec:
  initContainers:
    - name: log-shipper
      image: fluentd:v1.16
      restartPolicy: Always      # marks this as a sidecar, not a one-shot init
      volumeMounts:
        - name: logs
          mountPath: /var/log

  containers:
    - name: app
      image: myapp:1.0
      volumeMounts:
        - name: logs
          mountPath: /var/log

  volumes:
    - name: logs
      emptyDir: {}
```

Native sidecars:
- Start before main containers (like init containers)
- Stay running alongside main containers (like regular sidecars)
- Shut down after main containers exit (unlike regular sidecars)
- Support readiness/liveness probes

See [New Features](new_features.md) for more detail.

## Choosing the Right Pattern

| Pattern | Main Container Knows About | Helper Role |
|---------|---------------------------|-------------|
| Sidecar | Nothing about the helper | Enhances or extends |
| Ambassador | Talks to localhost | Proxies outbound requests |
| Adapter | Nothing about the adapter | Normalizes output |
