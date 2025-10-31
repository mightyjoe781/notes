# VPC Lattice

## Introduction

- Simplifies service-to-service (app-to-app) communication
- Enables secure, consistent connectivity without needing complex networking peering like VPC peering or Transit Gateways
- Provides Service Discovery and Dynamic Routing Capabilities
- Supports *Zero Trust* architectures with centralized access controls, IAM Authentication, and context-specific authorization.

### without VPC Lattice : Inter Services Communications


![](assets/Pasted%20image%2020251029103348.png)

If services want to interact with each other, then we can probably use VPC Peering, but it is not transitive in nature.
To solve that we can deploy Transit Gateway, but that opens up entire Mesh Connectivity.

Another Option is to use Private Link, which is difficult to manage and scale out & Inter Service communication becomes unmanageable.


### With VPC Lattice

![](assets/Pasted%20image%2020251029103631.png)
## VPC Lattice Components

![](assets/Pasted%20image%2020251029103834.png)

- Service Network
- Service
- Resource
- Service Directory
- Auth Policies

### Service Network

![](assets/Pasted%20image%2020251029103923.png)

- A service network is a logical boundary for a collection of services and resource configurations.

### VPC Lattice - Service

- An independently deployable unit of software that delivers a specific task or function.
- A service can run on EC2 instances, ALB, ECS/EKS/Fargate containers, Lambda functions or IP address
- VPC Lattice service has target groups, listeners, and rules
- Target groups can have weights and Rules can have priorities and conditions like header match, method match or path match

![](assets/Pasted%20image%2020251029104014.png)

### VPC Lattice - Resource

- A resource is an entity such as an Amazon RDS database, a cluster of nodes, an instance, an application endpoint, a domain-name target, or an IP address.
- Resource gateway is a point of ingress in which resources reside

![](assets/Pasted%20image%2020251029104101.png)
### VPC Lattice Auth Policies

- Fine-grained authorization policies that can be used to define access to services.
- Auth policy can be attached to individual services or to the service network.
- Auth type can be None or AWS_IAM
- By default, all requests are implicitly denied when auth is AWS_IAM
- Authorization evaluation
    - Collect all IAM identity-based policies and auth policies
    - Requestor should have IAM allow permissions in their identity-based policy in their AWS account (IAM User, Role).
    - VPC lattice service network auth policy and/or VPC lattice service auth policy should have explicit allow for the principal or None to allow the access

## VPC Lattice Network Association

### Service Association

![](assets/Pasted%20image%2020251029104925.png)

- Service is discoverable and reachable from VPC Lattice network when you associate a service with the VPC lattice network
- Service can be in the same AWS account or can be shared using RAM from another AWS account
### Resource Configuration Association

![](assets/Pasted%20image%2020251029104941.png)

- Resource is discoverable and reachable from VPC Lattice network when you associate a resource configuration with the VPC lattice network
- Resource configuration can be in the same AWS account or can be shared using RAM from another AWS account

### VPC Association

- Clients in the consumer VPC can access the VPC Lattice network over the link-local address 169.254.171.x

![](assets/Pasted%20image%2020251029105013.png)

![](assets/Pasted%20image%2020251029105024.png)
### VPC endpoint Association

![](assets/Pasted%20image%2020251029105114.png)

- A VPC endpoint of type service network connects a VPC to a service network.
- Client traffic that comes from outside the VPC over a VPC peering connection, Transit Gateway, Direct Connect, or VPN can use the VPC endpoint to reach lattice services.
- When you create a VPC endpoint in a VPC, IPs from the VPC (and not link local IPs) are used to establish connectivity to the service network.

![](assets/Pasted%20image%2020251029105125.png)


NOTE: If the VPC in which Service is hosted is not associated with the Service network over VPC association, then that Service can not initiate the request for other Service. It can only respond to the requests.

![](assets/Pasted%20image%2020251029105217.png)
![](assets/Pasted%20image%2020251029105228.png)

### VPC Lattice Responsibilities

- Admin
    - Create the service Network
    - Define Access Control
    - Associate the Service Network to VPCs
- Dev
    - Create the service
    - Define routing and authorization
    - Associate the services to service network

## VPC Lattice traffic Flow

![](assets/Pasted%20image%2020251029104800.png)
![](assets/Pasted%20image%2020251029104812.png)
![](assets/Pasted%20image%2020251029104821.png)
![](assets/Pasted%20image%2020251029104833.png)

## More on VPC Lattice

### VPC Lattice - Sharing with RAM

AWS Resource Access Manager (RAM) : Share Service networks, services, and resource configurations

![](assets/Pasted%20image%2020251029104436.png)

### VPC Lattice – Overlapping CIDRs, IPv6

- VPCs can have overlapping CIDRs
- Supports IPv4 and IPv6 traffic
- VPC lattice performs the NAT/NAT64 to allow
    - Overlapping CIDRs
    - IPv4 to IPv6 traffic
    - IPv6 to IPv4 traffic

![](assets/Pasted%20image%2020251029104522.png)

## VPC Lattice common architectures

- Connectivity between application within the VPC

![](assets/Pasted%20image%2020251029104608.png)

- Connectivity for accessing VPC lattice service in AWS from on-premises network

![](assets/Pasted%20image%2020251029104640.png)

- Connectivity for accessing on-premises application from AWS

![](assets/Pasted%20image%2020251029104704.png)

- Connectivity for accessing VPC lattice application from Internet

![](assets/Pasted%20image%2020251029104722.png)