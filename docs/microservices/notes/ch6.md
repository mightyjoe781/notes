## Delivering Microservices

#### Automated Deployments

In a monolith, deployments are often a manual process. But microservices are deployed frequently and independently across many services — manual deployments don't scale.

Microservices require **automated deployments** that are:

- Reliable and repeatable
- Triggered by every commit (Continuous Integration)
- Structured as a release pipeline

Example pipeline:

```
Build → Unit Tests → Deploy to Dev → Service Tests → Deploy to QA → End-to-End Tests → Release Gate → Deploy to Production
```

#### Deployment Environments

| Environment | Purpose |
|---|---|
| **Development** | Debug code locally |
| **QA / Staging** | End-to-end tests, manual testing, performance testing, pen testing |
| **Production** | Per-customer, per-region deployments |

**Parameterize your deployments**: use JSON or YAML config files to capture what differs between environments (connection strings, feature flags, replica counts).

For cloud infrastructure, use **Infrastructure as Code (IaC)**:

- **Terraform**: Cloud-agnostic, widely used for multi-cloud setups
- **AWS CloudFormation** / **Azure Bicep**: Cloud-native options (note: Azure ARM Templates have largely been superseded by [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview))

Use a base template with environment-specific overrides.

#### Artifact Registries

- Store build artifacts (Docker images, binaries)
- Deploy the latest version or roll back to a previous one
- **Docker container images**: Push to Docker Hub, AWS ECR, Azure Container Registry, or GitHub Container Registry
- **Deploy to Kubernetes**: Declare desired state via YAML manifests (`Deployment`, `Service`, `Ingress`) and let Kubernetes reconcile

#### Independent Upgrades

*Upgrading one microservice should not require other microservices to be upgraded simultaneously.*

Upgrade strategies:

| Strategy | How it works | Downtime |
|---|---|---|
| **Stop v1, start v2** | Simple swap | Brief downtime |
| **Blue-green deployment** | Run v1 and v2 simultaneously; switch traffic at the load balancer | Near-zero |
| **Rolling upgrade** | Gradually replace v1 instances with v2 (native to Kubernetes) | Zero |
| **Canary release** | Route a small percentage of traffic to v2 first; gradually increase | Zero |

#### Monitoring Microservices

**Host Metrics**:
- CPU usage
- Memory usage
- Disk I/O
- Configure alerts for thresholds

**Application Metrics**:
- HTTP request rate and latency
- Error rates (4xx, 5xx)
- Queue length (scale-out trigger or DDoS signal)
- Dead-letter queue size
- Health check status

**Logs**:
- Aggregate logs from all services into a central store
- Standardize log format (e.g., structured JSON)
- Use **correlation IDs** to trace a single request across multiple services
- Tools: ELK Stack (Elasticsearch + Logstash + Kibana), Grafana + Loki, Datadog, Azure Monitor / Application Insights

**Distributed Tracing**:
- Tools like [OpenTelemetry](https://opentelemetry.io/), Jaeger, or Zipkin provide end-to-end request traces across services — essential for diagnosing latency in complex call chains

*Take advantage of the built-in monitoring and observability capabilities of your microservices hosting platform.*

---

### Recommended Reading

- *Building Microservices* by Sam Newman (O'Reilly) — the definitive reference
- *Designing Distributed Systems* by Brendan Burns (O'Reilly)
- *Release It!* by Michael T. Nygard — resilience patterns for production systems
