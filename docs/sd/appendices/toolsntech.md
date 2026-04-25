# Tools & Technology

*Reference for development tools and cloud services used in distributed systems.*

---

## Development Tools

### Diagramming

**General purpose:**

- [Draw.io / Diagrams.net](https://diagrams.net) - free, web or desktop, good for most diagrams
- [Lucidchart](https://lucidchart.com) - web-based, real-time collaboration
- [Miro](https://miro.com) - whiteboard-style, good for workshops
- [Figma](https://figma.com) - design-focused, useful for UI/flow diagrams
- [Visio](https://microsoft.com/visio) - desktop/web, integrates with Office 365
- [Creately](https://creately.com) - web-based with templates

**Architecture-focused:**

- [PlantUML](https://plantuml.com) - code-based, version-controllable diagrams
- [Structurizr](https://structurizr.com) - C4 model diagrams as code
- [Cloudcraft](https://cloudcraft.co) - AWS-specific architecture diagrams
- [CloudSkew](https://cloudskew.com) - multi-cloud architecture, free

**Diagram types to know:**

- High-level architecture - overall system structure
- Component diagrams - service interactions
- Sequence diagrams - request flow and timing
- Deployment diagrams - infrastructure layout
- Data flow diagrams - information movement
- Database schema - data structure and relationships

---

### Performance Testing

**Load testing tools:**

- [Apache JMeter](https://jmeter.apache.org) - open source, HTTP/TCP/JDBC, GUI-based
- [k6](https://k6.io) - open source, JavaScript scripting, CI/CD friendly
- [Gatling](https://gatling.io) - open source, Scala/Java, excellent reporting
- [Artillery](https://artillery.io) - open source, YAML/JS config, lightweight
- [BlazeMeter](https://blazemeter.com) - SaaS, JMeter-compatible, cloud-scale runs
- [LoadRunner](https://microfocus.com/loadrunner) - commercial, enterprise-grade

**Specialized tools by use case:**

- API testing - Postman, k6, Insomnia
- Database performance - HammerDB, sysbench
- Network testing - iperf3, netperf
- Frontend performance - Lighthouse, WebPageTest
- Infrastructure - Prometheus, Grafana

**Testing categories:**

- Load testing - normal expected load
- Stress testing - beyond normal capacity
- Spike testing - sudden traffic increases
- Volume testing - large amounts of data
- Endurance testing - extended time periods
- Chaos testing - system resilience under failures

---

### Monitoring & Observability

**Application Performance Monitoring (APM):**

- [Datadog](https://datadoghq.com) - infrastructure + APM, 20+ languages
- [New Relic](https://newrelic.com) - full-stack APM, 15+ languages
- [Dynatrace](https://dynatrace.com) - AI-powered APM, SaaS/on-prem
- [AppDynamics](https://appdynamics.com) - enterprise APM, Java/.NET/Node focus
- [Elastic APM](https://elastic.co/apm) - open source, integrates with ELK stack
- [Jaeger](https://jaegertracing.io) - open source distributed tracing

**Infrastructure monitoring:**

- [Prometheus](https://prometheus.io) - metrics collection (pull-based), pairs with Grafana
- [Grafana](https://grafana.com) - visualization layer, multiple data sources
- [Nagios](https://nagios.org) - agent-based infrastructure checks
- [Zabbix](https://zabbix.com) - agent or agentless, high scalability

**Log management:**

- [ELK Stack](https://elastic.co/elk-stack) - Elasticsearch + Logstash + Kibana
- [Splunk](https://splunk.com) - commercial, powerful search and analytics
- [Graylog](https://graylog.org) - open source, structured log management
- [Fluentd](https://fluentd.org) - log collection and forwarding

**Common monitoring stacks:**

- TICK - Telegraf + InfluxDB + Chronograf + Kapacitor
- ELK - Elasticsearch + Logstash + Kibana
- Prometheus stack - Prometheus + Grafana + Alertmanager
- Commercial - Datadog + New Relic + PagerDuty

**Monitoring layers:**

- Infrastructure - CPU, memory, disk, network
- Application - response time, error rate, throughput
- Business - user actions, revenue, conversions
- User experience - page load, interactions
- Security - failed logins, anomalous activity

---

## Cloud Services

### AWS / GCP / Azure Service Mappings

#### Compute

| Category         | AWS          | Google Cloud    | Azure            |
| ---------------- | ------------ | --------------- | ---------------- |
| Virtual Machines | EC2          | Compute Engine  | Virtual Machines |
| Containers       | ECS / EKS    | GKE             | AKS              |
| Serverless       | Lambda       | Cloud Functions | Azure Functions  |
| Batch Processing | Batch        | Cloud Dataflow  | Batch            |
| Auto Scaling     | Auto Scaling | Autoscaler      | VM Scale Sets    |

#### Storage

| Category        | AWS        | Google Cloud    | Azure           |
| --------------- | ---------- | --------------- | --------------- |
| Object Storage  | S3         | Cloud Storage   | Blob Storage    |
| Block Storage   | EBS        | Persistent Disk | Managed Disks   |
| File Storage    | EFS        | Filestore       | Files           |
| Archive Storage | Glacier    | Archive Storage | Archive Storage |
| CDN             | CloudFront | Cloud CDN       | CDN             |

#### Databases

| Category        | AWS         | Google Cloud | Azure           |
| --------------- | ----------- | ------------ | --------------- |
| Relational      | RDS         | Cloud SQL    | SQL Database    |
| NoSQL Document  | DocumentDB  | Firestore    | Cosmos DB       |
| NoSQL Key-Value | DynamoDB    | Firestore    | Cosmos DB       |
| Data Warehouse  | Redshift    | BigQuery     | Synapse         |
| Cache           | ElastiCache | Memorystore  | Cache for Redis |
| Graph           | Neptune     | -            | Cosmos DB       |

#### Networking

| Category        | AWS         | Google Cloud  | Azure           |
| --------------- | ----------- | ------------- | --------------- |
| Virtual Network | VPC         | VPC           | Virtual Network |
| Load Balancer   | ALB / NLB   | Load Balancer | Load Balancer   |
| DNS             | Route 53    | Cloud DNS     | DNS             |
| API Gateway     | API Gateway | API Gateway   | API Management  |
| VPN             | VPN Gateway | VPN           | VPN Gateway     |

#### Messaging

| Category      | AWS         | Google Cloud | Azure       |
| ------------- | ----------- | ------------ | ----------- |
| Message Queue | SQS         | Cloud Tasks  | Service Bus |
| Pub/Sub       | SNS         | Pub/Sub      | Event Grid  |
| Streaming     | Kinesis     | Dataflow     | Event Hubs  |
| Event Bus     | EventBridge | Eventarc     | Event Grid  |

#### DevOps & Management

| Category  | AWS             | Google Cloud   | Azure            |
| --------- | --------------- | -------------- | ---------------- |
| CI/CD     | CodePipeline    | Cloud Build    | DevOps           |
| Monitoring| CloudWatch      | Monitoring     | Monitor          |
| Logging   | CloudTrail      | Logging        | Log Analytics    |
| Secrets   | Secrets Manager | Secret Manager | Key Vault        |
| Identity  | IAM             | IAM            | Active Directory |

---

### Managed vs. Self-Managed

**Managed services are better when:**

- Team is small (< 10 engineers) or ops experience is limited
- Time to market matters more than unit cost
- Scale is variable or moderate
- Standard compliance requirements apply
- OpEx budget model is preferred

**Self-managed is better when:**

- Team has strong ops capability
- Scale is massive and predictable (unit cost dominates)
- Extensive customization is required
- Custom compliance or data residency constraints exist
- CapEx budget model is used

**Decision factors:**

| Factor        | Managed                    | Self-Managed                   |
| ------------- | -------------------------- | ------------------------------ |
| Team size     | < 10 engineers             | > 20 engineers                 |
| Expertise     | Limited ops experience     | Strong ops team                |
| Customization | Standard features enough   | Extensive customization needed |
| Scale         | Variable or moderate       | Massive, predictable           |
| Control       | Convenience over control   | Full control needed            |

**Service migration path:**

1. Lift-and-shift - VMs to cloud VMs
2. Re-platform - adopt managed databases and queues
3. Re-architect - microservices and serverless
4. Rebuild - cloud-native applications
5. Replace - SaaS where applicable
