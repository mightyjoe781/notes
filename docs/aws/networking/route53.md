# Route 53

## DNS Fundamentals

### What is DNS ?

- Domain Name System which translates the human friendly hostnames into machine IP addresses
- E.g. `sudomoon.com -> 1.2.3.4`
- DNS uses hierarchical naming structure

### DNS Terminologies

- Domain Registrar : Amazon Route 53, Namecheap, Cloudflare
- DNS Records : A, AAAA, CNAME, NS, ...
- Zone File: contains DNS records
- Name Server: resolves DNS queries (Authoritative & Non-Authoritative)
- Top Level Domain (TLD): `.com`, `.us`, `.in`, ...
- Second Level Domain (SLD): `amazon.com`, `sudomoon.com`

![](assets/Pasted%20image%2020251029213143.png)

### How DNS Works

![](assets/Pasted%20image%2020251029215006.png)

## Amazon Route 53

![](assets/Pasted%20image%2020251029215104.png)

- A highly available, scalable, fully managed and Authoritative DNS
    - Authoritative = the customer (you) can update the DNS records
- Route 53 is also a Domain Registrar
- Ability to check the health of your resources
- The only AWS service which provides 100% availability SLA
- Why Route 53? 53 is a reference to the traditional DNS port

### Route 53 - Records

- How you want to route traffic for a domain
- Each Record Contains
    - Domain/subdomain Name - e.g. example.com
    - Record Type - A or AAAA, CNAME
    - Value - eg 1.2.3.4
    - Routing Policy
    - TTL - amount of time the record cached at DNS Resolvers
- Route 53 supports following DNS record types:
    - (must know) A / AAAA / CNAME / NS
    - (advanced) CAA / DS / MX / NAPTR / PTR / SOA / TXT / SPF / SRV

### Record Types

- A - maps a hostname to IPv4
- AAAA - maps a hostname to IPv6
- CNAME - maps a hostname to another hostname
    - NOTE: Target is a domain which must have A or AAAA record
- NS - Name servers for the Hosted Zone
    - control how traffic is routed for a domain

### Route 53 - Hosted Zones

- A container for records that define how to route traffic to a domain and its subdomains
- *Public Hosted Zones* - contains records that specify how to route traffic on the internet (public domain name)
- *Private Hosted Zones* - contain records that specify how you route traffic within one or more VPCs (private domain name)
- You pay $0.50 per month per hosted zone

![](assets/Pasted%20image%2020251029233409.png)

### Route 53 - Records TTL (Time to Live)

![](assets/Pasted%20image%2020251029233450.png)

- Except for Alias records, TTL is mandatory for each DNS record

### CNAME vs Alias

- AWS Resources (Load Balancer, CloudFront) expose an AWS hostname
    - `lb1-1234.us-east-2.elb.amazonaws.com` and you want `myapp.mydomain.com`
- CNAME :
    - points a hostname to any other hostname
    - ONLY for NON-ROOT DOMAIN
- Alias :
    - points to hostname to an AWS Resource
    - WORKS for ROOT DOMAIN and NON ROOT DOMAIN
    - free of charge
    - Native health check

### Route 53 - Alias Record

![](assets/Pasted%20image%2020251029233849.png)

- Maps a hostname to an AWS resource
- An extension to DNS functionality
- Automatically recognizes changes in the resource’s IP addresses
- Unlike CNAME, it can be used for the top node of a DNS namespace (Zone Apex), e.g.: example.com
- Alias Record is always of type A/AAAA for AWS resources (IPv4 / IPv6)
- TTL can't be set

#### Alias Record Targets

- Elastic Load Balancers
- CloudFront Distributions
- API Gateway
- Elastic Beanstalk environments
- S3 Websites
- VPC Interface Endpoints
- Global Accelerator accelerator
- Route 53 record in the same hosted zone

### Route 53 - Routing Policies

- Define how Route 53 responds to DNS queries
- Don’t get confused by the word “Routing”
- Route 53 Supports the following Routing Policies
    - Simple
    - Weighted
    - Failover
    - Latency Based
    - Geolocation
    - Multi-Value Answer
    - Geoproximity (using Route53 Traffic Flow feature)

## Health Checks

- HTTP Health Checks are only for public resources
- Health Check -> Automated DNS Failover
    - Endpoint Monitoring
    - Other Health Checks
    - CloudWatch Alarms monitoring
- Health Checks are integrated with CW Metrices

### Monitor an Endpoint

![](assets/Pasted%20image%2020251029234858.png)

- About 15 global health checkers will check the endpoint health
    - Healthy/Unhealthy Threshold ~ 3 (default)
    - Interval ~ 30sec (can set to 10sec - higher cost)
    - Supported Protocol : HTTP, HTTPS and TCP
    - Ability to choose which locations you want Route 53 to use
- Health Checks pass only when the endpoint responds with the 2xx and 3xx status codes
- Health Checks can be setup to pass / fail based on the text in the first 5120 bytes of the response
- Configure you router/firewall to allow incoming requests from Route 53 Health Checkers

### Calculated Health Checks

![](assets/Pasted%20image%2020251029235224.png)

- Combine the results of multiple Health Checks into a single Health Check
- You can use OR, AND, or NOT
- Can monitor up to 256 Child Health Checks
- Specify how many of the health checks need to pass to make the parent pass
- Usage: perform maintenance to your website without causing all health checks to fail

### Health Checks - Private Hosted Zones

![](assets/Pasted%20image%2020251029235313.png)

- Route 53 health checkers are outside the VPC
- They can’t access private endpoints (private VPC or on-premises resource)
- You can create a CloudWatch Metric and associate a CloudWatch Alarm, then create a Health Check that checks the alarm itself 

## Routing Policies

### Simple

- Typically, route traffic to a single resource
- Can specify multiple values in the same record
- If multiple values are returned, a random one is chosen by the client
- When Alias enabled, specify only one AWS resource
- Can’t be associated with Health Checks
### Weighted

- Control the % of the requests that go to each specific resource
- Assign each record a relative weight:

$$
\text{traffic} (\%) = \frac{\text{wt. for specific record}}{\text{sum of all weights for all records}}
$$

- Weights don’t need to sum up to 100
- DNS records must have the same name and type
- Can be associated with Health Checks
- Use cases: load balancing between regions, testing new application versions…
- Assign a weight of 0 to a record to stop sending traffic to a resource
- If all records have weight of 0, then all records will be returned equally
### Latency Based

![](assets/Pasted%20image%2020251030000435.png)

- Redirect to the resource that has the least latency close to us
- Super helpful when latency for users is a priority
- Latency is based on traffic between users and AWS Regions
- Germany users may be directed to the US (if that’s the lowest latency)
- Can be associated with Health Checks (has a failover capability

### Failover (Active-Passive)

![](assets/Pasted%20image%2020251029235446.png)

### Geolocation

- based on user location
- Specify location by Continent, Country or by US State
- Should create *Default* record (in case if no match)
- Use cases : website localization, restrict, content distribution, load balancing
- Health Check can be associated
### Geoproximity (using Route53 Traffic Flow feature)

![](assets/Pasted%20image%2020251030000505.png)

 - Route traffic to your resources based on the geographic location of users and resources
 - Ability to shift more traffic to resources based on the defined bias
 - Resources can be:
     - AWS resources (specify AWS region)
     - Non-AWS resources (specify Latitude and Longitude)
 - You must use Route 53 Traffic Flow to use this feature

### Route 53 - Traffic flow

- Simplify the process of creating and maintaining records in large and complex configurations
- Visual editor to manage complex routing decision trees
- Configurations can be saved as Traffic Flow Policy
    - Can be applied to different Route 53 Hosted Zones (different domain names)
    - Supports versioning

### Routing Policies ~ IP Based Routing

- Routing is based on client's IP address
- You provide a list of CIDR for your clients and corresponding endpoints/locations
- Use Cases : Optimize performance, reduce network costs...

### Routing Policies ~ Multi-Value

- Use when routing traffic to multiple resources
- Route 53 return multiple values/resources
- Can be associated with Health Checks (return only values for healthy resources)
- Up to 8 healthy records are returned for each Multi-Value query
- Multi-Value is not a substitute for having an ELB

## Domain Registrar vs DNS Services

- You can buy domain names from a Domain Registrar typically using annual charges
- The Domain Registrar usually provides you with a DNS Service to manage your DNS records
- But you can use another DNS service to manage your DNS Records
- Example : I bought domains from namecheap and then hosted them on Cloudflare.

## Route 53 Scenarios

Following AWS Resources and their configurations

- EC2 Instance
    - domain points to EC2 instances with public/Elastic IP
    - example.com => 1.2.3.4 (A)
- EC2 DNS Name
    - app.example.com  => c2-12-34-56-78.us-west- 2.compute.amazonaws.com (CNAME)
- ALB
    - domain points to AWS provided ALB DNS Name
    - example.com => my-load-balancer-1234567890.us-west-2.elb.amazonaws.com (Alias)
    - lb.example.com => my-load-balancer-1234567890.us-west-2.elb.amazonaws.com (Alias or CNAME)
- CloudFront Distribution
    - example.com => d2222222abcdef8.cloudfront.net (Alias)
    - cdn.example.com => d2222222abcdef8.cloudfront.net (Alias or CNAME)
- APIGW
    - domain points to API Gateway Regional/Edge Optimized DNS name
    - example.com => b123abcde4.execute-api.us-west-2.amazonaws.com (Alias)
- RDS DB Instance
    - points to RDS DB instance DNS name
    - Must create a CNAME record
    - db.example.com => myexampledb.a1b2c3d4wxyz.us-west-2.rds.amazonaws.com (CNAME)
- S3 Bucket
    - domain name points to S3 website endpoin
    - must create an Alias record for S3 endpoints
    - Bucket name must be the same as domain name
    - example.com => s3-website-us-west-2.amazonaws.com (Alias)
- VPC Endpoint
    - domain points to VPC Interface Endpoint (AWS Private Link)
    - example.com => vpce-1234-abcdev-us-east-1.vpce-svc-123345.us-east-1.vpce.amazonaws.com (Alias)

### Route 53 - Hosted Zones

- Route 53 automatically creates NS and SOA records
- For public/private and private Hosted Zones that have overlapping namespaces, Route 53 Resolvers routes traffic to the most specific match

### Using Route 53 as the DNS Service for a Subdomain without Migrating the Parent Domain

![](assets/Pasted%20image%2020251030001516.png)

## DNS Poisioning (Spoofing)

![](assets/Pasted%20image%2020251030001546.png)

## DNSSEC

- A protocol for securing DNS traffic, verifies DNS data integrity and origin
- Works only with Public Hosted Zones
- Route 53 supports both DNSSEC for Domain Registration and Signing
- DNSSEC Signing
    - Validate that a DNS response came from Route 53 and has not been tampered with
    - Route 53 cryptographically signs each record in the Hosted Zone
    - Two Keys:
        - Managed by you: Key-signing Key (KSK) – based on an asymmetric CMK in AWS KMS
        - Managed by AWS: Zone-signing Key (ZSK)
- When enabled, Route 53 enforces a TTL of one week for all records in the Hosted Zone (records that have TTL less than one week are not affected)

### DNSSEC - Chain of Trust

![](assets/Pasted%20image%2020251030082857.png)

## Hybrid DNS

![](assets/Pasted%20image%2020251030083005.png)

- By default, Route 53 Resolver automatically answers DNS queries for:
    - Local domain names for EC2 instances
    - Records in Private Hosted Zones
    - Records in public Name Servers
- Hybrid DNS – resolving DNS queries between VPC (Route 53 Resolver) and your networks (other DNS Resolvers)
- Networks can be:
    - VPC itself / Peered VPC
    - On-premises Network (connected through Direct Connect or AWS VPN)

## Resolver Endpoints

- Inbound Endpoint
    - DNS Resolvers on your network can forward DNS queries to Route 53 Resolver
    - Allows your DNS Resolvers to resolve domain names for AWS resources (e.g., EC2 instances) and records in Route 53 Private Hosted Zones
- Outbound Endpoint
    - Route 53 Resolver conditionally forwards DNS queries to your DNS Resolvers
    - Use Resolver Rules to forward DNS queries to your DNS Resolvers
- Associated with one or more VPCs in the same AWS Region
- Create in two AZs for high availability
- Each Endpoint supports 10,000 queries per second per IP address

### Resolver Inbound Endpoint

![](assets/Pasted%20image%2020251030083207.png)
### Resolver Outbound Endpoint

![](assets/Pasted%20image%2020251030083225.png)

### Resolver Rules

- Control which DNS queries are forwarded to DNS Resolvers on your network
- Conditional Forwarding Rules (Forwarding Rules)
    - Forward DNS queries for a specified domain and all its subdomains to target IP addresses
- System Rules
    - Selectively overriding the behavior defined in Forwarding Rules (e.g., don’t forward DNS queries for a subdomain acme.example.com)
- Auto-defined System Rules
    - Defines how DNS queries for selected domains are resolved (e.g., AWS internal domain names, Privated Hosted Zones)
- If multiple rules matched, Route 53 Resolver chooses the most specific match
- Resolver Rules can be shared across accounts using AWS RAM
    - Manage them centrally in one account
    - Send DNS queries from multiple VPC to the target IP defined in the rule

### DNS Query Logging

![](assets/Pasted%20image%2020251030083415.png)

- Log information about public DNS queries Route 53 Resolver receives
- Only for Public Hosted Zones
- Can send logs to CloudWatch Logs (can export to S3

### Resolver Query Logging

![](assets/Pasted%20image%2020251030083514.png)

- Logs all DNS queries made by resources within a VPC
    - Private Hosted Zones
    - Resolver Inbound & Outbound Endpoints
    - Resolver DNS Firewall
- Can send logs to CloudWatch Logs, S3 bucket, or Kinesis Data Firehose
- Configurations can be shared with other AWS Accounts using AWS Resource Access Manager (AWS RAM)

### Resolver DNS Firewall

![](assets/Pasted%20image%2020251030083540.png)

- A managed firewall enables you to filter outbound DNS requests going out through Route 53 Resolver from your VPC
- Blacklist malicious domains or Whitelist trusted domains
- This is to prevent a compromised application within your VPC to send data out through DNS (to a malicious domain) – also called DNS exfiltration
- Can be managed/configured from AWS Firewall Manager
- Integrated with CloudWatch Logs and Route 53 Resolver Query Logs
- Fail-close vs Fail-Open (DNS Firewall Configuration):
    - Fail-close: Resolver blocks query if no response from DNS Firewall (security over availability)
    - Fail-open: Resolver allows query if no response from DNS firewall (availability over security) 

## DNS Architectures

### Split-View DNS (Split-Horizon)

- Use the same domain for internal and external uses
- Public and Private hosted zones will have the same name (e.g., example.com)
- Use case: serve different content, require different authentication for internal and external users, …

![](assets/Pasted%20image%2020251030083732.png)

### Multi-Account DNS Management with Route53 Resolver

![](assets/Pasted%20image%2020251030083718.png)