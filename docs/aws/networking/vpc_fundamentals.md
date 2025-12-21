# Amazon VPC

- Amazon VPC ~ Amazon Virtual Private Cloud
- We usually launch AWS resources into a *virtual network* that we define
- VPC benefits of using of scalable infrastructure of AWS

![](assets/Pasted%20image%2020251025122306.png)

Above Diagram represents a Traditional Networking Infrastructure.
It includes devices like switches (Layer 2) and routers (Layer 3). Each physical device is connected to each other over a Physical LAN (layer 1), which is connected together Switch to a Router.
Each router is connected together to the top router, which has the internet access.

We could very well say LAN A, LAN B both are part of same subnet (there are many subnets), as they are connected to same router. So we can build an abstraction of virtual LAN on top of it. And VPC mimics the same concept providing us a top level view of Virtual Subnets and hiding away the entire complexity behind VPC.

![](assets/Pasted%20image%2020251025122804.png)

Network Hierarchy :

AWS Account -> Region -> AZs -> VPCs

Take a look at the diagram here. Reference : [Introduction to AWS](../ai_practitioner/introduction.md)
### AWS Availability Zones

Each Region (geographic) has at least 3 or more Availability Zones. e.g. us-east-1a, us-east-1b, us-east-1c. Here us-east-1 is the region.

All Availability Zones are connected thru a low latency optic fiber with different physical locations (to avoid disaster)

There is a misconception that we should not choose `us-east-1a` and choose other regions just because of the load. But internally `us-east-1a` for you might be `us-east-1b` some other user. AWS decides this based on load and occupancy at the availability zone.

![](../ai_practitioner/assets/Pasted%20image%2020251008094450.png)

![](../ai_practitioner/assets/Pasted%20image%2020251008094508.png)

#### AWS Services scope with respect to VPC

![](assets/Pasted%20image%2020251025123355.png)

NOTE: AZs are mapped to Regions, while Subnets are mapped to VPC.
ELB has scope of VPC Level, EC2 is subnet level.
Route 53 has global scope.
IAM has global scope on the Account.
Dynamo and S3 (regional) are Region Level services.

#### AWS Services inside VPC and outside VPC

![](assets/Pasted%20image%2020251025123420.png)

## VPC Building Blocks

![](assets/Pasted%20image%2020251025123452.png)

- Each Region will contain 3 or more AZs. 
- VPC can cover multiple AZs. 
- Each VPC will have a CIDR range. Ex 10.0.0.0/16 ~ 1,67,77,216 hosts.
- VPC Address range can be divided into Subnets
- EC2 are subnet level service.
- AWS will apply Route Table (*Router*) across subnets or on subnets.
- IGW (Internet Gateway) is the top level router allowing Internet.
- Security/Firewalls
    - Security Groups ~ EC2 level
    - Network ACLs ~ Network Level
- DNS ~ AWS DNS Server (Route53)
### CIDR

NOTE: Make sure you understand these notes first, Very Important for exam.

[Introduction to Networking](../../networking/neteng/fundamentals.md)
[IP](../../networking/neteng/ip.md)

Exercises

- 192.168.0.0/24 = 192.168.0.0 - 192.168.0.255 (256 IP)
- 192.168.0.0/16 = 192.168.0.0 - 192.168.255.255 (65,536 IPs)
- 134.56.78.123/32 = just 1 ~ 134.56.78.123
- 0.0.0.0/0
    - All IPs
- Use following Site : https://www.ipaddressguide.com/cidr

### Subnets, Route Tables & Internet Gateway

Each Subnet is restricted to 1 AZ, not multiple AZs. Both Subnets are connected with Local Router Table & Main Route Table

![](assets/Pasted%20image%2020251025135551.png)

This entry for destination to target (local), will always be present by default. As a result Instance A can simply look up addressing table to find how to send request to B, then will send request to upstream local router.

Essentially Internet Gateway would be the target to traffic to `0.0.0.0/0`

![](assets/Pasted%20image%2020251025135854.png)

Usually in Real-Life we never expose database to external traffic, we usually put it in a private subnet.

A subnet becomes private, when it has no outbound/inbound traffic.

We can create custom Route tables and by default remove internet access from the Route table. In this case Subnet starts following Custom Table, rather than the Main Route Table.

![](assets/Pasted%20image%2020251025140129.png)

#### Route Table

- Contains rules to route traffic
- Main route table is present at VPC Level, while custom route tables can be defined at Subnet levels.
- Each route table will contain default immutable local route for the VPC
- We can modify main route table.

| Destination | Target |
| ----------- | ------ |
| 10.0.0.0/16 | local  |
| 0.0.0.0/0   | igw-id |
#### Public/Private Subnet

Public Subnet

- Has route for internet (2nd entry)
- Instances with Public IP can communicate to Internet
- Ex ~ NAT, web servers, LBs

Private Subnet

- No route to internet
- Instances receive private IPs
- Typically uses NAT for instances to have internet access
- Ex ~ Databases, App server

#### AWS Subnets ~ IP Restrictions

- reserves 5 IPs (first 4 and last IP address) in each subnet
- Example for 10.0.0.0/24, reserved IPs are
    - 10.0.0.0 ~ network address
    - 10.0.0.1 ~ reserved by AWS for VPC Router
    - 10.0.0.2 ~ reserved by AWS for mapping to Amazon-provided DNS
    - 10.0.0.3 ~ Reserved by AWS for future use
    - 10.0.0.255 ~ Network broadcast address, AWS doesn't support broadcast in a VPC, therefore the address is used.
- For Exam, if we need 29 IPs we actually need 35 so choosing a subnet of /27 is not suitable we need to select /26 subnet.

### IP Addresses in VPC

![](assets/Pasted%20image%2020251025141153.png)

NOTE: *Elastic IP* is allocated to AWS account, and remains allocated until released and doesnt' get affected with instance restarts. **Can be mapped to another instance.** (using ENI)

#### VPC having both IPv4 and IPv6 subnets

- VPC supports dual-stack mode
- Resources inside VPC can communicate over IPv4 or IPv6 or both
- IPv4 support can not be disabled for the VPC
- VPC supports IPv6-only subnets

![](assets/Pasted%20image%2020251025141746.png)

NOTE: For IPv6 addressing, VPC CIDR with fixed prefix /56 and subnet CIDR prefix fixed /64. And restarting the instance doesn't change the IPv6 address.

## Firewalls inside VPC

### Security Groups

![](assets/Pasted%20image%2020251025142248.png)

- fundamental of network security in AWS
- They control how traffic is allowed into or out of our EC2 Machines
- It is most fundamental skill to learn to troubleshoot networking issues.
- Has SG1 (inbound) and SG1 (outbound) rules for each SG.
- Security Groups can regulate
    - Access to Ports
    - Authorised IP ranges
    - Control Inbound/Outbound Network
- Security Groups are stateful
- *We can reference another security group as source* :) Ex- All machines serving Web Traffic (Web-Tier) create a SG allow port 80, then we can reference this directly in every EC2 launched. This allows us to edit rules at a single place, rather than changing every machine.
- By default
    - All Inbound traffic is *blocked* by default.
    - All outbound traffic is *authorized* by default.

![](assets/Pasted%20image%2020251025142501.png)
### Network Access Control List (NACL)

- applies at subnet level, hence applies to all instances.
- Stateless ~ we need to explicitly open outbound traffic.
- Contains both Allow and Deny Rules
- Rules are evaluated in the order of the rules number
- Default NACL allows all inbound and outbound traffic, thats we do need notice NACL, it helps blocking subnet level traffic.

![](assets/Pasted%20image%2020251025143401.png)

![](assets/Pasted%20image%2020251025143416.png)

### Network ACLs vs Security Groups

| Security Group                           | Network ACL                                           |
| ---------------------------------------- | ----------------------------------------------------- |
| instance level                           | subnet level                                          |
| allow rules only                         | support allow/deny rules                              |
| stateful (return traffic always allowed) | stateless (return traffic must be explicitly allowed) |
| evaluate all rules before allow traffic  | process rules in number of order                      |
## Default VPC

![](assets/Pasted%20image%2020251025143725.png)

- AWS creates Default VPC in each AWS region
- Creates VPC with CIDR - 172.31.0.0/16
- Creates subnets in every AZ with CIDR /20
- Creates Internet Gateway
- Main route table with route to Internet which makes all subnets public
- If deleted can be recreated.

## NAT

![](assets/Pasted%20image%2020251025150004.png)

- To provide Internet Access to instances in private subnet without IGW
- Performs Network Address Translation when packet leaves the VPC
- NAT Gateway
    - Managed by AWS
    - Highly available within AZ
- NAT Instance
    - NAT EC2 can be launched using Amazon Linux NAT AMI
    - Disabled Source/Destination check on instance
    - Allocate EIP

### NAT Gateway

- AWS Managed NAT, higher bandwidth, better availability, no admin
- Pay by the hour for usage and bandwidth
- NAT is created in a specific AZ, uses an EIP
- 5 Gbps of bandwidth with scaling up to 100Gbps
- No security group to manage/required. NACL at subnet level applies to NAT Gateway
- Supported protocols : TCP, UDP and ICMP
- Uses port 1024-65535 for outbound connection
- NAT Gateway must be created in Public Subnet so that it can communicate with the internet
- NAT Gateway should be allocated Elastic IP

![](assets/Pasted%20image%2020251025150450.png)

![](assets/Pasted%20image%2020251025150514.png)

Notice how NAT doesn't need to have a new public subnet, or doesn't need to be in the same AZ, but should be one of the public subnet and AZ.

### NAT Gateway with High Availability

![](assets/Pasted%20image%2020251025150645.png)

- NAT Gateway is resilient within a single AZ
- Must create multiple NAT Gateway in multiple AZ for fault tolerance
- There is no cross AZ failover needed because if an AZ goes down it doesn't need NAT

[Example Setting up NAT on EC2](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_NAT_Instance.html)
