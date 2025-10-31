# Transit Gateway (TGW)

- Allows customers to interconnect thousands of VPCs and on-premises networks
- Transit Gateway attachments
    - One or more VPCs
    - Peering connection with another TGW
    - A connect SD-WAN/third party network appliances
    - VPN
    - Direct Connect Gateway
- Transit Gateway features ~ Multicast support, MTU, appliance mode, AZ consideration, TGW Sharing
- Architectures ~ Centralized traffic inspections, egress, interface endpoints etc.

![](assets/Pasted%20image%2020251026235815.png)
### Transit Gateway with multiple VPCs

Since VPC Peering doesn't have transitive property, we can use Transit Gateway!
NOTE: Transit Gateway is regional router.

![](assets/Pasted%20image%2020251026235825.png)

#### Transit Gateway across AWS Regions
![](assets/Pasted%20image%2020251027000003.png)
#### Transit Gateway with AWS site-to-site VPN
![](assets/Pasted%20image%2020251027000014.png)
#### Transit Gateway with Direct Connect
![](assets/Pasted%20image%2020251027000026.png)
#### Transit Gateway with 3rd party appliances for traffic inspection
![](assets/Pasted%20image%2020251027000039.png)


## Transit Gateway VPC attachments & Routing

### TGW Attachments
![](assets/Pasted%20image%2020251027090054.png)
### TGW Route Tables

- TGW Route table is populated automatically with Attachments, but each attachment will need to update their route table.
- NOTE: Attachments are AZ specific within a VPC

![](assets/Pasted%20image%2020251027090142.png)
![](assets/Pasted%20image%2020251027090154.png)
![](assets/Pasted%20image%2020251027090208.png)

## Transit Gateway Attachment specific routing

### Routing Control with Attachment RouteTables

- TGW support VRF (Virtual Routing and Forwarding), by default TGW RT (default) table allows connection between all VPCs, we restrict the access using Attachment RouteTables to restrict connections.
- To do so, disable default route table *propagation* and *association* while creating TGW.

![](assets/Pasted%20image%2020251027101423.png)
![](assets/Pasted%20image%2020251027101432.png)

## Transit Gateway VPC Network Patterns

### Flat Network

- All VPCs can communicate with each other, Default Route Tables & Associations,
- All VPCs will need to add a route table entry for TGW

![](assets/Pasted%20image%2020251027102126.png)

### Segmented Network

- Not All VPCs need to communicate then we can use following topology.
- We create two routing domain
    - Routing domain for VPCs
    - Routing domain for VPN
- Allows full connectivity from VPN to all VPCs, but not among VPCs

![](assets/Pasted%20image%2020251027102248.png)
## Transit Gateway AZ considerations

- When you attach a VPC to a TGW, you must enable one or more AZs to be used by TGW to route traffic to resources in the VPC subnets
- To enable each AZ, you specify exactly one subnet range to save IPs for workload subnets
- The TGW places a network interface in that subnet using one IP address from the subnet
- After you enable an AZs, traffic can be routed to all subnets in that zone, not just specified subnet
- Resources that reside in AZ where there is no transit gateway attachment cannot reach TGW

![](assets/Pasted%20image%2020251027102735.png)

## Transit Gateway AZ affinity & Appliance mode

### TGW AZ Affinity

#### Source & Destination in same AZ

TGW tries to keep traffic in same AZ, until it reaches its destination.

![](assets/Pasted%20image%2020251027103248.png)
#### Source & Destination in different AZ
- This causes Asymmetric Routing, when the Destination is in different AZs

![](assets/Pasted%20image%2020251027103518.png)

### TGW - Stateful Appliance

![](assets/Pasted%20image%2020251027103738.png)
With appliance mode disabled, Appliance B, will drop entire traffic because it never saw the originating request.

![](assets/Pasted%20image%2020251027103938.png)
## Transit Gateway Peering

- Transit Gateways are regional routers, which means we can connect only VPCs in same region,
- For inter region connectivity we can peer the transit gateway across regions
- static routes need to added for peering connection (no BGP)

![](assets/Pasted%20image%2020251027104607.png)
![](assets/Pasted%20image%2020251027104142.png)

- The inter-Region traffic is encrypted, traverses the AWS global network and is not exposed to public internet. Supports bandwidth upto 50Gbps
- Use unique ASNs for peered transit gateway (as much as possible)

![](assets/Pasted%20image%2020251027104253.png)
## Transit Gateway Connect Attachment

- You can create a transit gateway Connect attachment to establish a connection between a transit gateway and third-party virtual appliances (such as SD-WAN appliances) running in a VPC
- A Connect attachment uses an existing VPC or AWS Direct Connect attachment as the underlying transport mechanism.
- Supports Generic Routing Encapsulation (GRE) tunnel protocol for high performance, and Border Gateway Protocol (BGP) for dynamic routing.

![](assets/Pasted%20image%2020251027105130.png)

### TGW Connect attachment over VPC transport attachment

![](assets/Pasted%20image%2020251027105249.png)

### TGW Connect attachment over the DX transport attachment

Transit Gateway Connect can be used as a third-party branch or customer gateway appliance running in an on-premises network that uses AWS Direct Connect as transport.

![](assets/Pasted%20image%2020251027105321.png)

- Connect attachments do not support static routes. BGP is a minimum requirement for Transit Gateway Connect.
- Transit Gateway Connect supports a maximum bandwidth of 5 Gbps per GRE tunnel. Bandwidth above 5 Gbps is achieved by advertising the same prefixes across multiple Connect peer (GRE tunnel) for the same Connect attachment.
- A maximum of four Connect peers are supported for each Connect attachment there by providing total 20 Gbps bandwidth per connection
## Transit Gateway VPN Attachment

#### Single Site-to-Site VPN Connection over Virtual Private Gateway (VGW)
![](assets/Pasted%20image%2020251027105518.png)
#### Connecting multiple branch offices over Site-to-Site VPN
![](assets/Pasted%20image%2020251027105549.png)

#### Connecting multiple VPCs over Site-to-Site VPN connections
![](assets/Pasted%20image%2020251027105633.png)


Above all scenarios can be simplified using 1 TGW in between

#### Simplify Site-to-Site VPN network with Transit Gateway

![](assets/Pasted%20image%2020251027105723.png)

#### Accelerated Site-to-Site VPN network with Transit Gateway

![](assets/Pasted%20image%2020251027105744.png)

#### Limited n/w throughput with multiple VPN Connections over VGW

![](assets/Pasted%20image%2020251027105809.png)

#### ECMP over Transit Gateway & Site-to-Site VPN for higher aggregate throughput

![](assets/Pasted%20image%2020251027105833.png)
#### ECMP over Transit Gateway with dual VPN
![](assets/Pasted%20image%2020251027105853.png)

## Transit Gateway & Direct Connect

- Using Direct Connect Gateway over a Private VIF
- Allows connecting maximum of 10 VPCs

Connecting without TGW

![](assets/Pasted%20image%2020251027110846.png)

Direct Connect with Transit Gateway

![](assets/Pasted%20image%2020251027110910.png)

#### IPSec VPN to Transit Gateway over Direct Connect

![](assets/Pasted%20image%2020251027110943.png)

## Transit Gateway Multicast

### Multicast

- Communication protocol used for delivering single stream of data to multiple computers simultaneously
- Destination is a multicast group address
    - Class D - 244.0.0.0 to 239.255.255.255
- Connections are based on UDP based transport
- One way communication
- Multicast components
    - Multicast Domain
    - Multicast Group and member
    - Multicast source and receivers
    - Internet Group Management Protocol (IGMP)

More Here : https://en.wikipedia.org/wiki/Multicast

![](assets/Pasted%20image%2020251027122238.png)


### Multicast considerations for TGW

- Transit Gateway supports routing multicast traffic between subnets of attached VPCs
- A subnet can only be in one multicast-domain
- Hosts (ENIs) in the subnet can be part of one or more multicast group within the Multicast Domain
- Multicast group membership is managed using the VPC Console or the AWS CLI, or ICMP
- IGMPv2 support attribute determines how hosts join the multicast group. Members send `JOIN` or `LEAVE` IGMP message.

![](assets/Pasted%20image%2020251027122252.png)

- Transit gateway issues an IGMPv2 QUERY message to all members every two minutes. Each member sends an IGMPv2 JOIN message in response, which is how the members renew their membership.
- Members that do not support IGMP must be added or removed from the group using the Amazon VPC console or the AWS CLI.
- Igmpv2Support attribute determines how group members join or leave a multicast group. When this attribute enabled, members can send JOIN or LEAVE messages.
- StaticSourcesSupport multicast domain attributes determine whether there are static multicast sources for the group.

### Important Considerations for TGW

- A non-Nitro instance cannot be a multicast sender. If you use a non-Nitro instance as a receiver, you must disable the Source/Destination check
- Multicast routing is not supported over AWS Direct Connect, Site-to-Site VPN, TGW peering attachments, or transit gateway Connect attachments
- The source IP of these IGMP query packets is 0.0.0.0/32, destination IP is 224.0.0.1/32 and the protocol is IGMP(2)
- Security group configuration on the IGMP hosts (instances), and any ACLs configuration on the host subnets must allow these IGMP protocol messages

#### Multicast traffic in a VPC

![](assets/Pasted%20image%2020251027121029.png)

#### Integrating external multicast services

![](assets/Pasted%20image%2020251027121054.png)

![](assets/Pasted%20image%2020251027121104.png)
#### NACL & Security Group for Multicast
![](assets/Pasted%20image%2020251027122411.png)

## TGW Architecture

### Centralized egress internet
![](assets/Pasted%20image%2020251027123050.png)

#### Using NAT Gateway

- Use NAT gateway's each AZ for high availability for saving inter-AZ data transfer cost.
- If one AZ entirely fails, all traffic will flow via the Transit Gateway and NAT gateway endpoints in the other Availability Zones
- A NAT gateway can support 55k simultaneously connections to each unique destination
- NAT gateway can scale from 5 Gbps to 100 Gbps

![](assets/Pasted%20image%2020251027123307.png)

- Blackhole entry route blocks the interVPC communication,
- if removed, then request goes till one of the NAT gateway and returns back to second VPC
- This architecture doesn't necessarily save cost !!!
### Centralized traffic inspection with Gateway Load Balancer
![](assets/Pasted%20image%2020251027130709.png)
![](assets/Pasted%20image%2020251027130729.png)

#### Inter VPC Traffic
![](assets/Pasted%20image%2020251027131334.png)
#### Internet Traffic
![](assets/Pasted%20image%2020251027131313.png)

Important Points

- Using AWS PrivateLink, GWLB Endpoint routes traffic to GWLB. Traffic is routed securely over Amazon network without any additional configuration.
- GWLB encapsulates the original IP traffic with a *GENEVE* header and forwards it to the network appliance over UDP port 6081.
- GWLB uses 5-tuples or 3-tuples of an IP packet to pick an appliance for the life of that flow. This creates session stickiness to an appliance for the life of a flow required for stateful appliances like firewalls.
- This combined with Transit Gateway Appliance mode, provides session stickiness irrespective of source and destination AZ.
- Refer to this blog for further details: https://aws.amazon.com/blogs/networking-and-content-delivery/centralized-inspection-architecture-with-aws-gateway-load-balancer-and-aws-transit-gateway
### Centralized VPC interface endpoints

#### Interface Endpoints
![](assets/Pasted%20image%2020251027131647.png)

#### Centralized VPC interface endpoints

![](assets/Pasted%20image%2020251027131706.png)

#### DNS Resolution for above Architecture
![](assets/Pasted%20image%2020251027131743.png)
![](assets/Pasted%20image%2020251027131754.png)

#### Centralized VPC interface endpoint

- VPC interface endpoints provides the regional and AZ level DNS endpoints
- The regional DNS endpoint will return the IP address for all the AZ endpoints
- In order to save the inter-AZ data transfer cost from Spoke VPC to Hub VPC, you can use the AZ specific DNS endpoints. Selection has to be done by client

![](assets/Pasted%20image%2020251027132239.png)

### Cost Analysis of Various Approaches

![](assets/Pasted%20image%2020251027121225.png)

#### Cost of centralized VPC interface endpoints
![](assets/Pasted%20image%2020251027121241.png)
#### Using VPC peering instead of Transit Gateway
![](assets/Pasted%20image%2020251027121254.png)

## Transit Gateway Sharing

- Use AWS RAM to share a transit gateway for VPC attachments across accounts or across your org in AWS organizations

![](assets/Pasted%20image%2020251027121950.png)

- An AWS Site-to-Site VPN attachment must be created in the same AWS account that owns the transit gateway.
- An attachment to a Direct Connect gateway can be in the same AWS account as the Direct Connect gateway, or a different account from the Direct Connect gateway.
- When a transit gateway is shared with the AWS account, that AWS account cannot create, modify, or delete transit gateway route tables, or route table propagations and associations.
- When the transit gateway and the attachment entities are in different accounts, use the Availability Zone ID to uniquely and consistently identify the Availability Zone. For example, use1-az1 is an AZ ID for the us-east-1 Region and maps to the same location in every AWS account.

## VPC Peering vs Transit Gateway

| Feature                                  | VPC Peering                                                                                                      | Transit Gateway                                                                          |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Architecture**                         | One-One connection – Full Mesh                                                                                   | Hub and Spoke with multiple attachments                                                  |
| **Hybrid Connectivity**                  | Not supported                                                                                                    | Supported hybrid connectivity via VPN and DX                                             |
| **Complexity**                           | Simple for fewer VPCs, Complex as number of VPCs increase                                                        | Simple for any number of VPCs and hybrid network connectivity                            |
| **Scale**                                | 125 peering / VPC                                                                                                | 5000 attachments / TGW                                                                   |
| **Latency**                              | Lowest                                                                                                           | Additional Hop                                                                           |
| **Bandwidth**                            | No limit                                                                                                         | 50 Gbps / attachment                                                                     |
| **Ref Security Group**                   | Supported                                                                                                        | Not supported                                                                            |
| **Subnet Connectivity**                  | For all subnets across AZs                                                                                       | Only subnets within the same AZ in which TGW attachment is created                       |
| **Transitive Routing (e.g. IGW access)** | Not supported                                                                                                    | Supported                                                                                |
| **TCO (Total Cost of Ownership)**        | Lowest – Only Data transfer cost (free within same AZ, $0.01 across AZs in each direction, $0.02 across regions) | Per attachment cost + Data transfer cost (e.g. N. Virginia: $0.05 per hour + $0.02 / GB) |

## Summary

- DNS resolution is supported for all VPCs attached to the TGW
- Supports resolving `public` DNS names to Private IP's for EC2
- TGW can be shared using Resource Access Manager (RAM) across AWS Accounts
- Billed per hour, per attachment
- Data processing charges apply for each gigabyte sent from an Amazon VPC or Site-to-Site VPN to the AWS Transit Gateway
- Bandwidth at TGW is limited to 1.25 Gbps per VPN tunnel. With ECMP Transit Gateway can support up to 50 Gbps total VPN bandwidth
- Transit Gateway supports up to 5000 attachments
- Transit gateway supports MTU of 8500 bytes for traffic between VPCs, AWS DCX, TGW Connect, and peering attachments
- Traffic over VPN connection can have an MTU of 1500 bytes