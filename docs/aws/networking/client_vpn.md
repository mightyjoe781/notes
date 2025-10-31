# AWS Client VPN

![](assets/Pasted%20image%2020251028001450.png)

AWS Managed Client VPN was launched in 2018.

Client to Site VPN features

- AWS has a managed Client VPN (out of scope for exam)
- Or setup Client VPN on EC2
    - AWS Marketplace: Use pre-baked AMI with VPN software and license. Example vendors are Cisco, Aviatrix, Palo Alto, Sophos etc
    - Manual installation on EC2: OpenSwan, StrongSwan
- For high availability pointers
    - Multiple EC2 instances with NLB
    - Optionally use DNS load balancing (client side) instead of NLB
- You may also have to implement Split tunneling at client side

## AWS Client VPN

Connect from your computer using OpenVPN to your private network in AWS and on-premise

![](assets/Pasted%20image%2020251028001659.png)
![](assets/Pasted%20image%2020251028001721.png)

### Client VPN components

![](assets/Pasted%20image%2020251028001759.png)

AWS Client VPN Components

- VPC
- Target Network Subnet
- Client VPN Endpoint
- Route
- Authorization Rules
- Client CIDR range
- Client VPN Network Interfaces
- Authentication
- Authorization
- Client

### AWS Client VPN Limitations

- Client CIDR ranges cannot overlap with the local CIDR of the VPC in which the associated subnet is located
- Client CIDR ranges cannot overlap with any routes manually added to the Client VPN endpoint's route table
- Client CIDR ranges must have a block size between /22 and /12
- The client CIDR range cannot be changed after you create the Client VPN endpoint
- You cannot associate multiple subnets from the same Availability Zone with a Client VPN endpoint
- A Client VPN endpoint does not support subnet associations in a dedicated tenancy VPC
- Client VPN supports IPv4 traffic only

### Pricing (N. Virginia region)

![](assets/Pasted%20image%2020251028001936.png)

### Example Setup

![](assets/Pasted%20image%2020251028093135.png)

NOTE : Once you are connected to the VPN, you will not be able to access internet, because there is no route in the VPC for internet,
You can do two things here,

- Either add a IGW (Internet Gateway) to the VPC, or 
- Create a split tunnel on client end

![](assets/Pasted%20image%2020251028093440.png)