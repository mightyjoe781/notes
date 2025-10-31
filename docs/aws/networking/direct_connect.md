# Direct Connect (DX)

Direct Connect doesn't map to any specific layer of OSI Model, rather it encompasses multiple layers.

![](assets/Pasted%20image%2020251028133535.png)

AWS Direct Connect : *A dedicated network connection from on-premises to AWS*

![](assets/Pasted%20image%2020251028133716.png)

Advantages

- Low Latency & Consistent Bandwidth
- Lower data transfer Cost
- Access AWS Private Network (VPC) and AWS public services endpoints (e.g. S3, DynamoDB)

Important Points

- Leverages AWS Global Network Backbone
- DX locations are provided by authoritative 3rd party providers
- 115 DX locations across 31 AWS regions
- End to end provisioning takes 4-12 weeks
- Get Bandwidth of 1, 10 or 100 Gbps with Dedicated connections
- Get sub-1 Gbps bandwidth (50/100/200/400/500 Mbps, 1,10 Gbps) by leveraging AWS Direct Connect APN partner

### High Level Architecture

![](assets/Pasted%20image%2020251028133911.png)

## DX Network Requirements

- Single-Mode Fiber
    - 1000BASE-LX (1310 nm) transceiver for 1G
    - 10GBASE-LR (1310 nm) transceiver for 10G
    - 100GBASE-LR4 for 100G
- 802.IQ VLAN encapsulation must be supported ~ Virtual LAN, even though physically different hosts are behind different routers, it will appear as single LAN. Search for Trunk, VLAN Tagging
- Auto-negotiation for the port must be disabled for port speed more than 1Gbps
- End Customer Router (on-premises) must support Border Gateway Protocol (BGP) and BGP MD5 authentication
- (optional) Bidirectional Forwarding Detection ~ failure detection within 1 second

## BGP Autonomous System (AS) and ASN

![](assets/Pasted%20image%2020251028134716.png)

In a BGP system, all the connection points are called as BGP Peers which are uniquely identifiable using ASN

- Public and Private ASN
    - Public ASNs are assigned by IANA via Regional Internet Registries (RIRs)
    - You need to use the Public ASN if you are exchanging routes over a public internet
    - You can use private ASN for private connection between two AAS
- 2 Byte (16 bit) ASN (0-65535)
- 4 Bytes (32 bit) ASN (0 - 4294967295)
## DX Connection Types

- **Dedicated connections** : 1Gbps, 10 Gbps, 100 Gbps capacity
    - Physical ethernet port dedicated to a customer
    - Request made to AWS first then completed by AWS Direct Connect Partner
    - Can be either setup by your Network Provider or AWS Direct Connect Partner
- **Hosted Connections**
    - 50, 100, 200, 300, 400, 500 Mbps and 1 Gbps, 2 Gbps, 5 Gbps, 10 Gbps
    - Connection requests are made via AWS Direct Connect Partners
    - 1, 2, 5, 10 Gbps available at select AWS Direct Connect Partners
    - AWS uses traffic policing on hosted connections – excess traffic is dropped

### Dedicated Connection ~ AWS Account

![](assets/Pasted%20image%2020251028140000.png)

![](assets/Pasted%20image%2020251028140028.png)

### Hosted Connection ~ AWS Account

![](assets/Pasted%20image%2020251028140115.png)
![](assets/Pasted%20image%2020251028140130.png)

Hosted VIF is used in organization where central team owns the account which has provisioned DX service and provides it to other AWS Account.

### Hosted VIF

![](assets/Pasted%20image%2020251028140349.png)
![](assets/Pasted%20image%2020251028140413.png)

## Setup Direct Connect Connections

### Dedicated connection - Sequence of Events

1. You select the AWS region, DX location and submit the connection request via AWS console or CLI or API
2. AWS provisions your port within 72 hrs and provide you with the LOA-CFA (Letter of Authorization – Connection facility assignment)
3. LOA contains the demarcation details of assigned port within the facility
4. If your organization has physical presence in DX location, then you can request for cross-connect within the facility to connect to AWS device
5. If not, you provide the copy of LOA to DX APN partner and partner places the order for cross-connect
6. After connection is up, you receive Tx/Rx optical signal at your equipment
7. Now, you can create Private or Public Virtual Interfaces to connect to your VPC or public AWS services

### Hosted connection – Sequence of events

- To order Hosted connection, you don’t need to get LOA. You can directly contact a Direct Connect Partner to order the connection
- You provide your 12-digit AWS account number to the partner
- Partner will setup the hosted connection and this connection will be available in your account (in the given region) to accept it
- Once you accept the connection, it enables the billing for associated port hours and data transfer charges

### Hosted VIF

- Don’t get confused with Hosted Connection
- When creating a VIF you may choose “Another AWS account”
- You are still the owner of the Direct connect Connection however the VIF is created in another AWS account who must accept it
- For Private VIF, the other account should also associate it with VGW
- A connection of less than 1 Gbps supports only one virtual interface.
- Typically used in a scenario where centralized network team manages the DX connection and provisions VIFs for business accounts

## Introduction to DX Virtual Interfaces (VIFs)

### VIF (logical connectivity)

- In order to use the DX connection you must provision the Virtual Interfaces
- A VIF is a configuration consisting primarily of an 802.1Q VLAN
- There are 3 types of the VIFs
    - Public VIF - Enables the connectivity to all AWS public IP addresses
    - Private VIF - Enables the connectivity to VPC via Virtual Private Gateway or Direct Connect Gateway
    - Transit VIF – Enables the connectivity to Transit Gateways via Direct Connect gateway

![](assets/Pasted%20image%2020251028142639.png)
![](assets/Pasted%20image%2020251028142659.png)

### VIFs for Dedicated vs Hosted Connection

![](assets/Pasted%20image%2020251028142721.png)

## VIF Parameters

- Connection: AWS DX connection or a LAG
- VIF Type: Public or Private or Transit
- VIF Name: Anything
- VIF Owner: Your AWS account or other AWS account (hosted VIF)
- Gateway Type (Private VIF only)
- Virtual Private Gateway
- Direct Connect Gateway
- VLAN
    - Not duplicated on same DX connection (1-4094)
    - For hosted connection VLAN ID is already configured by the partner
- BGP address Family – IPv4 or IPv6
- BGP Peer IP Addresses
    - Public VIF (IPv4) - Public IPs (/30) allocated by you for the BGP session. Request to AWS if you don’t have it.
    - Private VIF (IPv4) - Specify private IPs in the range 169.254.0.0/16. By default AWS provides address space.
    - IPv6: Amazon automatically allocates you a /125 IPv6 CIDR. You cannot specify your own peer IPv6 addresses.
- BGP ASN
    - Public or Private BGP ASN
    - Public ASN must be owned by the customer and assigned by IANA
    - Private ASN can be set by you and must be between 64512 to 65534 (16-bit) or 1 to 2147483647 (32-bit)
- BGP MD5 authentication key. If not provides, AWS generates authentication key
-  Prefixes to be advertises (Public VIF only)
    - Public IPv4 routes or IPv6 routes to advertise over a BGP

## Public VIF

![](assets/Pasted%20image%2020251028145203.png)

- Enables your network to connect to all AWS Public IPs globally
- You can access services outside VPC eg S3, SQS, DynamoDB and other public endpoints like AWS managed VPN (VGW) Public IPs
- To create a public VIF with IPv4 addresses, you need to provide both the AWS router public IPs and your side of the router public IPs with /30 CIDR
- In case you don’t have your own Public IPs for peering, raise a support case to get it from AWS owned IP ranges (AWS provides /31 range)
- You must also specify the IPv4 address prefixes you want to advertise
- AWS verifies with Internet registries that these IP prefixes are owned by you and you are authorized to advertise those prefixes
- AWS advertises all Amazon prefixes over a BGP session. These includes prefixes for AWS services like EC2, S3 and Amazon.com
- No access to non-amazon prefixes
- Refer ip-ranges.json for current list of Amazon prefixes
- At customer router the firewall can be use to restrict access to and from specific Amazon prefixes
- From customer router to AWS maximum 1000 route prefixes can be advertised per Border Gateway Protocol (BGP) session

## Private VIF

![](assets/Pasted%20image%2020251028145145.png)

- Enables your network to connect to resources inside VPC using Private IPs for resources like EC2, RDS, Redshift over Private IPs
- You must attach your VPC to VGW and associate VGW with Private VIF
- Private VIF and VGW must be in the same AWS Region
- On BGP session, customer router will receive all the prefixes of VPC
- You can announce a maximum of 100 prefixes to AWS. These routes can be automatically be propagated into subnet route tables
- In order to advertise more than 100 prefixes, you should summarise the prefixes into larger range to reduce number of prefixes
- The propagated routes will take precedence over default route to internet via IGW
- Supports MTU of 1500 (default) and 9001 for propagated routes

### Private VIF - What you can’t access inside VPC?

- Does not provide access to VPC DNS resolver at Base + 2
- Does not provide access to VPC Gateway endpoints
## Transit VIF

![](assets/Pasted%20image%2020251028145050.png)
![](assets/Pasted%20image%2020251028145014.png)

- Enables the connection between Direct Connect and Transit Gateway
- Transit VIF is connected to Direct Connect Gateway and Direct Connect Gateway connects to Transit Gateway
- Support MTU of 1500 and 8500 (Jumbo Frames)
- You can attach multiple Transit Gateways to a single DX Gateway
- You can attach multiple DX Gateways to a single Transit Gateway
- The ASN for DX Gateway and Transit Gateway must be different. If you use the default ASN (64512) for both of them then the association fails.

## DX Gateway with Private VIF and Virtual Private Gateway

Problem : I want to access multiple VPCs over a same Direct Connect connection
solution: Use AWS Direct Connect Gateway

![](assets/Pasted%20image%2020251028145629.png)

- Global network device – Accessible in all regions
- Direct Connect integrates via a private VIF or a transit VIF
- DX Gateway is used for VPC <-> On-premise connectivity and can not be used for Public endpoint connectivity
- The Private VIF or Transit VIF and Direct Connect gateway must be owned by same AWS account however VPCs (VGWs) or Transit Gateways can be from same or different AWS accounts
- Overlapping CIDRs for VPCs are not allowed
- VPC to VPC communication is not allowed via DX Gateway
- Maximum 100 routes each for IPv4 and IPv6 can be advertised from on-premises to AWS (same as Private VIF and Transit VIF limit)
- Single Direct Connect Gateway can connect to 20 VGWs (VPCs) and this limit may increase in the future.

## DX Gateway Architectures

### Multiple Direct Connect Gateways
![](assets/Pasted%20image%2020251028145924.png)
### DX Gateway and multiple customer sites

![](assets/Pasted%20image%2020251028145906.png)
![](assets/Pasted%20image%2020251028145850.png)

## Direct Connect with Transit VIF and TGW

### DX Gateway with TGW
![](assets/Pasted%20image%2020251028150205.png)

### Multiple Transit VIFs
![](assets/Pasted%20image%2020251028150341.png)
### DX Gateway with Multiple TGWs
![](assets/Pasted%20image%2020251028150314.png)
### TGW Routes advertisements
![](assets/Pasted%20image%2020251028150328.png)

NOTE: Transit VIF and Direct Connect Gateway must be
owned by same AWS account, Transit Gateways can be owned by different AWS
accounts

![](assets/Pasted%20image%2020251028150626.png)

There is no routing between VPCs by default and requires Peering Connection

![](assets/Pasted%20image%2020251028150844.png)
Multiple customer sites & routing

![](assets/Pasted%20image%2020251028150920.png)

![](assets/Pasted%20image%2020251028150959.png)

## AWS Direct Connect - Site Link

Connects on-premises networks through the AWS global network backbone

![](assets/Pasted%20image%2020251028151308.png)

- SiteLink can be enabled for a Private VIF or a Transit VIF
- Supported on any combination of a dedicated or a hosted DX connection with different port speeds
- Takes the shortest path for the traffic sent over AWS global network
- Turn SiteLink on or off in minutes
- Supports both IPv4 and IPv6 routing prefixes and traffic
- Full mesh or isolated network connections between customer locations
- Cost: $0.50/hr + Data transfer cost
### Full Mesh Connectivity

![](assets/Pasted%20image%2020251028151347.png)

### Isolated Connectivity - Pattern 1
![](assets/Pasted%20image%2020251028151450.png)
### Isolated Connectivity - Pattern 2
![](assets/Pasted%20image%2020251028151511.png)

## DX Routing Policies

### Routing Priority out of the VPC

![](assets/Pasted%20image%2020251028173333.png)

- Longest prefix match first (more specific match)
- Static routes over propagated routes
- Propagated Routes
    - Direct Connects BGP routes (Dynamic routes)
    - VPN Static Routes
    - VPN BGP routes (Dynamic routes)

### DX Routing Policies and BGP communities

- Routing policies influence the routing decision when traffic flows through Direct Connect connections.
- Inbound routing Policies - from on-premises to AWS
- Outbound routing Policies - from AWS to on-premises
- Routing policies and BGP communities work differently for Public VIF and Private /Transit VIFs

![](assets/Pasted%20image%2020251028173652.png)

## DX Link Aggregation Groups (LAGs)

- Get increased bandwidth and failover by aggregating multiple Direct Connect connections into a single logical connection
- Uses Link Aggregation Control Protocol (LACP)
- All connections must be dedicated connections and have a port speed of 1 Gbps, 10 Gbps, or 100 Gbps.
- Can aggregate up to 4 connections (active-active mode)
- Can use existing connection or add new connections to the LAG
- All connections in the LAG must have the same bandwidth
- All connections in the LAG must terminate at the same AWS Direct Connect Endpoint
- Supports all virtual interface types - public, private, and transit

### LAG with 10 Gbps dedicated connections

![](assets/Pasted%20image%2020251028174935.png)

### LAG High Availability

![](assets/Pasted%20image%2020251028175007.png)

### LAG Operation Status

- All LAG connections operate in Active/Active mode
- LAG supports attribute to define minimum number of operational connections for the LAG to function (Default value = 0)
- If there are say 4 connections in the LAG and operational connection attribute value = 1 then LAG will be operational even if 3 connections are down
- If there are say 4 connections in the LAG and operational connection attribute value = 3 then LAG will be non-operational if 2 or more connections are down
- This attribute prevents over-utilization of active LAG connections in case of failures in other connections.

### MACSec with LAGs

- We can enable MACsec for the LAGs
- MACsec uses MACsec secret key which is generated using Connection Key Name (CKN) and Connectivity Association Key (CAK)
- For existing connections with MACsec, the MACsec key is disassociated with the connection and LAG MACsec security key is associated with the connection after connection is added to the LAG
- LAG MACsec key is associated with all the member connections

## DX Connection Resiliency

### Single DX Connection : VPN as a backup
![](assets/Pasted%20image%2020251028181452.png)
### Dual DX Connections : Dual devices
![](assets/Pasted%20image%2020251028181504.png)
### Dual DX Connections : Dual devices
![](assets/Pasted%20image%2020251028181525.png)
### Dual locations with DX connection backup
![](assets/Pasted%20image%2020251028181541.png)
### Using DX Console for Resiliency
Use AWS DirectConnect console to choose between Classic or Connection Wizard

- Classic allows you to create a single connection
- Connection Wizard allows to choose from three types of resiliency options
- Maximum Resiliency
- High Resiliency
- Development and Test
### DirectConnect fast failover using BFD

#### BFD Bidirectional Forwarding Detection

- It’s a simple Hello Network Protocol
- Lowers the network failure detection time between the neighboring peers
- BFD control packets are transmitted and received periodically between the BFD peers (Asynchronous mode)
- Neighbors can use dynamic routing protocol or static routes (BGP/OSPF)
- Provides the detection time less than 1 sec

![](assets/Pasted%20image%2020251028181427.png)

#### Using BFD with Direct Connect

- While using multiple DX connections or using VPN backup, its important to have fast failover to redundant connection
- By default, BGP waits for three keep-alives to fail at a hold-down time of 90 seconds.
- AWS enables BFD by default on DX connections. However BFD should be configured on customer side of the router
- AWS sets the BFD liveness detection interval to 300 ms and BFD liveness detection count to 3 which results in failover under 1 second
- Cisco Router example:
    - bfd interval 300 min_rx 300 multiplier 3

## DX Security & Encryption

AWS Offers 2 types of options

- Layer 3 VPN over DX Connection
- Layer 2 encryption using MACSec

Additionally for Layer 4 use TLS over TCP (HTTPS) for communication

- By default traffic is not encrypted
- If its required then setup VPN over DX connections using Public VIF
- AWS publishes Public IPs which also includes public id of AWS Managed VPN (VGW) and Transit Gateways (TGW)

### VPN over DX using VGW
![](assets/Pasted%20image%2020251028184558.png)
### VPN over a DX using TGW
![](assets/Pasted%20image%2020251028184610.png)

### MAC Security (MACSec) ~ Layer 2

- Mac Security is a IEEE 802.1 Layer 2 standard providing data confidentiality, data integrity, and data origin authenticity
- MACSec provides Layer 2 security for Dedicated connection.
- NOTE: available for certain Direct Connect Partneres only for now.
- Make sure that you have a device on your end of the connection that supports MACSec
- When you configure your connection, you can specify one of the following values: MACSec – `should_encrypt, must_encrypt, no_encrypt`

## DX support for MTU and Jumbo Frames

- MTU Recap: The size in bytes of the largest permissible packet that can be passed over the connection.
- Until Oct 2018, Direct connect used to support MTU of 1500 bytes
- Now Direct connect supports MTU up to 9001 bytes i.e. Jumbo Frames

### MTU and Jumbo Frames

![](assets/Pasted%20image%2020251028184913.png)

- Public VIFs don't support Jumbo Frames
- Transit VIFs support MTU 1500 or 8500
- Private VIFs support MTU 9001
- For supporting jumbo frames the Direct connect connection or a LAG must be jumbo frame capable
- Jumbo frames apply only to propagated routes from DX (traffic routed through the static routes is sent using 1500 MTU)
## DX Monitoring & Pricing

CloudWatch monitors DX connection and Virtual interfaces

![](assets/Pasted%20image%2020251028185239.png)

### Direct Connect Billing

- Port hour charges as per the DX connection type and capacity
    - Dedicated Connection
    - Hosted Connection
- Data transfer out charges - per GB depending on the DX location and source AWS region

![](assets/Pasted%20image%2020251028194239.png)
### Summary of DX Billing

- Port hour charges & Data Transfer Out (DTO) charges
- Port hour charges depend on the DX capacity
- The AWS account which created the DX connection pays for the Port hour charges
- Data Transfer out charges are usually allocated to the account that owns the resource sending the traffic (with exception of TGW)
- In case of multi account setup where owner of Connection and AWS resources are in different AWS organizations, the DTO is charged to Resource owner account based on standard AWS service DTO rate and not the DX DTO rate (exception is S3 which allows to set requestor pays option)
### Knowledge check

- Who pays for the charges for Hosted VIF?
- Answer:
    - Port hour charges will be billed to AWS account owning the connection wether it’s a dedicated connection or a hosted connection
    - Data transfer out charges will be billed to the AWS account which contains the resource sending the traffic over the Hosted VIF

Ask 2 questions: Who owns the connection and Who sends the traffic, Simple?
## DX Troubleshooting

![](assets/Pasted%20image%2020251028184958.png)

## DX Architecture

![](assets/Pasted%20image%2020251028185021.png)
