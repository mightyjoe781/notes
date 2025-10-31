# Additional Topics

## VPC Sharing

- Multiple AWS accounts in an AWS organization can share a VPC to launch their resources(e.g. EC2 instances, RDS database etc.)
- Account that owns the VPC (owner) shares one or more subnets with other accounts (participant)
- Must enable resource sharing from the management account for the AWS organization.
- Resource Share should be created for the subnet to be shared. It can be shared with AWS accounts, organizational units, or an entire organization.
- VPC owners can't share subnets that are in a default VPC.

![](assets/Pasted%20image%2020251030235137.png)
![](assets/Pasted%20image%2020251030235146.png)
![](assets/Pasted%20image%2020251030235218.png)

### Benefits of Sharing VPCs

- Simplified design — no complexity around inter-VPC connectivity
- Fewer managed VPCs
- Avoidance of the problem of CIDR overlap that is encountered with multiple VPCs
- Segregation of duties between network teams and application owners
- Better IPv4 address utilization
- Reuse of network address translation (NAT) gateways, VPC interface endpoints etc.
- No data transfer charges between instances belonging to different accounts within the same Availability Zone

### Shared VPC architectures

#### Shared Subnets across all accounts

![](assets/Pasted%20image%2020251030235331.png)
### Dedicated subnets per account

![](assets/Pasted%20image%2020251030235355.png)

### AZ Considerations
![](assets/Pasted%20image%2020251030235423.png)

#### Shared subnets across all accounts

![](assets/Pasted%20image%2020251030235446.png)

### VPC sharing and Transit Gateway

- We can use VPC sharing to enable subnet sharing within the same project/business unit across different teams and Transit Gateway to connect these VPCs for centralized routing, firewall and on-premises connectivity.

![](assets/Pasted%20image%2020251030235523.png)

https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html

## Private NAT Gateway

### Problems with Private IPs

- Limited by Private IP ranges defined by RFC1918
- Need to have separate Private IP range for different business units
- Microservices architecture require services to have their own Private IPs thereby requiring more and more Private IPs
- This causes.. : Difficulty to establish connectivity between the business units with overlapping CIDRs

### Possible solutions for overlapping IP ranges

- Using AWS PrivateLink
- Using IPv6 addresses
- Using self managed NAT’ing appliances
    - Additional appliances to manage
    - Operational overhead

### Private NAT Gateway

- Allows communication between VPCs or VPC and on-premises network having the overlapping CIDRs
- Networks could be connected over Virtual Private Gateway (VGW) or Transit Gateway
- Private NAT performs the Private IP network address translation
- For deploying Private NAT you would often need to divide your address space in routable and non-routable (overlapping) address space and then configure the routing such that there is a communication between non-routable address range via the routable IP addresses

### Solution Architectures

![](assets/Pasted%20image%2020251030235853.png)
![](assets/Pasted%20image%2020251030235905.png)
![](assets/Pasted%20image%2020251030235925.png)
![](assets/Pasted%20image%2020251030235933.png)

## Amazon Workspaces/Appstream networking

![](assets/Pasted%20image%2020251031000219.png)
![](assets/Pasted%20image%2020251031000229.png)

## AWS WaveLength

![](assets/Pasted%20image%2020251031000147.png)

- WaveLength Zones are infrastructure deployments embedded within the telecommunications providers’ datacenters at the edge of the 5G networks
- Brings AWS services to the edge of the 5G networks
- Example: EC2, EBS, VPC…
- Ultra-low latency applications through 5G networks
- Traffic doesn’t leave the Communication Service Provider’s (CSP) network
- High-bandwidth and secure connection to the parent AWS Region
- No additional charges or service agreements
- Use cases: Smart Cities, ML-assisted diagnostics, Connected Vehicles, Interactive Live Video Streams, AR/VR, Real-time Gaming, …
## AWS Local Zones

![](assets/Pasted%20image%2020251031000049.png)

- Places AWS compute, storage, database, and other selected AWS services closer to end users to run latency-sensitive applications
- Extend your VPC to more locations – “Extension of an AWS Region”
- Compatible with EC2, RDS, ECS, EBS, ElastiCache, Direct Connect …
- Example:
    - AWS Region: N. Virginia (us-east-1)
    - AWS Local Zones: Boston, Chicago, Dallas, Houston, Miami, 
