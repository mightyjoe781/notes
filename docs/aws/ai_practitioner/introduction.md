# Introduction to AWS & Public Cloud

### Deployment Model of Cloud

#### Private Cloud

- Cloud Services used by single organization, not exposed to public
- Complete control, secure for sensitive application
- Ex - Rackspace
#### Public Cloud

- Cloud resources are owned by another company, which will be delivered over internet.
- Ex - Azure, AWS, GCP
#### Hybrid Cloud

- Keep some servers on premises & extend some capabilities to Cloud
- Control sensitive data on private infrastructure
- Ex - On-Prem Servers ~ AWS (for S3)

### Five Characteristics of Cloud Computing

- On-Demand Self-Service ~ provision resources with no human intervention
- Broad Network Access ~ available over internet
- Multi-tenancy and resource pooling ~ multiple consumers can share resources
- Rapid Elasticity & Scalability ~ scale based on demand
- Measured Server ~ pay as you go

### Six Advantages of Cloud Computing

- Trade Capital Expense (CAPEX) for Operational Expense (OPEX)
- Benefit from Economies of Scale
- Exact Capacity
- Increase speed & Agility
- Focus on delivering product rather than building Infrastructure
- Go Global in minutes

### Types of Cloud Computing

![](assets/Pasted%20image%2020251008092920.png)

Examples

- IaaS - EC2 (AWS), Azure, Digital Ocean, Racknerd, Linode, ovhcloud, etc.
- PaaS - Beanstalk (AWS), Heroku, Google App Engine, etc.
- SaaS - Many AWS Services (e.g. Rekognition[ML]), Gmail, Dropbox, Zoom
### Pricing of the Cloud

AWS has 3 pricing fundamental, for its pay-as-you-go pricing model

- Compute
    - Pay for compute time
- Storage
    - Pay for data stored in the cloud
- Data transfer OUT of the Cloud
    - Data transfer IN is free

#### AWS Global Infrastructure

- AWS Region, Availability Zone, Data Centers, Edge Locations
- https://infrastructure.aws/

#### Factors while choosing an AWS Region

- Compliance
- Proximity
- Availability of the Service to be Deployed
- Pricing

### AWS Availability Zones

Each Region (geographic) has at least 3 or more Availability Zones. e.g. us-east-1a, us-east-1b, us-east-1c. Here us-east-1 is the region.

All Availability Zones are connected thru a low latency optic fiber with different physical locations (to avoid disaster)

There is a misconception that we should not choose `us-east-1a` and choose other regions just because of the load. But internally `us-east-1a` for you might be `us-east-1b` some other user. AWS decides this based on load and occupancy at the availability zone.

![](assets/Pasted%20image%2020251008094450.png)

![](assets/Pasted%20image%2020251008094508.png)

### Shared Responsibility Model Diagram

*Very Very Important for AWS Exams* ~ helps in critically answer situation based questions

![](assets/Pasted%20image%2020251008094621.png)

https://aws.amazon.com/compliance/shared-responsibility-model/