# Private Connectivity

This is direct connectivity to the Private Hosts on a VPC. Why do we actually need it ?

- Traffic flows over the internet (can be considered less secure)
- Internet connectivity may not provide consistent bandwidth and latency
- NAT devices comes with considerable per hour running cost and data processing charges.
- Might have to un-necessarily expose your servers publicly even if they don't need to be public.

## VPC Peering

![](assets/Pasted%20image%2020251026001034.png)

- Connect two VPC, privately using AWS network
- Make them behave as if they were in same network
- Peered VPCs can be in same region or across Region
- you can do VPC peering with another AWS Account

Caveats:

- VPC CIDRs should be non-overlapping
- You must update route tables in *each VPC's subnets* to ensure instances can communicate across VPC

### VPC Peering Limitations

- Must not have overlapping CIDR
- VPC Peering connection is not transitive
- You can setup only 1 VPC peering connection between 2 VPCs
- Maximum 125 VPC peering connections per VPC

#### VPC Peering invalid scenario - VPN or DX

- VPN or Direct Connect connection to on-premises network

![](assets/Pasted%20image%2020251026001336.png)

#### VPC Peering invalid scenarios - IGW

- Internet access through peered VPC internet gateway
- Internet access through peered VPC NAT Gateway
- Access to S3/DynamoDB through VPCe

![](assets/Pasted%20image%2020251026001446.png)

## VPC Endpoints ~ Gateway & Interface

![](assets/Pasted%20image%2020251026091147.png)

 - VPC endpoints and Private Link, work together to establish secure & private connections between your VPC and supported AWS services, including those hosted by AWS customers or partners

![](assets/Pasted%20image%2020251026091211.png)

Types of Endpoints

- VPC Gateway Endpoint
- Private Link
    - VPC Interface Endpoint
    - VPC Resource Endpoint
    - VPC Service-Network Endpoint
    - Gateway Load Balancer Endpoint

![](assets/Pasted%20image%2020251026091920.png)

#### without VPC endpoint & Private Link
![](assets/Pasted%20image%2020251026091418.png)

#### with VPC endpoints & Private Link
![](assets/Pasted%20image%2020251026091433.png)

### VPC Endpoints & Private Link

- VPC Endpoints allow you to connect to resources in another VPCs and AWS services using a private network instead of public network
- They remove the need of IGW, NAT GW to access AWS services
- Endpoint devices are horizontally scaled, redundant, and highly available without any bandwidth constraint
- Gateway Endpoint : To access Amazon S3 & Dynamo DB only
- Interface Endpoint : to access your services deployed in other VPCs and AWS accounts as well as broad set of other AWS services
- Other types of Endpoints : Gateway Load Balancer, Resource, Service-Networks


## VPC Gateway Endpoint

![](assets/Pasted%20image%2020251026092330.png)

- Enables private connection between VPC and S3/DynamoDB
- Need to modify the route tables and add an entry to route the traffic to S3 or DynamoDB through the gateway VPC endpoint
- When we create Gateway endpoint, a *prefix list* is created in VPC
- *A Prefix List* is collection of IP addresses for AWS services such as Amazon S3 or Dynamo DB
- Prefix list is formatted as `pl-xxxxxxx` and becomes available option in both subnet routing tables and security groups

![](assets/Pasted%20image%2020251026092556.png)

- Prefix list should be added in SG Outbound rules

![](assets/Pasted%20image%2020251026092615.png)

- VPC Gateway endpoints can only be accessed from within VPC in which its created in the same AWS region.
- It's *free* to use, hence always recommended to use to access Dynamo DB or S3 from applications deployed in the VPC.

#### Gateway endpoint access from Remote Networks

![](assets/Pasted%20image%2020251026092908.png)

## VPC endpoint & Private Link

*Not to be confused with VPC Gateway Endpoint.*

![](assets/Pasted%20image%2020251026091433.png)

![](assets/Pasted%20image%2020251026094926.png)

- Types of Endpoint
    - Interface endpoint
    - Resource endpoint
    - Service-network Endpoint
- Support for IPv4 and IPv6 NAT
- Cross-region VPC Endpoints
- UDP traffic support over IPv4 and IPv6
### VPC PrivateLink

![](assets/Pasted%20image%2020251026095039.png)

- VPC endpoints create local IP address (using ENI) in your VPC
- VPC endpoints can be used to connect services inside VPCs with overlapping CIDR blocks
- For High Availability create VPC endpoints across multiple Availability zones
- Uses SGs ~ inbound rules
- VPC endpoint supports IPv4 and IPv6 traffic
- VPC endpoint supports traffic over TCP and UDP
- VPC endpoint can be accessed from other networks, e.g. Peered VPCs, Transit gateway, VPN or Direct Connect
#### VPCs with overlapping CIDR
![](assets/Pasted%20image%2020251026095401.png)

#### VPC endpoint - Availability Zones
![](assets/Pasted%20image%2020251026095437.png)

![](assets/Pasted%20image%2020251026095445.png)

#### VPC endpoint ~ Security Group
![](assets/Pasted%20image%2020251026095626.png)

#### Accessing VPC endpoint from remote Networks

![](assets/Pasted%20image%2020251026095612.png)

## VPC Endpoint DNS

- AWS assigns DNS names to VPC endpoint. It creates availability zone specific DNS and a regional DNS which resolves to the Private IP address of the endpoint ENIs
    - Regional : `vpce-0b7d2995e9dfe5418-mwrths3x.athena.us-east-1.vpce.amazonaws.com`
    - Zonal : `vpce-0b7d2995e9dfe5418-mwrths3x-us-east-1a.athena.us-east-1.vpce.amazonaws.com`
    - Zonal : `vpce-0b7d2995e9dfe5418-mwrths3x-us-east-1b.athena.us-east-1.vpce.amazonaws.com`
- Optionally we can enable Private DNS for the endpoint
    - With Private DNS enabled, consumer VPC can access endpoint services using Service's default DNS like `pce-12345-ab.kinesis.ap-south-1.vpce.amazonaws.com`
    - VPC Setting "Enable DNS hostnames" and "Enable DNS Support" must be set to true.

### VPC Endpoint DNS

![](assets/Pasted%20image%2020251026161331.png)

Without Private DNS all the traffic from API/CLI goes through Internet.

![](assets/Pasted%20image%2020251026161358.png)

Using Endpoint specific DNS name, resolves to Private IP of ENI and connects to WS services privately. Using endpoint DNS in API/CLI is not desirable.

![](assets/Pasted%20image%2020251026161503.png)

With Private DNS Enabled, Applications inside the VPC using API/CLI/SDK do not need any change for accessing AWS Service.

## VPC Endpoint Service

### VPC Endpoint ~ accessing AWS services

![](assets/Pasted%20image%2020251026171126.png)

### VPC Endpoint Services ~ accessing Self Hosted Services

- Most secure & scalable way to expose a service to 1000s of VPC across AWS account
- Doesn't require VPC peering, internet gateway, NAT, route tables,
- Requires a NLB in Provider VPC and VPC endpoint in customer VPC

![](assets/Pasted%20image%2020251026171314.png)

### VPC Endpoint Service AZ considerations

- Service provider VPC should have targets across multiple AZs
- VPC Endpoint in Service Consumer VPC should also be created in corresponding AZs
- In Consumer VPC, application to use zone specific DNS for keeping the traffic in the same AZ
- If using regional endpoints, then DNS will resolve the ENI IPs in round robin fashion
- Optionally, enable cross-zone load balancing for NLB so that it can send traffic to backend instances in another AZ (inter AZ data transfer charges apply)

![](assets/Pasted%20image%2020251026172755.png)

### VPC Endpoint service with on-premise targets

- NLB can have target IPs from your on-premises network if VPC is connected to the on-premises network over the VPN or Direct Connect

![](assets/Pasted%20image%2020251026172914.png)

#### To create VPC endpoint Service Provider VPC

- Choose the NLB (+ availability zones) and register the targets in the Target group
- Create a VPC endpoint Service
    - Choose AWS regions for Cross-region access to the service
    - Configure `Require Acceptance` flag
    - Optionally configure `Enable Private DNS` ~ The DNS must be owned by you
    - Configure IP type
    - Allow other AWS accounts to access your endpoint service by adding AWS account or Role or User ARN in the `Allow Principlas` settings

![](assets/Pasted%20image%2020251026173454.png)
## VPC endpoints Security

### VPC endpoint security - IAM Policies
![](assets/Pasted%20image%2020251026180234.png)

### VPC endpoint default policy

- If no policy is explicitly assigned the default policy is applied
- Custom VPC endpoint Policy can be applied for the supported AWS services
- You can check whether endpoint policy is supported for a given AWS service
- For VPC endpoint service, the default policy is applied.

```json
{
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "*",
            "Resource": "*"
        }
    ]
}
```

### VPC Endpoint Policy

- VPC Endpoint Policy to restrict access to a specific AWS service resources
![](assets/Pasted%20image%2020251026180550.png)

- VPC Endpoint Policy to restrict access for a specific IAM account/user/role

![](assets/Pasted%20image%2020251026180627.png)

### AWS Resource based policy - S3 bucket policy

![](assets/Pasted%20image%2020251026180726.png)

## Other VPC endpoint types

### Gateway Load Balancer Endpoint

- An endpoint to direct traffic from VPC to GWLB
- Primarily used to insert third - party virtual appliances transparently into traffic flows.

![](assets/Pasted%20image%2020251026180908.png)

### Resource Endpoint

- Access VPC resources privately using Privatelink
- For cross-account access the resource need to be shared using RAM
- Resources can be identified using ARN (for RDS) or publicly resolvable domain-name or private IPv4 address range.
- No need to have NLB

![](assets/Pasted%20image%2020251026181052.png)

### Service Network Endpoint

#### VPC endpoint for lattice network

- A VPC endpoint of type service network connects a VPC to a service network
- Client traffic that comes from outside the VPC over a VPC peering connection, Transit Gateway, Direct Connect, or VPN can use the VPC endpoint to read lattice services.

![](assets/Pasted%20image%2020251026181215.png)

## Other VPCe architectures

### Accessing on-premises services

![](assets/Pasted%20image%2020251026181820.png)

VPC Interface Endpoint can be accessed from over the

- From inside AWS
    - VPC peering connection
    - AWS Transit Gateway
- From outside AWS
    - AWS Direct Connect
    - AWS Site-to-Site VPN
### Accessing from peered or connected VPC

![](assets/Pasted%20image%2020251026181953.png)
![](assets/Pasted%20image%2020251026182309.png)
![](assets/Pasted%20image%2020251026182349.png)

### Accessing from on-premises network

![](assets/Pasted%20image%2020251026182425.png)
![](assets/Pasted%20image%2020251026182443.png)
![](assets/Pasted%20image%2020251026182508.png)
![](assets/Pasted%20image%2020251026182605.png)

### Centralized VPC Endpoints

![](assets/Pasted%20image%2020251026182751.png)
![](assets/Pasted%20image%2020251026182804.png)
### DNS Resolution

![](assets/Pasted%20image%2020251026182859.png)
#### Option 1 : Create PHZ and associate with spoke VPCs
![](assets/Pasted%20image%2020251026182959.png)
#### Option 2 : Use R53 resolver endpoints

![](assets/Pasted%20image%2020251026183011.png)
## VPC Peering vs VPC Endpoints

- VPC peering is useful when there are many resources that should communicate between peered VPCs
- PrivateLink should be used when you want to allow access to only single application hosted in your VPC to other VPCs without peering the VPCs
- When there is overlapping CIDRs, VPC peering connection can not be created. However private link does support overlapping CIDR
- We can create a maximum of 125 peering connections. There is no limit on private link connections.
- VPC peering enables bidirectional traffic origin. PrivateLink allows only consumer to originate the traffic.

## Summary

- There are different types of the VPC endpoints (PrivateLink):
    - Interface endpoint
    - Gateway Load Balancer endpoint
    - Resource endpoint
    - Service-network endpoint (VPC lattice)
- Interface endpoint creates ENI into the consumer VPC subnets (AZs) and receives Private IP address from the subnet CIDR range. 
- Uses Security Groups – inbound rules
- VPC endpoint supports IPv4 and IPv6 traffic.
- VPC endpoint supports traffic over TCP and UDP
- VPC endpoint can be used to connect VPCs with overlapping CIDR blocks
- VPC endpoint can be accessed from other networks e.g. Peered VPCs, Transit gateway, VPN or Direct Connect
- VPC interface endpoint supports cross-region access
- Traffic originates from the resources in the consumer VPC, and endpoint service can only respond to the request.
- VPC Interface endpoint receives the Regional and zonal DNS name.
- Use AZ specific DNS to save cross-AZ data transfer cost
- VPC endpoint policy to restrict access to specific AWS resources and principals