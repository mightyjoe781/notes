# Internet Protocol

## IP Building Blocks

- Layer 3 property
- Can be set automatically (DHCP Lease) or statically
- Network and Host Portion
- 4 bytes in IPv4 - 32 bits

### Network vs Host

- `a.b.c.d/x` (`a.b.c.d` are integers) x is the network bits and remaining are host
- Example `192.168.254.0/24`
- The first 24 bits (3 bytes) are network, the rest 8 are for the host
- This means we can have $2^{24} = 16777216$ network and each network has $2^8 = (255)$  hosts
- Also called a subnet

### Subnet Mask

- `192.168.254.0/24` is also called a subnet
- The subnet has a mask `255.255.255.0`
- Subnet mask is used to determine whether an IP is in the same subnet

### Default Gateway

- Most network consists of hosts and a Default Gateway
- When host A want to talk to B directly if both are in same subnet
- Otherwise A sends it to someone who might know, the gateway
- The Gateway has an IP Address and each host should know its gateway

![](assets/Pasted%20image%2020250929090147.png)

![](assets/Pasted%20image%2020250929090158.png)
## IP Packet

- IP packet has headers and data sections
- IP Packet header is 20 bytes (can go up to 60 bytes if options are enabled)
- Data section can go up to 65536

![](assets/Pasted%20image%2020250929090938.png)

- Version ~ The protocol version
- Internet Header Length(ILH) - Defines the Options length
- Total Length ~ 16 bit data + header
- Fragmentation ~ Jumbo Packets
- TTL - How many hops packet can survive
- Protocol - What protocol is inside data section
- Source & Destination IP
- ECN (Explicit Congestion Notification)

NOTE: Packets need to get fragmented if it doesn't fit in a frame. Reassembling a packet from different frame is a very tedious and vulnerable process, some routers will just deny fragmentation.
## ICMP

- Stands for Internet Control Message Protocol
- Designed for informational message
    - Host unreachable, port unreachable, fragmentation needed
    - packet expired (infinite loop in routers)
- Uses IP directly
- PING traceroute use it
- Doesn't require listeners or ports to be opened

![](assets/Pasted%20image%2020250929093229.png)

- Some firewalls block ICMP for security reasons
- That is why PING might not work in those cases
- Disabling ICMP also can cause real damage with connection establishment (TCP black hole)
    - fragmentation needed
- PING demo

```bash
ping 192.168.254.254

ping google.com
```

### PING 

![](assets/Pasted%20image%2020250929094632.png)

![](assets/Pasted%20image%2020250929094640.png)

### TraceRoute

- Can you identify the entire path your IP packet takes ?
- Clever use of TTL
- Increment TTL slowly and you will get the route IP address for each hop (TTL 1, TTL2, TTL 3, ....)
- Doesn't always work as path changes and ICMP might be blocked

## ARP

- Address Resolution Protocol
- we need the MAC address to send frames (layer 2)
- Most of the time we know the IP address but not the MAC
- ARP Table is cached IP -> Mac Mapping
- Attacks can be performed on ARP (ARP Poisoning)
- VRRP can be used to create load balancer, basically 7 machines share the same IP.

### ARP Broadcast

![](assets/Pasted%20image%2020250929101635.png)

![](assets/Pasted%20image%2020250929101612.png)
![](assets/Pasted%20image%2020250929101625.png)

## Capturing IP, ARP and ICMP Packets with `tcpdump`

```bash
# ipconfig or ifconfig ~ to list interfaces

# ARP
tcpdump -n -i en0 arp

# ICMP
tcpdump -n -i en0 icmp # in another term : ping exmaple.com
tcpdump -n -v -i en0 icmp # notice we can see entire packet headers
tcpdump -n -v -i en0 icmp src 93.184.216.14 # filters

```
## Routing Example

How IP Packets are routed in Switches and Routers

![](assets/Pasted%20image%2020250929103232.png)

traceroute:

- A -> B
- D -> X
- B -> G
## Private IP Addresses

following IPS are reserved.

| RFC 1918 name | IP address range              | Number of addresses | Largest [CIDR](https://en.wikipedia.org/wiki/CIDR "CIDR") block (subnet mask) | Host ID size | Mask bits | _[Classful](https://en.wikipedia.org/wiki/Classful "Classful")_ description |
| ------------- | ----------------------------- | ------------------- | ----------------------------------------------------------------------------- | ------------ | --------- | --------------------------------------------------------------------------- |
| 24-bit block  | 10.0.0.0 – 10.255.255.255     | 16777216            | 10.0.0.0/8 (255.0.0.0)                                                        | 24 bits      | 8 bits    | single class A network                                                      |
| 20-bit block  | 172.16.0.0 – 172.31.255.255   | 1048576             | 172.16.0.0/12 (255.240.0.0)                                                   | 20 bits      | 12 bits   | 16 contiguous class B networks                                              |
| 16-bit block  | 192.168.0.0 – 192.168.255.255 | 65536               | 192.168.0.0/16 (255.255.0.0)                                                  | 16 bits      | 16 bits   | 256 contiguous class C networks                                             |

Open Up your wifi and check the IP Address, Subnet Mask, Router

- NOTE: often written IPs like 10.0.0.0/8 ~ meaning 8 bits are reserved for the network, so subnet mask would be 255.0.0.0. That means Hosts ID can be 24 bits giving use $2^{24}$ host in a class A network.


- https://en.wikipedia.org/wiki/Private_network