# AWS Cloud WAN

- A managed wide-area networking (WAN) service to build, manage, and monitor a global network across AWS and on-premises network
- Simple network policies to configure and automate network management
- Provides a central dashboard (through AWS Network Manager

![](assets/Pasted%20image%2020251028232336.png)

### Networking Scenarios in AWS

#### VPC Peering

- Non-Transitive

![](assets/Pasted%20image%2020251028232430.png)
#### Transit Gateway with Peering

- Regional Components, supports mesh connectivity

![](assets/Pasted%20image%2020251028232448.png)

#### Hybrid ~ DXG with Transit VIP

![](assets/Pasted%20image%2020251028232416.png)

#### SD-WAN with Transit Gateway Connect

![](assets/Pasted%20image%2020251028232647.png)

![](assets/Pasted%20image%2020251028232702.png)

#### Cloud WAN

![](assets/Pasted%20image%2020251028232740.png)

### Components of Cloud WAN

- Global Network - Core Networks + Transit Gateway Network
- Core Network
    - Core Network Edge
    - Core Network Policy
- Network Segments
    - Segment actions
- Attachment
    - Attachment policies
- Peering

![](assets/Pasted%20image%2020251028232900.png)

![](assets/Pasted%20image%2020251028232912.png)

## Core Network Policy

![](assets/Pasted%20image%2020251028234349.png)

- Network configurations
    - ASN ranges
    - Regions (Core Network Edge)
- Segments
    - Name
    - Regions
    - Require acceptance
    - Sharing between segments
    - Static routes
- Attachment policies
    - Rules
    - Associate the attachments to the segments
    - Require Acceptance
- Network Configuration
    - ASN ranges
        - 64512-65534
        - 4200000000-4294967294
    - Edge locations (Regions)
    - Inside CIDR blocks
        - For Transit Gateway Connect tunnels
        - Can be defined per region
    - ECMP support

### Segments

![](assets/Pasted%20image%2020251028234317.png)

- Name
- Edge locations
    - Subset of Core Network edges
- Isolate attachments (default: False)
    - If True, attachment routes are not shared automatically
    - Routes can be shared through Share segment action or by adding static routes
- Require attachment acceptance (default: True)
- Filters
    - allow or deny routes sharing between segments
- Segment Actions
    - Share segments
    - Create static routes
### Attachments

![](assets/Pasted%20image%2020251028234329.png)

- VPC
- VPN
- Connect & Connect Peer
    - Connects to 3rd party virtual appliances hosted inside VPC
    - Supports both GRE and Tunnel-less protocols
    - BGP for Dynamic routing (two BGP sessions for redundance)
- Transit Gateway Route table

### Attachments Policies
- Rule numbers
    - 1-65535
    - Lower number takes priority
    - Rule evaluation stops after first match 
- Require acceptance
    - In effect only when Segment require acceptance is false
- Logical conditions: AND or OR
    - AWS Account
    - Region
    - TagKey, TagValue
    - Resource ID (e.g. VPC ID/ VPN ID)
- Association-method
    - Constant or Tag
    - If “Constant” then provide the segment name

### Process to make changes to the Network Policy

![](assets/Pasted%20image%2020251028233649.png)

### Cloud WAN Walkthrough

![](assets/Pasted%20image%2020251028233725.png)
![](assets/Pasted%20image%2020251028233738.png)

## AWS CloudWAN + Transit Gateway & Direct Connect

### AWS Cloud WAN and Transit Gateway

![](assets/Pasted%20image%2020251028233809.png)

### AWS Cloud WAN with Direct Connect

- Connect Direct Connect to Transit Gateway over a Transit VIF & DX Gateway
- Create Cloud WAN peering with Transit Gateway
- Create Transit Gateway route table attachments connecting to Cloud WAN segments

![](assets/Pasted%20image%2020251028233922.png)