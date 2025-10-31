# AWS Elastic Load Balancer (ELB)

Ques : What is Load Balancing ?
Ans : *Load Balancers* are servers that forward traffic to multiple servers (e.g. EC2 instances) downstream.

Why do we use LBs ?

- spread load across a fleet of servers
- expose a single point of access DNS to your application
- seamlessly handle failures of downstream instance
- Provide SSL termination (HTTPS) for your websites
- Enforce stickiness with cookies
- High availability across zones
- separate public traffic from private traffic

### Why use an ELB (Elastic Load Balancer)

- ELB is *managed load balancer*
- costs less to setup your own load balancer but more effort to maintain it
- It is integrated with many AWS offerings/services
    - EC2, EC2 Autoscaling Groups, Amazon ECS
    - AWS Certificate Manager (ACM), CloudWatch
    - Route 53, AWS WAF, AWS Global Accelerator

### Health Checks

- They enable LBs to check instances it forward traffic to are healthy or not
- Heath Check can be done on a port or a route (`/health`)
- If response is not 200 (OK), then instance is unhealthy

![](assets/Pasted%20image%2020251029164702.png)

### Types of Load Balancer on AWS

- Traditionally Load Balancers are of two types Layer 4 (Network) & Layer 7 (Application) and there is huge debate around which one is better.
- You trade off speed/privacy for advanced features on application layers.
- In AWS However, we can have broadly 4 types of managed Load Balancers
    - Classic Load Balancer (v1 - old generation) ~ 2009 CLB
        - HTTP/HTTPS/TCP/SSL (Secure TCP)
    - Application Load Balancer (v2 - new gen) ~ 2016 ALB
        - HTTP/HTTPS/Websockets
    - Network Load Balancer (v2 - new gen) ~ 2017 NLB
        - TCP/TLS(secure TLS)/UDP
    - Gateway Load Balancer ~ 2020 ~ GWLB
        - operates at layer 3 (Network layer) ~ IP Protocol
- Some load balancers can be setup as *internal* (private) or *external* (public) ELBs.

### Load Balancer Security Groups

![](assets/Pasted%20image%2020251029165136.png)

## Classic  Load Balancer

![](assets/Pasted%20image%2020251029165452.png)

- Operates at layer 4/ layer 7
- Supported protocols HTTP, HTTPS, TCP, and SSL/TLS
- EC2 instances registered directly with the CLB (no Target Groups)
- Health Checks can be HTTP, HTTPS, or TCP
- Supports EC2 - classic networks

### Classic Load Balancer - SSL considerations

- Enabling HTTPS or SSL on EC2 instances is called *Backend Authentication*
- TCP => TCP passes all the traffic to the EC2 instance (no termination): the only way to do 2-way Mutual SSL Auth

![](assets/Pasted%20image%2020251029165654.png)

## Application Load Balancer

![](assets/Pasted%20image%2020251029165844.png)

- operates at Layer 7
- Supports : HTTP, HTTPS, WS, HTTP/2 and gRPC
- Load balancing to multiple HTTP applications across machines (target groups)
- Load balancing to multiple application/ports on the same server
- Supports for returning custom HTTP responses
- supports redirects (HTTP-> HTTPS)
- Target Groups
    - EC2 Instances (can be managed by a ASG) - HTTP
    - EC2 Tasks (managed by ECS itself) - HTTP
    - Lambda Functions - HTTP request is translated into a JSON event
    - IP Addresses - must be private IP addresses
- Supports Weighted Target Groups
- Health Checks can be HTTP or HTTPS (WS is not supported)
- Each subnet must have a min of /27 and 8 free IP addresses
- Across all subnets, a maximum of 100 IP addresses will be used per ALB
- Routing to different target groups
    - Routing based on URL Path
    - Routing based on Hostname
    - Routing based on Query String, HTTP Headers, Source IP Address
- ALB are great fit for micro services & container based applications
- Has port mapping feature to redirect to a dynamic ports in ECS

![](assets/Pasted%20image%2020251029170145.png)

### Auth in ALB

![](assets/Pasted%20image%2020251029170247.png)

- Ability to authenticate users before routing requests to registered targets
    - Amazon Cognito User Pools and Identity Providers
    - Microsoft Active Directory, OIDC, SAML, LDAP,
    - OpenID
    - Social Identity Providers such as Amazon, Facebook, Google
- TLS Certificates (multiple listeners & SNI)

### ALB - Listener Rules

![](assets/Pasted%20image%2020251029170435.png)

- Processed in order (last is Default Rule)
- Supported Actions (forward, redirect, fixed-response)
- Rule Conditions:
    - host-header
    - http-request-method
    - path-pattern
    - source-ip
    - http-header
    - query-string

### Target Group Weighting

![](assets/Pasted%20image%2020251029170422.png)

- Specify weight for each Target Group on a single Rule
- Example: multiple versions of your app, blue/green deployment
- Allows you to control the distribution of the traffic to your applications

## Network Load Balancer

![](assets/Pasted%20image%2020251029170610.png)

- operates at Layer 4
- Supported protocols TCP, UDP and TLS
- Handle millions of request per second
- NLB has *one static IP per AZ* and supports assigning *Elastic IP* (Internet facing NLB)
- Load balancing to multiple applications/ports on the same machine
- Less Latency ~ 100 ms (vs 400ms for ALB)
- supports websocket protocol
- NLB are used for
    - extreme performance, TCP or UDP traffic
    - within AWS PrivateLink
- Target Groups
    - EC2 instances ~ can be managed by ASG
    - EC2 Tasks ~ managed by ECS itself
    - IP addresses
        - must be private IP addresses, TCP listeners only
- You can't register EC2 instances by instance ID if these EC2 instances are in another VPC (even if peered with NLBVPC)
    - register by IP address instead
- Health Checks
    - supported protocols HTTP, HTTPS, and TCP
    - Active Health checks
    - Passive Health Check

![](assets/Pasted%20image%2020251029171107.png)

- Client IP Preservation : client IP is forwarded to targest
    - Targets by instance ID / ECS Tasks: Enabled
    - Targets by IP address TCP & TLS: Disabled by default
    - Targets by IP address UDP & TCP_UDP: Enabled by default
- When disabled, use Proxy Protocol v2 (will add headers)

![](assets/Pasted%20image%2020251029171217.png)

### Network Load Balancer - Zonal DNS Name

![](assets/Pasted%20image%2020251029171250.png)

- Resolving Regional NLB DNS name returns the IP addresses for all NLB nodes in all enabled AZs
    - `my-nlb-1234567890abcdef.elb.us-east-1.amazon.aws.com`
- Zonal DNS Name
    - NLB has DNS names for each of its nodes
    - Use to determine the IP address of each node
    - `us-east-1a.my-nlb-1234567890abcdef.elb.us-east-1.amazon.aws.com`
    - Used to minimize latency and data transfer costs
    - You need to implement app specific logic

### Good To Know

- You can’t disable/remove an AZ after you create it
- You can’t modify ENIs created for the NLB in each AZ (view only)
- You can’t change EIPs and private IPv4 addresses attached to the ENIs after you create the load balancer
- Supports 440,000 simultaneous connections/minute per target
- For internet-facing load balancers, the subnets that you specify must have at least 8 available IP addresses (e.g. min /28). For internal load balancers, this is only required if you let AWS select a private IPv4 address from the subnet.

## Connection Idle Timeout

![](assets/Pasted%20image%2020251029171651.png)

- Idle Timeout period for ELB’s connections (client-ELB connection & ELB-target connection)
    - Connection closed if no data has been sent/received during that period
    - Opened if at least 1 byte is sent before that timeout period elapses
- Supported for CLB, ALB, and NLB
- Can be configured for CLB & ALB (default 60 seconds)
- Can’t be configured for NLB (350 sec. for TCP, 120 sec. for UDP)
- Usage: avoid timeouts while uploading files
- Recommended to enable HTTP keep-alive in the web server settings for your EC2 instances, thus makes the ELB reuse the backend connections until the keep-alive timeout expires

## Request Routing Algorithms

### Least Outstanding Requests

- Chooses the next instance to receive the request by selecting the instance that has the lowest number of pending/unfinished requests
- Works with Application Load Balancer and Classic Load Balancer (HTTP/HTTPS)

![](assets/Pasted%20image%2020251029171833.png)
### Round Robin

- Equally choose the targets from the target group
- Works with Application Load Balancer and Classic Load Balancer (TCP)

![](assets/Pasted%20image%2020251029171859.png)
### Flow Hash

- Selects a target based on the protocol, source/destination IP address, source/destination port, and TCP sequence number
- Each TCP/UDP connection is routed to a single target for the life of the connection
- Works with Network Load Balancer

![](assets/Pasted%20image%2020251029172045.png)

## Sticky Sessions (Session Affinity)

![](assets/Pasted%20image%2020251029173109.png)

- It is possible to implement stickiness so that the same client is always redirected to the same instance behind a load balancer
- This works for Classic Load Balancer, Application Load Balancer, and Network Load Balancer
- For both CLB & ALB, the “cookie” used for stickiness has an expiration date you control
- Use case: make sure the user doesn’t lose his session data
- Enabling stickiness may bring imbalance to the load over the backend EC2 instances

### Sticky Sessions - Cookie Names

-  Application-based Cookies
    - Custom cookie
        - Generated by the target
        - Can include any custom attributes required by the application
        - Cookie name must be specified individually for each target group
        - Don’t use AWSALB, AWSALBAPP, or AWSALBTG (reserved for use by the ELB)
    - Application cookie
        - Generated by the load balancer
        - Cookie name is AWSALBAPP
    - Should be used if you need sticky sessions across all layers
- Duration-based Cookies
    - Cookie generated by the load balancer
    - Cookie name is AWSALB for ALB, AWSELB for CLB

## Cross-Zone Load Balancing

![](assets/Pasted%20image%2020251029173244.png)

- Application Load Balancer
    - Enabled by default (can be disabled at the Target Group level)
    - No charges for inter AZ data
- Network Load Balancer & Gateway Load Balancer
    - Disabled by default
    - You pay charges ($) for inter AZ data if enabled
- Classic Load Balancer
    - Disabled by default
    - No charges for inter AZ data if enabled

## SSL/TLS

- An SSL Certificate allows traffic between your clients and your load balancer to be encrypted in transit (in-flight encryption)
- SSL refers to Secure Socket Layer, used to encrypt connections
- TLS refers to Transport Layer Security, which is a newer version
- Nowadays, TLS certificates are mainly used, but people still refer as SSL
- Public SSL certificates are issued by Certificate Authorities (CA)
- Comodo, Symantec, GoDaddy, GlobalSign, DigiCert, Let’s Encrypt, …
- SSL certificates have an expiration date (you set) and must be renewed

### Elastic Load Balancer - SSL Certificates


- The load balancer uses an X.509 certificates (SSL/TLS server certs)
- You can manage certificates using ACM (AWS Certificate Manager)
- You can create upload your own certs alternatively
- HTTPS listener:
    - You must specify a default certificate
    - You can add an optional list of certs to support multiple domains
    - Clients can use SNI (Server Name Indication) to specify the hostname they reach
    - Ability to specify a Security Policy (for compliance, features, compatibility or security)

### SSL - Server Name Indication (SNI)

![](assets/Pasted%20image%2020251029181935.png)

- SNI solves the problem of loading multiple SSL certificates onto one web server (to serve multiple websites)
- It’s a “newer” protocol, and requires the client to indicate the hostname of the target hostname in the initial SSL handshake
- The server will then find the correct certificate, or return the default one
- Only works for ALB & NLB

### Elastic Load Balancer - SSL Certificates

- Classic Load Balancer
    - Supports only one SSL certificate
    - The SSL certificate can have many Subject Alternate Name (SAN), but the SSL certificate must be changed anytime a SAN is added / edited / removed
    - Must use multiple CLB for multiple hostnames with multiple SSL certificates
    - Better to use ALB with Server Name Indication (SNI) if possible
- Application Load Balancer
    - Supports multiple listeners with multiple SSL certificates
    - Uses Server Name Indication (SNI) to make it work
- Network Load Balancer
    - Supports multiple listeners with multiple SSL certificates
    - Uses Server Name Indication (SNI) to make it work

### HTTPS/SSL Listener - Security Policy

- A combination of SSL protocols, SSL ciphers, and Server Order Preference option supported during SSL negotiations
- Predefined Security Policies (e.g., ELBSecurityPolicy-2016-08)
- For ALB and NLB
    - Frontend connections, you can use a predefined Security Policy
    - Backend connections, ELBSecurityPolicy-2016-08 Security Policy is always used
- Use ELBSecurityPolicy-TLS policies
    - To meet compliance and security standards that require certain TLS protocol version
    - To support older versions of SSL/TLS (legacy clients)
- Use ELBSecurityPolicy-FS policies, if you require Forward Secrecy
    - Provides additional safeguards against the eavesdropping of encrypted data
    - Using a unique random session key

## Connection Draining

- Feature naming
    - Connection Draining - for CLB
    - Reregistration Delay - for ALB & NLB
- Time to complete “in-flight requests” while the instance is de-registering or unhealthy
- Stops sending new requests to the EC2 instance which is de-registering
- Between 1 to 3600 seconds (default: 300 seconds)
- Can be disabled (set value to 0)
- Set to a low value if your requests are short

## X-Forwarded Headers (HTTP)

![](assets/Pasted%20image%2020251029182543.png)

- Non-standard HTTP headers that have an X-Forwarded prefix
- Used by ELB to forward client information to the targets (e.g., client IP address)
- You can use to log client requests on your server
- Supported by Classic Load Balancer (HTTP/HTTPS) and Application Load Balancer
- X-Forwarded-For
    - Contains the IP address of the client
    - May contain comma-separated list of multiple IP addresses, such as proxies (left-most is the client IP address)
- X-Forwarded-Proto – the protocol used between client and the ELB (HTTP/HTTPS)
- X-Forwarded-Port – the destination port the client used to connect to the ELB

## Proxy Protocol

![](assets/Pasted%20image%2020251029182603.png)

- An Internet protocol used to carry information from the source (requesting the connection) to the destination (where connection was requested)
- If the LB terminates the connection, the source IP address of the client cannot be preserved
- We use the Proxy Protocol to pass the source/destination IP address and port numbers
- The load balancer prepends a proxy protocol header to the TCP dat
- Available for both Classic Load Balancer (TCP/SSL) and Network Load Balancer
- CLB uses Proxy Protocol version 1 & NLB uses Proxy Protocol version 2
- For Network Load Balancer
- Target with Instance ID and ECS Tasks: the source IP of the client is preserved
    - Target with IP Address:
        - TCP & TLS: the source IP of the client isn’t preserved, enable Proxy Protocol
        - UDP & TCP_UDP: the source IP of the client is preserved
- Load balancer should not be behind proxy server, otherwise backend may receive duplicate configuration information resulting in error
- Proxy protocol is not needed when using an Application Load Balancer, as ALB already inserts HTTP X-Forwarded-For headers

## Application Load Balancer & gRPC

![](assets/Pasted%20image%2020251029182842.png)

- gRPC is a popular choice for microservice integrations using HTTP/2
- The Application Load Balancer fully supports gRPC
    - Supports gRPC health checks from target group
    - Content based routing feature to route to the appropriate service
    - Supports all kind of gRPC communication (including bidirectional streaming)
    - Listener protocol is HTTPS
    - Note: gRPC would work with NLB but you wouldn’t have any “HTTP-specific” features

## Load Balancing Architectures

### across on-premises servers
![](assets/Pasted%20image%2020251029182928.png)

### across Peered VPCs
![](assets/Pasted%20image%2020251029182949.png)

## Internet-Facing vs Internal Load Balancer

![](assets/Pasted%20image%2020251029183038.png)

## Security Groups

- default is allowed 0.0.0.0/0 anywhere
- But we can remove and just allow specific prefixes

![](assets/Pasted%20image%2020251029183121.png)

## Managed Prefix List

![](assets/Pasted%20image%2020251029183234.png)

- A set of one or more CIDR blocks
- Makes it easier to configure and maintain Security Groups and Route Tables
- Customer-Managed Prefix List
    - Set of CIDRs that you define and managed by you
    - Can be shared with other AWS accounts or AWS Organization
    - Modify to update many Security Groups at once
- AWS-Managed Prefix List
    - Set of CIDRs for AWS services
    - You can’t create, modify, share, or delete them
    - S3, CloudFront, DynamoDB, Ground Station…

