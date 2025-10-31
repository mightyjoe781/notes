# AWS Network Security Services

AWS Security services can broadly be divided into 2 types

- Preventive Services
- Detective Services

![](assets/Pasted%20image%2020251031095454.png)

We can visualize all these services and their placement with respect to our VPC.

![](assets/Pasted%20image%2020251031095529.png)

## Security Groups & Network ACL

![](assets/Pasted%20image%2020251031095844.png)

- Security Groups
    - Attached to ENIs ~ EC2, RDS, Lambda in VPC, etc
    - Stateful (Any traffic in is allowed to go out, any traffic out can go back in)
    - referenced by CIDR & group id
    - supports SG reference for VPC Peering
    - Default : Inbound denied, Outbound all allowed
- NACL (Network ACL):
    - Attached at Subnet Level
    - Are stateless (inbound & outbound rules apply for all traffic)
    - Can only reference a CIDR range (no hostnames)
    - Default : denies all inbound, denies all outbound

### Blocking an IP Address

![](assets/Pasted%20image%2020251031095930.png)

### Blocking an IP Address - with an ALB

![](assets/Pasted%20image%2020251031095941.png)
### Blocking an IP Address - with a NLB

![](assets/Pasted%20image%2020251031100000.png)

### Blocking an IP Address - CloudFront

![](assets/Pasted%20image%2020251031100023.png)

## AWS WAF

### Amazon Web Application Firewall (WAF)

![](assets/Pasted%20image%2020251031100054.png)

- protects web applications from common web exploits (Layer 7)
- Deploy on ALB, APIGW or AppSync GraphQL APIs, CloudFront
- Define Web ACL with which we can allow, block, monitor web requests by inspecting IP addresses, HTTP headers, HTTP Body, or URI Strings, Size Constraint, Geo match, String match, etc.
- Web ACLs also supports Rate-based rules
- When body of the request is evaluated, it inspect first 8KB.
- On blocking malicious traffic WAF return 403 (Forbidden)
- It takes a less than 1 minutes for WAF rules to propagate


WAF ACL regular rules support following

- xss
- IP Addresses
- Size
- SQL Injection
- Geographic match
- String/Regex match

## AWS Shield

Common DDoS (Distributed Denial of Services) attacks

![](assets/Pasted%20image%2020251031134921.png)

- SYN Flood attack: Too many half open TCP connections
- UDP Flood attack: Too many UDP requests
- UDP Reflection attack: Spoof the victim server IP as a source for UDP packet. Victim server receives the unexpected responses.
- DNS Flood Attack: Overwhelm the DNS so legitimate users can't find the site
- Slow Loris attack (Layer 7): A lot HTTP connections are opened and maintained

![](assets/Pasted%20image%2020251031135122.png)

### AWS Shield & AWS Shield Advanced

- AWS Shield Standard (Free service)
    - provides protection from attacks such as SYN/UDP Floods, Reflection attacks & other layer 3/4 attacks
    - Enabled automatically for ELB, CloudFront and Route 53
- AWS Shield Advanced (Paid Service)
    - Options DDoS mitigation service (3000$/month/org)
    - protection against most sophisticated attacks
    - 24/7 access to AWS Shield Response Team (SRT)
    - SRT team also helps to identify layer 7 attacks/patterns and deploys Web ACL rules on WAF (you must grant IAM role to SRT team)
    - Customer receives attack forensic report from SRT

## AWS Network Firewall

A stateful network firewall and intrusion detection & prevention service

![](assets/Pasted%20image%2020251031135452.png)

![](assets/Pasted%20image%2020251031135505.png)

- Stateful Firewalls
    - Filters traffic based on network packet context and connection state
    - Context involves metadata of the packet including IP addresses, ports, packet length, information about reassembly and defragmentation, flags, TCP sequence number etc
    - State refers to the state of the connection e.g for TCP connection the state of connection is SYN, ACK, FIN and RST
- Stateless Firewalls
    - Inspects each packet in isolation
    - Performs well in case of heavy traffic

### AWS Network Firewall

- Filters traffic at the perimeter of the VPC such as traffic going to or coming from internet gateway, NAT gateway, over VPN or Direct connect
- Uses the Suricata for stateful inspection
- Suricata is an open source-based intrusion detection system and intrusion prevention system developed by the Open Information Security Foundation
- Allows domain name filtering e.g only AWS service endpoints
- Block access to bad domains and limit the types of domain names
- Deep packet inspection on traffic entering or leaving your VPC
- Stateful protocol detection to filter protocols like HTTPS (independent of the port used)

### Network Firewall traffic flow - Inbound

![](assets/Pasted%20image%2020251031135800.png)

### Network Firewall traffic flow - Outbound

![](assets/Pasted%20image%2020251031135814.png)

### Network Firewall Components

- Firewall
- Firewall Policy
- Rule Groups

![](assets/Pasted%20image%2020251031135857.png)

### Rules Evaluation order

![](assets/Pasted%20image%2020251031205543.png)

## Gateway Load Balancer

![](assets/Pasted%20image%2020251031205620.png)
![](assets/Pasted%20image%2020251031205656.png)

### Centralized Inspection using GWLB

![](assets/Pasted%20image%2020251031205717.png)

### Summary

- GWLB is used to deploy, scale, and manage a fleet of 3rd party network appliances in AWS.
- Example: Firewalls, Intrusion Detection and Preventions Systems, Deep Packet Inspection Systems, payload manipulation etc.
- GWLB operates at Layer 3 (Network Layer) – As opposed to ALB (Layer7) and NLB (Layer4)
- It’s a transparent network gateway which acts as single entry and exit point for all traffic
- Load balances the traffic and scales virtual appliances on demand
- GWLB integrates with industry leading partners Aviatrix, Cisco Systems, Fortinet, Palo Alto Networks, …
## ACM

### How to get SSL/TLS Certificate ?

![](assets/Pasted%20image%2020251031205852.png)

### How to issue certificate using ACM ?

![](assets/Pasted%20image%2020251031205945.png)

### AWS Certificate Manager

- AWS Certificate Manager (ACM)
- AWS Private CA

### HTTPS, SSL/TLS with AWS Services

![](assets/Pasted%20image%2020251031210144.png)

### AWS Certificate Manager (ACM)

- Provides the free SSL/TLS X.509 Certificate which you can deploy on CloudFront, ELB, ElasticBeanstalk, API Gateway
- You can also request wildcard certificate e.g. `*.example.com`
- ACM is a regional service and you need to generate certificate in each region. However for CloudFront you must request certificate in us-east-1 i.e. North Virginia region.
- You can not have wildcard in the middle of the domain name
    - Example: `app.*.example.com` is not allowed
    - Example: `*.app.example.com` is allowed
- Public certificates that you request through ACM are obtained from Amazon Trust Services which is an Amazon managed public certificate authority (CA)
- Public certificates issued through ACM are valid for 13 months (395 days) However, with private CA you may chose the certificate validity period
- ACM automatically renews the Certificates which are domain validated
- You can import your own Certificate into ACM. You have to renew imported certificates.

## AWS Firewall Manager

- Security management tool which simplifies security administration and maintenance tasks across multiple AWS accounts and resources
- Manages the rules for AWS WAF, AWS Shield Advanced, Amazon VPC security groups, AWS Network Firewall, and Amazon Route 53 Resolver DNS Firewall
- New accounts added under the AWS Organizations are automatically protected
- Provides centralized monitoring of DDoS attacks across AWS organization

### Pre-requisites for Firewall Manager

- Enable AWS Organization (full features)
- Enable AWS Config
- Enable AWS Resource Access Manager (RAM)

![](assets/Pasted%20image%2020251031210345.png)
### AWS Firewall Manager

![](assets/Pasted%20image%2020251031210359.png)

### When to use what?

![](assets/Pasted%20image%2020251031210420.png)