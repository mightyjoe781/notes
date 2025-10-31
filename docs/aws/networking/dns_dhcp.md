# VPC DNS and DHCP

## How DNS works ?

### What is DNS

- Domain Name Server resolves human readable names into IPv4/IPv6 addresses
- Backbone of internet
- If Local DNS Server doesn't have address, it could be routed to Domain Registrar servers
- Usually Browsers cache DNS Servers

![](assets/Pasted%20image%2020251025170427.png)

### DNS resolution for Amazon VPC

![](assets/Pasted%20image%2020251025170559.png)

## VPC DNS Server (Route 53 Resolver)

- VPC comes with default DNS Server also called as Route 53 DNS Resolver
- Runs at VPC Base + 2 Address (can be accessed from within the VPC at virtual IP 169.254.169.253)
- Resolves DNS requests from
    - Route 53 Private Hosted Zone
    - VPC internal DNS
    - Forwards other requests to Public DNS (including Route 53 Public Hosted Zone)
- Accessible from within the VPC

![](assets/Pasted%20image%2020251025171104.png)

### Amazon DNS Server - Amazon Route53 Resolver

Amazon Route53 Private Hosted Zone

- Creates a private hosted zone : *example.internal*
- Create record sets pointing to EC2 instances private IPs
- DNS queries from within the VPC

![](assets/Pasted%20image%2020251025171349.png)

VPC DNS

- EC2 instances get Private DNS name such as
    - ip-`<private-ipv4-address>.region.compute.internal`
    - ip-10-10-0-15-ap.south-1.compute.internal

Public DNS

- google.com, amazon.com etc
- Amazon services public endpoints
    - `sqs.ap-south-1.aws.amazon.com`

![](assets/Pasted%20image%2020251025171714.png)

### How VPC knows about this Amazon DNS Server ?

- DHCP Option Sets
- VPC comes with default DHCP Option set which provides these dynamic host configurations to instances on launch

## VPC DHCP Option sets

- Dynamic Host Configuration Protocol, message contains the configuration parameters like *domain name*, *NTP server* and NetBIOS node type.
- AWS automatically creates and associates a DHCP option set for your VPC upon creation and sets following parameters.
    - domain-name-servers: his defaults to AmazonProvidedDNS
    - domain-name: This defaults to the internal Amazon domain name for your
region (e.g `<ip>.ap-south-1.compute.internal`)

![](assets/Pasted%20image%2020251025172451.png)

### AWS assigned domain names for EC2

- Internal DNS
    - `ip-<private-ipv4-address>-ec2.internal` (us-east-1 region)
    - `ip-<private-ipv4-address>.region.compute.internal` (for all other regions)
- External DNS (If instance has a public IP)
    - `ip-<public-ipv4-address>.compute-1.amazonaws.com` (us-east-1 region)
    - `ip-<public-ipv4-address>.region.amazonaws.com` (for all other regions)

### Attaching VPC a new DHCP Options set

![](assets/Pasted%20image%2020251025172746.png)

### VPC DNS Attributes

- enableDnsSupport (= DNS Resolution setting)
    - default = true
    - helps decide if DNS resolution is supported for the VPC
    - If True, queries the AWS DNS server at 169.254.169.253 (=> VPC+2
- enableDNSHostname (= DNS Hostname setting)
    - False by default for newly created VPC, true by default for default VPC
    - Won’t do anything unless enableDnsSupport=true
    - If True, assigns public hostname to EC2 instance if it has a public IP
- If you use custom DNS domain names in a Route53 Private hosted zone, you must set both these attributes to true.

### Important Notes on DHCP Options Sets

- Once created, you can not modify DHCP Options set however you can create new DHCP Options set and associate it with VPC
- You can only associate a single DHCP Options set with a VPC
- VPC can also be setup without DHCP Options set. In that case the instances in the VPC can't access the internet as there is no access to a DNS server.
- After DHCP Option set is associated with VPC, the instances automatically use new option set, but this may take a few hours
- You can also refresh the DHCP option parameters using an operating system command: `sudo dhclient -r eth0`

## Introduction to Route 53 DNS Resolver Endpoints (Hybrid DNS)

### How to resolve DNS from outside VPC ?

- AWS to On-premises (When DNS server is located on-premises)
- On-premises to AWS (When DNS server is located in AWS)
- Bi-directional (When DNS server is located at both the sites)

![](assets/Pasted%20image%2020251025175359.png)

### Route 53 Resolver Endpoint

- Officially named the `.2 DNS` resolver to Route53 Resolver
- Provides Inbound & Outbound Route53 resolver endpoints
- Provisions ENI in the VPC which are accessible over VPN or DX
- Inbound -> On-premise forwards DNS request to R53 Resolver
- Outbound -> Conditional forwarders for AWS to On-premise

### Route53 Resolver Endpoint - Inbound

![](assets/Pasted%20image%2020251025175649.png)

### Route53 Resolver Endpoint - Outbound

![](assets/Pasted%20image%2020251025175706.png)

