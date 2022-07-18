## Delivering Microservices

#### Automated Deployments

In monoliths usually deployment is manual process, but microservices are deployed frequently and there are bunch of them, so manual process is not feasible.

Microservices requires Automated Deployments : 

- Reliable and repeatable 
- frequent deployments
- Continous Integration
- Release Pipelines : Build -> Unit Tests -> Deploy Microservices -> Service Tests -> Deploy to QA -> End-to-end test -> Release gate -> Deploy to Production

#### Deployment Environments

Development : Debug Code

QA : End-to end test, manual testing, Pen testing, Performance testing

Production : per-customer, per-region

It is helpful to parameterize your deployments. Common way is json/yaml config files which explain whats different about environments.

Cloud Infrastructure Deployment, Terraform or Azure ARM Templates.

Base template + environment-specific override

#### Artifact Registries

- Store Build artificats
- Deploy latest or previous version
- Docker Container Images
- Deploy to Kubernetes : (yaml config files, desired state)

#### Independent Upgrades

*Upgrading one microservice should not require microservices to be upgraded.*

Upgrade Strategies : 

- Stop v1, start v2 : short period of unavailability 
- blue-green swap : run v1 & v2 simultaneously and swap traffic from v1 to v2 using load balancer (minimal downtime).
- rolling upgrade : there are several v1 instances running, removing one by one v1 instances and replacting with v2 (kubernetes is useful).

#### Monitoring Microservices

What should we monitor ?

Host Metrices 

- CPU percentages
- Memory Usage
- Configure alerts

Application Metrices

- HTTP requests
- Errors (401, 500)
- Queue Length (scale out or DDOS)
- Dead-letter queue
- Health checks

Logs

- Aggregated
- Standardize log output 
- Kibana
- Application Insights

*Take advantage of builtin monitoring and observability capabilities of your microservices hosting platform.*

### Recommended Reading : ORILEY’s Building Microservices by Sam Newman