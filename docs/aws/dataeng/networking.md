# Networking & CDN

## VPC & Subnets Primer

![](assets/Pasted%20image%2020251113000104.png)

- VPC: private network to deploy your resources (regional resource)
- Subnets : partitions of network inside VPC
- A *public subnet* is a subnet that is accessible from the internet
- A *private Subnet* is a subnet that is not accessible from the internet
- To define access to internet and between subnets, we use Route Tables

![](assets/Pasted%20image%2020251113000304.png)

- Internet Gateway ~ helps our VPC instances connect with internet
- Public Subnet have a route to internet gateway
- NAT Gateways (AWS-managed) & NAT Instances (self-managed) allow your instances in your Private Subnets to access the internet while remaining private

| ![](assets/Pasted%20image%2020251113000541.png) | ![](assets/Pasted%20image%2020251113000605.png) |
| ----------------------------------------------- | ----------------------------------------------- |

- NACL (Network ACL)
    - A firewall which controls traffic from and to subnet
    - Can have ALLOW and DENY rules
    - Are attached at the Subnet level
    - Rules only include IP addresses
- Security Groups
    - A firewall that controls traffic to and from an ENI / an EC2 Instance
    - Can have only ALLOW rules
    - Rules include IP addresses and other security groups

![](assets/Pasted%20image%2020251113000644.png)

### VPC Flow Logs

- Capture information about IP traffic going into your interfaces:
    - VPC Flow Logs
    - Subnet Flow Logs
    - Elastic Network Interface Flow Logs
- Helps to monitor & troubleshoot connectivity issues. Example:
    - Subnets to internet
    - Subnets to subnets
    - Internet to subnets
    - Captures network information from AWS managed interfaces too: Elastic Load Balancers, ElastiCache, RDS, Aurora, etc…
    - VPC Flow logs data can go to S3, CloudWatch Logs, and Kinesis Data Firehose

### VPC Peering

![](assets/Pasted%20image%2020251113000750.png)

- Connect two VPC, privately using AWS’ network
- Make them behave as if they were in the same network
- Must not have overlapping CIDR (IP address range)
- VPC Peering connection is not transitive (must be established for each VPC that need to communicate with one another)

### VPC Endpoints

![](assets/Pasted%20image%2020251113000832.png)

- Endpoints allow you to connect to AWS Services using a private network instead of the public www network
- This gives you enhanced security and lower latency to access AWS services
- VPC Endpoint Gateway: S3 & DynamoDB
- VPC Endpoint Interface: most services (including S3 & DynamoDB)
- Only used within your VPC

### Site-to-Site VPN & Direct Connect

- Site to Site VPN
    - Connect an on-premises VPN to AWS
    - The connection is automatically encrypted
    - Goes over the public internet
- Direct Connect (DX)
    - Establish a physical connection between on- premises and AWS
    - The connection is private, secure and fast
    - Goes over a private network
    - Takes at least a month to establish

### AWS Private Link (VPC Endpoint Services)

![](assets/Pasted%20image%2020251113001012.png)

- Most secure & scalable way to expose a service to 1000s of VPCs
- Does not require VPC peering, internet gateway, NAT, route tables…
- Requires a network load balancer (Service VPC) and ENI (Customer VPC)

## Amazon CloudFront

- Content Delivery Network (CDN)
- Improves read performance, content is cached at the edge
- Improves users experience
- Hundreds of Points of Presence globally (edge locations, caches)
- DDoS protection (because worldwide), integration with Shield, AWS Web Application Firewall

### CloudFront Origins

- S3 bucket
    - For distributing files and caching them at the edge
    - For uploading files to S3 through CloudFront
    - Secured using Origin Access Control (OAC)
- VPC Origin
    - For applications hosted in VPC private subnets
    - Application Load Balancer / Network Load Balancer / EC2 Instances
- Custom Origin (HTTP)
    - S3 website (must first enable the bucket as a static S3 website)
    - Any public HTTP backend you want

![](assets/Pasted%20image%2020251113001251.png)

### CloudFront - S3 as an Origin

![](assets/Pasted%20image%2020251113001316.png)

### CloudFront vs S3 Cross Region Replications

- CloudFront:
    - Global Edge network
    - Files are cached for a TTL (maybe a day)
    - Great for static content that must be available everywhere
- S3 Cross Region Replication:
    - Must be setup for each region you want replication to happen
    - Files are updated in near real-time
    - Read only
    - Great for dynamic content that needs to be available at low- latency in few regions

### CloudFront - ALB or EC2 as an origin ~  Using VPC Origins

![](assets/Pasted%20image%2020251113001638.png)
### CloudFront - ALB or EC2 as an origin ~  Using Public Network

![](assets/Pasted%20image%2020251113001621.png)

### CloudFront - Cache Invalidations

![](assets/Pasted%20image%2020251113001437.png)

- In case you update the back-end origin, CloudFront doesn’t know about it and will only get the refreshed content after the TTL has expired
- However, you can force an entire or partial cache refresh (thus bypassing the TTL) by performing a CloudFront Invalidation
- You can invalidate all files (`*`) or a special path (`/images/*`)
