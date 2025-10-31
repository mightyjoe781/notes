# AWS Site-to-Site VPN

AWS Connectivity Options include following methods.

![](assets/Pasted%20image%2020251027170731.png)

- AWS Site-to-Site VPN & AWS Client VPN also goes over the internet, but it is secure

![](assets/Pasted%20image%2020251027170859.png)

### How Site-to-Site VPN works in AWS

There are two ways to approach this, using VPN Gateway or use Transit Gateway.

![](assets/Pasted%20image%2020251027171110.png)
![](assets/Pasted%20image%2020251027171124.png)

- VPN connection is established between AWS Network and Customer corporate network
- At AWS end, VPN can be terminated on Virtual Private Gateway (VGW) or AWS TGW
- Each AWS Site-to-Site VPN connection has 2 IP Security (IPSec) Tunnels for High Availability

### AWS Site-to-Site Fundamentals

- VPN allows hosts to communicate privately over an untrusted intermediary network like internet, in encrypted form.
- AWS supports Layer 3 VPN (not Layer 2)
- VPN has 2 forms
    - Site-to-Site connects 2 different network
    - Client-to-Site connects client device like laptop to private network
- VPN types
    - IPSec VPN which is supported by AWS managed VPN
    - Other VPNs like GRE and DMVPN are not supported by AWS managed VPN
- VPN gateway or Virtual Private Gateway (VGW) is the managed gateway endpoint for the VPC
- Only one VGW can be attached to VPC at a time
- Supports both Static & Dynamic routing using BGP
- for BGP, you can assign the private ASN to VGW in the range 64512 to 65534 (2 bytes) or 1-2147483647 (4-bytes)
- If ASN is not defined, AWS assigns default ASN 64512
- You can use preshared keys or Private CA certificates to authenticate Site-to-Site VPN tunnel endpoints

## IPv4 and IPv6 support

### VPN outside and inside IP address

![](assets/Pasted%20image%2020251027172438.png)

![](assets/Pasted%20image%2020251027172450.png)

- IPv4 outer tunnel with IPv4 inner packets - Default configuration for IPv4 traffic, Supported for Virtual Private Gateway, Transit Gateway and Cloud WAN
- IPv4 outer tunnel with IPv6 inner packets – Allows IPv6 traffic within IPv4 VPN tunnels, Supported for Transit gateway and Cloud WAN
- IPv6 outer tunnel with IPv6 inner packets – Allows full IPv6 traffic and routing, Supported for Transit Gateway and Cloud WAN IPv6 outer tunnel with IPv4 inner packets - Allows IPv6 outer tunnel addressing while supporting legacy IPv4 applications within the tunnel. Supported for both Transit gateway and Cloud WAN.
- A single Site-to-Site VPN connection cannot support both IPv4 and IPv6 traffic simultaneously. You need separate VPN connections to transport IPv4 and IPv6 packets.

## Accelerated Site-to-Site VPN

![](assets/Pasted%20image%2020251027172630.png)

![](assets/Pasted%20image%2020251027172642.png)

- Supported only for AWS Transit Gateway. VPN terminating on VGW isn’t supported.
- Can be enabled only when creating the new VPN connection. We can not enable the acceleration on the existing VPN connection.
- Provides the 2 Static anycast IPs which are different than VPN endpoint IPs
- NAT-traversal (NAT-T) must be enabled on customer gateway device as global accelerator does not support ESP 50
- IKE negotiation for the accelerated VPN tunnels must be initiated from the CGW
- Additional charge applied

## VPN NAT Traversal (NAT-T)

![](assets/Pasted%20image%2020251027183807.png)

- In above diagram, UDP 500 (IKE negotiation) happens over port 500, then ESP 50 takes place (not port 50)
- This process will not work if CGW is behind a NAT. In that case ESP 50 must be wrapped into a UDP header.

![](assets/Pasted%20image%2020251027183931.png)

- AWS automatically detects NAT during IKE negotiation and switched to UDP 4500 (instead of ESP 50 protocol). You will need to enable NAT-T on the CGW as well.
- Usually on AWS side, no configuration is required, but on consumer side
    - When not using NAT: Allow inbound/outbound UDP 500, ESP 50
    - When using NAT: Allow inbound/outbound UDP500, UDP 4500
- For using Accelerated Site-to-Site VPN, NAT-T must be enabled, because AWS Global accelerator doesn't support ESP 50 traffic

## VPN Route Propagation (Static vs Dynamic)

- In case of static routing, you must pre-define the CIDR ranges on the both sides of the VPN connection. If you add new network ranges on either side, the routing changes are not propagated automatically
- In case of Dynamic routing, both the ends learns the new network changes automatically. On AWS side, the new routes are automatically propagated in the route table.
- AWS route table can not have more than 100 propagated routes. Hence you need to make sure not to publish more than 100 routes from on-premise network
- To avoid this situation, you may think to consolidate network ranges into larger CIDR ranges.

### Route propagation in Site-to-Site VPN

![](assets/Pasted%20image%2020251027184423.png)

- Static Routing:
    - Create static route in corporate data center for 10.0.0.1/24 through the CGW
    - Create static route in AWS for 10.3.0.0/20 through the VGW
- Dynamic Routing (BGP)
    - Uses BGP (Border Gateway Protocol) to share routes automatically (eBGP for internet)
    - We don’t need to update the routing tables, it will be done for us dynamically
    - Just need to specify the ASN (Autonomous System Number) of the CGW and VGW
## VPN Transitive Routing Scenarios

### Site-to-Site VPN and Internet Access

VGW can't route traffic to IGW, its a gateway device, not an ENI.

![](assets/Pasted%20image%2020251027190306.png)

Even if NAT Gateway is present we can't reach to internet because its a managed device, but if NAT is EC2 Instance then its possible to redirect traffic to Internet.

![](assets/Pasted%20image%2020251027190329.png)
![](assets/Pasted%20image%2020251027190339.png)

### Site-to-Site VPN and VPC Peering

![](assets/Pasted%20image%2020251027190428.png)

### Site-to-Site VPN and VPC gateway endpoint
![](assets/Pasted%20image%2020251027190440.png)

### Site-to-Site VPN and VPC Interface endpoint
This works because of ENI in the VPC.

![](assets/Pasted%20image%2020251027190453.png)

### Site-to-Site VPN and on-premises Internet Access

![](assets/Pasted%20image%2020251027190526.png)

## VPC Tunnels ~ Active/Passive Mode

### Static Routing - Active/Active Tunnels
- In Static Routing : Traffic is redirected back from VGW randomly to the one of the Tunnel. Its not stateful.
- Active/Active tunnel may cause Asymmetric routing & Asymmetric routing should be enabled on the CGW
- For traffic originating from AWS, one of the tunnel is selected randomly.
![](assets/Pasted%20image%2020251027191142.png)
### Static Routing - Active/Passive Tunnels

- Since there is no issue of Asymmetric Routing since one of the tunnel is up.
- Many routers can detect if Tunnel 1 is down, and bring up Tunnel 2. Needs to handled by you!!
![](assets/Pasted%20image%2020251027191154.png)
### Dynamic Routing - Active/Active Tunnels

- Both tunnels can be used simultaneously for highly available use cases.
- Advertise a more specific prefix on the tunnel
- For matching prefixes where each VPN connection uses BGP, use ASPATH
- When the ASPATHs are the same length, use multi-exit discriminators (MEDs)
- The path with the lowest MED value is preferred.

![](assets/Pasted%20image%2020251027191205.png)

## VPN Dead Peer Detection (DPD)

- Dead Peer Detection (DPD) is a method to detect liveliness of IPSec VPN connection
- VPN peers can decide during “IKE Phase 1” if they want to use DPD
- If DPD is enabled AWS continuously (every 10 sec) sends DPD (R-U-THERE) message to customer gateway and waits for the R-U-THERE-ACK. If there is no response to consecutive 3 requests, then DPD times out.

![](assets/Pasted%20image%2020251027191356.png)

- By default, when DPD occurs, the gateways delete the security associations. During this process, the alternate IPsec tunnel is used if possible.
- Default DPD timeout value is 30 sec which can be set higher than 30 seconds.
- DPD uses UDP 500 or UDP 4500 to send DPD messages
-  DPD timeout actions:
    - Clear (default action) - End the IPSec IKE session, stop the tunnel and clear the routes
    - Restart - AWS Restarts the IKE Phase 1
    - None – Take no action
- Customer router must support DPD when using Dynamic Routing (BGP)
- Can set up appropriate die timed dur se ip a host ride sends ion. (pins) requests every say 5-10 seconds

## VPN Monitoring

### VPN Monitoring with Cloud Watch

- TunnelState: The state of the tunnel. 0 indicates DOWN and 1 indicates UP. Value between 0 and 1 indicates that at least 1 tunnel is not UP.
- TunnelDataIn: The bytes received through the VPN tunnel
- TunnelDataOut: The bytes sent through the VPN tunnel
![](assets/Pasted%20image%2020251027191942.png)

### VPN Monitoring with Health Dashboard

- AWS Site-to-Site VPN automatically sends notifications to the AWS Personal Health Dashboard (PHD)
- Tunnel endpoint replacement notification
- Single Tunnel VPN notification (when one of the tunnel is down for more than one hour in a day)
![](assets/Pasted%20image%2020251027192023.png)

## AWS Site-to-Site VPN Architectures

- Single Site-to-Site VPN connection
    - With Virtual Private Gateway (VGW)
    - With Transit Gateway (TGW)
- Multiple Site-to-Site VPN Connections to branch offices
- Redundant VPN connections for High Availability

### Single Site-to-Site VPN Connection using TGW
![](assets/Pasted%20image%2020251027192149.png)

### Single Site-to-Site VPN Connection using TGW
![](assets/Pasted%20image%2020251027192200.png)

### Multiple Site-to-Site VPN Connection using VGW
![](assets/Pasted%20image%2020251027192254.png)

### Multiple Site-to-Site VPN Connections using TGW
![](assets/Pasted%20image%2020251027192310.png)
### Redundant VPN connections for HA
![](assets/Pasted%20image%2020251027192328.png)

## AWS VPN CloudHub

![](assets/Pasted%20image%2020251027192610.png)
### Routing between multiple customer sites

![](assets/Pasted%20image%2020251027192558.png)

- Each VPN Gateway in detached mode
- Each customer gateway must have unique BGP ASN with dynamic routing
- Sites must not have overlapping IP ranges
- Connect up to 10 Customer Gateways
- Can server as failover connection between on-premise locations

![](assets/Pasted%20image%2020251027192546.png)

- VPN gateways can also be attached to VPC to enable communication
## EC2 based VPN

![](assets/Pasted%20image%2020251027192812.png)
### VPN Termination on EC2
Why would you do that?

- You want to use different VPN protocol than IPSec e.g General Routing Encapsulation (GRE) or Dynamic MultiPoint VPN (DMVPN)
- You are using overlapping CIDRs
- You want to enable transitive routing on AWS side
- You want to have special features on VPN termination endpoints such as Advanced Threat Protection
- When bandwidth required > 1.25 Gbps
### Considerations for EC2 based VPN

- To enable routing of traffic, make sure that the source/destination check is disabled on the VPN termination EC2 instance and IP forwarding is enabled at the operating system level.
- In case of hardware failure, EC2 will be recovered automatically if EC2 auto recovery has been setup using CloudWatch status check
- Bandwidth limitations between EC2 instances:
    - Up to 5 Gbps outside VPC
- AWS does not provide or maintain third party software VPN appliances
    - Partner VPN Solutions on AWS Marketpalce: Cisco, Juniper, Palo Alto You may get a highly available & self-healing setup with their solution
- Vertical Scaling
- Horizontal Scaling
- IPsec as a protocol doesn’t function through a Network Load Balancer due to non-Transmission Control Protocol (TCP) (IPSec protocol 50)

![](assets/Pasted%20image%2020251027193119.png)
## AWS Transit VPC architecture using VPN connections

### Multiple Site-to-Site VPN Connections using VGW
![](assets/Pasted%20image%2020251027195051.png)

### VPN CloudHub - Routing between multiple customer sites

- VPN Gateway can also be attached to VPC to enable communcation

![](assets/Pasted%20image%2020251027195128.png)

### Transit VPC - What is it & Why its required ?

![](assets/Pasted%20image%2020251027195153.png)

![](assets/Pasted%20image%2020251027195204.png)

Solution !

![](assets/Pasted%20image%2020251027195219.png)
![](assets/Pasted%20image%2020251027195313.png)
![](assets/Pasted%20image%2020251027195324.png)
![](assets/Pasted%20image%2020251027195335.png)
![](assets/Pasted%20image%2020251027195346.png)

### Transit VPC scenarios

1. When multiple VPCs needs to be connected with on-premises network
2. Advanced Threat protection where traffic should be routed through centralized firewall systems
3. When you want to connect to on-premises network having overlapping CIDRs. Transit VPC acts as a NAT translating IPs to different range to enable communication.
4. Allow access for remote networks (Spoke VPC or On-premise network) to endpoints hosted in Transit Hub VPC
5. Client-to-Site VPN where client devices can connect to the Transit VPC EC2 instance by establishing VPN connection

### Transit VPC architecture for Transit Hub

![](assets/Pasted%20image%2020251027195530.png)

https://docs.aws.amazon.com/network-manager/latest/tgwnm/what-are-global-networks.html

https://aws.amazon.com/solutions/implementations/aws-global-transit-network/

Transit VPC scenarios

- Global VPN infrastructure with Single Transit Hub
- Global VPN infrastructure with Transit Hubs in each region

NOTE: Transit Gateway essentially does above ^. only if questions ask about NAT between overlapping network addresses then the answer would be Transit VPC, or else mostly answers will be leaning towards Transit Gateways.