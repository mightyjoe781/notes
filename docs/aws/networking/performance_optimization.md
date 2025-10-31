# Network Performance & Optimization

## Network Performance - Basics

- Bandwidth - Maximum rate of transfer over the network
- Latency - Delay between two points in a network
    - Delays include propagation delay for signals to travel across medium
    - Also includes the processing delays by network devices
- Jitter - Variation in inter packet delays
- Throughput - Rate of successful data transfer (measured in bits/sec)
    - Bandwidth, Latency and Packet loss directly affects the throughput
- Packet Per seconds (PPS) ~ how many packets are processed per seconds
- Maximum Transmission Unit (MTU) ~ Largest packet that can be sent over the network

Refer to this : [Network Performance](../../networking/neteng/network_performance.md) & Understand MTU Path Discovery (requires ICMP enabled)

![](assets/Pasted%20image%2020251025190054.png)

Usually default MTU is 1500 bytes, in usual networking scenarios this is limited by the smallest MTU supported by Routers at the end. But in Private cloud this could be overcome by cloud providers.
AWS supports jumbo frames of `9001` bytes.

Benefits of using Jumbo Frames

- Less Packets
- More throughput
- Increasing MTU increases throughput when you can't increase Packet Per Second (PPS)
- Supported Within VPC, between VPC and on-premises Network using AWS Direct Connect.
- Defined at MTU level


!!! note "Warning"

    Use Jumbo frames with caution for traffic leaving the VPC. If packets are over 1500 bytes, they are fragmented, or they are dropped if the Don't fragment flag is set in IP header.


To check MTU between your device and target endpoint using tracepath : `tracepath amazon.com`
To check MTU on Linux : `ip link show eth0`
To set MTU value on Linux: `sudo ip link set dev eth0 mtu 9001`


MTU Optimization Guidelines

- Within AWS:
    - Within VPC: Supports Jumbo frames (9001 bytes)
    - Over the VPC Endpoint : MTU (8500 bytes)
    - Over the Internet Gateway : MTU 1500 bytes
    - Intra region VPC Peering : MTU 9001 bytes
    - Inter region VPC Perring : MTU 1500 bytes
- On-Premise Network
    - Over the VPN using VGW: MTU 1500 bytes
    - Over the VPN via Transit Gateway: MTU 1500 for traffic for Site-to-Site VPN
    - Over the Direct Connect (DX) Supports jumbo frames (9001 bytes)
    - Over the DX vis Transit Gateway : MTU for VPC attachments connected over the Direct Connect

## Placement Groups and EBS Optimized EC2 instances

### Cluster Placement Groups

- A logical grouping of instances within single AZs
- Ideal for distributed applications that require low latency like HPC
- Same Rack, Same AZs

![](assets/Pasted%20image%2020251025191736.png)

### EBS Optimized Instances

![](assets/Pasted%20image%2020251025191929.png)

- EBS is a network drive
    - It uses network to communicate the instance, which means there might be a bit of latency
- Hence, EBS i/o affect network performance
- Amazon EBS-optimized instances deliver dedicated throughput between Amazon EC2 & EBS
- This minimizes contention between Amazon EBS i/o and other traffic from Amazon EC2 instances.

### Enhanced Networking

- Over 1M PPS performance
- Reduces instance-to-instance latencies
- SR-IOV with PCI passthrough, to get the hypervisor out of the way and for consistent performance
- Enabled using intel *ixbevf* driver or Elastic Network Adaptor (ENA)

#### SR-IOV and PCI for Enhanced Networking

- SR-IOV and PCI passthrough are methods of device virtualization that provide higher I/O performance and lower CPU utilization
- SR-IOV allows a single physical NIC to present itself as multiple vNICs
- PCI passthrough enables PCI devices such as ENI to appear as if they are physically attached to the guest operating system bypassing hypervisor
- Ultimately in combination this allows low latency, high rate data transfer (>1 M PPS)

#### Enhanced Networking pre-requisites

- Depending on Instance Type, Enhanced Networking can be enabled using one of the following Network drivers
    - Option 1: Intel 82599 VF up to 10 Gbps (VF uses ixgbevf driver
    - Option 2: Elastic Network Adapter (ENA) up to 100 Gbps
- The eligible EC2 instance families support either of the above two drivers

NOTE: For Enhanced Networking, it requires support from both EC2 operating system (AMI) and Instance Type that is flagged for Enhanced Networking
#### Supported Instance Types

- Instances supporting Elastic Network Adapter (ENA) for speed upto 100GBps
    - A1, C5, C5a, C5d, C5n, C6g, F1, G3, G4, H1, I3, I3en etc
- Instances supporting Intel 82599 Virtual Function (VF) interface for speed upto 10Gbps
    - C3, C4, D2, I2, M4 (excluding m4.16xlarge), and R3 etc

#### Default Networking EC2

![](assets/Pasted%20image%2020251025192506.png)

#### Enhanced Networking - with Intel VF

![](assets/Pasted%20image%2020251025192527.png)

#### Enhanced Networking with ENA

![](assets/Pasted%20image%2020251025192548.png)


## DPDK and Elastic Fabric Adapter (EFA)

### DPDK

- Intel Data Plane Development Kit (DPDK) is a set of libraries and drivers for fast packet processing.
- While Enhanced Networking and SR-IOV reduce overhead of packet processing between Instance and Hypervisor, DPDK reduces overhead of packet processing inside the Operating System
- DPDK provides
    - Lower latency due to Kernel bypass
    - More control of packer processing
    - Lower CPU overhead

#### without DPDK
![](assets/Pasted%20image%2020251025192933.png)

#### with DPDK
![](assets/Pasted%20image%2020251025192952.png)

### EFA - Elastic Fabric Adapter

![](assets/Pasted%20image%2020251025193021.png)

- EFA is an ENA with added capabilities
- Provides lower latency and higher throughput
- Provides OS bypass functionality (Linux)
- For windows instance, it acts just as ENA
- With an EFA, HPC applications use MPI to interface with the Libfabric API which bypasses OS kernel and communicates directly with the EFA device to put packets on the network

## Bandwidth Limits inside and outside of VPC

### VPC Bandwidth Limits

- No VPC specific limits
- No limit for any Internet Gateway
- No limit for VPC Peering
- Each NAT gateway can provide up to 45Gbps, Use Multiple NAT gateways to scale beyond 45 Gbps

### EC2 Bandwidth Limits

- Depends on factors like instance family, vCPU, traffic destination etc.
- Within the Region
    - Can utilize the full bandwidth available to the instance
- To other regions, and internet gateway or Direct Connect
    - Can utilize up to 50% of the network bandwidth
    - otherwise limited to 5 Gbps
- With intel 82599 VF interface
    - 10Gbps aggregate and 5 Gbps flow-based bandwidth limit
- With AWS ENA driver
    - 10Gbps flow limit inside a placement
    - 5 Gbps flow limit outside a placement group
    - aggregate bandwith of 100Gbps with multiple flows within a VPC or a peered VPC or to S3 (using VPCe) in the same region

### Bandwidth over VPN Connections, AWS DC, Transit Gateway

- 1.25 Gbps aggregate bandwidth per Virtual Private Gateway for traffic from AWS to on-premises
- Multiple VPN connections to the same Virtual Private Gateway are bound by an aggregate throughput limit
- AWS Direct connect bandwidth is defined by Port Speed opted
- For AWS Direct Connect connection on a Virtual Private Gateway, the throughput is bound by the Direct Connect physical port itself.
- Transit Gateway supports 1.25Gbps per VPN tunnel and 50 Gbps total VPN bandwidth

![](assets/Pasted%20image%2020251025200548.png)

### Network Flow

- Network flow is a 5 tuple point to point connection (Protocol src ip, port and dest ip, port)
- Multiple flows allows to scale the network performance.

## Network I/O credits

- Instance families such as R4 and C5 use a network I/O credit mechanism
- Most application do not consistently need a high network performance
- These instances perform well above baseline n/w performance during peak requirement
- Make sure that you consider the accumulated n/w credits before doing performance benchmark for instances supporting network I/O credits mechanism

### Use Cases for high performance networks

- High Performance Computing (HPC) workloads
- Real Time Media
- More use cases : Data Processing, Backups, On-prem Data Transfer, etc.