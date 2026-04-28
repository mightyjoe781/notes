# Kubernetes

[Kubernetes](https://kubernetes.io/docs/concepts/overview/) (K8s) is an open-source system for automating deployment, scaling, and management of containerized applications.

## Table of Contents

| Topic | Description |
|-------|-------------|
| [Overview](overview.md) | Architecture, control plane, kubectl basics |
| [Setup](setup.md) | minikube, Docker Desktop, managed clusters |
| [Pods](pods.md) | Pod spec, labels, resource limits, namespaces |
| [Services](services.md) | ClusterIP, NodePort, LoadBalancer, service discovery |
| [Deployments](deployments.md) | Replica sets, rolling updates, rollbacks |
| [Scaling](scaling.md) | Horizontal Pod Autoscaler, metrics server |
| [Health Checks](health_checks.md) | Liveness, readiness, startup probes, init containers |
| [Storage](storage.md) | Volumes, Persistent Volumes, PVCs, storage classes |
| [Config and Secrets](config.md) | ConfigMaps, Secrets, environment variables |
| [Networking](networking.md) | Pod networking, DNS, network policies |
| [Multi-Container Patterns](multi_container.md) | Sidecar, ambassador, adapter patterns |
| [RBAC](rbac.md) | Service accounts, roles, cluster role bindings |
| [Helm](helm.md) | Package manager: charts, commands, templates |
| [Ingress](ingress.md) | nginx-ingress, TLS, cert-manager |
| [Production](production.md) | GKE setup, CI/CD, kubectl productivity tips |
| [New Features](new_features.md) | Gateway API, native sidecars, in-place resize |

## Quick Reference

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes

# Resources
kubectl get pods,svc,deployments -n <namespace>
kubectl describe pod <pod-name>
kubectl logs <pod-name> -c <container-name>

# Apply / delete
kubectl apply -f <file-or-dir>
kubectl delete -f <file-or-dir>

# Exec into a pod
kubectl exec -it <pod-name> -- /bin/bash
```

## Resources

- [Official Docs](https://kubernetes.io/docs/home/)
- [K8s API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [CKAD Curriculum](https://github.com/cncf/curriculum)
- [Artifact Hub (Helm charts)](https://artifacthub.io)
