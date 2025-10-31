# Additional VPC Topics

All these topics are important for Exam

## Egress only Internet Gateway

### Internet Access for instance in a Private subnet (IPv4)

![](assets/Pasted%20image%2020251025161501.png)

- Since VPC supports dual-stack mode
- Resources inside VPC can communicate over IPv4 or IPv6 or both

### Internet access for instance in a Private Subnet

![](assets/Pasted%20image%2020251025161623.png)

By default NAT doesn't support IPv6 to IPv6 NAT Translation. We use Egress-only internet gateway

### Egress-only internet gateway

![](assets/Pasted%20image%2020251025161724.png)

## Extending VPC Address Space

- Why ?
    - IP Addresses are exhausted, and want to create another secondary VPC CIDR
    - Overlapping On-prem CIDR blocks
- Restrictions
    - You can add secondary VPC CIDRs to existing VPC
    - CIDR block must not overlap with existing CIDR or peered VPC CIDR
    - If primary CIDR is from RFC1918 then you cannot add secondary CIDR from other RFC1918IP ranges
    - CIDR block must not be same or larger than CIDR range of routes in any of the VPC Route Tables
    - You can have total 5 IPv4 and 1 IPv6 CIDR block for VPC

#### VPC with Primary CIDR Block

![](assets/Pasted%20image%2020251025163005.png)

#### VPC with Primary & Secondary CIDR Block

![](assets/Pasted%20image%2020251025163042.png)

![](assets/Pasted%20image%2020251025163119.png)

## Elastic Network Interface (ENI)

- Logical Component in a VPC that represents a virtual network card
- ENIs are bound to a specific AZ
- ENI can have following attributes
    - A primary private IPv4 address from the IPv4 address range of the VPC
    - A primary IPv6 address range of your VPC
    - One or more secondary private IPv4 addresses from the IPv4 address range of your VPC
    - One EIP (IPv4) per private IPv4 address
    - One public IPv4 address
    - One or more IPv6 address
    - One or more security groups
    - A MAC address
    - A source/destination check flag

![](assets/Pasted%20image%2020251025163639.png)

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailablelpPerENI

### ENI Use Cases

- Requester managed ENIs that AWS creates in your VPC
- Creating Management Network/Dual home instances
- Preserving EC2 IP Address in case of instance failure
- Using ENI secondary IPs for EKS Pods

### Requestor Managed ENIs

- RDS DB instance is fully managed by AWS but allows customer to control the traffic using security groups. For this, AWS creates a requester managed ENI into customer VPC
- EKS(Control Plane) master nodes are launched in AWS managed VPC and it creates ENIs into your VPC so that it can communicate with EKS worker nodes.
- For AWS Workspaces or Appstream 2.0, the underlying EC2 instances are launched inside AWS managed VPC and ENIs are created into your VPC so that those instance can communicate with applications inside your VPC

Example ~ Amazon Workspace/Appstream 2.0

![](assets/Pasted%20image%2020251025164306.png)

Example ~ Lambda to access VPC Resource

![](assets/Pasted%20image%2020251025164334.png)

### Customer Managed Network/ Dual Home Instances

![](assets/Pasted%20image%2020251025164355.png)

### Secondary IPs for PODs in EKS

![](assets/Pasted%20image%2020251025164444.png)

## Bring Your Own IP (BYOIP)

- You can migrate your Publicly routable IPv4 and IPv6 IP addresses to AWS
- But Why ?
    - Keep your IP address reputation
    - Avoid Changes to IP Address whitelisting
    - Move applications without change in the IP address
    - AWS as a hot standby

### Pre-requisites to BYOIP

- Address range must be registered with Regional Internet registry (RIR) - ARIN or RIPE or APNIC
- The addresses in the IP address range must have a clean history. AWS reserve the right to reject poor reputation IP address ranges.
- The most specific IPv4 address range that you can bring is /24
- The most specific IPv6 address range that you can bring is /48 for CIDRs that are publicly advertised.
- The most specific IPv6 address range that you can bring is /56 for CIDRs that are not publicly advertised (can be advertised over Direct Connect)
- Create a Route Origin Authorization to authorize ASNs 16509 and 14618 to advertise the address range.

### Important Notes on BYOIP

- You continue to own the address range, but AWS advertises it on the internet by default
- After you bring the address range to AWS, it appears in your AWS account as an address pool.
- You can associate these IP addresses to Amazon EC2 instances, Network Load Balancers, and NAT gateways
- You can bring a total of five IPv4 and IPv6 address ranges per Region to your AWS account
